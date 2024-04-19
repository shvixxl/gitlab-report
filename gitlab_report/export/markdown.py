from datetime import datetime
from pathlib import Path

from ..report import Report


def export(
    report: Report,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Export the report to the output directory in Markdown format."""
    with open(output_dir / f"{prefix}.md", "w") as file:
        content = generate_markdown(report)
        file.write(content)


def generate_markdown(report: Report) -> str:
    """Generate the Markdown content from the report."""
    content = f"# {report.title}\n\n"

    if report.period_from or report.period_to:
        period = "Period "
        period += (
            report.period_from.strftime("from %Y-%m-%d ") if report.period_from else ""
        )
        period += (
            report.period_to.strftime("to %Y-%m-%d")
            if report.period_to
            else datetime.now().strftime("to %Y-%m-%d (Today)")
        )

        content += f"{period}\n"

    for section in report.sections:
        content += f"\n## {section.title}\n\n"

        max_group_title_length = max(len(group.title) for group in section.groups)

        header = "|"
        separator = "|:"

        header += " " * max_group_title_length
        separator += "-" * (max_group_title_length - 1)

        total_column = "Number of Issues"

        header += f"|{total_column}|"
        separator += f"|:{'-' * (len(total_column) - 1)}|"

        header += "".join(f"{column.title}|" for column in section.groups[0].columns)
        separator += "".join(
            f":{'-' * (len(column.title) - 1)}|" for column in section.groups[0].columns
        )

        header += "\n"
        separator += "\n"

        content += header + separator

        for group in section.groups:
            row = "|"

            row += group.title.ljust(max_group_title_length) + "|"

            percent = int(group.total / section.total * 100) if section.total else 0
            row += f"{group.total} ({percent}%)".rjust(len(total_column)) + "|"

            for column in group.columns:
                percent = int(column.total / group.total * 100) if group.total else 0
                row += f"{column.total} ({percent}%)".rjust(len(column.title)) + "|"

            row += "\n"

            content += row

    return content
