from datetime import datetime
from enum import Enum
from typing import Self

from pydantic import Field, HttpUrl, model_validator
from pydantic.dataclasses import dataclass


class ReportFormat(str, Enum):
    """Format for the report."""

    PDF = "pdf"
    Excel = "excel"
    HTML = "html"
    Markdown = "markdown"
    JSON = "json"


class FilterKeyword(str, Enum):
    """Keyword for filtering issues."""

    Any = "Any"
    None_ = "None"


class IssueType(str, Enum):
    """Type of the issue."""

    Issue = "issue"
    Incident = "incident"
    TestCase = "test_case"
    Task = "task"


class IssueState(str, Enum):
    """State of the issue."""

    Opened = "opened"
    Closed = "closed"


@dataclass(kw_only=True)
class FilterConfig:
    """Configuration for filtering issues."""

    group: str | list[str] | None = None
    project: str | list[str] | None = None
    assignee: FilterKeyword | str | list[str] | None = None
    label: FilterKeyword | str | list[str] | None = None
    type: str | list[IssueType] | None = None
    state: str | list[IssueState] | None = None


class GroupType(str, Enum):
    """Grouping for the section."""

    Group = "group"
    Project = "project"
    Assignee = "assignee"
    Label = "label"
    Type = "type"
    State = "state"


@dataclass(kw_only=True)
class GroupConfig(FilterConfig):
    """Configuration for a group of a section."""

    title: str


@dataclass(kw_only=True)
class ColumnConfig(FilterConfig):
    """Configuration for a column of a section."""

    title: str


@dataclass(kw_only=True)
class SectionConfig(FilterConfig):
    """Configuration for a section of a report."""

    title: str

    group_by: GroupType | list[GroupConfig] = Field(
        default_factory=lambda: [GroupConfig(title="All Issues")]
    )

    columns: list[ColumnConfig] = Field(
        default_factory=lambda: [ColumnConfig(title="Total")]
    )


@dataclass(kw_only=True)
class ReportConfig:
    """Configuration for the report."""

    url: HttpUrl = Field(default="https://gitlab.com")

    private_token: str | None = None
    oauth_token: str | None = None

    title: str = "GitLab Report"
    image: str | None = None

    period_from: datetime | None = None
    period_to: datetime | None = None

    sections: list[SectionConfig] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_tokens(self) -> Self:
        if self.private_token is None and self.oauth_token is None:
            raise ValueError("either `private_token` or `oauth_token` must be set")
        return self

    @model_validator(mode="after")
    def validate_period(self) -> Self:
        if self.period_from and self.period_to and self.period_from > self.period_to:
            raise ValueError("`period_from` must be before `period_to`")
        return self
