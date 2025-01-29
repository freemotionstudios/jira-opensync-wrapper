from jira import JIRA

class JiraOpenSyncWrapper:
    def __init__(self, server, username, password):
        self.jira = JIRA(server=server, basic_auth=(username, password))
        self.local_store = {}

    def open_issue(self, project_key, summary, description, alert_criteria):
        existing_issues = self.jira.search_issues(f'project={project_key} AND summary~"{summary}"')
        for issue in existing_issues:
            if alert_criteria in issue.fields.description:
                return issue
        new_issue = self.jira.create_issue(project=project_key, summary=summary, description=description, issuetype={'name': 'Task'})
        return new_issue

    def sync_issues(self, project_key):
        issues = self.jira.search_issues(f'project={project_key}')
        for issue in issues:
            self.local_store[issue.key] = {
                'summary': issue.fields.summary,
                'description': issue.fields.description,
                'status': issue.fields.status.name
            }
        return self.local_store
