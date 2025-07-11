"""Type definitions for the Cursor DevOps Toolkit"""
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class LinearTask:
    """Linear task representation"""
    id: str
    identifier: str  # e.g., "PROJ-123"
    title: str
    description: str
    state: str
    labels: List[str]

@dataclass
class GitHubPR:
    """GitHub PR representation"""
    number: int
    html_url: str
    branch: str 