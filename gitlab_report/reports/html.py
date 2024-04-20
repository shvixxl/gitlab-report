from pathlib import Path

import mistune

from ..config import Config

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>{company} - {title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
        }}
        h1 {{
            font-size: 2em;
            padding-top: 1em;
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
            border: 1px solid rgb(226, 226, 226);
            padding: 13px;
        }}
        th {{
            background-color: rgb(248, 248, 248);
        }}
        tr:nth-child(even) {{
            background-color: rgb(248, 248, 248);
        }}
        hr {{
            border: 1px solid rgb(226, 226, 226);
        }}
    </style>
</head>
<body>
    {body}
</body>
</html>
"""


def create_html_report(
    config: Config,
    markdown_report_path: Path,
    *,
    output_dir: Path,
    prefix: str,
) -> Path:
    """Export the report to the output directory in HTML format."""
    with open(markdown_report_path) as file:
        markdown = file.read()

    output_path = output_dir / f"{prefix}.html"
    with open(output_path, "w") as file:
        body = str(object=mistune.html(markdown))
        file.write(
            TEMPLATE.format(
                company=config.company,
                title=config.title,
                body=body,
            )
        )

    return output_path
