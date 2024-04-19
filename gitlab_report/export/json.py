import json
from pathlib import Path

from ..report import Report


def export(
    report: Report,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Export the report to the output directory in JSON format."""
    dump = {
        "title": report.title,
        "image": report.image,
        "period_from": (
            report.period_from.strftime("%Y-%m-%d") if report.period_from else None
        ),
        "period_to": (
            report.period_to.strftime("%Y-%m-%d") if report.period_to else None
        ),
        "sections": [
            {
                "title": section.title,
                "total": section.total,
                "groups": [
                    {
                        "title": group.title,
                        "total": group.total,
                        "columns": [
                            {
                                "title": column.title,
                                "total": column.total,
                            }
                            for column in group.columns
                        ],
                    }
                    for group in section.groups
                ],
            }
            for section in report.sections
        ],
    }

    with open(output_dir / f"{prefix}.json", "w") as file:
        json.dump(dump, file, indent=2)
