import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from . import __version__
from .components import Report
from .config import ReportConfig, ReportFormat
from .export import export_dump

app = typer.Typer(
    add_completion=False,
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
)


def version_callback(value: bool):
    """Shows version information and exit."""
    if value:
        print(__version__)
        raise typer.Exit()


@app.command()
def report(
    config_file: Annotated[
        Path,
        typer.Argument(
            help="Configuration file.",
            show_default=False,
            exists=True,
            dir_okay=False,
        ),
    ],
    *,
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Output directory for the reports.",
            exists=True,
            file_okay=False,
        ),
    ] = Path.cwd(),
    prefix: Annotated[
        str,
        typer.Option(
            "--prefix",
            "-p",
            help="Prefix for the report filenames.",
        ),
    ] = datetime.now().strftime("%Y-%m-%d"),
    formats: Annotated[
        list[ReportFormat],
        typer.Option(
            "--format",
            "-f",
            help="Formats for the report.",
        ),
    ] = [ReportFormat.PDF],
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Show version information and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """Create GitLab report."""
    with config_file.open() as file:
        config = ReportConfig(**json.load(file))

    report = Report(config)
    report.load()

    dump = report.dump()

    export_dump(dump, output_dir=output_dir, prefix=prefix, formats=formats)
