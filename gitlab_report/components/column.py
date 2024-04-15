import pandas as pd

from ..config import ColumnConfig
from ..filter import filter_issues


class Column:
    """A column of a section."""

    def __init__(self, config: ColumnConfig) -> None:
        self._config = config

        self._value = None

    def load(self, issues: pd.DataFrame) -> None:
        """Load the data for the column."""
        self._issues = filter_issues(issues, self._config)
        self._value = len(self._issues)

    @property
    def title(self) -> str:
        """Get the title of the column."""
        return self._config.title

    def dump(self) -> int | str:
        """Get the value of the column."""
        return self._value
