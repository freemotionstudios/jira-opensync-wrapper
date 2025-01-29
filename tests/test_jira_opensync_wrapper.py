import pytest
from jira_opensync_wrapper.jira_opensync_wrapper import JiraOpenSyncWrapper

class MockJIRA:
    def __init__(self, server, basic_auth):
        self.server = server
        self.basic_auth = basic_auth
        self.issues = []

    def search_issues(self, jql):
        return [issue for issue in self.issues if jql in issue.fields.description]

    def create_issue(self, project, summary, description, issuetype):
        issue = MockIssue(summary, description)
        self.issues.append(issue)
        return issue

class MockIssue:
    def __init__(self, summary, description):
        self.fields = MockFields(summary, description)

class MockFields:
    def __init__(self, summary, description):
        self.summary = summary
        self.description = description
        self.status = MockStatus()

class MockStatus:
    def __init__(self):
        self.name = "Open"

@pytest.fixture
def jira_wrapper():
    mock_jira = MockJIRA(server="http://mockserver", basic_auth=("user", "pass"))
    return JiraOpenSyncWrapper(mock_jira)

def test_open_issue(jira_wrapper):
    issue = jira_wrapper.open_issue("TEST", "Test Summary", "Test Description", "alert")
    assert issue.fields.summary == "Test Summary"
    assert issue.fields.description == "Test Description"

def test_sync_issues(jira_wrapper):
    jira_wrapper.open_issue("TEST", "Test Summary", "Test Description", "alert")
    local_store = jira_wrapper.sync_issues("TEST")
    assert "TEST-1" in local_store
    assert local_store["TEST-1"]["summary"] == "Test Summary"
    assert local_store["TEST-1"]["description"] == "Test Description"
    assert local_store["TEST-1"]["status"] == "Open"

def test_sync_issues_correctly_syncs(jira_wrapper):
    jira_wrapper.open_issue("TEST", "Test Summary 1", "Test Description 1", "alert")
    jira_wrapper.open_issue("TEST", "Test Summary 2", "Test Description 2", "alert")
    local_store = jira_wrapper.sync_issues("TEST")
    assert len(local_store) == 2
    assert "TEST-1" in local_store
    assert "TEST-2" in local_store
    assert local_store["TEST-1"]["summary"] == "Test Summary 1"
    assert local_store["TEST-1"]["description"] == "Test Description 1"
    assert local_store["TEST-1"]["status"] == "Open"
    assert local_store["TEST-2"]["summary"] == "Test Summary 2"
    assert local_store["TEST-2"]["description"] == "Test Description 2"
    assert local_store["TEST-2"]["status"] == "Open"

def test_open_issue_creates_new_issue(jira_wrapper):
    issue = jira_wrapper.open_issue("TEST", "Test Summary", "Test Description", "alert")
    assert issue.fields.summary == "Test Summary"
    assert issue.fields.description == "Test Description"
    assert issue.fields.status.name == "Open"
