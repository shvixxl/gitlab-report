from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field

from .blocks.section import Section, SectionConfig
from .database import Database


class ReportConfig(BaseModel):
    """Configuration for the report."""

    title: str = "GitLab Report"
    image: str | None = None

    period_from: datetime | None = None
    period_to: datetime | None = None

    sections: list[SectionConfig] = Field(default_factory=list)


@dataclass
class Report:
    """A GitLab report."""

    title: str
    image: str | None

    period_from: datetime | None
    period_to: datetime | None

    sections: list[Section]


def create_report(
    config: ReportConfig,
    *,
    url: str,
    access_token: str | None = None,
    oauth_token: str | None = None,
    skip_ssl: bool = False,
    ca_file: Path | None = None,
) -> Report:
    """Create a GitLab report."""
    with Database(
        url=url,
        access_token=access_token,
        oauth_token=oauth_token,
        skip_ssl=skip_ssl,
        ca_file=ca_file,
    ) as db:
        issues = db.get_issues(
            created_after=config.period_from,
            created_before=config.period_to,
        )

    sections = [Section(section_config) for section_config in config.sections]
    for section in sections:
        section.load(issues)

    return Report(
        title=config.title,
        image=config.image,
        period_from=config.period_from,
        period_to=config.period_to,
        sections=sections,
    )
