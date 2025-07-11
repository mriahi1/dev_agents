"""GitHub API client for repository operations."""

import os
from typing import Optional, Dict, Any, List
from github import Github
from loguru import logger


class GitHubClient:
    """Client for interacting with GitHub API."""
    
    def __init__(self, token: str, repo: str):
        """Initialize GitHub client."""
        self.github = Github(token)
        self.repo_name = repo
        self.repo = self.github.get_repo(repo)
        logger.debug(f"Initialized GitHub client for {repo}")
    
    def create_branch(self, branch_name: str, base: str = "main") -> bool:
        """Create a new branch from base."""
        try:
            # Get the SHA of the base branch
            base_ref = self.repo.get_git_ref(f"heads/{base}")
            base_sha = base_ref.object.sha
            
            # Create new branch
            self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=base_sha
            )
            logger.info(f"Created branch {branch_name} from {base}")
            return True
        except Exception as e:
            if "Reference already exists" in str(e):
                logger.info(f"Branch {branch_name} already exists")
                return True
            logger.error(f"Failed to create branch: {e}")
            return False
    
    def create_pull_request(
        self,
        title: str,
        body: str,
        branch: str,
        base: str = "main"
    ) -> Optional[int]:
        """Create a pull request."""
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=branch,
                base=base
            )
            logger.info(f"Created PR #{pr.number}: {title}")
            logger.info(f"PR URL: {pr.html_url}")
            return pr.number
        except Exception as e:
            logger.error(f"Failed to create PR: {e}")
            return None
    
    def list_pull_requests(
        self,
        state: str = "all",
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """List pull requests.
        
        Args:
            state: 'open', 'closed', or 'all'
            limit: Maximum number of PRs to return
            
        Returns:
            List of PR information dictionaries
        """
        try:
            pulls = self.repo.get_pulls(
                state=state,
                sort="created",
                direction="desc"
            )
            
            pr_list = []
            for i, pr in enumerate(pulls):
                if i >= limit:
                    break
                    
                pr_info = {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "author": pr.user.login,
                    "created_at": pr.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "url": pr.html_url,
                    "base": pr.base.ref,
                    "head": pr.head.ref
                }
                pr_list.append(pr_info)
            
            logger.info(f"Found {len(pr_list)} pull requests")
            return pr_list
            
        except Exception as e:
            logger.error(f"Failed to list PRs: {e}")
            return []
    
    def create_or_update_file(
        self,
        path: str,
        content: str,
        message: str,
        branch: str
    ) -> bool:
        """Create or update a file in the repository."""
        try:
            # Try to get existing file
            try:
                file = self.repo.get_contents(path, ref=branch)
                # Update existing file
                self.repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=file.sha,
                    branch=branch
                )
                logger.info(f"Updated file {path} on branch {branch}")
            except:
                # Create new file
                self.repo.create_file(
                    path=path,
                    message=message,
                    content=content,
                    branch=branch
                )
                logger.info(f"Created file {path} on branch {branch}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to create/update file: {e}")
            return False 