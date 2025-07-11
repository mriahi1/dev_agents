"""Linear API client for task management."""

from typing import List, Optional
import requests
from loguru import logger

from ..utils.types import LinearTask


class LinearClient:
    """Client for interacting with Linear API."""
    
    def __init__(self, api_key: str, team_id: str):
        """Initialize Linear client."""
        self.api_key = api_key
        self.team_id = team_id
        self.base_url = "https://api.linear.app/graphql"
        logger.debug(f"Initialized Linear client for team {team_id}")
    
    def get_ready_tasks(self, state: str = "Ready for Dev") -> List[LinearTask]:
        """Get tasks in specified state."""
        query = """
        query($teamId: ID!, $state: String!) {
            issues(
                filter: {
                    team: { id: { eq: $teamId } }
                    state: { name: { eq: $state } }
                }
                first: 50
            ) {
                nodes {
                    id
                    identifier
                    title
                    description
                    state { name }
                    labels { nodes { name } }
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": query,
                    "variables": {"teamId": self.team_id, "state": state}
                },
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return []
            
            issues = data.get("data", {}).get("issues", {}).get("nodes", [])
            logger.info(f"Found {len(issues)} tasks from Linear")
            
            return [
                LinearTask(
                    id=issue["id"],
                    identifier=issue["identifier"],
                    title=issue["title"],
                    description=issue.get("description", ""),
                    state=issue["state"]["name"],
                    labels=[label["name"] for label in issue.get("labels", {}).get("nodes", [])]
                )
                for issue in issues
            ]
            
        except Exception as e:
            logger.error(f"Failed to get tasks: {e}")
            return []
    
    def create_task(
        self,
        title: str,
        description: str = "",
        labels: List[str] = None
    ) -> Optional[str]:
        """Create a new task in Linear.
        
        Returns:
            Task identifier (e.g., "KEY-123") if successful, None otherwise
        """
        # First get the default state ID for "Ready for Dev"
        state_id = self._get_state_id("Ready for Dev")
        if not state_id:
            logger.error("Could not find 'Ready for Dev' state")
            return None
        
        # Get label IDs if provided
        label_ids = []
        if labels:
            label_ids = self._get_label_ids(labels)
        
        mutation = """
        mutation($teamId: String!, $title: String!, $description: String!, $stateId: String!, $labelIds: [String!]) {
            issueCreate(
                input: {
                    teamId: $teamId
                    title: $title
                    description: $description
                    stateId: $stateId
                    labelIds: $labelIds
                }
            ) {
                success
                issue {
                    id
                    identifier
                    title
                    url
                }
            }
        }
        """
        
        variables = {
            "teamId": self.team_id,
            "title": title,
            "description": description,
            "stateId": state_id
        }
        
        if label_ids:
            variables["labelIds"] = label_ids
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": mutation, "variables": variables},
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                logger.error(f"Failed to create task: {data['errors']}")
                return None
            
            if data.get("data", {}).get("issueCreate", {}).get("success"):
                issue = data["data"]["issueCreate"]["issue"]
                logger.info(f"Created task: {issue['identifier']} - {issue['title']}")
                return issue["identifier"]
            else:
                logger.error("Failed to create task")
                return None
                
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return None
    
    def update_task(
        self,
        task_id: str,
        state: Optional[str] = None,
        comment: Optional[str] = None
    ) -> bool:
        """Update a task's state and/or add a comment.
        
        Args:
            task_id: Task identifier (e.g., "KEY-123")
            state: New state name (e.g., "In Progress")
            comment: Comment to add
            
        Returns:
            True if successful, False otherwise
        """
        success = True
        
        # Update state if provided
        if state:
            state_id = self._get_state_id(state)
            if not state_id:
                logger.error(f"Could not find state '{state}'")
                return False
            
            success = self._update_task_state(task_id, state_id)
            if success:
                logger.info(f"Successfully updated task state to {state}")
        
        # Add comment if provided
        if comment and success:
            success = self._add_comment(task_id, comment)
            if success:
                logger.info("Successfully added comment")
        
        return success
    
    def _get_state_id(self, state_name: str) -> Optional[str]:
        """Get state ID from state name."""
        query = """
        query($teamId: ID!) {
            workflowStates(
                filter: { team: { id: { eq: $teamId } } }
            ) {
                nodes {
                    id
                    name
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": {"teamId": self.team_id}},
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            states = data.get("data", {}).get("workflowStates", {}).get("nodes", [])
            
            for state in states:
                if state["name"] == state_name:
                    return state["id"]
                    
            return None
            
        except Exception as e:
            logger.error(f"Error getting state ID: {e}")
            return None
    
    def _get_label_ids(self, label_names: List[str]) -> List[str]:
        """Get label IDs from label names."""
        query = """
        query($teamId: ID!) {
            issueLabels(
                filter: { team: { id: { eq: $teamId } } }
            ) {
                nodes {
                    id
                    name
                }
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": query, "variables": {"teamId": self.team_id}},
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            all_labels = data.get("data", {}).get("issueLabels", {}).get("nodes", [])
            
            label_ids = []
            for label_name in label_names:
                for label in all_labels:
                    if label["name"] == label_name:
                        label_ids.append(label["id"])
                        break
                        
            return label_ids
            
        except Exception as e:
            logger.error(f"Error getting label IDs: {e}")
            return []
    
    def _update_task_state(self, task_id: str, state_id: str) -> bool:
        """Update task state."""
        mutation = """
        mutation($issueId: String!, $stateId: String!) {
            issueUpdate(
                id: $issueId,
                input: { stateId: $stateId }
            ) {
                success
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": mutation,
                    "variables": {"issueId": task_id, "stateId": state_id}
                },
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                logger.error(f"Failed to update state: {data['errors']}")
                return False
                
            return data.get("data", {}).get("issueUpdate", {}).get("success", False)
            
        except Exception as e:
            logger.error(f"Error updating task state: {e}")
            return False
    
    def _add_comment(self, task_id: str, comment: str) -> bool:
        """Add comment to task."""
        mutation = """
        mutation($issueId: String!, $body: String!) {
            commentCreate(
                input: {
                    issueId: $issueId,
                    body: $body
                }
            ) {
                success
            }
        }
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={
                    "query": mutation,
                    "variables": {
                        "issueId": task_id,
                        "body": f"🤖 {comment}"
                    }
                },
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "errors" in data:
                logger.error(f"Failed to add comment: {data['errors']}")
                return False
                
            return data.get("data", {}).get("commentCreate", {}).get("success", False)
            
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            return False 