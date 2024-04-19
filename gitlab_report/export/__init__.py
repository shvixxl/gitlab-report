from enum import Enum

__all__ = ["Format"]


class Format(str, Enum):
    """Export format."""

    PDF = "pdf"
    # Excel = "excel"
    HTML = "html"
    Markdown = "markdown"
    JSON = "json"
