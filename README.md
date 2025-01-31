# jira-opensync-wrapper

A Python wrapper for the JIRA API that provides simplified issue creation with duplicate detection and local state synchronization capabilities.

## Features

- Create JIRA issues with duplicate detection
- Synchronize JIRA issues to local storage
- Type-hinted methods for better IDE support

## Installation

```bash
pip install jira-opensync-wrapper
```

## Usage

### Basic Setup

```python
from jira_opensync_wrapper import JiraOpenSyncWrapper

# Initialize the wrapper
jira = JiraOpenSyncWrapper(
    server="https://your-jira-instance.com",
    username="your-username",
    password="your-password"
)
```

### Create an Issue

```python
# Create a new issue
issue = jira.open_issue(
    project_key="PROJ",
    summary="CPU Usage Alert",
    description="CPU usage exceeded 90%",
    alert_criteria="CPU usage"
)
```

### Synchronize Issues

```python
# Sync all issues from a project
local_issues = jira.sync_issues("PROJ")

# Access synced issues
for issue_key, issue_data in local_issues.items():
    print(f"Issue {issue_key}:")
    print(f"  Summary: {issue_data['summary']}")
    print(f"  Status: {issue_data['status']}")
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

