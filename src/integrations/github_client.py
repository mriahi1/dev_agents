"""GitHub API client for repository operations."""

import os
from typing import Optional, Dict, Any, List
from github import Github
from loguru import logger


class GitHubClient:
    """GitHub integration client."""
    
    def __init__(self, token: str, repo: str):
        """Initialize GitHub client.
        
        Args:
            token: GitHub personal access token
            repo: Repository in format 'owner/repo'
        """
        self.token = token
        self.repo_name = repo
        self.github = Github(token)
        self.repo = None
        logger.debug(f"Initialized GitHub client for {repo}")
    
    def _init_repo(self):
        """Initialize repository object if not already done."""
        if self.repo is None:
            self.repo = self.github.get_repo(self.repo_name)
    
    def create_branch(self, branch_name: str, base_branch: str = "main") -> bool:
        """Create a new branch from base."""
        self._init_repo()
        try:
            # Get the SHA of the base branch
            base_ref = self.repo.get_git_ref(f"heads/{base_branch}")
            base_sha = base_ref.object.sha
            
            # Create new branch
            self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=base_sha
            )
            logger.info(f"Created branch {branch_name} from {base_branch}")
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
        self._init_repo()
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
    
    def list_pull_requests(self, state: str = "open"):
        """List pull requests with specified state."""
        self._init_repo()
        
        if state == "all":
            # Get both open and closed PRs
            open_prs = list(self.repo.get_pulls(state='open'))
            closed_prs = list(self.repo.get_pulls(state='closed'))
            pulls = open_prs + closed_prs
        else:
            pulls = self.repo.get_pulls(state=state)
        
        pr_list = []
        for pr in pulls:
            pr_list.append({
                'number': pr.number,
                'title': pr.title,
                'state': pr.state,
                'author': pr.user.login,
                'created_at': pr.created_at.isoformat() if pr.created_at else None,
                'updated_at': pr.updated_at.isoformat() if pr.updated_at else None,
                'draft': pr.draft,
                'url': pr.html_url
            })
        
        return pr_list
    
    def get_pr_files(self, pr_number: int) -> List[str]:
        """Get list of changed files in a pull request."""
        self._init_repo()
        
        try:
            pr = self.repo.get_pull(pr_number)
            files = pr.get_files()
            
            # Return list of file paths
            return [f.filename for f in files]
        except github.GithubException as e:
            logger.error(f"Failed to get PR files: {e}")
            raise Exception(f"Failed to get PR #{pr_number} files: {e}")
    
    def create_or_update_file(
        self,
        path: str,
        content: str,
        message: str,
        branch: str
    ) -> bool:
        """Create or update a file in the repository."""
        self._init_repo()
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