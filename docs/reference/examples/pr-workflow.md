# Example PR Workflow - Real Task Walkthrough

## 📋 Example Linear Task

```yaml
Task ID: KEY-123
Title: "Add loading skeleton to user profile page"
Project: keysy3
Priority: Medium
Estimate: 2 points
Labels: ["ui", "auto-pr-safe"]
Description: |
  The user profile page currently shows a blank screen while loading.
  Add a skeleton loader to improve perceived performance.
  
  Acceptance Criteria:
  - Show skeleton for avatar, name, and bio sections
  - Match existing skeleton patterns in the app
  - Transition smoothly when data loads
```

---

## 🤖 System Execution Flow

### Step 1: BacklogReader Selects Task

```python
# agents/backlog_reader.py execution
async def execute(self):
    # Query Linear for ready tasks
    tasks = await self.linear.get_ready_issues({
        "labels": ["auto-pr-safe"],
        "estimate": {"lte": 3}
    })
    
    # Score this task
    task_score = self.score_issue(tasks[0])
    # Score: 8.5/10 (Medium priority + Clear criteria + Safe UI work)
    
    # Safety check passes
    # ✅ UI component work
    # ✅ No auth/payment logic
    # ✅ Clear acceptance criteria
    # ✅ Has "auto-pr-safe" label
    
    self.state.current_issue = tasks[0]
    await self.linear.update_issue_state(task.id, "In Progress")
```

**Agent Decision Log:**
```
[BacklogReader] Selected KEY-123: "Add loading skeleton to user profile page"
[BacklogReader] Score: 8.5 | Safety: PASS | Project: keysy3
[BacklogReader] Updated Linear status to "In Progress"
```

### Step 2: Creator Agent Generates Initial Solution

```python
# agents/creator.py execution
async def execute(self):
    # Load project context
    context = await self.load_project_context("keysy3")
    # Found: 3 existing skeleton components in codebase
    # Pattern: Using react-loading-skeleton library
    
    # Generate solution
    solution = await self.generate_initial_code()
```

**Generated Code:**

```typescript
// components/profile/ProfileSkeleton.tsx
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

export const ProfileSkeleton = () => {
  return (
    <div className="space-y-4 p-6">
      <div className="flex items-center space-x-4">
        <Skeleton circle width={80} height={80} />
        <div className="flex-1">
          <Skeleton width="60%" height={24} />
          <Skeleton width="40%" height={16} className="mt-2" />
        </div>
      </div>
      <Skeleton count={3} height={20} />
    </div>
  );
};
```

```typescript
// app/(dashboard)/profile/[id]/page.tsx
import { ProfileSkeleton } from '@/components/profile/ProfileSkeleton';

export default function ProfilePage({ params }: { params: { id: string } }) {
  const { data: profile, isLoading } = useProfile(params.id);
  
  if (isLoading) {
    return <ProfileSkeleton />;
  }
  
  return <ProfileContent profile={profile} />;
}
```

### Step 3: Editor Agent Refines

```python
# agents/editor.py execution
async def execute(self):
    # Analyze Creator's code
    improvements = []
    
    # 1. Add tests
    test_code = await self.generate_tests()
    improvements.append(test_code)
    
    # 2. Add animation
    animation_improvement = await self.add_smooth_transition()
    improvements.append(animation_improvement)
    
    # 3. Add Storybook story
    story_code = await self.generate_storybook_story()
    improvements.append(story_code)
```

**Added by Editor:**

```typescript
// components/profile/__tests__/ProfileSkeleton.test.tsx
import { render } from '@testing-library/react';
import { ProfileSkeleton } from '../ProfileSkeleton';

describe('ProfileSkeleton', () => {
  it('renders skeleton elements', () => {
    const { container } = render(<ProfileSkeleton />);
    
    // Check for avatar skeleton
    expect(container.querySelector('.react-loading-skeleton')).toBeInTheDocument();
    
    // Check structure matches loaded state
    expect(container.querySelector('.space-y-4')).toBeInTheDocument();
  });
});
```

```typescript
// components/profile/ProfileSkeleton.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { ProfileSkeleton } from './ProfileSkeleton';

const meta: Meta<typeof ProfileSkeleton> = {
  title: 'Components/Profile/ProfileSkeleton',
  component: ProfileSkeleton,
};

export default meta;

export const Default: StoryObj<typeof ProfileSkeleton> = {};
```

**Animation Enhancement:**
```css
/* Added fade transition */
.skeleton-wrapper {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### Step 4: Reviewer Agent Validates

```python
# agents/reviewer.py execution
async def execute(self):
    pr = self.state.current_pr
    
    checks = {
        "code_quality": await self.check_code_quality(pr),      # ✅ PASS
        "tests": await self.check_test_coverage(pr),            # ✅ PASS
        "build": await self.check_build_success(pr),            # ✅ PASS
        "security": await self.check_security(pr),              # ✅ PASS
        "size": await self.check_pr_size(pr),                   # ✅ PASS (4 files, 85 lines)
        "patterns": await self.check_follows_patterns(pr),      # ✅ PASS
    }
    
    return AgentResult(
        success=all(checks.values()),
        data={"approval": True, "checks": checks}
    )
```

**Review Summary:**
```
✅ Code Quality: Follows project conventions
✅ Tests: Coverage maintained (82.3% → 82.5%)
✅ Build: All checks pass
✅ Security: No vulnerabilities detected
✅ Size: Appropriate (4 files, 85 lines)
✅ Patterns: Matches existing skeleton usage
```

### Step 5: Merger Agent Creates PR

**Generated PR:**

```markdown
## 🤖 Automated PR

**Linear Issue**: [KEY-123](https://linear.app/team/issue/KEY-123)
**Project**: keysy3
**Risk Level**: LOW
**Estimated Review Time**: 5 minutes

### Changes Made
Added loading skeleton to user profile page to improve perceived performance during data fetching.

### Implementation Details
- Created `ProfileSkeleton` component following existing patterns
- Integrated with profile page loading state  
- Added smooth fade-in animation
- Included tests and Storybook story

### Testing
- [x] All tests pass
- [x] Added new tests for skeleton component
- [x] Manually tested loading state
- [x] No console errors

### Safety Checks
- [x] No sensitive files modified
- [x] No authentication/authorization changes
- [x] No payment/billing logic touched
- [x] No database migrations needed
- [x] Changes are reversible

### Screenshots
![Loading State](https://via.placeholder.com/400x200?text=Skeleton+Loading)
![Loaded State](https://via.placeholder.com/400x200?text=Profile+Loaded)

---
*This PR was automatically generated and has passed all quality gates.*
```

### Step 6: Post-Merge Monitoring

```python
# monitoring/deployment_monitor.py
async def monitor_deployment(self):
    # Wait for Vercel deployment
    deployment = await self.wait_for_deployment("staging")
    # ✅ Deployment successful in 2m 34s
    
    # Check Sentry for errors
    errors = await self.check_sentry_errors()
    # ✅ No new errors in 30 minutes
    
    # Run synthetic tests
    synthetic_results = await self.run_synthetic_tests([
        "/profile/123",  # Test the changed page
        "/profile/456"   # Test another instance
    ])
    # ✅ All pages load successfully
    
    # Update Linear
    await self.linear.update_issue_state(task.id, "Done")
    await self.linear.add_comment(
        task.id,
        "✅ Successfully deployed to staging\n" +
        "Deployment: https://keysy3-staging.vercel.app\n" +
        "No errors detected in monitoring"
    )
```

### Step 7: Analyst Learns

```python
# agents/analyst.py
async def analyze_cycle(self):
    insights = {
        "success_patterns": [
            "Skeleton components are low-risk and high-value",
            "Following existing patterns increases merge rate",
            "Small, focused PRs review faster"
        ],
        "time_metrics": {
            "total_time": "18 minutes",
            "review_time": "3 minutes",
            "deployment_time": "2.5 minutes"
        },
        "quality_score": 0.95,
        "recommendation": "Prioritize similar UI enhancement tasks"
    }
    
    # Feed back to Prospect Agent
    await self.update_value_model({
        "task_type": "ui_skeleton",
        "success_rate": 1.0,
        "time_to_complete": 18,
        "user_value": "high"
    })
```

---

## 📊 Outcome Summary

```yaml
Task: KEY-123 - Add loading skeleton to user profile page
Result: SUCCESS

Timeline:
  - Task Selected: 10:00 AM
  - PR Created: 10:12 AM  
  - PR Merged: 10:15 AM
  - Deployed: 10:18 AM
  - Verified: 10:30 AM

Metrics:
  - Lines of Code: 85
  - Files Changed: 4
  - Test Coverage: +0.2%
  - Review Time: 3 minutes
  - Zero post-deploy errors

Learnings Applied:
  - UI skeleton tasks marked as preferred
  - Pattern matching improved for similar components
  - Test generation enhanced for loading states
```

---

## 🔄 Next Task Selection

Based on this success, the system now prioritizes:

1. **Similar UI Tasks** in Linear:
   - "Add skeleton to dashboard widgets" (KEY-124)
   - "Add loading state to data tables" (KEY-125)

2. **Confidence Adjustments**:
   - UI tasks: confidence +10%
   - Skeleton patterns: confidence +15%
   - keysy3 project: success rate 95%

3. **Time Estimates**:
   - Similar tasks estimated at 15-20 minutes
   - Review time expected under 5 minutes 