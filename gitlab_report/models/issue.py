from datetime import datetime

from pydantic import BaseModel, computed_field
from pytz import UTC


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

        due_date = self.due_date.replace(tzinfo=UTC)

        if self.state == "closed" and self.closed_at:
            closed_at = self.closed_at.replace(tzinfo=UTC)
            if closed_at > due_date:
                return (closed_at - due_date).days
            return None

        now = datetime.now(tz=UTC)
        if self.state == "opened" and now > due_date:
            return (now - due_date).days

        return None
