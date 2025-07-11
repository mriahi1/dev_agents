"""Tests for GitHub client functionality."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.integrations.github_client import GitHubClient


@pytest.fixture
def mock_github():
    """Mock PyGithub."""
    with patch('src.integrations.github_client.Github') as mock_github_class:
        yield mock_github_class


@pytest.fixture
def github_client(mock_github):
    """Create a GitHub client instance for testing."""
    mock_instance = Mock()
    mock_repo = Mock()
    mock_instance.get_repo.return_value = mock_repo
    mock_github.return_value = mock_instance
    
    client = GitHubClient(token='test_token', repo='owner/repo')
    # Force initialization of repo by calling _init_repo
    client._init_repo()
    
    return client


class TestGitHubClient:
    """Test cases for GitHubClient."""

    def test_initialization(self, mock_github):
        """Test client initialization."""
        mock_instance = Mock()
        mock_github.return_value = mock_instance
        
        client = GitHubClient(token='test_token', repo='owner/repo')
        
        assert client.repo_name == 'owner/repo'
        assert client.repo is None  # Should be None initially
        mock_github.assert_called_once_with('test_token')
        
        # Test lazy initialization
        mock_repo = Mock()
        mock_instance.get_repo.return_value = mock_repo
        client._init_repo()
        
        assert client.repo == mock_repo
        mock_instance.get_repo.assert_called_once_with('owner/repo')

    def test_create_branch_success(self, github_client):
        """Test successful branch creation."""
        # Mock repo and refs
        mock_repo = github_client.repo
        mock_master_ref = Mock()
        mock_master_ref.object.sha = 'abc123'
        mock_repo.get_git_ref.return_value = mock_master_ref
        
        # Test branch creation
        result = github_client.create_branch('feature/test-branch')
        
        assert result is True
        mock_repo.create_git_ref.assert_called_once_with(
            ref='refs/heads/feature/test-branch',
            sha='abc123'
        )

    def test_create_branch_already_exists(self, github_client):
        """Test branch creation when branch already exists."""
        mock_repo = github_client.repo
        mock_repo.get_git_ref.side_effect = Exception("Reference already exists")
        
        result = github_client.create_branch('feature/existing-branch')
        
        assert result is True  # Should return True even if branch exists

    def test_create_branch_from_custom_base(self, github_client):
        """Test creating branch from custom base branch."""
        mock_repo = github_client.repo
        mock_base_ref = Mock()
        mock_base_ref.object.sha = 'def456'
        mock_repo.get_git_ref.return_value = mock_base_ref
        
        result = github_client.create_branch('feature/test', base_branch='staging')
        
        assert result is True
        mock_repo.get_git_ref.assert_called_with('heads/staging')

    def test_create_pull_request_success(self, github_client):
        """Test successful PR creation."""
        mock_repo = github_client.repo
        mock_pr = Mock()
        mock_pr.number = 123
        mock_pr.html_url = 'https://github.com/owner/repo/pull/123'
        mock_repo.create_pull.return_value = mock_pr
    
        pr_number = github_client.create_pull_request(
            title='Test PR',
            body='Test description',
            branch='feature/test'
        )
        
        assert pr_number == 123
        mock_repo.create_pull.assert_called_once_with(
            title='Test PR',
            body='Test description',
            head='feature/test',
            base='main'
        )

    def test_create_pull_request_with_custom_base(self, github_client):
        """Test PR creation with custom base branch."""
        mock_repo = github_client.repo
        mock_pr = Mock()
        mock_pr.number = 456
        mock_repo.create_pull.return_value = mock_pr
        
        pr_number = github_client.create_pull_request(
            title='Test PR',
            body='Test description',
            branch='feature/test',
            base='staging'
        )
        
        assert pr_number == 456
        mock_repo.create_pull.assert_called_once_with(
            title='Test PR',
            body='Test description',
            head='feature/test',
            base='staging'
        )

    def test_create_pull_request_failure(self, github_client):
        """Test PR creation failure."""
        mock_repo = github_client.repo
        mock_repo.create_pull.side_effect = Exception("API Error")
        
        pr_number = github_client.create_pull_request(
            title='Test PR',
            body='Test description',
            branch='feature/test'
        )
        
        assert pr_number is None

    def test_list_pull_requests_all(self, github_client):
        """Test listing all pull requests."""
        mock_repo = github_client.repo
        
        # Create mock PRs
        mock_pr1 = Mock()
        mock_pr1.number = 1
        mock_pr1.title = 'First PR'
        mock_pr1.state = 'open'
        mock_pr1.user.login = 'user1'
        mock_pr1.created_at = datetime(2023, 1, 1)
        mock_pr1.html_url = 'https://github.com/owner/repo/pull/1'
        mock_pr1.base.ref = 'main'
        mock_pr1.head.ref = 'feature/test1'
        
        mock_pr2 = Mock()
        mock_pr2.number = 2
        mock_pr2.title = 'Second PR'
        mock_pr2.state = 'closed'
        mock_pr2.user.login = 'user2'
        mock_pr2.created_at = datetime(2023, 1, 2)
        mock_pr2.html_url = 'https://github.com/owner/repo/pull/2'
        mock_pr2.base.ref = 'main'
        mock_pr2.head.ref = 'feature/test2'
        
        # Mock both calls for open and closed PRs
        mock_repo.get_pulls.side_effect = [[mock_pr1], [mock_pr2]]
        
        # Test list PRs
        prs = github_client.list_pull_requests(state='all')
        
        assert len(prs) == 2
        assert prs[0]['number'] == 1
        assert prs[0]['title'] == 'First PR'
        assert prs[0]['state'] == 'open'
        assert prs[1]['number'] == 2
        assert prs[1]['state'] == 'closed'
        
        # Should be called twice - once for open, once for closed
        assert mock_repo.get_pulls.call_count == 2
        mock_repo.get_pulls.assert_any_call(state='open')
        mock_repo.get_pulls.assert_any_call(state='closed')

    def test_list_pull_requests_open_only(self, github_client):
        """Test listing only open pull requests."""
        mock_repo = github_client.repo
        mock_pr = Mock()
        mock_pr.number = 1
        mock_pr.title = 'Open PR'
        mock_pr.state = 'open'
        mock_pr.user.login = 'user1'
        mock_pr.created_at = datetime.now()
        mock_pr.html_url = 'https://github.com/owner/repo/pull/1'
        mock_pr.base.ref = 'main'
        mock_pr.head.ref = 'feature/test'
        
        mock_repo.get_pulls.return_value = [mock_pr]
        
        prs = github_client.list_pull_requests(state='open')
        
        assert len(prs) == 1
        assert prs[0]['state'] == 'open'
        
        mock_repo.get_pulls.assert_called_once_with(state='open')

    def test_create_or_update_file_new(self, github_client):
        """Test creating a new file."""
        mock_repo = github_client.repo
        mock_repo.get_contents.side_effect = Exception("Not found")
        
        result = github_client.create_or_update_file(
            path='new_file.md',
            content='# New File',
            message='Add new file',
            branch='feature/test'
        )
        
        assert result is True
        mock_repo.create_file.assert_called_once_with(
            path='new_file.md',
            message='Add new file',
            content='# New File',
            branch='feature/test'
        )

    def test_create_or_update_file_existing(self, github_client):
        """Test updating an existing file."""
        mock_repo = github_client.repo
        mock_file = Mock()
        mock_file.sha = 'file_sha'
        mock_repo.get_contents.return_value = mock_file
        
        result = github_client.create_or_update_file(
            path='existing_file.md',
            content='# Updated Content',
            message='Update file',
            branch='feature/test'
        )
        
        assert result is True
        mock_repo.update_file.assert_called_once_with(
            path='existing_file.md',
            message='Update file',
            content='# Updated Content',
            sha='file_sha',
            branch='feature/test'
        ) 