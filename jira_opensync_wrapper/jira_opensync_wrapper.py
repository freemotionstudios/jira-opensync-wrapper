from typing import Dict, Any
from jira import JIRA


class JiraOpenSyncWrapper:
    """Wrapper class for JIRA operations with local sync capability."""

    def __init__(self, server: str, username: str, password: str) -> None:
        """Initialize JIRA connection and local store.

        Args:
            server: JIRA server URL
            username: JIRA username
            password: JIRA password
        """
        self.jira = JIRA(server=server, basic_auth=(username, password))
        self.local_store = {}

    def open_issue(
        self, project_key: str, summary: str, description: str, alert_criteria: str
    ) -> Any:
        """Create a new JIRA issue or return existing one if matches criteria.

        Args:
            project_key: JIRA project identifier
            summary: Issue summary
            description: Issue description
            alert_criteria: Criteria to match in existing issues

        Returns:
            JIRA issue object
        """
        existing_issues = self.jira.search_issues(
            f'project={project_key} AND summary~"{summary}"'
        )
        for issue in existing_issues:
            if alert_criteria in issue.fields.description:
                return issue
        new_issue = self.jira.create_issue(
            project=project_key,
            summary=summary,
            description=description,
            issuetype={"name": "Task"},
        )
        return new_issue

    def sync_issues(self, project_key: str) -> Dict[str, Dict[str, str]]:
        """Synchronize project issues to local store.

        Args:
            project_key: JIRA project identifier

        Returns:
            Dictionary of issues with their details
        """
        issues = self.jira.search_issues(f"project={project_key}")
        for issue in issues:
            self.local_store[issue.key] = {
                "summary": issue.fields.summary,
                "description": issue.fields.description,
                "status": issue.fields.status.name,
            }
        return self.local_store
