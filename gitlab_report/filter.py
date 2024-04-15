import pandas as pd

from .config import FilterConfig, FilterKeyword


def filter_issues(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues."""
    filters = [
        filter_by_group,
        filter_by_project,
        filter_by_assignee,
        filter_by_label,
        filter_by_type,
        filter_by_state,
    ]

    for filter_fn in filters:
        issues = filter_fn(issues, config)

    return issues


def filter_by_group(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues by group."""
    if not config.group:
        return issues

    if isinstance(config.group, str):
        return issues[issues["group"] == config.group]

    return issues[issues["group"].isin(config.group)]


def filter_by_project(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues by project."""
    if not config.project:
        return issues

    if isinstance(config.project, str):
        return issues[issues["project"] == config.project]

    return issues[issues["project"].isin(config.project)]


def filter_by_assignee(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues by assignee."""
    if not config.assignee:
        return issues

    if isinstance(config.assignee, str):
        match config.assignee:
            case FilterKeyword.Any:
                return issues[issues["assignees"].notna()]
            case FilterKeyword.None_:
                return issues[issues["assignees"].isna()]

        return issues[
            issues["assignees"].apply(
                lambda assignees: assignees and config.assignee in assignees
            )
        ]

    issues = issues[
        issues["assignees"].apply(
            lambda assignees: all(assignee in assignees for assignee in config.assignee)
        )
    ]
    return issues


def filter_by_label(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues by label."""
    if not config.label:
        return issues

    if isinstance(config.label, FilterKeyword):
        match config.label:
            case FilterKeyword.Any:
                return issues[issues["labels"].notna()]
            case FilterKeyword.None_:
                return issues[issues["labels"].isna()]

    if isinstance(config.label, str):
        return issues[
            issues["labels"].apply(lambda labels: labels and config.label in labels)
        ]

    issues = issues[
        issues["labels"].apply(
            lambda labels: all(label in labels for label in config.label)
        )
    ]
    return issues


def filter_by_type(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues by type."""
    if not config.type:
        return issues

    if isinstance(config.type, str):
        return issues[issues["type"] == config.type]

    return issues[issues["type"].isin(config.type)]


def filter_by_state(issues: pd.DataFrame, config: FilterConfig) -> pd.DataFrame:
    """Filter the issues by state."""
    if not config.state:
        return issues

    if isinstance(config.state, str):
        return issues[issues["state"] == config.state]

    return issues[issues["state"].isin(config.state)]
