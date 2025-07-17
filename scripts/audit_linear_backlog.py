#!/usr/bin/env python3
"""
Linear Backlog Audit Script

This script audits all issues in the Linear backlog to ensure they are:
1. Clear and well-defined
2. Actionable with specific requirements
3. Have proper acceptance criteria

Issues that meet the criteria are moved to "Awaiting Approval" state.
Issues that need improvement get enhanced descriptions.
"""

import os
import sys
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.integrations.linear_client import LinearClient
from src.utils.types import LinearTask
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

@dataclass
class AuditResult:
    """Result of auditing a single issue."""
    task: LinearTask
    is_actionable: bool
    clarity_score: int  # 0-10 scale
    missing_elements: List[str]
    suggested_improvements: List[str]
    improved_description: Optional[str] = None
    improved_title: Optional[str] = None

class LinearBacklogAuditor:
    """Auditor for Linear backlog issues."""
    
    def __init__(self, api_key: str, team_id: str):
        """Initialize the auditor."""
        self.client = LinearClient(api_key, team_id)
        self.backlog_state = "Backlog"
        self.target_state = "Awaiting Approval"
        
        # Criteria for actionable issues
        self.required_elements = [
            "clear_objective",
            "acceptance_criteria",
            "user_story_format",
            "technical_details",
            "priority_indication"
        ]
        
        logger.info("Initialized Linear Backlog Auditor")
    
    def audit_backlog(self) -> List[AuditResult]:
        """Audit all backlog issues."""
        logger.info("Starting backlog audit...")
        
        # Get all backlog issues
        backlog_issues = self.client.get_tasks(self.backlog_state)
        logger.info(f"Found {len(backlog_issues)} issues in backlog")
        
        if not backlog_issues:
            logger.warning("No issues found in backlog")
            return []
        
        # Audit each issue
        audit_results = []
        for issue in backlog_issues:
            logger.info(f"Auditing {issue.identifier}: {issue.title}")
            result = self.audit_issue(issue)
            audit_results.append(result)
        
        return audit_results
    
    def audit_issue(self, task: LinearTask) -> AuditResult:
        """Audit a single issue for clarity and actionability."""
        missing_elements = []
        suggested_improvements = []
        clarity_score = 0
        
        # Check title clarity (0-2 points)
        title_score, title_issues = self._analyze_title(task.title)
        clarity_score += title_score
        if title_issues:
            missing_elements.extend(title_issues)
        
        # Check description completeness (0-5 points)
        desc_score, desc_issues, desc_suggestions = self._analyze_description(task.description)
        clarity_score += desc_score
        if desc_issues:
            missing_elements.extend(desc_issues)
        if desc_suggestions:
            suggested_improvements.extend(desc_suggestions)
        
        # Check for acceptance criteria (0-2 points)
        ac_score, ac_issues = self._check_acceptance_criteria(task.description)
        clarity_score += ac_score
        if ac_issues:
            missing_elements.extend(ac_issues)
        
        # Check for technical details (0-1 point)
        tech_score, tech_issues = self._check_technical_details(task.description)
        clarity_score += tech_score
        if tech_issues:
            missing_elements.extend(tech_issues)
        
        # Generate improved description if needed
        improved_description = None
        improved_title = None
        
        if clarity_score < 7:  # Needs improvement
            improved_description = self._generate_improved_description(task, missing_elements, suggested_improvements)
            if title_score < 2:
                improved_title = self._generate_improved_title(task.title, task.description)
        
        # Determine if actionable (score >= 7 and has core elements)
        is_actionable = (
            clarity_score >= 7 and
            "clear_objective" not in missing_elements and
            "acceptance_criteria" not in missing_elements
        )
        
        return AuditResult(
            task=task,
            is_actionable=is_actionable,
            clarity_score=clarity_score,
            missing_elements=missing_elements,
            suggested_improvements=suggested_improvements,
            improved_description=improved_description,
            improved_title=improved_title
        )
    
    def _analyze_title(self, title: str) -> Tuple[int, List[str]]:
        """Analyze title clarity (0-2 points)."""
        score = 0
        issues = []
        
        if not title or len(title.strip()) < 5:
            issues.append("title_too_short")
            return score, issues
        
        # Check for action words
        action_words = ['add', 'fix', 'update', 'create', 'implement', 'improve', 'remove', 'refactor']
        if any(word in title.lower() for word in action_words):
            score += 1
        else:
            issues.append("title_lacks_action_word")
        
        # Check for specific components/areas
        if any(char in title for char in [':', '-', '|']) or len(title.split()) >= 4:
            score += 1
        else:
            issues.append("title_lacks_specificity")
        
        return score, issues
    
    def _analyze_description(self, description: str) -> Tuple[int, List[str], List[str]]:
        """Analyze description completeness (0-5 points)."""
        score = 0
        issues = []
        suggestions = []
        
        if not description or len(description.strip()) < 20:
            issues.append("description_too_short")
            suggestions.append("Add detailed description explaining the problem and solution")
            return score, issues, suggestions
        
        desc_lower = description.lower()
        
        # Check for problem statement (1 point)
        problem_indicators = ['problem', 'issue', 'bug', 'error', 'need', 'should', 'currently']
        if any(indicator in desc_lower for indicator in problem_indicators):
            score += 1
        else:
            issues.append("missing_problem_statement")
            suggestions.append("Add clear problem statement explaining what needs to be solved")
        
        # Check for solution approach (1 point)
        solution_indicators = ['solution', 'approach', 'implement', 'add', 'create', 'update', 'change']
        if any(indicator in desc_lower for indicator in solution_indicators):
            score += 1
        else:
            issues.append("missing_solution_approach")
            suggestions.append("Add proposed solution or approach")
        
        # Check for user story format (1 point)
        user_story_patterns = [
            r'as a .* i want .* so that',
            r'as a .* i need .* to',
            r'user should be able to'
        ]
        if any(re.search(pattern, desc_lower) for pattern in user_story_patterns):
            score += 1
        else:
            issues.append("missing_user_story_format")
            suggestions.append("Add user story format: 'As a [user], I want [goal] so that [benefit]'")
        
        # Check for technical considerations (1 point)
        tech_indicators = ['api', 'database', 'frontend', 'backend', 'component', 'endpoint', 'ui', 'ux']
        if any(indicator in desc_lower for indicator in tech_indicators):
            score += 1
        else:
            suggestions.append("Consider adding technical implementation details")
        
        # Check for completeness indicators (1 point)
        completeness_indicators = ['requirements', 'steps', 'criteria', 'outcome', 'deliverable']
        if any(indicator in desc_lower for indicator in completeness_indicators):
            score += 1
        else:
            suggestions.append("Add clear requirements or deliverables")
        
        return score, issues, suggestions
    
    def _check_acceptance_criteria(self, description: str) -> Tuple[int, List[str]]:
        """Check for acceptance criteria (0-2 points)."""
        score = 0
        issues = []
        
        if not description:
            issues.append("acceptance_criteria")
            return score, issues
        
        desc_lower = description.lower()
        
        # Check for AC keywords
        ac_indicators = ['acceptance criteria', 'ac:', 'given', 'when', 'then', 'should', 'must', '✓', '- [', 'checklist']
        if any(indicator in desc_lower for indicator in ac_indicators):
            score += 1
            
            # Check for multiple criteria (additional point)
            criteria_count = len([line for line in description.split('\n') 
                                if any(indicator in line.lower() for indicator in ['✓', '- [', 'should', 'must', 'given', 'when', 'then'])])
            if criteria_count >= 2:
                score += 1
            else:
                issues.append("insufficient_acceptance_criteria")
        else:
            issues.append("acceptance_criteria")
        
        return score, issues
    
    def _check_technical_details(self, description: str) -> Tuple[int, List[str]]:
        """Check for technical implementation details (0-1 point)."""
        score = 0
        issues = []
        
        if not description:
            issues.append("technical_details")
            return score, issues
        
        desc_lower = description.lower()
        
        # Check for technical details
        tech_details = [
            'component', 'api', 'endpoint', 'database', 'table', 'field',
            'frontend', 'backend', 'service', 'function', 'method',
            'ui', 'ux', 'design', 'layout', 'responsive', 'mobile'
        ]
        
        if any(detail in desc_lower for detail in tech_details):
            score += 1
        else:
            issues.append("technical_details")
        
        return score, issues
    
    def _generate_improved_description(self, task: LinearTask, missing_elements: List[str], suggestions: List[str]) -> str:
        """Generate an improved description based on audit results."""
        improved_desc = task.description or ""
        
        # Add header if missing
        if not improved_desc.startswith('#'):
            improved_desc = f"# {task.title}\n\n{improved_desc}"
        
        # Add sections based on missing elements
        if "missing_problem_statement" in missing_elements:
            improved_desc += "\n\n## Problem Statement\n[TODO: Describe the current problem or need]"
        
        if "missing_solution_approach" in missing_elements:
            improved_desc += "\n\n## Proposed Solution\n[TODO: Describe the proposed approach or solution]"
        
        if "missing_user_story_format" in missing_elements:
            improved_desc += "\n\n## User Story\nAs a [type of user], I want [goal] so that [benefit]."
        
        if "acceptance_criteria" in missing_elements or "insufficient_acceptance_criteria" in missing_elements:
            improved_desc += "\n\n## Acceptance Criteria\n- [ ] [TODO: Add specific, testable criteria]\n- [ ] [TODO: Add another criteria]\n- [ ] [TODO: Add edge cases]"
        
        if "technical_details" in missing_elements:
            improved_desc += "\n\n## Technical Implementation\n- **Components affected:** [TODO: List components]\n- **API changes:** [TODO: List any API changes]\n- **Database changes:** [TODO: List any DB changes]"
        
        # Add improvement notes
        if suggestions:
            improved_desc += "\n\n## Implementation Notes\n"
            for suggestion in suggestions:
                improved_desc += f"- {suggestion}\n"
        
        # Add audit metadata
        improved_desc += f"\n\n---\n*Automated audit completed on {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
        
        return improved_desc.strip()
    
    def _generate_improved_title(self, title: str, description: str) -> str:
        """Generate an improved title if needed."""
        # Extract key information from description for better title
        if not title or len(title.strip()) < 5:
            return "TODO: Add descriptive title"
        
        # Ensure title has action word
        action_words = ['Add', 'Fix', 'Update', 'Create', 'Implement', 'Improve', 'Remove', 'Refactor']
        if not any(word in title for word in action_words):
            # Try to infer action from description
            if description:
                desc_lower = description.lower()
                if 'bug' in desc_lower or 'error' in desc_lower or 'fix' in desc_lower:
                    return f"Fix: {title}"
                elif 'add' in desc_lower or 'create' in desc_lower or 'new' in desc_lower:
                    return f"Add: {title}"
                elif 'update' in desc_lower or 'change' in desc_lower or 'modify' in desc_lower:
                    return f"Update: {title}"
                else:
                    return f"Implement: {title}"
            else:
                return f"Implement: {title}"
        
        return title
    
    def apply_improvements(self, audit_results: List[AuditResult], dry_run: bool = True) -> Dict[str, int]:
        """Apply improvements to issues based on audit results."""
        stats = {
            "total_audited": len(audit_results),
            "needs_improvement": 0,
            "moved_to_approval": 0,
            "updated_descriptions": 0,
            "updated_titles": 0,
            "errors": 0
        }
        
        for result in audit_results:
            task = result.task
            
            try:
                # Update description if improved
                if result.improved_description:
                    stats["needs_improvement"] += 1
                    
                    if not dry_run:
                        success = self.client.update_task_description(
                            task.id,
                            result.improved_description,
                            result.improved_title
                        )
                        
                        if success:
                            stats["updated_descriptions"] += 1
                            if result.improved_title:
                                stats["updated_titles"] += 1
                            logger.info(f"Updated {task.identifier} description")
                        else:
                            stats["errors"] += 1
                            logger.error(f"Failed to update {task.identifier} description")
                    else:
                        logger.info(f"[DRY RUN] Would update {task.identifier} description")
                
                # Move to awaiting approval if actionable
                if result.is_actionable:
                    if not dry_run:
                        success = self.client.update_task(
                            task.id,
                            state=self.target_state,
                            comment=f"Moved to {self.target_state} after automated audit. Clarity score: {result.clarity_score}/10"
                        )
                        
                        if success:
                            stats["moved_to_approval"] += 1
                            logger.info(f"Moved {task.identifier} to {self.target_state}")
                        else:
                            stats["errors"] += 1
                            logger.error(f"Failed to move {task.identifier} to {self.target_state}")
                    else:
                        logger.info(f"[DRY RUN] Would move {task.identifier} to {self.target_state}")
                        
            except Exception as e:
                stats["errors"] += 1
                logger.error(f"Error processing {task.identifier}: {e}")
        
        return stats
    
    def generate_audit_report(self, audit_results: List[AuditResult]) -> str:
        """Generate a comprehensive audit report."""
        total_issues = len(audit_results)
        actionable_issues = sum(1 for r in audit_results if r.is_actionable)
        needs_improvement = sum(1 for r in audit_results if r.improved_description)
        
        avg_clarity = sum(r.clarity_score for r in audit_results) / total_issues if total_issues > 0 else 0
        
        report = f"""
# Linear Backlog Audit Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- **Total Issues Audited:** {total_issues}
- **Actionable Issues:** {actionable_issues} ({actionable_issues/total_issues*100:.1f}% if total_issues > 0 else 0)
- **Issues Needing Improvement:** {needs_improvement} ({needs_improvement/total_issues*100:.1f}% if total_issues > 0 else 0)
- **Average Clarity Score:** {avg_clarity:.1f}/10

## Detailed Results

### Actionable Issues (Ready for Approval)
"""
        
        for result in audit_results:
            if result.is_actionable:
                report += f"- **{result.task.identifier}**: {result.task.title} (Score: {result.clarity_score}/10)\n"
        
        report += "\n### Issues Needing Improvement\n"
        
        for result in audit_results:
            if not result.is_actionable:
                report += f"\n#### {result.task.identifier}: {result.task.title}\n"
                report += f"**Clarity Score:** {result.clarity_score}/10\n\n"
                
                if result.missing_elements:
                    report += "**Missing Elements:**\n"
                    for element in result.missing_elements:
                        report += f"- {element.replace('_', ' ').title()}\n"
                
                if result.suggested_improvements:
                    report += "\n**Suggested Improvements:**\n"
                    for improvement in result.suggested_improvements:
                        report += f"- {improvement}\n"
        
        return report

def main():
    """Main function to run the audit."""
    # Check environment variables
    api_key = os.getenv('LINEAR_API_KEY')
    team_id = os.getenv('LINEAR_TEAM_ID')
    
    if not api_key or not team_id:
        logger.error("Missing LINEAR_API_KEY or LINEAR_TEAM_ID environment variables")
        print("Error: Please set LINEAR_API_KEY and LINEAR_TEAM_ID in your .env file")
        return 1
    
    # Parse command line arguments
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    if verbose:
        logger.add(sys.stdout, level="DEBUG")
    
    # Initialize auditor
    auditor = LinearBacklogAuditor(api_key, team_id)
    
    try:
        # Run audit
        print("🔍 Starting Linear backlog audit...")
        audit_results = auditor.audit_backlog()
        
        if not audit_results:
            print("✅ No issues found in backlog")
            return 0
        
        # Generate report
        report = auditor.generate_audit_report(audit_results)
        print(report)
        
        # Apply improvements
        if dry_run:
            print("\n🧪 Running in DRY RUN mode - no changes will be made")
        else:
            print("\n🔄 Applying improvements...")
        
        stats = auditor.apply_improvements(audit_results, dry_run=dry_run)
        
        # Print summary
        print(f"\n📊 Audit Summary:")
        print(f"   Total audited: {stats['total_audited']}")
        print(f"   Needs improvement: {stats['needs_improvement']}")
        print(f"   Moved to approval: {stats['moved_to_approval']}")
        print(f"   Updated descriptions: {stats['updated_descriptions']}")
        print(f"   Updated titles: {stats['updated_titles']}")
        print(f"   Errors: {stats['errors']}")
        
        if dry_run:
            print("\n💡 Run without --dry-run to apply changes")
        
        return 0
        
    except Exception as e:
        logger.error(f"Audit failed: {e}")
        print(f"❌ Audit failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 