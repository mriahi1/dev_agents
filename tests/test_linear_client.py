"""Tests for Linear client functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.integrations.linear_client import LinearClient
from src.utils.types import LinearTask


@pytest.fixture
def mock_linear_api():
    """Mock Linear GraphQL API responses."""
    with patch('src.integrations.linear_client.requests.post') as mock_post:
        yield mock_post


@pytest.fixture
def linear_client():
    """Create a Linear client instance for testing."""
    return LinearClient(api_key='test_api_key', team_id='test_team_id')


class TestLinearClient:
    """Test cases for LinearClient."""

    def test_initialization(self):
        """Test client initialization."""
        client = LinearClient(api_key='test_key', team_id='team_123')
        assert client.api_key == 'test_key'
        assert client.team_id == 'team_123'
        assert client.base_url == 'https://api.linear.app/graphql'

    def test_get_ready_tasks_success(self, linear_client, mock_linear_api):
        """Test successful retrieval of ready tasks."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {
                'issues': {
                    'nodes': [
                        {
                            'id': '123',
                            'identifier': 'KEY-100',
                            'title': 'Fix bug in dashboard',
                            'description': 'Dashboard shows error',
                            'state': {'name': 'Ready for Dev'},
                            'labels': {'nodes': [{'name': 'bug'}, {'name': 'frontend'}]}
                        },
                        {
                            'id': '456',
                            'identifier': 'KEY-101',
                            'title': 'Add loading state',
                            'description': 'Add spinner to form',
                            'state': {'name': 'Ready for Dev'},
                            'labels': {'nodes': []}
                        }
                    ]
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_linear_api.return_value = mock_response

        # Get tasks
        tasks = linear_client.get_ready_tasks()

        # Verify
        assert len(tasks) == 2
        assert tasks[0].identifier == 'KEY-100'
        assert tasks[0].title == 'Fix bug in dashboard'
        assert 'bug' in tasks[0].labels
        assert tasks[1].identifier == 'KEY-101'
        assert len(tasks[1].labels) == 0

    def test_get_ready_tasks_empty(self, linear_client, mock_linear_api):
        """Test when no ready tasks exist."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {'issues': {'nodes': []}}
        }
        mock_response.raise_for_status = Mock()
        mock_linear_api.return_value = mock_response

        tasks = linear_client.get_ready_tasks()
        assert len(tasks) == 0

    def test_get_ready_tasks_api_error(self, linear_client, mock_linear_api):
        """Test API error handling."""
        mock_linear_api.side_effect = Exception("API Error")
        
        tasks = linear_client.get_ready_tasks()
        assert len(tasks) == 0  # Should return empty list on error

    def test_create_task_success(self, linear_client, mock_linear_api):
        """Test successful task creation."""
        # Mock state query response
        mock_state_response = Mock()
        mock_state_response.json.return_value = {
            'data': {
                'workflowStates': {
                    'nodes': [
                        {'id': 'state-1', 'name': 'Ready for Dev'},
                        {'id': 'state-2', 'name': 'In Progress'}
                    ]
                }
            }
        }
        mock_state_response.raise_for_status = Mock()
        
        # Mock label query response
        mock_label_response = Mock()
        mock_label_response.json.return_value = {
            'data': {
                'issueLabels': {
                    'nodes': [
                        {'id': 'label-1', 'name': 'feature'},
                        {'id': 'label-2', 'name': 'bug'}
                    ]
                }
            }
        }
        mock_label_response.raise_for_status = Mock()
        
        # Mock create task response
        mock_create_response = Mock()
        mock_create_response.json.return_value = {
            'data': {
                'issueCreate': {
                    'success': True,
                    'issue': {
                        'id': '789',
                        'identifier': 'KEY-102',
                        'title': 'New task',
                        'url': 'https://linear.app/team/issue/KEY-102'
                    }
                }
            }
        }
        mock_create_response.raise_for_status = Mock()
        
        # Set up side effects for multiple calls
        mock_linear_api.side_effect = [
            mock_state_response,  # First call: get states
            mock_label_response,  # Second call: get labels
            mock_create_response  # Third call: create task
        ]

        task_id = linear_client.create_task(
            title='New task',
            description='Task description',
            labels=['feature']
        )

        assert task_id == 'KEY-102'
        assert mock_linear_api.call_count == 3

    def test_create_task_without_labels(self, linear_client, mock_linear_api):
        """Test task creation without labels."""
        # Mock state query response
        mock_state_response = Mock()
        mock_state_response.json.return_value = {
            'data': {
                'workflowStates': {
                    'nodes': [
                        {'id': 'state-1', 'name': 'Ready for Dev'}
                    ]
                }
            }
        }
        mock_state_response.raise_for_status = Mock()
        
        # Mock create task response
        mock_create_response = Mock()
        mock_create_response.json.return_value = {
            'data': {
                'issueCreate': {
                    'success': True,
                    'issue': {
                        'id': '790',
                        'identifier': 'KEY-103',
                        'title': 'Task without labels',
                        'url': 'https://linear.app/team/issue/KEY-103'
                    }
                }
            }
        }
        mock_create_response.raise_for_status = Mock()
        
        # Set up side effects - no label query when labels not provided
        mock_linear_api.side_effect = [
            mock_state_response,  # First call: get states
            mock_create_response  # Second call: create task
        ]

        task_id = linear_client.create_task(
            title='Task without labels',
            description='No labels needed'
        )

        assert task_id == 'KEY-103'
        assert mock_linear_api.call_count == 2  # Only state query and create

    def test_update_task_state_success(self, linear_client, mock_linear_api):
        """Test successful task state update."""
        # Mock getting workflow states
        mock_response_states = Mock()
        mock_response_states.json.return_value = {
            'data': {
                'workflowStates': {
                    'nodes': [
                        {'id': 'state-1', 'name': 'Ready for Dev'},
                        {'id': 'state-2', 'name': 'In Progress'},
                        {'id': 'state-3', 'name': 'In Review'}
                    ]
                }
            }
        }
        mock_response_states.raise_for_status = Mock()
        
        # Mock update response
        mock_response_update = Mock()
        mock_response_update.json.return_value = {
            'data': {
                'issueUpdate': {
                    'success': True
                }
            }
        }
        mock_response_update.raise_for_status = Mock()
        
        # Set up side effects for multiple calls
        mock_linear_api.side_effect = [mock_response_states, mock_response_update]

        # Update task
        result = linear_client.update_task('KEY-100', state='In Progress')
        
        assert result is True
        assert mock_linear_api.call_count == 2

    def test_update_task_with_comment(self, linear_client, mock_linear_api):
        """Test updating task with state and comment."""
        # Mock getting workflow states
        mock_response_states = Mock()
        mock_response_states.json.return_value = {
            'data': {
                'workflowStates': {
                    'nodes': [
                        {'id': 'state-1', 'name': 'Ready for Dev'},
                        {'id': 'state-2', 'name': 'In Progress'}
                    ]
                }
            }
        }
        mock_response_states.raise_for_status = Mock()
        
        # Mock update response
        mock_response_update = Mock()
        mock_response_update.json.return_value = {
            'data': {
                'issueUpdate': {
                    'success': True
                }
            }
        }
        mock_response_update.raise_for_status = Mock()
        
        # Mock comment response
        mock_response_comment = Mock()
        mock_response_comment.json.return_value = {
            'data': {
                'commentCreate': {
                    'success': True
                }
            }
        }
        mock_response_comment.raise_for_status = Mock()
        
        # Set up side effects for multiple calls
        mock_linear_api.side_effect = [
            mock_response_states,   # Get states
            mock_response_update,   # Update state
            mock_response_comment   # Add comment
        ]

        # Update task
        result = linear_client.update_task('KEY-100', state='In Progress', comment='Starting work')
        
        assert result is True
        assert mock_linear_api.call_count == 3

    def test_update_task_invalid_state(self, linear_client, mock_linear_api):
        """Test updating task with invalid state."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'data': {
                'workflowStates': {
                    'nodes': [
                        {'id': 'state-1', 'name': 'Ready for Dev'},
                        {'id': 'state-2', 'name': 'In Progress'}
                    ]
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_linear_api.return_value = mock_response

        # Try to update with non-existent state
        result = linear_client.update_task('KEY-100', state='Invalid State')
        
        assert result is False  # Should fail gracefully 