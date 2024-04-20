from datetime import datetime

import urllib3
from gitlab import Gitlab

from .models.group import Group
from .models.issue import Issue
from .models.project import Project

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def create_session(
    url: str,
    access_token: str | None = None,
    oauth_token: str | None = None,
) -> Gitlab:
    """Create a GitLab session."""
    if access_token is None and oauth_token is None:
        raise ValueError("Either access_token or oauth_token must be provided.")

    return Gitlab(
        url=url,
        private_token=access_token,
        oauth_token=oauth_token,
        ssl_verify=False,
    )


def get_groups(
    session: Gitlab,
    *,
    min_access_level: int = 10,
    with_issues_created_after: datetime | None = None,
    with_issues_created_before: datetime | None = None,
) -> list[Group]:
    """Get a list of GitLab groups."""
    return [
        Group(
            id=group.id,
            name=group.name,
            projects=get_projects(
                session=session,
                group_id=group.id,
                group_name=group.name,
                with_issues_created_after=with_issues_created_after,
                with_issues_created_before=with_issues_created_before,
            ),
        )
        for group in session.groups.list(
            iterator=True,
            min_access_level=min_access_level,
        )
    ]


def get_projects(
    session: Gitlab,
    group_id: int,
    group_name: str,
    *,
    with_issues_created_after: datetime | None = None,
    with_issues_created_before: datetime | None = None,
) -> list[Project]:
    """Get a list of GitLab projects."""
    group = session.groups.get(group_id, lazy=True)
    return [
        Project(
            id=project.id,
            name=project.name,
            issue_objects=get_issues(
                session=session,
                group_name=group_name,
                project_id=project.id,
                project_name=project.name,
                created_after=with_issues_created_after,
                created_before=with_issues_created_before,
            ),
        )
        for project in group.projects.list(
            iterator=True,
        )
    ]


def get_issues(
    session: Gitlab,
    group_name: str,
    project_id: int,
    project_name: str,
    *,
    created_after: datetime | None = None,
    created_before: datetime | None = None,
) -> list[Issue]:
    """Get a list of GitLab issues."""
    project = session.projects.get(project_id, lazy=True)
    return [
        Issue(
            id=issue.iid,
            moved_to_id=issue.moved_to_id,
            group=group_name,
            project=project_name,
            type=issue.type,
            state=issue.state,
            labels=issue.labels,
            due_date=issue.due_date,
            created_at=issue.created_at,
            closed_at=issue.closed_at,
        )
        for issue in project.issues.list(
            iterator=True,
            assignee_id="Any",
            created_after=created_after.isoformat() if created_after else None,
            created_before=created_before.isoformat() if created_before else None,
        )
    ]
