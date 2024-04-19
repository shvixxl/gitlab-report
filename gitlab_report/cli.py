import importlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from . import __version__
from .export import Format
from .report import ReportConfig, create_report

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
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-u",
            help="URL of the GitLab instance.",
            envvar="GITLAB_URL",
        ),
    ] = "https://gitlab.com",
    access_token: Annotated[
        Optional[str],
        typer.Option(
            help="Either personal, project or group access token for the GitLab API.",
            envvar="GITLAB_ACCESS_TOKEN",
        ),
    ] = None,
    oauth_token: Annotated[
        Optional[str],
        typer.Option(
            help="OAuth 2.0 access token for the GitLab API.",
            envvar="GITLAB_OAUTH_TOKEN",
        ),
    ] = None,
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
        list[Format],
        typer.Option(
            "--format",
            "-f",
            help="Formats for the report.",
        ),
    ] = [Format.JSON],
    ca_file: Annotated[
        Optional[Path],
        typer.Option(
            help="Path to a custom CA file for SSL verification.",
            exists=True,
            dir_okay=False,
        ),
    ] = None,
    skip_ssl: Annotated[
        bool,
        typer.Option(
            "--skip-ssl",
            help="Skip SSL verification.",
        ),
    ] = False,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            help="Show version information and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Create GitLab report."""
    with config_file.open() as file:
        config = ReportConfig(**json.load(file))

    report = create_report(
        config,
        url=url,
        access_token=access_token,
        oauth_token=oauth_token,
        skip_ssl=skip_ssl,
        ca_file=ca_file,
    )

    for format in formats:
        exporter = importlib.import_module(
            f"gitlab_report.export.{format.name.lower()}"
        )
        exporter.export(report, output_dir=output_dir, prefix=prefix)
