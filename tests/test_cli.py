"""Tests for CLI commands."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner

from src.main import cli


@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv('LINEAR_API_KEY', 'test_linear_key')
    monkeypatch.setenv('LINEAR_TEAM_ID', 'test_team_id')
    monkeypatch.setenv('GITHUB_TOKEN', 'test_github_token')
    monkeypatch.setenv('GITHUB_REPO', 'test/repo')


class TestLinearCommands:
    """Test Linear CLI commands."""

    @patch('src.main.LinearClient')
    def test_linear_list_command(self, mock_client_class, runner, mock_env):
        """Test linear list command."""
        # Mock client
        mock_client = Mock()
        mock_client.get_ready_tasks.return_value = [
            Mock(
                id='1',
                identifier='KEY-100',
                title='Test task',
                description='Test description',
                state='Ready for Dev',
                labels=['bug', 'frontend']
            )
        ]
        mock_client_class.return_value = mock_client

        # Test normal output
        result = runner.invoke(cli, ['linear', 'list'])
        assert result.exit_code == 0
        assert 'KEY-100: Test task' in result.output
        assert 'Labels: bug, frontend' in result.output

        # Test JSON output
        result = runner.invoke(cli, ['linear', 'list', '--json'])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]['identifier'] == 'KEY-100'

    @patch('src.main.LinearClient')
    def test_linear_create_command(self, mock_client_class, runner, mock_env):
        """Test linear create command."""
        mock_client = Mock()
        mock_client.create_task.return_value = 'KEY-101'
        mock_client_class.return_value = mock_client

        result = runner.invoke(cli, [
            'linear', 'create',
            '--title', 'New task',
            '--description', 'Task description',
            '--labels', 'bug',
            '--labels', 'frontend'
        ])

        assert result.exit_code == 0
        assert 'Created task KEY-101' in result.output
        mock_client.create_task.assert_called_once_with(
            title='New task',
            description='Task description',
            labels=['bug', 'frontend']
        )

    @patch('src.main.LinearClient')
    def test_linear_update_command(self, mock_client_class, runner, mock_env):
        """Test linear update command."""
        mock_client = Mock()
        mock_client.update_task.return_value = True
        mock_client_class.return_value = mock_client

        result = runner.invoke(cli, [
            'linear', 'update', 'KEY-100',
            '--state', 'In Progress',
            '--comment', 'Starting work'
        ])

        assert result.exit_code == 0
        assert 'Updated task KEY-100' in result.output
        mock_client.update_task.assert_called_once_with(
            'KEY-100',
            state='In Progress',
            comment='Starting work'
        )

    def test_linear_list_missing_env(self, runner, monkeypatch):
        """Test linear list with missing environment variables."""
        # Clear the environment variables
        monkeypatch.delenv('LINEAR_API_KEY', raising=False)
        monkeypatch.delenv('LINEAR_TEAM_ID', raising=False)
        
        result = runner.invoke(cli, ['linear', 'list'])
        assert result.exit_code == 0
        assert 'Error: Please set LINEAR_API_KEY and LINEAR_TEAM_ID in .env file' in result.output


class TestGitHubCommands:
    """Test GitHub CLI commands."""

    @patch('src.main.GitHubClient')
    def test_github_branch_command(self, mock_client_class, runner, mock_env):
        """Test github branch command."""
        mock_client = Mock()
        mock_client.create_branch.return_value = True
        mock_client_class.return_value = mock_client

        result = runner.invoke(cli, ['github', 'branch', 'feature/test'])

        assert result.exit_code == 0
        assert 'Created branch feature/test' in result.output
        mock_client.create_branch.assert_called_once_with('feature/test', base='main')

    @patch('src.main.GitHubClient')
    def test_github_pr_create_command(self, mock_client_class, runner, mock_env):
        """Test github pr create command."""
        mock_client = Mock()
        mock_client.create_pull_request.return_value = 123
        mock_client_class.return_value = mock_client

        result = runner.invoke(cli, [
            'github', 'pr', 'create',
            '--title', 'Test PR',
            '--body', 'PR description',
            '--branch', 'feature/test',
            '--base', 'staging'
        ])

        assert result.exit_code == 0
        assert 'Created PR #123' in result.output
        mock_client.create_pull_request.assert_called_once_with(
            'Test PR',
            'PR description',
            'feature/test',
            'staging'
        )

    @patch('src.main.GitHubClient')
    def test_github_pr_list_command(self, mock_client_class, runner, mock_env):
        """Test github pr list command."""
        mock_client = Mock()
        mock_client.list_pull_requests.return_value = [
            {
                'number': 1,
                'title': 'First PR',
                'state': 'open',
                'author': 'user1',
                'created_at': '2023-01-01 12:00:00',
                'url': 'https://github.com/test/repo/pull/1',
                'base': 'main',
                'head': 'feature/test'
            }
        ]
        mock_client_class.return_value = mock_client

        # Test normal output
        result = runner.invoke(cli, ['github', 'pr', 'list'])
        assert result.exit_code == 0
        assert 'PR #1: First PR' in result.output
        assert 'Author: user1' in result.output

        # Test JSON output
        result = runner.invoke(cli, ['github', 'pr', 'list', '--json'])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]['number'] == 1

    def test_github_branch_missing_env(self, runner, monkeypatch):
        """Test github command with missing environment variables."""
        # Clear the environment variables
        monkeypatch.delenv('GITHUB_TOKEN', raising=False)
        monkeypatch.delenv('GITHUB_REPO', raising=False)
        
        result = runner.invoke(cli, ['github', 'branch', 'test'])
        assert result.exit_code == 0
        assert 'Error: Please set GITHUB_TOKEN and GITHUB_REPO in .env file' in result.output


class TestProjectCommands:
    """Test project management commands."""

    def test_project_list_no_projects(self, runner, monkeypatch):
        """Test project list with no configured projects."""
        # Clear all project-related environment variables
        for key in ['KEYSY3_GITHUB_REPO', 'IMMO_GITHUB_REPO', 'BACKEND_GITHUB_REPO', 
                    'TARGET_PROJECT', 'GITHUB_REPO']:
            monkeypatch.delenv(key, raising=False)
            
        result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0
        assert 'No projects configured' in result.output

    def test_project_list_with_projects(self, runner, monkeypatch):
        """Test project list with configured projects."""
        monkeypatch.setenv('KEYSY3_GITHUB_REPO', 'owner/keysy3')
        monkeypatch.setenv('IMMO_GITHUB_REPO', 'owner/immo')
        monkeypatch.setenv('TARGET_PROJECT', 'keysy3')
        monkeypatch.setenv('GITHUB_REPO', 'owner/default')

        result = runner.invoke(cli, ['project', 'list'])
        assert result.exit_code == 0
        assert '[✓] keysy3: owner/keysy3' in result.output
        assert '[ ] immo: owner/immo' in result.output

    def test_project_list_json(self, runner, monkeypatch):
        """Test project list JSON output."""
        # Clear any existing project env vars first
        for key in ['KEYSY3_GITHUB_REPO', 'IMMO_GITHUB_REPO', 'BACKEND_GITHUB_REPO', 
                    'TARGET_PROJECT', 'GITHUB_REPO']:
            monkeypatch.delenv(key, raising=False)
            
        monkeypatch.setenv('KEYSY3_GITHUB_REPO', 'owner/keysy3')
        monkeypatch.setenv('TARGET_PROJECT', 'keysy3')

        result = runner.invoke(cli, ['project', 'list', '--json'])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert len(data) == 1
        assert data[0]['name'] == 'keysy3'
        assert data[0]['active'] is True


class TestCLIGeneral:
    """Test general CLI functionality."""

    def test_cli_help(self, runner):
        """Test CLI help output."""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Cursor DevOps Toolkit' in result.output

    def test_cli_version(self, runner):
        """Test CLI version output."""
        result = runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '1.0.0' in result.output

    def test_linear_help(self, runner):
        """Test Linear group help."""
        result = runner.invoke(cli, ['linear', '--help'])
        assert result.exit_code == 0
        assert 'Linear issue tracking operations' in result.output

    def test_github_help(self, runner):
        """Test GitHub group help."""
        result = runner.invoke(cli, ['github', '--help'])
        assert result.exit_code == 0
        assert 'GitHub repository operations' in result.output 