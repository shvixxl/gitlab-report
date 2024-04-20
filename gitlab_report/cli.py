from datetime import datetime
from pathlib import Path

import typer
from typing_extensions import Annotated

from .config import Config
from .report import create_report

app = typer.Typer(
    add_completion=False,
    context_settings={
        "help_option_names": ["-h", "--help"],
    },
)


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
    ] = datetime.now().strftime("%Y%m%d_Report"),
) -> None:
    """Create GitLab report."""
    with config_file.open() as file:
        config_json = file.read()

    config = Config.model_validate_json(config_json)

    create_report(config, output_dir=output_dir, prefix=prefix)
