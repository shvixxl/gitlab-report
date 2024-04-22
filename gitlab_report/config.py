from datetime import datetime
from typing import Literal, Self

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class Config(BaseModel):
    """Configuration for the report."""

    url: AnyHttpUrl = Field(default="https://gitlab.com/")
    access_token: str | None = None
    oauth_token: str | None = None

    title: str = "GitLab Report"
    company: str | None = None
    logo: str | None = None

    period: "PeriodConfig" = Field(default_factory=lambda: PeriodConfig())

    issues: "IssuesConfig"
    groups: "GroupsConfig"
    projects: "ProjectsConfig"

    @model_validator(mode="after")
    def either_access_token_or_oauth_token_must_be_provided(self) -> Self:
        if self.access_token is None and self.oauth_token is None:
            raise ValueError("Either access_token or oauth_token must be provided.")
        return self


class PeriodConfig(BaseModel):
    """Configuration for the period section of the report."""

    from_: datetime | None = Field(default=None, alias="from")
    to: datetime | None = None


class IssuesConfig(BaseModel):
    """Configuration for the issues section of the report."""

    ongoing: list[str] = Field(default_factory=list)
    pending: list[str] = Field(default_factory=list)

    stats: "StatsConfig"


class StatsConfig(BaseModel):
    """Configuration for the stats section of the issues section of the report."""

    incidents_solving_rate: str
    solving_rate: str
    average_delay: str


class GroupsConfig(BaseModel):
    """Configuration for the groups section of the report."""

    top: Literal["All"] | int

    @field_validator("top")
    @classmethod
    def top_must_be_greater_than_zero(
        cls, v: Literal["All"] | int
    ) -> Literal["All"] | int:
        if v == "All":
            return v
        if v < 1:
            raise ValueError("top must be greater than 0")
        return v


class ProjectsConfig(GroupsConfig):
    """Configuration for the projects section of the report."""

    model_config = ConfigDict(extra="allow")

    __pydantic_extra__: dict[str, list[int]]  # type: ignore
