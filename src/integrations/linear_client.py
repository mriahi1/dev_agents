from typing import List, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_fixed
from ..utils.types import LinearTask
from loguru import logger
import os

class LinearClient:
    """Minimal Linear API client"""
    
    def __init__(self, api_key: str, team_id: str):
        self.api_key = api_key
        self.team_id = team_id
        self.base_url = "https://api.linear.app/graphql"
        
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def get_ready_tasks(self) -> List[LinearTask]:
        """Get tasks in Ready for Dev state"""
        
        query = """
        query($teamId: ID!) {
            issues(
                filter: {
                    team: { id: { eq: $teamId } }
                    state: { name: { eq: "Ready for Dev" } }
                }
                first: 20
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
        
        async with httpx.AsyncClient() as client:
            try:
                logger.debug(f"Making Linear API request to {self.base_url}")
                logger.debug(f"Team ID: {self.team_id}")
                
                response = await client.post(
                    self.base_url,
                    json={"query": query, "variables": {"teamId": self.team_id}},
                    headers={"Authorization": self.api_key}
                )
                
                logger.debug(f"Response status: {response.status_code}")
                
                if response.status_code != 200:
                    logger.error(f"Linear API error: Status {response.status_code}")
                    logger.error(f"Response body: {response.text}")
                    
                response.raise_for_status()
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e}")
                logger.error(f"Request URL: {e.request.url}")
                logger.error(f"Response status: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error: {type(e).__name__}: {e}")
                raise
            
        data = response.json()
        
        # Check for GraphQL errors
        if "errors" in data:
            logger.error(f"GraphQL errors: {data['errors']}")
            raise Exception(f"GraphQL query failed: {data['errors']}")
            
        # Check if data structure is as expected
        if "data" not in data or "issues" not in data["data"]:
            logger.error(f"Unexpected response structure: {data}")
            raise Exception(f"Unexpected Linear API response structure")
            
        issues = data["data"]["issues"]["nodes"]
        logger.info(f"Found {len(issues)} tasks from Linear")
        
        return [
            LinearTask(
                id=issue["id"],
                identifier=issue["identifier"],
                title=issue["title"],
                description=issue["description"] or "",
                state=issue["state"]["name"],
                labels=[label["name"] for label in issue["labels"]["nodes"]]
            )
            for issue in issues
        ]
    
    async def debug_get_all_tasks(self) -> List[dict]:
        """Debug method to get all tasks for the team"""
        query = """
        query($teamId: ID!) {
            issues(
                filter: {
                    team: { id: { eq: $teamId } }
                }
                first: 10
            ) {
                nodes {
                    id
                    identifier
                    title
                    description
                    state { name }
                    labels { nodes { name } }
                    assignee { name }
                }
            }
        }
        """
        
        async with httpx.AsyncClient() as client:
            try:
                logger.debug(f"Debug: Fetching all tasks for team {self.team_id}")
                
                response = await client.post(
                    self.base_url,
                    json={"query": query, "variables": {"teamId": self.team_id}},
                    headers={"Authorization": self.api_key}
                )
                
                response.raise_for_status()
                
            except Exception as e:
                logger.error(f"Debug query error: {e}")
                raise
            
        data = response.json()
        
        if "errors" in data:
            logger.error(f"GraphQL errors: {data['errors']}")
            raise Exception(f"GraphQL query failed: {data['errors']}")
            
        issues = data["data"]["issues"]["nodes"]
        logger.info(f"Debug: Found {len(issues)} total tasks")
        
        for issue in issues:
            logger.info(f"  - {issue['identifier']}: {issue['title']}")
            logger.info(f"    State: {issue['state']['name']}")
            logger.info(f"    Labels: {[label['name'] for label in issue['labels']['nodes']]}")
            logger.info(f"    Assignee: {issue['assignee']['name'] if issue['assignee'] else 'Unassigned'}")
            
        return issues
    
    async def create_task(self, title: str, description: str, state_name: str = "Ready for Dev", labels: List[str] = None) -> dict:
        """Create a new task in Linear"""
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
        
        # First, we need to get the state ID
        state_query = """
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
        
        # Get label IDs if labels are provided
        label_ids = []
        if labels:
            label_query = """
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
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    json={"query": label_query, "variables": {"teamId": self.team_id}},
                    headers={"Authorization": self.api_key}
                )
                response.raise_for_status()
                
            label_data = response.json()
            all_labels = label_data["data"]["issueLabels"]["nodes"]
            
            for label_name in labels:
                for label in all_labels:
                    if label["name"] == label_name:
                        label_ids.append(label["id"])
                        break
        
        async with httpx.AsyncClient() as client:
            # Get state ID
            response = await client.post(
                self.base_url,
                json={"query": state_query, "variables": {"teamId": self.team_id}},
                headers={"Authorization": self.api_key}
            )
            response.raise_for_status()
            
            state_data = response.json()
            states = state_data["data"]["workflowStates"]["nodes"]
            
            state_id = None
            for state in states:
                if state["name"] == state_name:
                    state_id = state["id"]
                    break
                    
            if not state_id:
                raise Exception(f"State '{state_name}' not found")
            
            # Create the issue
            logger.debug(f"Creating issue with variables: teamId={self.team_id}, title={title}, stateId={state_id}")
            
            # Build variables dict - only include labelIds if we have labels
            variables = {
                "teamId": self.team_id,
                "title": title,
                "description": description,
                "stateId": state_id
            }
            
            if label_ids:
                variables["labelIds"] = label_ids
                
            response = await client.post(
                self.base_url,
                json={
                    "query": mutation,
                    "variables": variables
                },
                headers={"Authorization": self.api_key}
            )
            
            if response.status_code != 200:
                logger.error(f"Create task failed with status {response.status_code}")
                logger.error(f"Response: {response.text}")
                
            response.raise_for_status()
            
        data = response.json()
        
        if "errors" in data:
            raise Exception(f"Failed to create task: {data['errors']}")
            
        if data["data"]["issueCreate"]["success"]:
            issue = data["data"]["issueCreate"]["issue"]
            logger.info(f"Created task: {issue['identifier']} - {issue['title']}")
            logger.info(f"Task URL: {issue['url']}")
            return issue
        else:
            raise Exception("Failed to create task")
    
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def update_task(self, task_id: str, state_name: str, comment: str) -> bool:
        """Update task state and add comment"""
        
        # First, get the state ID from state name
        state_query = """
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
        
        # Update state mutation
        state_mutation = """
        mutation($issueId: String!, $stateId: String!) {
            issueUpdate(
                id: $issueId,
                input: { stateId: $stateId }
            ) {
                success
            }
        }
        """
        
        # Then add comment
        comment_mutation = """
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
        
        async with httpx.AsyncClient() as client:
            try:
                # Get state ID
                response = await client.post(
                    self.base_url,
                    json={"query": state_query, "variables": {"teamId": self.team_id}},
                    headers={"Authorization": self.api_key}
                )
                response.raise_for_status()
                
                state_data = response.json()
                states = state_data["data"]["workflowStates"]["nodes"]
                
                state_id = None
                for state in states:
                    if state["name"] == state_name:
                        state_id = state["id"]
                        break
                        
                if not state_id:
                    raise Exception(f"State '{state_name}' not found")
                
                # Update state
                logger.debug(f"Updating task {task_id} to state: {state_name} (ID: {state_id})")
                response = await client.post(
                    self.base_url,
                    json={"query": state_mutation, "variables": {
                        "issueId": task_id,
                        "stateId": state_id
                    }},
                    headers={"Authorization": self.api_key}
                )
                
                if response.status_code != 200:
                    logger.error(f"Failed to update task state: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    raise Exception(f"Failed to update task state: HTTP {response.status_code}")
                
                data = response.json()
                if "errors" in data:
                    logger.error(f"GraphQL errors updating state: {data['errors']}")
                    raise Exception(f"Failed to update task state: {data['errors']}")
                    
                if not data.get("data", {}).get("issueUpdate", {}).get("success", False):
                    logger.error(f"State update failed: {data}")
                    raise Exception("Failed to update task state")
                    
                logger.info(f"Successfully updated task state to {state_name}")
                
                # Add comment
                logger.debug(f"Adding comment to task {task_id}")
                response = await client.post(
                    self.base_url,
                    json={"query": comment_mutation, "variables": {
                        "issueId": task_id,
                        "body": f"🤖 {comment}"
                    }},
                    headers={"Authorization": self.api_key}
                )
                
                if response.status_code != 200:
                    logger.error(f"Failed to add comment: {response.status_code}")
                    logger.error(f"Response: {response.text}")
                    # Don't fail if comment fails, just log it
                    
                data = response.json()
                if "errors" in data:
                    logger.error(f"GraphQL errors adding comment: {data['errors']}")
                    # Don't fail if comment fails, just log it
                    
            except Exception as e:
                logger.error(f"Error updating task: {e}")
                raise
            
        return True 