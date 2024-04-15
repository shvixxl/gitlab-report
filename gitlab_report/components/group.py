import pandas as pd
from pandas.core.groupby.generic import DataFrameGroupBy

from ..config import ColumnConfig, GroupConfig, GroupType
from ..filter import filter_issues
from .column import Column


class Group:
    """A group of a section."""

    def __init__(self, config: GroupConfig, columns: list[ColumnConfig]) -> None:
        self._config = config

        self._issues = None

        self._columns = [Column(column_config) for column_config in columns]

    def load(self, issues: pd.DataFrame) -> None:
        """Load the data for the group."""
        self._issues = filter_issues(issues, self._config)
        for column in self._columns:
            column.load(self._issues)

    @classmethod
    def from_group_by(
        cls,
        gb: DataFrameGroupBy,
        columns: list[ColumnConfig],
    ) -> "list[Group]":
        """Create a group from the data."""
        groups = []
        for group_name, group_issues in gb:
            group = cls(GroupConfig(title=str(group_name)), columns)
            group.load(group_issues)
            groups.append(group)
        return groups

    @property
    def title(self) -> str:
        """Get the group title."""
        return self._config.title

    def dump(self) -> dict:
        """Dump the group data."""
        return {column.title: column.dump() for column in self._columns}


def group_by(
    issues: pd.DataFrame,
    group_type: GroupType,
    columns: list[ColumnConfig],
) -> list[Group]:
    """Group the issues by the specified type."""
    return groupings[group_type](issues, columns)


def group_by_group(issues: pd.DataFrame, columns: list[ColumnConfig]) -> list[Group]:
    """Group the issues by group."""
    gb = issues.groupby("group")
    return Group.from_group_by(gb, columns)


def group_by_project(issues: pd.DataFrame, columns: list[ColumnConfig]) -> list[Group]:
    """Group the issues by project."""
    gb = issues.groupby("project")
    return Group.from_group_by(gb, columns)


def group_by_assignee(issues: pd.DataFrame, columns: list[ColumnConfig]) -> list[Group]:
    """Group the issues by assignee."""
    gb = issues.explode("assignees").groupby("assignees")
    return Group.from_group_by(gb, columns)


def group_by_type(issues: pd.DataFrame, columns: list[ColumnConfig]) -> list[Group]:
    """Group the issues by type."""
    gb = issues.groupby("type")
    return Group.from_group_by(gb, columns)


def group_by_state(issues: pd.DataFrame, columns: list[ColumnConfig]) -> list[Group]:
    """Group the issues by state."""
    gb = issues.groupby("state")
    return Group.from_group_by(gb, columns)


groupings = {
    GroupType.Group: group_by_group,
    GroupType.Project: group_by_project,
    GroupType.Type: group_by_type,
    GroupType.State: group_by_state,
}
