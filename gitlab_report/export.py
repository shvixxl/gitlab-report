import json
from pathlib import Path

from .config import ReportFormat


def export_dump(
    dump: dict,
    *,
    output_dir: Path,
    prefix: str,
    formats: list[ReportFormat],
) -> None:
    """Export the report to the output directory."""
    for format in formats:
        export = exporters[format]
        export(dump, output_dir=output_dir, prefix=prefix)


def export_json(
    dump: dict,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Export the report to the output directory in JSON format."""
    dump = dump.copy()

    if dump["period_from"]:
        dump["period_from"] = dump["period_from"].isoformat()

    if dump["period_to"]:
        dump["period_to"] = dump["period_to"].isoformat()

    with open(output_dir / f"{prefix}.json", "w") as file:
        json.dump(dump, file, indent=2)


exporters = {
    ReportFormat.JSON: export_json,
}
