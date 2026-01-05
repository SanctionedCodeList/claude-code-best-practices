"""Pytest fixtures for testing sessions skill documentation."""

import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import pytest
import sys

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent / "scripts"))


@pytest.fixture
def temp_claude_dir(tmp_path, monkeypatch):
    """Create a temporary .claude directory structure with test sessions."""
    claude_dir = tmp_path / ".claude"
    projects_dir = claude_dir / "projects"
    index_dir = claude_dir / "session-index"

    # Create test project
    project_dir = projects_dir / "-test-project"
    project_dir.mkdir(parents=True)

    # Create a test session file
    session_id = "test-session-001"
    session_file = project_dir / f"{session_id}.jsonl"

    base_time = datetime(2026, 1, 5, 10, 0, 0)

    messages = [
        {"type": "summary", "summary": "Debug authentication flow", "leafUuid": "leaf-1"},
        {
            "type": "user",
            "message": {"role": "user", "content": "Help me fix the JWT token validation"},
            "timestamp": base_time.isoformat() + "Z",
            "sessionId": session_id,
            "cwd": "/test/project",
            "gitBranch": "main"
        },
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "thinking", "thinking": "Let me analyze the token validation..."},
                    {"type": "text", "text": "I'll help you fix the JWT validation. Let me check the code."},
                    {"type": "tool_use", "id": "tool-1", "name": "Read", "input": {"file_path": "/test/auth.py"}}
                ]
            }
        },
        {
            "type": "user",
            "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "tool-1", "content": "def validate_token(token):..."}
            ]},
            "timestamp": (base_time + timedelta(minutes=1)).isoformat() + "Z",
            "sessionId": session_id,
            "cwd": "/test/project",
            "gitBranch": "main"
        },
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "I found the issue. The token expiry check is incorrect."},
                    {"type": "tool_use", "id": "tool-2", "name": "Edit", "input": {"file_path": "/test/auth.py", "old": "exp > now", "new": "exp >= now"}}
                ]
            }
        },
        {
            "type": "user",
            "message": {"role": "user", "content": "Thanks, that fixed it!"},
            "timestamp": (base_time + timedelta(minutes=5)).isoformat() + "Z",
            "sessionId": session_id,
            "cwd": "/test/project",
            "gitBranch": "main"
        },
        {
            "type": "assistant",
            "message": {
                "role": "assistant",
                "content": [{"type": "text", "text": "You're welcome! The token validation should work correctly now."}]
            }
        }
    ]

    with open(session_file, 'w') as f:
        for msg in messages:
            f.write(json.dumps(msg) + "\n")

    # Patch the module constants
    import sessions
    monkeypatch.setattr(sessions, "CLAUDE_DIR", claude_dir)
    monkeypatch.setattr(sessions, "PROJECTS_DIR", projects_dir)
    monkeypatch.setattr(sessions, "INDEX_DIR", index_dir)
    monkeypatch.setattr(sessions, "DB_PATH", index_dir / "sessions.db")
    monkeypatch.setattr(sessions, "EMBEDDINGS_PATH", index_dir / "embeddings.npy")

    return {
        "claude_dir": claude_dir,
        "projects_dir": projects_dir,
        "index_dir": index_dir,
        "session_id": session_id,
        "session_file": session_file,
    }


@pytest.fixture
def indexed_sessions(temp_claude_dir):
    """Build the index for the test sessions."""
    import sessions
    stats = sessions.build_index(force=True, verbose=False)
    return {**temp_claude_dir, "stats": stats}


def pytest_markdown_docs_globals():
    """Provide globals available to all markdown code blocks."""
    # Import lazily to avoid issues when sessions isn't installed
    try:
        import sessions
        return {
            "sessions": sessions,
            "search": sessions.search,
            "meta": sessions.meta,
            "read": sessions.read,
            "list_sessions": sessions.list_sessions,
            "build_index": sessions.build_index,
        }
    except ImportError:
        return {}
