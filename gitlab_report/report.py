from pathlib import Path

from .config import Config
from .gitlab import create_session, get_groups
from .reports import (
    create_html_report,
    create_json_report,
    create_markdown_report,
    create_pdf_report,
)


def create_report(
    config: Config,
    *,
    output_dir: Path,
    prefix: str,
) -> None:
    """Create GitLab report."""
    with create_session(
        url=str(config.url),
        access_token=config.access_token,
        oauth_token=config.oauth_token,
    ) as session:
        groups = get_groups(session)

    create_json_report(config, groups, output_dir=output_dir, prefix=prefix)

    markdown_report_path = create_markdown_report(
        config, groups, output_dir=output_dir, prefix=prefix
    )

    html_report_path = create_html_report(
        config, markdown_report_path, output_dir=output_dir, prefix=prefix
    )

    create_pdf_report(html_report_path, output_dir=output_dir, prefix=prefix)
