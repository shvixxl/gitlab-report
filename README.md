# GitLab Report

Python script for creating GitLab reports for Issues. Reports are produced in PDF, HTML, Markdown and JSON formats.

## Dependencies

- [Mistune](https://mistune.lepture.com) for rendering Markdown reports to HTML format.
- [Pydantic](https://pydantic.dev) for configuration validation.
- [`python-gitlab`](https://python-gitlab.readthedocs.io) for communicating with GitLab's REST API.
- [Typer](https://typer.tiangolo.com) for CLI interface.
- [`xhtml2pdf`](https://xhtml2pdf.readthedocs.io/en/latest/) for rendering HTML reports to PDF format.

## Installation

```shell
python3 -m pip install <path>
```

where `<path>` is a directory where you cloned this repository or a URL to the repository.

## Usage

Either directly:

```shell
gitlab-report <config-file>
```

or via Python:

```shell
python3 -m gitlab_report <config-file>
```

where `<config-file>` is a JSON file which content is described in [Configuration](#configuration) section below.

### Options

You can also specify following options:

- `--output-dir` or `-o` - path to a directory where all created reports will be saved, by default all reports will be saved in current directory.
- `--prefix` or `-p` - prefix for the report filenames, by default current date is used as prefix.

## Configuration

Report configuration is a JSON file with following properties:

- `url` - URL of the GitLab instance, defaults to `https://gitlab.com`
- `access_token` - either personal, project or group access token for the GitLab API.
- `oauth_token` - OAuth 2.0 access token for the GitLab API.
- `title` - title for the report.
- `company` - name of the company
- `logo` - image to attach to the report as a logo.

> Either `access_token` or `oauth_token` must be provided.

Optionally, you can set a period for the report in `period` object with following properties:

- `from` - starting period.
- `to` - ending period.

> Period is used for filtering issues by their creation date.

### Sections

Report consists of three sections: Issues, Groups and Projects.

#### Issues

Configured in `issues` object. There are several options:

- `ongoing` - an array of labels that filters "ongoing" issues.
- `pending` - an array of labels that filters "pending" issues.

You can also configure stat comments in `stats` object:

- `incidents_solving_rate` - solving rate for incident issues (closed incidents / created incidents).
- `solving_rate` - solving rate for all issues (closed / created).
- `average_delay` - average delay in days for overdue issues (days since due date for opened issues or days since due date until closed at date for closed issues)

#### Groups

Configured in `groups` object. You can configure the `top` option here which affects the amount of groups showed in the result table.

#### Projects

Configured in `projects` object. As well as `top` option from [Groups](#groups), you can also configure custom subsections with a selection of IDs of the projects you want to include.

### Example

```json
{
  "url": "https://gitlab.com",
  "access_token": "glpat-EXAMPLE",
  "title": "Activity Report",
  "company": "Company Name",
  "logo": "./Logo.jpg",
  "period": {
    "from": "2024-04-01",
    "to": "2024-05-01"
  },
  "issues": {
    "ongoing": [
      "ToDo",
      "Develop"
    ],
    "pending": [],
    "stats": {
      "incidents_solving_rate": "> 1 ok",
      "solving_rate": "> 1 ok",
      "average_delay": "< 5 Good"
    }
  },
  "groups": {
    "top": "All"
  },
  "projects": {
    "top": 10,
    "Custom Name 1": [
      3,
      10
    ],
    "Custom Name 2": [
      1,
      8,
      6
    ]
  }
}
```
