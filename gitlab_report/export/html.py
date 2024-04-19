from pathlib import Path

import mistune

from ..report import Report
from .markdown import generate_markdown


class HTMLRenderer(mistune.HTMLRenderer): ...


def export(
    report: Report,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Export the report to the output directory in HTML format."""
    with open(output_dir / f"{prefix}.html", "w") as file:
        content = generate_html(report)
        file.write(content)


def generate_html(report: Report) -> str:
    """Generate the HTML content from the report."""
    markdown = generate_markdown(report)
    body = str(mistune.html(markdown))
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{report.title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
        }}
        h1 {{
            font-size: 2em;
        }}
        h2 {{
            font-size: 1.5em;
            padding-top: 1em;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    {body}
</body>
</html>
"""
