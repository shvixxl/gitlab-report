from dataclasses import dataclass

from ..database import Issues
from ..database.collections.issues import Filter, GroupBy
from .column import Column, ColumnConfig


@dataclass(kw_only=True)
class GroupConfig(Filter):
    """Configuration for a group of a section."""

    title: str


class Group:
    """A group of a section."""

    def __init__(self, config: GroupConfig, columns: list[ColumnConfig]) -> None:
        self._config = config
        self._issues = None
        self._columns = [Column(column_config) for column_config in columns]

    def load(self, issues: Issues) -> None:
        """Load the data for the group."""
        self._issues = issues.filter(self._config)
        for column in self._columns:
            column.load(self._issues)

    @classmethod
    def from_group_by(
        cls,
        group_by: GroupBy,
        issues: Issues,
        columns: list[ColumnConfig],
    ) -> "list[Group]":
        """Create a group from the data."""
        groups = []
        for title, group_issues in issues.group_by(group_by).items():
            group = cls(GroupConfig(title=str(title)), columns)
            group.load(group_issues)
            groups.append(group)
        return groups

    @property
    def title(self) -> str:
        """Get the title of the group."""
        return self._config.title

    @property
    def total(self) -> int:
        """Get the total number of issues."""
        if not self._issues:
            raise ValueError("group data has not been loaded")
        return self._issues.total()

    @property
    def columns(self) -> list[Column]:
        """Get the columns of the group."""
        return self._columns

    def __lt__(self, other: "Group") -> bool:
        """Compare the groups."""
        if not self._issues or not other._issues:
            raise ValueError("group data has not been loaded")
        return self._issues.total() < other._issues.total()
