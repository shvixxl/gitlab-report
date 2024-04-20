from pathlib import Path

from xhtml2pdf import pisa


def create_pdf_report(
    html_report_path: Path,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Export the report to the output directory in PDF format."""
    with (
        open(html_report_path) as input_file,
        open(output_dir / f"{prefix}.pdf", "wb") as output_file,
    ):
        pisa.CreatePDF(input_file, output_file)
