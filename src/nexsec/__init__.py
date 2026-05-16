"""NexSec package shim — re-export from siyarix_agent for backwards compatibility.

This allows `import siyarix` while the current implementation lives in
`src/siyarix_agent`.
"""
from __future__ import annotations

from siyarix_agent import *  # noqa: F401,F403

__all__ = getattr(__import__("siyarix_agent"), "__all__", [])
