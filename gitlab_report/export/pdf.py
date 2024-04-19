from pathlib import Path

import pdfkit

from ..report import Report
from .html import generate_html


def export(
    report: Report,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Export the report to the output directory in PDF format."""
    html = generate_html(report)
    pdfkit.from_string(html, output_dir / f"{prefix}.pdf")
