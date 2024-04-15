import gitlab
import pandas as pd

from ..config import ReportConfig
from ..normalize import normalize_issues
from .section import Section


class Report:
    """A GitLab report."""

    def __init__(self, config: ReportConfig) -> None:
        self._config = config

        self._sections = []
        if self._config.sections:
            for section_config in self._config.sections:
                self._sections.append(Section(section_config))

        self._issues = None

    def load(self) -> None:
        """Load the data for the report."""

        # TODO: Load only the data needed for the report.

        # TODO: Load data in batches.

        # TODO: Consider using GraphQL API.

        with gitlab.Gitlab(
            url=str(self._config.url),
            private_token=self._config.private_token,
            oauth_token=self._config.oauth_token,
        ) as gl:
            if self._config.period_to:
                period_to = self._config.period_to.isoformat()
                opened_issues = gl.issues.list(
                    get_all=True,
                    state="opened",
                    created_before=period_to,
                )
            else:
                opened_issues = gl.issues.list(
                    get_all=True,
                    state="opened",
                )

            if self._config.period_from:
                period_from = self._config.period_from.isoformat()
                closed_issues = gl.issues.list(
                    get_all=True,
                    state="closed",
                    updated_after=period_from,
                )
                closed_issues = [
                    issue for issue in closed_issues if issue.closed_at >= period_from
                ]
            else:
                closed_issues = gl.issues.list(
                    get_all=True,
                    state="closed",
                )

        issues = list(opened_issues) + list(closed_issues)

        normalized_issues = normalize_issues(issues)

        self._issues = pd.DataFrame(normalized_issues)

        for section in self._sections:
            section.load(self._issues)

    def dump(self) -> dict:
        """Dump the report data."""
        return {
            "title": self._config.title,
            "image": self._config.image,
            "period_from": self._config.period_from,
            "period_to": self._config.period_to,
            "sections": {section.title: section.dump() for section in self._sections},
        }
