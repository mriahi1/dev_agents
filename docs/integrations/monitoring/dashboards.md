# Monitoring Dashboard Specification

## 🎯 Purpose

Real-time monitoring of the autonomous PR system to ensure:
- **Safety**: No risky operations are performed
- **Quality**: PRs meet high standards
- **Performance**: System operates efficiently
- **Learning**: Continuous improvement is happening

---

## 📊 Dashboard Layout

### Header Section
```
┌─────────────────────────────────────────────────────────────────┐
│ 🤖 Autonomous PR System Dashboard                               │
│ Status: ACTIVE | Mode: SAFE | Projects: keysy3, immo           │
│ Last Update: 2024-01-15 10:32:45                               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Metrics Grid
```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ PRs Today   │ Success Rate│ Avg Review  │ Risk Score  │
│     3/5     │    94.2%    │   12 min    │    0.15     │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ This Week   │ Rejections  │ Rollbacks   │ Incidents   │
│     18      │      1      │      0      │      0      │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

---

## 🔍 Detailed Monitoring Sections

### 1. Real-Time Activity Feed

```python
class ActivityFeed:
    def get_recent_activities(self, limit=20):
        return [
            {
                "timestamp": "10:32:12",
                "agent": "BacklogReader",
                "action": "Selected task KEY-123",
                "risk": "LOW",
                "status": "✅"
            },
            {
                "timestamp": "10:35:45", 
                "agent": "Creator",
                "action": "Generated PR for KEY-123",
                "risk": "LOW",
                "status": "✅"
            },
            {
                "timestamp": "10:38:00",
                "agent": "Reviewer",
                "action": "Approved PR #1234",
                "risk": "LOW", 
                "status": "✅"
            }
        ]
```

### 2. Project Health Matrix

| Project | PRs Today | Success % | Avg Time | Coverage | Risk Level |
|---------|-----------|-----------|----------|----------|------------|
| keysy3  | 2/3       | 95%       | 15 min   | 82.5%    | 🟢 LOW     |
| immo    | 1/2       | 90%       | 22 min   | 85.1%    | 🟡 MEDIUM  |

### 3. Safety Monitoring Panel

```yaml
Safety Checks:
  ✅ No unsafe files touched (0/0)
  ✅ No auth/payment code modified (0/0)
  ✅ All PRs under size limit (avg: 45 lines)
  ✅ No database migrations created (0/0)
  ✅ No production branch access (0/0)
  
Current Restrictions:
  - Max files per PR: 5
  - Max lines per PR: 200
  - Allowed projects: [keysy3, immo]
  - Allowed branches: [staging]
  - Required labels: [auto-pr-safe]
```

### 4. Agent Performance Dashboard

```python
agent_metrics = {
    "BacklogReader": {
        "tasks_evaluated": 45,
        "tasks_selected": 12,
        "selection_accuracy": 0.92,
        "avg_decision_time": "1.2s"
    },
    "Creator": {
        "prs_created": 12,
        "build_success_rate": 0.95,
        "avg_generation_time": "45s",
        "code_quality_score": 8.5
    },
    "Editor": {
        "improvements_made": 36,
        "tests_added": 24,
        "refactorings": 8,
        "avg_improvement_time": "30s"
    },
    "Reviewer": {
        "prs_reviewed": 12,
        "approval_rate": 0.92,
        "issues_caught": 3,
        "avg_review_time": "15s"
    }
}
```

### 5. Learning & Evolution Tracker

```
Learning Insights (Last 7 Days):
┌─────────────────────────────────────────────────────────┐
│ • UI skeleton tasks: Success rate improved 15%          │
│ • Test generation: Now covers edge cases better         │
│ • Django admin tasks: Reduced complexity score by 0.5   │
│ • Error handling: New patterns learned from PR #1230    │
│ • Code style: Adapted to team's async/await preferences │
└─────────────────────────────────────────────────────────┘

Pattern Recognition:
- Successful: Loading states, error messages, tests
- Challenging: Complex refactoring, API changes
- Avoided: Auth logic, payment processing, migrations
```

---

## 📈 Graphical Visualizations

### PR Success Rate Trend (7 Days)
```
100% │     ●───●
 95% │   ●       ●───●
 90% │ ●               ●
 85% │
     └─┬───┬───┬───┬───┬───┬───┬─
       Mon Tue Wed Thu Fri Sat Sun
```

### Time to Merge Distribution
```
<15min  ████████████████ 45%
15-30   ██████████ 30%
30-60   ████ 15%
>60min  ██ 10%
```

### Risk Level Distribution
```
LOW     ████████████████████ 75%
MEDIUM  ████ 20%
HIGH    █ 5%
BLOCKED ─ 0%
```

---

## 🚨 Alert Configuration

### Critical Alerts (Immediate)
- 🔴 Any attempt to modify unsafe files
- 🔴 PR creation failure rate > 20%
- 🔴 Deployment errors detected
- 🔴 Test coverage drops below threshold

### Warning Alerts (Within 5 min)
- 🟡 PR rejection rate > 10%
- 🟡 Review time > 30 minutes
- 🟡 Task complexity > configured limit
- 🟡 Agent error rate > 5%

### Info Alerts (Daily Summary)
- 🔵 Daily PR count and success rate
- 🔵 Learning insights discovered
- 🔵 Performance improvements
- 🔵 Backlog completion progress

---

## 🖥️ Implementation

### Web Dashboard (React)

```typescript
// components/Dashboard.tsx
import { useState, useEffect } from 'react';
import { MetricsGrid } from './MetricsGrid';
import { ActivityFeed } from './ActivityFeed';
import { SafetyPanel } from './SafetyPanel';
import { AgentPerformance } from './AgentPerformance';

export function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [activities, setActivities] = useState([]);
  
  useEffect(() => {
    // WebSocket connection for real-time updates
    const ws = new WebSocket('ws://localhost:8080/metrics');
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data.metrics);
      setActivities(prev => [data.activity, ...prev].slice(0, 50));
    };
    
    return () => ws.close();
  }, []);
  
  return (
    <div className="dashboard">
      <MetricsGrid metrics={metrics} />
      <div className="grid grid-cols-2 gap-4">
        <ActivityFeed activities={activities} />
        <SafetyPanel />
      </div>
      <AgentPerformance />
    </div>
  );
}
```

### CLI Dashboard (Python)

```python
# monitoring/cli_dashboard.py
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

class CLIDashboard:
    def __init__(self):
        self.console = Console()
        
    def render(self):
        layout = Layout()
        layout.split_column(
            Layout(self.get_header(), size=3),
            Layout(self.get_metrics_table(), size=8),
            Layout(self.get_activity_feed(), size=10),
            Layout(self.get_alerts(), size=5)
        )
        return layout
    
    def get_metrics_table(self):
        table = Table(title="System Metrics")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_column("Status")
        
        metrics = self.fetch_metrics()
        for metric in metrics:
            status = "🟢" if metric.is_healthy else "🔴"
            table.add_row(metric.name, str(metric.value), status)
        
        return table
```

### Slack Integration

```python
# monitoring/slack_notifier.py
class SlackNotifier:
    def send_alert(self, level: str, message: str):
        if level == "critical":
            self.send_to_channel("#alerts-critical", f"🚨 {message}")
        elif level == "warning":
            self.send_to_channel("#alerts-warning", f"⚠️ {message}")
        
    def send_daily_summary(self):
        summary = self.generate_summary()
        self.send_to_channel("#pr-system-updates", summary)
```

---

## 📱 Mobile Monitoring

### Key Mobile Views
1. **Status Overview** - Quick health check
2. **Recent PRs** - Last 10 PRs with status
3. **Alerts** - Active warnings/errors
4. **Quick Actions** - Pause/Resume system

---

## 🔐 Access Control

### Roles
- **Viewer**: Read-only access to all metrics
- **Operator**: Can pause/resume system
- **Admin**: Full control including configuration

### Audit Trail
- All actions logged with timestamp and user
- Configuration changes tracked
- Emergency stops recorded

---

## 📊 Export & Reporting

### Daily Reports
- PR summary with success/failure breakdown
- Learning insights and improvements
- Performance metrics and trends
- Risk assessment summary

### Weekly Reports
- Velocity trends
- Quality metrics evolution
- Cost savings estimate
- Recommendations for expansion

### Data Export
- CSV export for all metrics
- API endpoints for integration
- Webhook support for external systems

---

## 🚀 Getting Started

1. **Start the monitoring server**:
   ```bash
   python -m monitoring.server --port 8080
   ```

2. **Open web dashboard**:
   ```
   http://localhost:8080
   ```

3. **Or use CLI dashboard**:
   ```bash
   python -m monitoring.cli_dashboard
   ```

4. **Configure alerts**:
   ```bash
   python -m monitoring.configure_alerts --slack-webhook $WEBHOOK_URL
   ```

Remember: Good monitoring is the key to safe autonomous operation! 📊✨ 