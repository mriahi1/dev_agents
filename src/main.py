#!/usr/bin/env python3
"""
Cursor DevOps Toolkit - CLI for Linear and GitHub operations
"""
import asyncio
import click
import os
from dotenv import load_dotenv
from loguru import logger
from .integrations.linear_client import LinearClient
from .integrations.github_client import GitHubClient
from .utils.types import LinearTask, GitHubPR
import json

load_dotenv()

# Configure logging based on debug flag
def setup_logging(debug: bool):
    logger.remove()
    level = "DEBUG" if debug else "INFO"
    logger.add(lambda msg: print(msg, end=""), level=level)

@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable debug logging')
@click.pass_context
def cli(ctx, debug):
    """Cursor DevOps Toolkit - Extend Cursor with Linear and GitHub capabilities"""
    setup_logging(debug)
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug

@cli.group()
@click.pass_context
def linear(ctx):
    """Linear issue tracking commands"""
    ctx.obj['linear'] = LinearClient(
        api_key=os.getenv("LINEAR_API_KEY"),
        team_id=os.getenv("LINEAR_TEAM_ID")
    )

@linear.command('list')
@click.option('--state', default='Ready for Dev', help='Filter by state')
@click.option('--limit', default=10, help='Maximum number of tasks')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def list_tasks_cmd(ctx, state, limit, output_json):
    """List Linear tasks"""
    
    async def list_tasks():
        client = ctx.obj['linear']
        
        # For now, using the existing method that filters by state
        tasks = await client.get_ready_tasks()
        
        if output_json:
            # Output JSON for Cursor to parse
            data = [{
                'id': t.id,
                'identifier': t.identifier,
                'title': t.title,
                'state': t.state,
                'labels': t.labels,
                'description': t.description[:200] + '...' if len(t.description) > 200 else t.description
            } for t in tasks[:limit]]
            print(json.dumps(data, indent=2))
        else:
            # Human-readable output
            if not tasks:
                logger.info(f"No tasks found in '{state}' state")
                return
                
            logger.info(f"Found {len(tasks)} tasks in '{state}' state:")
            for task in tasks[:limit]:
                print(f"\n📋 {task.identifier}: {task.title}")
                print(f"   State: {task.state}")
                print(f"   Labels: {', '.join(task.labels) if task.labels else 'None'}")
    
    asyncio.run(list_tasks())

@linear.command('create')
@click.option('--title', required=True, help='Task title')
@click.option('--description', required=True, help='Task description')
@click.option('--state', default='Ready for Dev', help='Initial state')
@click.option('--labels', multiple=True, help='Labels to add')
@click.pass_context
def create_task_cmd(ctx, title, description, state, labels):
    """Create a new Linear task"""
    
    async def create_task():
        client = ctx.obj['linear']
        
        try:
            task = await client.create_task(
                title=title,
                description=description,
                state_name=state,
                labels=list(labels) if labels else None
            )
            logger.success(f"Created task {task['identifier']}: {task['title']}")
            logger.info(f"URL: {task['url']}")
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
    
    asyncio.run(create_task())

@linear.command('update')
@click.argument('task_id')
@click.option('--state', help='New state')
@click.option('--comment', help='Add a comment')
@click.pass_context
def update_task_cmd(ctx, task_id, state, comment):
    """Update a Linear task"""
    
    async def update_task():
        client = ctx.obj['linear']
        
        if not state and not comment:
            logger.error("Provide either --state or --comment")
            return
            
        try:
            if state:
                await client.update_task(
                    task_id=task_id,
                    state_name=state,
                    comment=comment or f"Updated to {state}"
                )
                logger.success(f"Updated task {task_id}")
        except Exception as e:
            logger.error(f"Failed to update task: {e}")
    
    asyncio.run(update_task())

@cli.group()
@click.option('--repo', help='Repository (owner/name)')
@click.pass_context
def github(ctx, repo):
    """GitHub repository commands"""
    repo_name = repo or os.getenv("GITHUB_REPO")
    
    if not repo_name:
        # Try to get from current project
        target_project = os.getenv("TARGET_PROJECT")
        if target_project:
            repo_env = f"{target_project.upper().replace('-', '_')}_GITHUB_REPO"
            repo_name = os.getenv(repo_env)
    
    if not repo_name:
        logger.error("No repository specified. Use --repo or set GITHUB_REPO")
        ctx.exit(1)
        
    ctx.obj['github'] = GitHubClient(
        token=os.getenv("GITHUB_TOKEN"),
        repo_name=repo_name
    )

@github.command('branch')
@click.argument('branch_name')
@click.option('--base', default='staging', help='Base branch')
@click.pass_context
def create_branch(ctx, branch_name, base):
    """Create a new branch"""
    client = ctx.obj['github']
    
    try:
        if client.create_branch(branch_name, base):
            logger.success(f"Created branch '{branch_name}' from '{base}'")
        else:
            logger.error("Failed to create branch")
    except Exception as e:
        logger.error(f"Error: {e}")

@github.group('pr')
def pr_group():
    """Pull request commands"""
    pass

@pr_group.command('create')
@click.option('--title', required=True, help='PR title')
@click.option('--body', required=True, help='PR description')
@click.option('--branch', required=True, help='Source branch')
@click.option('--base', default='staging', help='Target branch')
@click.pass_context
def create_pr(ctx, title, body, branch, base):
    """Create a pull request"""
    client = ctx.obj['github']
    
    try:
        pr = client.create_pull_request(title, body, branch, base)
        if pr:
            logger.success(f"Created PR #{pr.number}")
            logger.info(f"URL: {pr.html_url}")
        else:
            logger.error("Failed to create PR")
    except Exception as e:
        logger.error(f"Error: {e}")

@pr_group.command('list')
@click.option('--state', default='open', help='PR state (open/closed/all)')
@click.option('--json', 'output_json', is_flag=True, help='Output as JSON')
@click.pass_context
def list_prs(ctx, state, output_json):
    """List pull requests"""
    client = ctx.obj['github']
    
    # This would need to be implemented in GitHubClient
    logger.info(f"Listing {state} pull requests...")
    # TODO: Implement PR listing

# Multi-project support
@cli.command('projects')
@click.option('--set', 'project_name', help='Set active project')
def projects(project_name):
    """Manage multiple projects"""
    if project_name:
        # Update .env with new TARGET_PROJECT
        logger.info(f"Switching to project: {project_name}")
        # TODO: Implement project switching
    else:
        # List available projects
        logger.info("Available projects:")
        # TODO: List projects from configuration

if __name__ == '__main__':
    cli() 