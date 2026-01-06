#!/usr/bin/env python3
"""
Claude Code Session History API

Provides search, meta, and read operations for Claude Code session histories.
"""

import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional
from collections import defaultdict
import hashlib

# Lazy imports for heavy dependencies
_model = None
_np = None

CLAUDE_DIR = Path.home() / ".claude"
PROJECTS_DIR = CLAUDE_DIR / "projects"
INDEX_DIR = CLAUDE_DIR / "session-index"
DB_PATH = INDEX_DIR / "sessions.db"
EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npy"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def _get_model():
    """Lazy load the sentence transformer model."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _get_numpy():
    """Lazy load numpy."""
    global _np
    if _np is None:
        import numpy as np
        _np = np
    return _np


def _init_db(conn: sqlite3.Connection):
    """Initialize database schema."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            project_path TEXT,
            project_name TEXT,
            start_time TEXT,
            end_time TEXT,
            git_branch TEXT,
            message_count INTEGER,
            user_count INTEGER,
            assistant_count INTEGER,
            tool_use_count INTEGER,
            tool_result_count INTEGER,
            thinking_count INTEGER,
            summary_count INTEGER,
            tools_json TEXT,
            summaries_json TEXT,
            first_user_message TEXT,
            file_path TEXT,
            file_hash TEXT,
            indexed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS embeddings_meta (
            id INTEGER PRIMARY KEY,
            session_id TEXT,
            text TEXT,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id)
        );

        CREATE INDEX IF NOT EXISTS idx_sessions_project ON sessions(project_path);
        CREATE INDEX IF NOT EXISTS idx_sessions_start ON sessions(start_time);
        CREATE INDEX IF NOT EXISTS idx_embeddings_session ON embeddings_meta(session_id);
    """)
    conn.commit()


def _parse_session_file(file_path: Path) -> dict:
    """Parse a session JSONL file and extract metadata."""
    messages = []
    summaries = []
    tools_used = defaultdict(int)
    first_user_message = None
    start_time = None
    end_time = None
    git_branch = None
    project_path = None

    counts = {
        "user": 0,
        "assistant": 0,
        "tool_use": 0,
        "tool_result": 0,
        "thinking": 0,
        "summary": 0,
    }

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = msg.get("type")

            if msg_type == "summary":
                summaries.append(msg.get("summary", ""))
                counts["summary"] += 1

            elif msg_type == "user":
                counts["user"] += 1
                timestamp = msg.get("timestamp")
                if timestamp:
                    if start_time is None or timestamp < start_time:
                        start_time = timestamp
                    if end_time is None or timestamp > end_time:
                        end_time = timestamp

                if git_branch is None:
                    git_branch = msg.get("gitBranch")
                if project_path is None:
                    project_path = msg.get("cwd")

                # Extract user text (not tool results)
                content = msg.get("message", {}).get("content")
                if isinstance(content, str):
                    if first_user_message is None:
                        first_user_message = content[:500]
                elif isinstance(content, list):
                    for block in content:
                        if block.get("type") == "tool_result":
                            counts["tool_result"] += 1
                        elif block.get("type") == "text" and first_user_message is None:
                            first_user_message = block.get("text", "")[:500]

            elif msg_type == "assistant":
                counts["assistant"] += 1
                content = msg.get("message", {}).get("content", [])
                if isinstance(content, list):
                    for block in content:
                        block_type = block.get("type")
                        if block_type == "tool_use":
                            counts["tool_use"] += 1
                            tool_name = block.get("name", "unknown")
                            tools_used[tool_name] += 1
                        elif block_type == "thinking":
                            counts["thinking"] += 1

    session_id = file_path.stem

    return {
        "session_id": session_id,
        "project_path": project_path,
        "project_name": Path(project_path).name if project_path else None,
        "start_time": start_time,
        "end_time": end_time,
        "git_branch": git_branch,
        "message_count": counts["user"] + counts["assistant"],
        "user_count": counts["user"],
        "assistant_count": counts["assistant"],
        "tool_use_count": counts["tool_use"],
        "tool_result_count": counts["tool_result"],
        "thinking_count": counts["thinking"],
        "summary_count": counts["summary"],
        "tools_json": json.dumps(dict(tools_used)),
        "summaries_json": json.dumps(summaries),
        "first_user_message": first_user_message,
        "file_path": str(file_path),
        "summaries": summaries,
    }


def _file_hash(file_path: Path) -> str:
    """Calculate MD5 hash of file for change detection."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def build_index(force: bool = False, verbose: bool = False) -> dict:
    """
    Build or update the session index.

    Args:
        force: Rebuild entire index even if files haven't changed
        verbose: Print progress information

    Returns:
        Dict with indexing statistics
    """
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    _init_db(conn)

    # Get existing indexed files
    existing = {}
    if not force:
        cursor = conn.execute("SELECT file_path, file_hash FROM sessions")
        existing = {row[0]: row[1] for row in cursor.fetchall()}

    # Find all session files
    session_files = list(PROJECTS_DIR.glob("*/*.jsonl"))

    stats = {"total": len(session_files), "indexed": 0, "skipped": 0, "errors": 0}
    sessions_to_embed = []

    for file_path in session_files:
        file_path_str = str(file_path)
        current_hash = _file_hash(file_path)

        # Skip if unchanged
        if file_path_str in existing and existing[file_path_str] == current_hash:
            stats["skipped"] += 1
            continue

        try:
            metadata = _parse_session_file(file_path)
            metadata["file_hash"] = current_hash
            metadata["indexed_at"] = datetime.now().isoformat()

            # Prepare embedding text
            embed_text_parts = []
            if metadata["summaries"]:
                embed_text_parts.extend(metadata["summaries"])
            if metadata["first_user_message"]:
                embed_text_parts.append(metadata["first_user_message"])
            embed_text = " ".join(embed_text_parts)[:1000] if embed_text_parts else ""

            # Remove summaries list (not stored in DB)
            del metadata["summaries"]

            # Upsert session
            conn.execute("""
                INSERT OR REPLACE INTO sessions
                (session_id, project_path, project_name, start_time, end_time,
                 git_branch, message_count, user_count, assistant_count,
                 tool_use_count, tool_result_count, thinking_count, summary_count,
                 tools_json, summaries_json, first_user_message, file_path,
                 file_hash, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, tuple(metadata.values()))

            # Store embedding text
            conn.execute("DELETE FROM embeddings_meta WHERE session_id = ?",
                        (metadata["session_id"],))
            if embed_text:
                conn.execute(
                    "INSERT INTO embeddings_meta (session_id, text) VALUES (?, ?)",
                    (metadata["session_id"], embed_text)
                )
                sessions_to_embed.append((metadata["session_id"], embed_text))

            stats["indexed"] += 1
            if verbose:
                print(f"Indexed: {metadata['session_id']}")

        except Exception as e:
            stats["errors"] += 1
            if verbose:
                print(f"Error indexing {file_path}: {e}")

    conn.commit()

    # Generate embeddings for new sessions
    if sessions_to_embed:
        if verbose:
            print(f"Generating embeddings for {len(sessions_to_embed)} sessions...")

        model = _get_model()
        np = _get_numpy()

        texts = [t[1] for t in sessions_to_embed]
        new_embeddings = model.encode(texts, show_progress_bar=verbose)

        # Load existing embeddings and merge
        if EMBEDDINGS_PATH.exists() and not force:
            existing_data = np.load(EMBEDDINGS_PATH, allow_pickle=True).item()
            existing_embeddings = existing_data.get("embeddings", np.array([]))
            existing_ids = existing_data.get("session_ids", [])
        else:
            existing_embeddings = np.array([])
            existing_ids = []

        # Create mapping of session_id -> index for existing
        id_to_idx = {sid: idx for idx, sid in enumerate(existing_ids)}

        # Update or append embeddings
        new_ids = [t[0] for t in sessions_to_embed]

        if len(existing_embeddings) > 0:
            # Update existing, append new
            all_embeddings = list(existing_embeddings)
            all_ids = list(existing_ids)

            for sid, emb in zip(new_ids, new_embeddings):
                if sid in id_to_idx:
                    all_embeddings[id_to_idx[sid]] = emb
                else:
                    all_embeddings.append(emb)
                    all_ids.append(sid)

            final_embeddings = np.array(all_embeddings)
            final_ids = all_ids
        else:
            final_embeddings = new_embeddings
            final_ids = new_ids

        np.save(EMBEDDINGS_PATH, {"embeddings": final_embeddings, "session_ids": final_ids})
        stats["embeddings_generated"] = len(sessions_to_embed)

    conn.close()
    return stats


def search(query: str, limit: int = 10, project: Optional[str] = None) -> list[dict]:
    """
    Semantic search across sessions.

    Args:
        query: Search query string
        limit: Maximum results to return
        project: Optional project name filter

    Returns:
        List of matching sessions with scores
    """
    if not DB_PATH.exists() or not EMBEDDINGS_PATH.exists():
        return []

    model = _get_model()
    np = _get_numpy()

    # Generate query embedding
    query_embedding = model.encode([query])[0]

    # Load embeddings
    data = np.load(EMBEDDINGS_PATH, allow_pickle=True).item()
    embeddings = data["embeddings"]
    session_ids = data["session_ids"]

    # Compute cosine similarities
    norms = np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    similarities = np.dot(embeddings, query_embedding) / (norms + 1e-10)

    # Get top results
    top_indices = np.argsort(similarities)[::-1][:limit * 2]  # Get more for filtering

    # Fetch session details
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    results = []
    for idx in top_indices:
        if len(results) >= limit:
            break

        session_id = session_ids[idx]
        score = float(similarities[idx])

        cursor = conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?",
            (session_id,)
        )
        row = cursor.fetchone()
        if row:
            if project and project.lower() not in (row["project_name"] or "").lower():
                continue
            results.append({
                "session_id": row["session_id"],
                "project": row["project_name"],
                "score": round(score, 3),
                "summary": json.loads(row["summaries_json"])[0] if row["summaries_json"] != "[]" else None,
                "first_message": row["first_user_message"][:200] if row["first_user_message"] else None,
                "start_time": row["start_time"],
                "message_count": row["message_count"],
            })

    conn.close()
    return results


def meta(session_id: str) -> Optional[dict]:
    """
    Get metadata for a session without loading messages.

    Args:
        session_id: The session UUID

    Returns:
        Session metadata dict or None if not found
    """
    if not DB_PATH.exists():
        return None

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    cursor = conn.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "session_id": row["session_id"],
        "project": row["project_name"],
        "project_path": row["project_path"],
        "git_branch": row["git_branch"],
        "start_time": row["start_time"],
        "end_time": row["end_time"],
        "message_counts": {
            "user": row["user_count"],
            "assistant": row["assistant_count"],
            "tool_use": row["tool_use_count"],
            "tool_result": row["tool_result_count"],
            "thinking": row["thinking_count"],
            "summary": row["summary_count"],
        },
        "summaries": json.loads(row["summaries_json"]),
        "tools_used": json.loads(row["tools_json"]),
        "first_message": row["first_user_message"],
    }


def _extract_messages(file_path: str, types: Optional[list] = None,
                      tools: Optional[list] = None,
                      first: Optional[int] = None,
                      last: Optional[int] = None,
                      offset: int = 0,
                      limit: Optional[int] = None) -> list[dict]:
    """Extract and filter messages from a session file."""

    all_types = types or ["user", "assistant", "summary", "thinking", "tool_use", "tool_result"]

    messages = []

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue

            msg_type = msg.get("type")

            if msg_type == "summary" and "summary" in all_types:
                messages.append({
                    "type": "summary",
                    "content": msg.get("summary"),
                })

            elif msg_type == "user":
                timestamp = msg.get("timestamp")
                content = msg.get("message", {}).get("content")

                if isinstance(content, str):
                    if "user" in all_types:
                        messages.append({
                            "type": "user",
                            "timestamp": timestamp,
                            "content": content,
                        })
                elif isinstance(content, list):
                    for block in content:
                        if block.get("type") == "tool_result" and "tool_result" in all_types:
                            tool_use_id = block.get("tool_use_id")
                            result_content = block.get("content", "")
                            if tools is None or True:  # Can't filter tool_result by name easily
                                messages.append({
                                    "type": "tool_result",
                                    "timestamp": timestamp,
                                    "tool_use_id": tool_use_id,
                                    "content": result_content[:2000] if isinstance(result_content, str) else str(result_content)[:2000],
                                })
                        elif block.get("type") == "text" and "user" in all_types:
                            messages.append({
                                "type": "user",
                                "timestamp": timestamp,
                                "content": block.get("text"),
                            })

            elif msg_type == "assistant":
                content = msg.get("message", {}).get("content", [])
                if isinstance(content, list):
                    for block in content:
                        block_type = block.get("type")

                        if block_type == "text" and "assistant" in all_types:
                            messages.append({
                                "type": "assistant",
                                "content": block.get("text"),
                            })
                        elif block_type == "thinking" and "thinking" in all_types:
                            messages.append({
                                "type": "thinking",
                                "content": block.get("thinking"),
                            })
                        elif block_type == "tool_use" and "tool_use" in all_types:
                            tool_name = block.get("name")
                            if tools is None or tool_name in tools:
                                messages.append({
                                    "type": "tool_use",
                                    "tool_name": tool_name,
                                    "tool_use_id": block.get("id"),
                                    "input": block.get("input"),
                                })

    # Apply positional filters
    if first is not None:
        messages = messages[:first]
    elif last is not None:
        messages = messages[-last:]
    else:
        if offset > 0:
            messages = messages[offset:]
        if limit is not None:
            messages = messages[:limit]

    return messages


def read(session_id: str,
         types: Optional[list] = None,
         tools: Optional[list] = None,
         first: Optional[int] = None,
         last: Optional[int] = None,
         offset: int = 0,
         limit: Optional[int] = None) -> list[dict]:
    """
    Read messages from a session with filtering.

    Args:
        session_id: The session UUID
        types: Filter by message types: user, assistant, summary, thinking, tool_use, tool_result
        tools: Filter tool_use by tool names: Write, Edit, Bash, Read, etc.
        first: Return only first N messages
        last: Return only last N messages
        offset: Skip first N messages (incompatible with first/last)
        limit: Maximum messages to return (incompatible with first/last)

    Returns:
        List of filtered messages
    """
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT file_path FROM sessions WHERE session_id = ?",
        (session_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return []

    file_path = row[0]
    if not Path(file_path).exists():
        return []

    return _extract_messages(file_path, types, tools, first, last, offset, limit)


def list_sessions(project: Optional[str] = None,
                  limit: int = 20,
                  order_by: str = "start_time") -> list[dict]:
    """
    List sessions with optional filtering.

    Args:
        project: Filter by project name (partial match)
        limit: Maximum results
        order_by: Sort field (start_time, message_count)

    Returns:
        List of session summaries
    """
    if not DB_PATH.exists():
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    query = "SELECT * FROM sessions"
    params = []

    if project:
        query += " WHERE project_name LIKE ?"
        params.append(f"%{project}%")

    query += f" ORDER BY {order_by} DESC LIMIT ?"
    params.append(limit)

    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [{
        "session_id": row["session_id"],
        "project": row["project_name"],
        "start_time": row["start_time"],
        "message_count": row["message_count"],
        "summary": json.loads(row["summaries_json"])[0] if row["summaries_json"] != "[]" else None,
        "first_message": row["first_user_message"][:150] if row["first_user_message"] else None,
    } for row in rows]
