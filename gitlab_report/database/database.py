from pathlib import Path
from typing import Self

import gitlab
import gitlab.base

from .collections import Issues
from .models import Issue


class Database:
    """Database abstraction for GitLab."""

    def __init__(
        self,
        *,
        url: str,
        access_token: str | None = None,
        oauth_token: str | None = None,
        ca_file: Path | None = None,
        skip_ssl: bool = False,
        debug: bool = False,
    ) -> None:
        self._gitlab = gitlab.Gitlab(
            url=url,
            private_token=access_token,
            oauth_token=oauth_token,
            ssl_verify=str(ca_file) if ca_file else not skip_ssl,
        )

        if debug:
            self._gitlab.enable_debug()

        self._gitlab.auth()

    def get_issues(self, **kwargs) -> Issues:
        issues = self._gitlab.issues.list(get_all=True, **kwargs)

        projects = {}
        for issue in issues:
            if issue.project_id not in projects:
                projects[issue.project_id] = self._gitlab.projects.get(issue.project_id)

        return Issues(
            [Issue.from_gitlab(issue, projects[issue.project_id]) for issue in issues]
        )

    def close(self) -> None:
        self._gitlab.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()
