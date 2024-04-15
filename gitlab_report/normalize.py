import gitlab.base


def normalize_issues(issues: list[gitlab.base.RESTObject]) -> list[dict]:
    """Normalize the issues data."""
    normalized_issues = [
        {
            "id": issue.id,
            "project_id": issue.project_id,
            "assignees": [assignee["username"] for assignee in issue.assignees] or None,
            "type": issue.issue_type,
            "labels": issue.labels or None,
            "state": issue.state,
            "project": issue.references["full"].split("#")[0],
            "group": issue.references["full"].split("/")[0],
        }
        for issue in issues
    ]

    return normalized_issues
