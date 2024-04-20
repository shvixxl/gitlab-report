from pydantic import BaseModel, computed_field

from .project import Project


class Group(BaseModel):
    """A GitLab group."""

    id: int
    name: str
    projects: list[Project]

    @computed_field
    @property
    def issues(self) -> int:
        """Issues from all projects in the group."""
        return sum(project.issues for project in self.projects)

    @computed_field
    @property
    def incidents(self) -> int:
        """Incidents from all projects in the group."""
        return sum(project.incidents for project in self.projects)

    @computed_field
    @property
    def closed_issues(self) -> int:
        """Created issues from all projects in the group."""
        return sum(project.closed_issues for project in self.projects)

    @computed_field
    @property
    def closed_incidents(self) -> int:
        """Created issues from all projects in the group."""
        return sum(project.closed_incidents for project in self.projects)
