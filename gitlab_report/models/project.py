from pydantic import BaseModel, Field, computed_field

from .issue import Issue


class Project(BaseModel):
    """A GitLab project."""

    id: int
    name: str
    issue_objects: list[Issue] = Field(exclude=True)

    @computed_field
    @property
    def issues(self) -> int:
        """Issues from all projects in the group."""
        return len(self.issue_objects)

    @computed_field
    @property
    def incidents(self) -> int:
        """Incidents from all projects in the group."""
        return len([issue for issue in self.issue_objects if issue.type == "incident"])

    @computed_field
    @property
    def closed_issues(self) -> int:
        """Created issues from all projects in the group."""
        return len([issue for issue in self.issue_objects if issue.state == "closed"])

    @computed_field
    @property
    def closed_incidents(self) -> int:
        """Created issues from all projects in the group."""
        return len(
            [
                issue
                for issue in self.issue_objects
                if issue.state == "closed" and issue.type == "incident"
            ]
        )

    @computed_field
    @property
    def avg_delay(self) -> float:
        """The average delay of the issues."""
        delays = [
            issue.delay for issue in self.issue_objects if issue.delay is not None
        ]
        return sum(delays) / len(delays) if delays else 0
