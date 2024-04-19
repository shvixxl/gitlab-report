from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from ..models import Group, Issue, IssueState, IssueType, Project, User


class FilterKeyword(str, Enum):
    """Keywords for filtering."""

    Any = "Any"
    None_ = "None"


@dataclass(kw_only=True)
class Filter:
    """Configuration for filtering issues."""

    type: IssueType | set[IssueType] | None = None
    state: IssueState | set[IssueState] | None = None

    author: int | set[int] | None = None
    assignee: int | set[int] | FilterKeyword | None = None
    label: str | set[str] | FilterKeyword | None = None

    group: int | set[int] | FilterKeyword | None = None
    project: int | set[int] | None = None

    overdue: bool | None = None


class GroupBy(str, Enum):
    """Grouping for the section."""

    Group = "group"
    Project = "project"
    Author = "author"
    Assignee = "assignee"
    Label = "label"
    Type = "type"
    State = "state"


class Issues:
    """Collection of issues."""

    def __init__(self, issues: list[Issue]) -> None:
        self._issues = issues

    def total(self) -> int:
        """Count the number of issues."""
        return len(self._issues)

    def filter(self, filter: Filter) -> "Issues":
        """Filter the issues."""
        filters = [
            Issues._filter_by_type,
            Issues._filter_by_state,
            Issues._filter_by_author,
            Issues._filter_by_assignee,
            Issues._filter_by_label,
            Issues._filter_by_group,
            Issues._filter_by_project,
            Issues._filter_by_overdue,
        ]

        issues = self._issues
        for filter_fn in filters:
            issues = filter_fn(issues, filter)

        return Issues(issues)

    @staticmethod
    def _filter_by_type(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by type."""
        if not filter.type:
            return issues

        if isinstance(filter.type, set):
            return [issue for issue in issues if issue.type in filter.type]

        return [issue for issue in issues if issue.type == filter.type]

    @staticmethod
    def _filter_by_state(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by state."""
        if not filter.state:
            return issues

        if isinstance(filter.state, set):
            return [issue for issue in issues if issue.state in filter.state]

        return [issue for issue in issues if issue.state == filter.state]

    @staticmethod
    def _filter_by_author(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by author."""
        if not filter.author:
            return issues

        if isinstance(filter.author, set):
            return [issue for issue in issues if issue.author.id in filter.author]

        return [issue for issue in issues if issue.author.id == filter.author]

    @staticmethod
    def _filter_by_assignee(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by assignee."""
        if not filter.assignee:
            return issues

        if isinstance(filter.assignee, set):
            return [
                issue
                for issue in issues
                if any(assignee.id in filter.assignee for assignee in issue.assignees)
            ]

        if filter.assignee == FilterKeyword.Any:
            return [issue for issue in issues if issue.assignees]

        if filter.assignee == FilterKeyword.None_:
            return [issue for issue in issues if not issue.assignees]

        return [
            issue
            for issue in issues
            if any(assignee.id == filter.assignee for assignee in issue.assignees)
        ]

    @staticmethod
    def _filter_by_label(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by label."""
        if not filter.label:
            return issues

        if isinstance(filter.label, set):
            return [
                issue
                for issue in issues
                if any(label in issue.labels for label in filter.label)
            ]

        if filter.label == FilterKeyword.Any:
            return [issue for issue in issues if issue.labels]

        if filter.label == FilterKeyword.None_:
            return [issue for issue in issues if not issue.labels]

        return [
            issue
            for issue in issues
            if any(label == filter.label for label in issue.labels)
        ]

    @staticmethod
    def _filter_by_group(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by group."""
        if not filter.group:
            return issues

        if isinstance(filter.group, set):
            return [
                issue
                for issue in issues
                if issue.group and issue.group.id in filter.group
            ]

        if filter.group == FilterKeyword.Any:
            return [issue for issue in issues if issue.group]

        if filter.group == FilterKeyword.None_:
            return [issue for issue in issues if not issue.group]

        return [
            issue for issue in issues if issue.group and issue.group.id == filter.group
        ]

    @staticmethod
    def _filter_by_project(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by project."""
        if not filter.project:
            return issues

        if isinstance(filter.project, set):
            return [issue for issue in issues if issue.project.id in filter.project]

        return [issue for issue in issues if issue.project.id == filter.project]

    @staticmethod
    def _filter_by_overdue(issues: list[Issue], filter: Filter) -> list[Issue]:
        """Filter the issues by outdated state."""
        if filter.overdue is None:
            return issues

        today = datetime.now().isoformat()

        if filter.overdue:
            return [
                issue
                for issue in issues
                if (
                    issue.state == IssueState.Opened
                    and issue.due_date
                    and issue.due_date < today
                )
                or (
                    issue.closed_at
                    and issue.due_date
                    and issue.due_date < issue.closed_at
                )
            ]

        return [
            issue
            for issue in issues
            if not issue.due_date
            or (issue.state == IssueState.Opened and issue.due_date > today)
            or (issue.closed_at and issue.due_date > issue.closed_at)
        ]

    def group_by(self, group_by: GroupBy) -> "dict[Any, Issues]":
        """Group the issues by the specified type."""
        groupings = {
            GroupBy.Group: self._group_by_group,
            GroupBy.Project: self._group_by_project,
            GroupBy.Author: self._group_by_author,
            GroupBy.Assignee: self._group_by_assignee,
            GroupBy.Label: self._group_by_label,
            GroupBy.Type: self._group_by_type,
            GroupBy.State: self._group_by_state,
        }

        groups = groupings[group_by]()
        return {group: Issues(issues) for group, issues in groups.items()}

    def _group_by_group(self) -> dict[Group, list[Issue]]:
        """Group the issues by group."""
        groups = {}
        for issue in self._issues:
            if issue.group not in groups:
                groups[issue.group] = []

            groups[issue.group].append(issue)

        return groups

    def _group_by_project(self) -> dict[Project, list[Issue]]:
        """Group the issues by project."""
        groups: dict[Project, list[Issue]] = {}
        for issue in self._issues:
            if issue.project not in groups:
                groups[issue.project] = []

            groups[issue.project].append(issue)

        return groups

    def _group_by_author(self) -> dict[User, list[Issue]]:
        """Group the issues by author."""
        groups: dict[User, list[Issue]] = {}
        for issue in self._issues:
            if issue.author not in groups:
                groups[issue.author] = []

            groups[issue.author].append(issue)

        return groups

    def _group_by_assignee(self) -> dict[User | None, list[Issue]]:
        """Group the issues by assignee."""
        groups: dict[User | None, list[Issue]] = {}
        for issue in self._issues:
            if not issue.assignees:
                if None not in groups:
                    groups[None] = []

                groups[None].append(issue)
                continue

            for assignee in issue.assignees:
                if assignee not in groups:
                    groups[assignee] = []

                groups[assignee].append(issue)

        return groups

    def _group_by_type(self) -> dict[IssueType, list[Issue]]:
        """Group the issues by type."""
        groups: dict[IssueType, list[Issue]] = {}
        for issue in self._issues:
            if issue.type not in groups:
                groups[issue.type] = []

            groups[issue.type].append(issue)

        return groups

    def _group_by_state(self) -> dict[IssueState, list[Issue]]:
        """Group the issues by state."""
        groups: dict[IssueState, list[Issue]] = {}
        for issue in self._issues:
            if issue.state not in groups:
                groups[issue.state] = []

            groups[issue.state].append(issue)

        return groups

    def _group_by_label(self) -> dict[str | None, list[Issue]]:
        """Group the issues by label."""
        groups: dict[str | None, list[Issue]] = {}
        for issue in self._issues:
            if not issue.labels:
                if None not in groups:
                    groups[None] = []

                groups[None].append(issue)
                continue

            for label in issue.labels:
                if label not in groups:
                    groups[label] = []

                groups[label].append(issue)

        return groups
