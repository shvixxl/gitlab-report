import pandas as pd

from ..config import GroupType, SectionConfig
from ..filter import filter_issues
from .group import Group, group_by


class Section:
    """A section of a report."""

    def __init__(self, config: SectionConfig) -> None:
        self._config = config

        self._issues = None
        self._groups = None

    def load(self, issues: pd.DataFrame) -> None:
        """Load the data for the section."""
        self._issues = filter_issues(issues, self._config)

        if isinstance(self._config.group_by, GroupType):
            self._groups = group_by(
                issues=self._issues,
                group_type=self._config.group_by,
                columns=self._config.columns,
            )

        elif isinstance(self._config.group_by, list):
            self._groups = [
                Group(group_config, self._config.columns)
                for group_config in self._config.group_by
            ]
            for group in self._groups:
                group.load(self._issues)

    @property
    def title(self) -> str:
        """Get the section title."""
        return self._config.title

    def dump(self) -> dict:
        """Dump the section data."""
        return {group.title: group.dump() for group in self._groups}
