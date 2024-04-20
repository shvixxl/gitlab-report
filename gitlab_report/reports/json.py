from pathlib import Path

from pydantic import BaseModel

from ..config import Config, PeriodConfig
from ..models import Group, Issue, Project


class ReportSchema(BaseModel):
    period: PeriodConfig

    issues: list[Issue]
    groups: list[Group]
    projects: list[Project]


def create_json_report(
    config: Config,
    groups: list[Group],
    *,
    output_dir: Path,
    prefix: str,
) -> Path:
    """Export the report to the output directory in JSON format."""
    output_path = output_dir / f"{prefix}.json"

    report = ReportSchema(
        period=config.period,
        issues=[
            issue
            for group in groups
            for project in group.projects
            for issue in project.issue_objects
        ],
        groups=groups,
        projects=[project for group in groups for project in group.projects],
    )

    with open(output_path, "w") as file:
        file.write(report.model_dump_json(indent=2))

    return output_path
