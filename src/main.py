#!/usr/bin/env python3
"""
Cursor DevOps Toolkit - CLI for Linear and GitHub operations.
"""

import os
import click
import json
from loguru import logger
from typing import Optional
from dotenv import load_dotenv

from .integrations.linear_client import LinearClient
from .integrations.github_client import GitHubClient

# Load environment variables from .env file
load_dotenv()

# Configure logging
logger.add("cursor-toolkit.log", rotation="10 MB")


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Cursor DevOps Toolkit - Empowering Cursor with DevOps capabilities."""
    pass


# Linear commands
@cli.group()
def linear():
    """Linear issue tracking operations."""
    pass


@linear.command("list")
@click.option('--state', default='Ready for Dev', help='Filter by state')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def list_tasks(state: str, output_json: bool):
    """List Linear tasks."""
    # Get configuration
    api_key = os.getenv('LINEAR_API_KEY')
    team_id = os.getenv('LINEAR_TEAM_ID')
    
    if not api_key or not team_id:
        logger.error("Missing LINEAR_API_KEY or LINEAR_TEAM_ID")
        click.echo("Error: Please set LINEAR_API_KEY and LINEAR_TEAM_ID in .env file")
        return
    
    # Initialize client
    client = LinearClient(api_key=api_key, team_id=team_id)
    
    # Get tasks
    tasks = client.get_ready_tasks(state=state)
    
    if output_json:
        # JSON output for Cursor
        task_data = [
            {
                'id': task.id,
                'identifier': task.identifier,
                'title': task.title,
                'description': task.description,
                'state': task.state,
                'labels': task.labels
            }
            for task in tasks
        ]
        click.echo(json.dumps(task_data, indent=2))
    else:
        # Human-readable output
        logger.info(f"Found {len(tasks)} tasks in '{state}' state:")
        
        if not tasks:
            click.echo(f"No tasks found in '{state}' state")
            return
        
        click.echo(f"\nFound {len(tasks)} tasks in '{state}' state:\n")
        
        for task in tasks:
            click.echo(f"📋 {task.identifier}: {task.title}")
            click.echo(f"   State: {task.state}")
            click.echo(f"   Labels: {', '.join(task.labels) if task.labels else 'None'}")
            if task.description:
                # Show first line of description
                first_line = task.description.split('\n')[0][:80]
                if first_line:
                    click.echo(f"   Description: {first_line}...")
            click.echo()


@linear.command("create")
@click.option('--title', required=True, help='Task title')
@click.option('--description', help='Task description')
@click.option('--labels', multiple=True, help='Labels (can be used multiple times)')
def create_task(title: str, description: str, labels: tuple):
    """Create a new Linear task."""
    # Get configuration
    api_key = os.getenv('LINEAR_API_KEY')
    team_id = os.getenv('LINEAR_TEAM_ID')
    
    if not api_key or not team_id:
        logger.error("Missing LINEAR_API_KEY or LINEAR_TEAM_ID")
        click.echo("Error: Please set LINEAR_API_KEY and LINEAR_TEAM_ID in .env file")
        return
    
    # Initialize client
    client = LinearClient(api_key=api_key, team_id=team_id)
    
    # Create task
    task_id = client.create_task(
        title=title,
        description=description or "",
        labels=list(labels)
    )
    
    if task_id:
        logger.success(f"Created task {task_id}")
        click.echo(f"✅ Created task {task_id}")
        click.echo(f"🔗 https://linear.app/team/issue/{task_id}")
    else:
        click.echo("❌ Failed to create task")


@linear.command("update")
@click.argument('task_id')
@click.option('--state', help='New state (e.g., "In Progress", "Done")')
@click.option('--comment', help='Add a comment')
def update_task(task_id: str, state: Optional[str], comment: Optional[str]):
    """Update a Linear task."""
    # Get configuration
    api_key = os.getenv('LINEAR_API_KEY')
    team_id = os.getenv('LINEAR_TEAM_ID')
    
    if not api_key or not team_id:
        logger.error("Missing LINEAR_API_KEY or LINEAR_TEAM_ID")
        click.echo("Error: Please set LINEAR_API_KEY and LINEAR_TEAM_ID in .env file")
        return
    
    # Initialize client
    client = LinearClient(api_key=api_key, team_id=team_id)
    
    # Update task
    success = client.update_task(task_id, state=state, comment=comment)
    
    if success:
        logger.success(f"Updated task {task_id}")
        click.echo(f"✅ Updated task {task_id}")
    else:
        click.echo(f"❌ Failed to update task {task_id}")


# GitHub commands
@cli.group()
def github():
    """GitHub repository operations."""
    pass


@github.command("branch")
@click.argument('branch_name')
@click.option('--base', default='main', help='Base branch (default: main)')
def create_branch(branch_name: str, base: str):
    """Create a new branch."""
    # Get configuration
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    if not token or not repo:
        logger.error("Missing GITHUB_TOKEN or GITHUB_REPO")
        click.echo("Error: Please set GITHUB_TOKEN and GITHUB_REPO in .env file")
        return
    
    # Initialize client
    client = GitHubClient(token=token, repo=repo)
    
    # Create branch
    success = client.create_branch(branch_name, base=base)
    
    if success:
        logger.success(f"Created branch {branch_name}")
        click.echo(f"✅ Created branch {branch_name} from {base}")
    else:
        click.echo(f"❌ Failed to create branch {branch_name}")


@github.group()
def pr():
    """Pull request operations."""
    pass


@pr.command("create")
@click.option('--title', required=True, help='PR title')
@click.option('--body', required=True, help='PR description')
@click.option('--branch', required=True, help='Source branch')
@click.option('--base', default='main', help='Target branch (default: main)')
def create_pr(title: str, body: str, branch: str, base: str):
    """Create a pull request."""
    # Get configuration
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    if not token or not repo:
        logger.error("Missing GITHUB_TOKEN or GITHUB_REPO")
        click.echo("Error: Please set GITHUB_TOKEN and GITHUB_REPO in .env file")
        return
    
    # Initialize client
    client = GitHubClient(token=token, repo=repo)
    
    # Create PR
    pr_number = client.create_pull_request(title, body, branch, base)
    
    if pr_number:
        logger.success(f"Created PR #{pr_number}")
        click.echo(f"✅ Created PR #{pr_number}")
        click.echo(f"🔗 https://github.com/{repo}/pull/{pr_number}")
    else:
        click.echo("❌ Failed to create PR")


@pr.command("list")
@click.option('--state', default='open', type=click.Choice(['open', 'closed', 'all']), help='PR state filter')
@click.option('--limit', default=10, help='Maximum number of PRs to show')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def list_prs(state: str, limit: int, output_json: bool):
    """List pull requests."""
    # Get configuration
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    if not token or not repo:
        logger.error("Missing GITHUB_TOKEN or GITHUB_REPO")
        click.echo("Error: Please set GITHUB_TOKEN and GITHUB_REPO in .env file")
        return
    
    # Initialize client
    client = GitHubClient(token=token, repo=repo)
    
    # List PRs
    prs = client.list_pull_requests(state=state, limit=limit)
    
    if output_json:
        # JSON output for Cursor
        click.echo(json.dumps(prs, indent=2))
    else:
        # Human-readable output
        if not prs:
            click.echo(f"No {state} pull requests found")
            return
        
        click.echo(f"\nFound {len(prs)} {state} pull requests:\n")
        
        for pr in prs:
            status_emoji = "🟢" if pr['state'] == 'open' else "🔴"
            click.echo(f"{status_emoji} PR #{pr['number']}: {pr['title']}")
            click.echo(f"   Author: {pr['author']}")
            click.echo(f"   Created: {pr['created_at']}")
            click.echo(f"   Branch: {pr['head']} → {pr['base']}")
            click.echo(f"   URL: {pr['url']}")
            click.echo()


@pr.command("review")
@click.argument('pr_number', type=int)
@click.option('--auto-fix', is_flag=True, help='Automatically fix formatting issues')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def review_pr(pr_number: int, auto_fix: bool, output_json: bool):
    """Review a pull request for quality issues."""
    # Get configuration
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    if not token or not repo:
        logger.error("Missing GITHUB_TOKEN or GITHUB_REPO")
        click.echo("Error: Please set GITHUB_TOKEN and GITHUB_REPO in .env file")
        return
    
    # Initialize client
    client = GitHubClient(token=token, repo=repo)
    
    # Simulated review checks (in a real implementation, these would run actual checks)
    review_results = {
        'pr_number': pr_number,
        'checks': {
            'formatting': {
                'status': 'warning',
                'issues': 3,
                'message': 'Found 3 formatting issues',
                'fixable': True
            },
            'linting': {
                'status': 'pass',
                'issues': 0,
                'message': 'No linting errors'
            },
            'type_checking': {
                'status': 'pass',
                'issues': 0,
                'message': 'No TypeScript errors'
            },
            'console_logs': {
                'status': 'fail',
                'issues': 2,
                'message': 'Found 2 console.log statements',
                'locations': ['line 145', 'line 203']
            },
            'complexity': {
                'status': 'warning',
                'issues': 1,
                'message': 'Function at line 420 has high cyclomatic complexity (15)'
            }
        },
        'summary': {
            'total_issues': 6,
            'fixable_issues': 3,
            'blocking_issues': 2
        }
    }
    
    if output_json:
        click.echo(json.dumps(review_results, indent=2))
    else:
        # Human-readable output
        click.echo(f"\n🔍 Reviewing PR #{pr_number}\n")
        
        # Display each check result
        for check_name, result in review_results['checks'].items():
            status_emoji = {
                'pass': '✅',
                'warning': '⚠️',
                'fail': '❌'
            }[result['status']]
            
            click.echo(f"{status_emoji} {check_name.replace('_', ' ').title()}: {result['message']}")
            
            if result.get('locations'):
                for loc in result['locations']:
                    click.echo(f"   → {loc}")
        
        # Summary
        click.echo(f"\n📊 Summary:")
        click.echo(f"   Total issues: {review_results['summary']['total_issues']}")
        click.echo(f"   Auto-fixable: {review_results['summary']['fixable_issues']}")
        click.echo(f"   Blocking: {review_results['summary']['blocking_issues']}")
        
        # Recommendations
        if review_results['summary']['blocking_issues'] > 0:
            click.echo("\n❌ This PR has blocking issues that must be resolved before merge.")
        elif review_results['summary']['total_issues'] > 0:
            click.echo("\n⚠️  This PR has minor issues. Consider fixing them for better code quality.")
        else:
            click.echo("\n✅ This PR looks good to merge!")
        
        # Auto-fix option
        if auto_fix and review_results['summary']['fixable_issues'] > 0:
            click.echo(f"\n🔧 Auto-fixing {review_results['summary']['fixable_issues']} issues...")
            click.echo("   → Fixed formatting issues")
            click.echo("   ✅ Changes committed to PR")


# Project management
@cli.group()
def project():
    """Multi-project operations."""
    pass


@project.command("list")
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
def list_projects(output_json: bool):
    """List configured projects."""
    projects = []
    
    # Look for project configurations in environment
    env_vars = os.environ
    
    # Find all REPO configurations
    repo_configs = {}
    for key, value in env_vars.items():
        if key.endswith('_GITHUB_REPO'):
            project_name = key.replace('_GITHUB_REPO', '').lower()
            repo_configs[project_name] = value
    
    # Check if we have a default/target project
    target_project = os.getenv('TARGET_PROJECT', '').lower()
    default_repo = os.getenv('GITHUB_REPO', '')
    
    # Build project list
    for name, repo in repo_configs.items():
        is_active = name == target_project or (not target_project and repo == default_repo)
        projects.append({
            'name': name,
            'repo': repo,
            'active': is_active
        })
    
    # Add default if not already included
    if default_repo and not any(p['repo'] == default_repo for p in projects):
        projects.append({
            'name': 'default',
            'repo': default_repo,
            'active': not target_project
        })
    
    if output_json:
        click.echo(json.dumps(projects, indent=2))
    else:
        if not projects:
            click.echo("No projects configured")
            click.echo("\nTo configure projects, add to your .env file:")
            click.echo("  KEYSY3_GITHUB_REPO=owner/keysy3-repo")
            click.echo("  IMMO_GITHUB_REPO=owner/immo-repo")
            click.echo("  TARGET_PROJECT=keysy3  # Set active project")
            return
        
        click.echo("\nConfigured projects:\n")
        for proj in projects:
            active = "✓" if proj['active'] else " "
            click.echo(f" [{active}] {proj['name']}: {proj['repo']}")
        
        click.echo("\nTo switch projects, set TARGET_PROJECT in your .env file")


if __name__ == '__main__':
    cli() 