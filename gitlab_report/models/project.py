from pydantic import BaseModel, Field, computed_field

from .issue import Issue, IssueState, IssueType


class Project(BaseModel):
    """A GitLab project."""

    id: int
    name: str
    all_issues: list[Issue] = Field(exclude=True)
    period_issue: list[Issue] = Field(exclude=True)

    @computed_field
    @property
    def issues(self) -> int:
        """Issues from all projects in the group."""
        return len(self.period_issue)

    @computed_field
    @property
    def incidents(self) -> int:
        """Incidents from all projects in the group."""
        return len(
            [issue for issue in self.period_issue if issue.type == IssueType.INCIDENT]
        )

    @computed_field
    @property
    def closed_issues(self) -> int:
        """Created issues from all projects in the group."""
        return len(
            [issue for issue in self.period_issue if issue.state == IssueState.CLOSED]
        )

    @computed_field
    @property
    def closed_incidents(self) -> int:
        """Created issues from all projects in the group."""
        return len(
            [
                issue
                for issue in self.period_issue
                if issue.state == IssueState.CLOSED and issue.type == IssueType.INCIDENT
            ]
        )

    @computed_field
    @property
    def avg_delay(self) -> float:
        """The average delay of the issues."""
        delays = [issue.delay for issue in self.period_issue if issue.delay is not None]
        return sum(delays) / len(delays) if delays else 0
