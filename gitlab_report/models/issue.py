from datetime import datetime

from pydantic import BaseModel, computed_field


class Issue(BaseModel):
    """A GitLab issue."""

    id: int
    moved_to_id: int | None

    group: str
    project: str

    type: str
    state: str
    labels: list[str]

    due_date: datetime | None

    created_at: datetime
    closed_at: datetime | None

    @computed_field
    @property
    def delay(self) -> int | None:
        """The duration of the issue."""
        if not self.due_date:
            return None

        if self.state == "closed" and self.closed_at:
            if self.closed_at > self.due_date:
                return (self.closed_at - self.due_date).days
            return None

        now = datetime.now()
        if self.state == "opened" and now > self.due_date:
            return (datetime.now() - self.due_date).days

        return None
