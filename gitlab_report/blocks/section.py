from dataclasses import dataclass

from pydantic import Field

from ..database.collections.issues import Filter, GroupBy, Issues
from .column import ColumnConfig
from .group import Group, GroupConfig


@dataclass(kw_only=True)
class SectionConfig(Filter):
    """Configuration for a section of a report."""

    title: str
    group_by: GroupBy | list[GroupConfig] = Field(
        default_factory=lambda: [GroupConfig(title="All Issues")]
    )
    columns: list[ColumnConfig] = Field(default_factory=list)
    limit: int | None = None


class Section:
    """A section of a report."""

    def __init__(self, config: SectionConfig) -> None:
        self._config = config
        self._issues = None
        self._groups = None

    def load(self, issues: Issues) -> None:
        """Load the data for the section."""
        self._issues = issues.filter(self._config)

        if isinstance(self._config.group_by, GroupBy):
            self._groups = Group.from_group_by(
                self._config.group_by, self._issues, self._config.columns
            )
            self._groups.sort(reverse=True)
            self._groups = self._groups[: self._config.limit]

        else:
            self._groups = [
                Group(group_config, self._config.columns)
                for group_config in self._config.group_by
            ]
            for group in self._groups:
                group.load(self._issues)

    @property
    def title(self) -> str:
        """Get the title of the section."""
        return self._config.title

    @property
    def total(self) -> int:
        """Get the total number of issues."""
        if not self._issues:
            raise ValueError("section data has not been loaded")
        return self._issues.total()

    @property
    def groups(self) -> list[Group]:
        """Get the groups of the section."""
        if not self._groups:
            raise ValueError("section groups have not been loaded")
        return self._groups
