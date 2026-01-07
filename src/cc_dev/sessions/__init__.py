"""
Claude Code Session History API

Provides search, meta, read, and list operations for Claude Code session histories.

Usage:
    from cc_dev.sessions import search, meta, read, list_sessions, sync

    # Search sessions semantically
    results = search("debugging authentication", limit=5)

    # Get session metadata
    info = meta(session_id)

    # Read messages with filtering
    messages = read(session_id, types=["user", "assistant"])

    # List recent sessions
    sessions = list_sessions(project="my-app", limit=10)

    # Sync the index (run periodically)
    stats = sync()
"""

from cc_dev.sessions.core import (
    search,
    meta,
    read,
    list_sessions,
    build_index as sync,
)

__all__ = ["search", "meta", "read", "list_sessions", "sync"]
