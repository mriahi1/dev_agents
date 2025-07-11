from typing import Dict, Optional
from github import Github, GithubException
from ..utils.types import GitHubPR
from loguru import logger
import base64

class GitHubClient:
    """Minimal GitHub client for MVP"""
    
    def __init__(self, token: str, repo_name: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo_name)
        
    def create_branch(self, branch_name: str, base: str = "staging") -> bool:
        """Create a new branch from staging"""
        try:
            # Check if branch already exists
            try:
                existing_ref = self.repo.get_git_ref(f"heads/{branch_name}")
                logger.warning(f"Branch {branch_name} already exists, deleting it first")
                # Delete the existing branch
                existing_ref.delete()
            except GithubException:
                # Branch doesn't exist, which is what we want
                pass
                
            base_ref = self.repo.get_git_ref(f"heads/{base}")
            self.repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=base_ref.object.sha
            )
            logger.info(f"Created branch: {branch_name}")
            return True
        except GithubException as e:
            logger.error(f"Failed to create branch: {e}")
            return False
    
    def update_file(
        self, 
        branch: str, 
        file_path: str, 
        new_content: str, 
        commit_message: str
    ) -> bool:
        """Update or create a file on a branch"""
        try:
            # Try to get current file
            try:
                file = self.repo.get_contents(file_path, ref=branch)
                # File exists, update it
                self.repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=new_content,
                    sha=file.sha,
                    branch=branch
                )
                logger.info(f"Updated existing file: {file_path}")
            except GithubException:
                # File doesn't exist, create it
                self.repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=new_content,
                    branch=branch
                )
                logger.info(f"Created new file: {file_path}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to update/create file: {e}")
            return False
    
    def create_pull_request(
        self,
        title: str,
        body: str,
        branch: str,
        base: str = "staging"
    ) -> Optional[GitHubPR]:
        """Create a PR to staging"""
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=branch,
                base=base
            )
            
            return GitHubPR(
                number=pr.number,
                html_url=pr.html_url,
                branch=branch
            )
        except Exception as e:
            logger.error(f"Failed to create PR: {e}")
            return None 