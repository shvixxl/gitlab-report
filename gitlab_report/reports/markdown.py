from datetime import datetime
from io import TextIOBase
from pathlib import Path

from ..config import Config
from ..models import Group, IssueType
from ..models.issue import IssueState


def create_markdown_report(
    config: Config,
    groups: list[Group],
    *,
    output_dir: Path,
    prefix: str,
) -> Path:
    """Export the report to the output directory in Markdown format."""
    output_path = output_dir / f"{prefix}.md"

    with open(output_path, "w") as file:
        add_header(config, file)
        file.write("---\n\n")

        add_issues_section(config, groups, file)
        file.write("---\n\n")

        add_group_section(config, groups, file)
        file.write("---\n\n")

        add_project_section(config, groups, file)

    return output_path


def add_header(
    config: Config,
    file: TextIOBase,
) -> None:
    """Add header to the Markdown report."""

    file.write("| ")

    info_block = f"{config.title}<br>"

    if config.company:
        info_block = f"{config.company}<br>" + info_block

    if config.period.from_:
        info_block += f"Period from {config.period.from_.strftime('%m / %Y')} to "
    else:
        info_block += "Period until "

    if config.period.to:
        info_block += config.period.to.strftime("%m / %Y</br/")
    else:
        info_block += datetime.now().strftime("%m / %Y (Today)<br>")

    file.write(info_block)
    file.write(" | ")

    if config.logo:
        logo_block = f'<img src="{config.logo}" align="right" style="zoom:25%;">'
    else:
        logo_block = "    "

    file.write(logo_block)
    file.write(" |\n")

    file.write(
        f"| :{'-' * (len(info_block) - 1)} | {'-' * (len(logo_block) - 1)}: |\n\n"
    )


def add_issues_section(
    config: Config,
    groups: list[Group],
    file: TextIOBase,
) -> None:
    """Add issues section to the Markdown report."""

    file.write("# Issues section\n\n")

    file.write(
        "| Issues status (selected period) | Number of issues | % of the Total |\n"
        "| :------------------------------ | ---------------: | -------------: |\n"
    )

    issues = [
        issue
        for group in groups
        for project in group.projects
        for issue in project.all_issues
    ]
    issues_total = len(issues)
    issues_percent = 100

    incidents = [issue for issue in issues if issue.type == IssueType.INCIDENT]
    incidents_total = len(incidents)
    incidents_percent = int(incidents_total / issues_total * 100) if issues_total else 0

    created = [
        issue
        for group in groups
        for project in group.projects
        for issue in project.period_issue
    ]
    created_total = len(created)
    created_percent = int(created_total / issues_total * 100) if issues_total else 0

    closed = [issue for issue in issues if issue.state == IssueState.CLOSED]
    closed_total = len(closed)
    closed_percent = int(closed_total / issues_total * 100) if issues_total else 0

    opened = [issue for issue in issues if issue.state == IssueState.OPENED]

    ongoing = [
        issue
        for issue in opened
        if any(label in issue.labels for label in config.issues.ongoing)
    ]
    ongoing_total = len(ongoing)
    ongoing_percent = int(ongoing_total / issues_total * 100) if issues_total else 0

    pending = (
        [
            issue
            for issue in opened
            if any(label in issue.labels for label in config.issues.pending)
        ]
        if config.issues.pending
        else [issue for issue in opened if not issue.labels]
    )
    pending_total = len(pending)
    pending_percent = int(pending_total / issues_total * 100) if issues_total else 0

    overdue = [issue for issue in issues if issue.delay is not None]
    overdue_total = len(overdue)
    overdue_percent = int(overdue_total / issues_total * 100) if issues_total else 0

    ongoing_labels = " / ".join(config.issues.ongoing) or "no label"
    pending_labels = " / ".join(config.issues.pending) or "no label"

    file.write(
        f"| Active issues (Assigned)        | {issues_total:>16} | {issues_percent:>13}% |\n"
        f"| Incidents                       | {incidents_total:>16} | {incidents_percent:>13}% |\n"
        f"| Created                         | {created_total:>16} | {created_percent:>13}% |\n"
        f"| Closed                          | {closed_total:>16} | {closed_percent:>13}% |\n"
        f"| Ongoing ({ongoing_labels + ')':<22} | {ongoing_total:>16} | {ongoing_percent:>13}% |\n"
        f"| Pending ({pending_labels + ')':<22} | {pending_total:>16} | {pending_percent:>13}% |\n"
        f"| Overdue                         | {overdue_total:>16} | {overdue_percent:>13}% |\n"
    )

    file.write("\n")

    closed_in_period = [issue for issue in created if issue.state == IssueState.CLOSED]
    incidents_created_in_period = [
        issue for issue in created if issue.type == IssueType.INCIDENT
    ]
    incidents_closed_in_period = [
        issue for issue in closed_in_period if issue.type == IssueType.INCIDENT
    ]

    incidents_solving_rate = (
        len(incidents_closed_in_period) / len(incidents_created_in_period)
        if incidents_created_in_period
        else 0
    )
    file.write(
        "**Incidents Solving Rate** (Incidents Closed / Created): "
        f"**{incidents_solving_rate:.1f}** ( {config.issues.stats.incidents_solving_rate} )\n\n"
    )

    solving_rate = len(closed_in_period) / len(created) if created else 0
    file.write(
        "**Solving Rate** (Closed / Created): "
        f"**{solving_rate:.1f}** ( {config.issues.stats.solving_rate} )\n\n"
    )

    average_delay = (
        (sum(issue.delay for issue in overdue) / len(overdue)) if overdue else 0  # type: ignore
    )
    file.write(
        "**Average Delay** (Overdue Issues): "
        f"**{average_delay:.1f} gg** ( {config.issues.stats.average_delay} )\n\n"
    )


def add_group_section(
    config: Config,
    groups: list[Group],
    file: TextIOBase,
) -> None:
    """Add group section to the Markdown report."""

    file.write("# Group section\n\n")

    file.write(
        "| Group name | Number of issues | % of the Total | Number of Incidents | % of the Group |\n"
        "| :--------- | ---------------: | -------------: | ------------------: | -------------: |\n"
    )

    total_issues = sum(group.issues for group in groups)

    sorted_groups = sorted(
        groups,
        key=lambda group: group.issues,
        reverse=True,
    )

    for group in sorted_groups[
        : config.groups.top if config.groups.top != "All" else len(sorted_groups)
    ]:
        total_percent = int(group.issues / total_issues * 100) if total_issues else 0
        closed_percent = (
            int(group.closed_issues / group.issues * 100) if group.issues else 0
        )
        incidents_percent = (
            int(group.incidents / group.issues * 100) if group.issues else 0
        )
        closed_incidents_percent = (
            int(group.closed_incidents / group.incidents * 100)
            if group.incidents
            else 0
        )

        file.write(
            f"| {group.name:<10} "
            f"| {f'{group.issues} (closed {group.closed_issues})':>16} "
            f"| {f'{total_percent}% (closed {closed_percent}%)':>14} "
            f"| {f'{group.incidents} (closed {group.closed_incidents})':>19} "
            f"| {f'{incidents_percent}% (closed {closed_incidents_percent}%)':>14} "
            "|\n"
        )

    file.write("\n")


def add_project_section(
    config: Config,
    groups: list[Group],
    file: TextIOBase,
) -> None:
    """Add project section to the Markdown report."""

    file.write("# Project section\n\n")

    file.write(
        "| Project name | Number of issues | % of the Total | Number of Incidents | % of the Project |\n"
        "| :----------- | ---------------: | -------------: | ------------------: | ---------------: |\n"
    )

    total_issues = sum(project.issues for group in groups for project in group.projects)

    sorted_projects = sorted(
        (project for group in groups for project in group.projects),
        key=lambda project: project.issues,
        reverse=True,
    )

    for project in sorted_projects[
        : config.projects.top if config.projects.top != "All" else len(sorted_projects)
    ]:
        total_percent = int(project.issues / total_issues * 100) if total_issues else 0
        closed_percent = (
            int(project.closed_issues / project.issues * 100) if project.issues else 0
        )
        incidents_percent = (
            int(project.incidents / project.issues * 100) if project.issues else 0
        )
        closed_incidents_percent = (
            int(project.closed_incidents / project.incidents * 100)
            if project.incidents
            else 0
        )

        file.write(
            f"| {project.name:<12} "
            f"| {f'{project.issues} (closed {project.closed_issues})':>16} "
            f"| {f'{total_percent}% (closed {closed_percent}%)':>15} "
            f"| {f'{project.incidents} (closed {project.closed_incidents})':>19} "
            f"| {f'{incidents_percent}% (closed {closed_incidents_percent}%)':>16} "
            "|\n"
        )

    file.write("\n")

    for title, project_ids in config.projects.__pydantic_extra__.items():
        add_custom_project_subsection(title, project_ids, config, groups, file)


def add_custom_project_subsection(
    title: str,
    project_ids: list[int],
    config: Config,
    groups: list[Group],
    file: TextIOBase,
) -> None:
    """Add custom project subsection to the Markdown report."""
    file.write(f"## {title}\n\n")

    file.write(
        "| Project name | Number of issues | % of the Total | Number of Incidents | % of the Project |\n"
        "| :----------- | ---------------: | -------------: | ------------------: | ---------------: |\n"
    )

    total_issues = sum(project.issues for group in groups for project in group.projects)

    projects = [
        project
        for group in groups
        for project in group.projects
        if project.id in project_ids
    ]

    for project in projects:
        total_percent = int(project.issues / total_issues * 100) if total_issues else 0
        closed_percent = (
            int(project.closed_issues / project.issues * 100) if project.issues else 0
        )
        incidents_percent = (
            int(project.incidents / project.issues * 100) if project.issues else 0
        )
        closed_incidents_percent = (
            int(project.closed_incidents / project.incidents * 100)
            if project.incidents
            else 0
        )

        file.write(
            f"| {project.name:<12} "
            f"| {f'{project.issues} (closed {project.closed_issues})':>16} "
            f"| {f'{total_percent}% (closed {closed_percent}%)':>15} "
            f"| {f'{project.incidents} (closed {project.closed_incidents})':>19} "
            f"| {f'{incidents_percent}% (closed {closed_incidents_percent}%)':>16} "
            "|\n"
        )

    total_section_issues = sum(project.issues for project in projects)
    total_section_closed_issues: int = sum(
        project.closed_issues for project in projects
    )

    total_section_issues_percent = (
        int(total_section_issues / total_issues * 100) if total_issues else 0
    )
    total_section_closed_issues_percent = (
        int(total_section_closed_issues / total_section_issues * 100)
        if total_section_issues
        else 0
    )

    total_section_incidents = sum(project.incidents for project in projects)
    total_section_closed_incidents = sum(
        project.closed_incidents for project in projects
    )

    total_section_incidents_percent = (
        int(total_section_incidents / total_section_issues * 100)
        if total_section_issues
        else 0
    )
    total_section_closed_incidents_percent = (
        int(total_section_closed_incidents / total_section_incidents * 100)
        if total_section_incidents
        else 0
    )

    file.write(
        f"| **Total**    "
        f"| {f'{total_section_issues} (closed {total_section_closed_issues})':>16} "
        f"| {f'{total_section_issues_percent}% (closed {total_section_closed_issues_percent}%)':>15} "
        f"| {f'{total_section_incidents} (closed {total_section_closed_incidents})':>19} "
        f"| {f'{total_section_incidents_percent}% (closed {total_section_closed_incidents_percent}%)':>16} "
        "|\n"
    )

    file.write("\n")

    average_delay = (
        (sum(project.avg_delay for project in projects) / len(projects))
        if projects
        else 0
    )
    file.write("**Average Delay**: " f"**{average_delay:.1f} gg** ( < 5 Good )\n\n")
