from dataclasses import dataclass
from enum import Enum

import gitlab.base

from .group import Group
from .project import Project
from .user import User


class IssueType(str, Enum):
    """Type of the issue."""

    Issue = "issue"
    Incident = "incident"
    TestCase = "test_case"
    Task = "task"


class IssueState(str, Enum):
    """State of the issue."""

    Opened = "opened"
    Closed = "closed"


@dataclass(kw_only=True, slots=True)
class Issue:
    """GitLab issue data."""

    type: IssueType
    state: IssueState

    author: User
    assignees: list[User]
    labels: list[str]

    group: Group | None
    project: Project

    created_at: str
    updated_at: str
    closed_at: str | None
    due_date: str | None

    @classmethod
    def from_gitlab(
        cls,
        issue: gitlab.base.RESTObject,
        project: gitlab.base.RESTObject,
    ) -> "Issue":
        """Create an Issue instance from GitLab issue."""
        return cls(
            type=issue.issue_type,
            state=issue.state,
            author=User(
                id=issue.author["id"],
                name=issue.author["name"],
            ),
            assignees=[
                User(
                    id=assignee["id"],
                    name=assignee["name"],
                )
                for assignee in issue.assignees
            ],
            labels=issue.labels,
            group=(
                Group(
                    id=project.namespace["id"],
                    name=project.namespace["name"],
                )
                if project.namespace["kind"] == "group"
                else None
            ),
            project=Project(
                id=project.id,
                name=project.name,
            ),
            created_at=issue.created_at,
            updated_at=issue.updated_at,
            closed_at=issue.closed_at,
            due_date=issue.due_date,
        )
