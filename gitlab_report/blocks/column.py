from dataclasses import dataclass

from ..database import Issues
from ..database.collections.issues import Filter


@dataclass(kw_only=True)
class ColumnConfig(Filter):
    """Configuration for a column of a section."""

    title: str


class Column:
    """A column of a section."""

    def __init__(self, config: ColumnConfig) -> None:
        self._config = config
        self._issues = None

    def load(self, issues: Issues) -> None:
        """Load the data for the column."""
        self._issues = issues.filter(self._config)

    @property
    def title(self) -> str:
        """Get the title of the column."""
        return self._config.title

    @property
    def total(self) -> int:
        """Get the total number of issues."""
        if not self._issues:
            raise ValueError("column data has not been loaded")
        return self._issues.total()
