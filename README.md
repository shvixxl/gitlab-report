# GitLab Report

Python script for creating GitLab reports for Issues. Reports can be produced in PDF, Excel, HTML, Markdown and JSON formats.

## Dependencies

This script is built using [Pandas](https://pandas.pydata.org), [Pydantic](https://pydantic.dev), [python-gitlab](https://python-gitlab.readthedocs.io) and [Typer](https://typer.tiangolo.com).

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
- `--format` or `-f` - format of the report (`pdf`, `excel`, `html`, `markdown`, `json`). Multiple formats can be specified by using this option multiple times, e.g. `-f pdf -f json -f markdown`. By default script produces reports in PDF format.

## Configuration

Configuration for this script is provided via a JSON file. At its minimum it should have following properties:

- `url` - GitLab server URL, e.g. `https://gitlab.com`.
- `private_token` or `oauth_token` - either personal, project or group access tokens or an OAuth 2.0 access token.

You can also customize reports by providing following properties:

- `title` - title for the report, it could be your company name.
- `image` - image attached the report, for example your company logo.

Optionally, you set a period for the report:

- `period_from` - starting period.
- `period_to` - ending period.

### Sections

Report consists of sections. They are configured in `sections` array in the configuration, each section configuration is an object with following properties:

- `title` - title of the section.

#### Filters

You can narrow report results using following properties for filtering:

- `group` - a group path or an array of group paths.
- `project` - a project path or an array of project paths, e.g. `my-group/my-project`.
- `assignee` - a assignee username array of assignee usernames.
- `label` - a label name or an array of label names.
- `type` - an issue type or an array of issue types (`"issue"`, `"incident"`, `"test_case"` or `"task"`).
- `state` - an issue state or an array of issue states (`"opened"`, `"closed"`).

`"None"` and `"Any"` can be used as values to match issues with either no values for selected key or with at least any value, e.g. issues with no assignees or with at least one label.

#### Groups

Since by default all issues are grouped into a single group, you would probably want to change it by specifying `group_by` property. There are a few basic groupings available:

- `"group"` - by groups.
- `"project"` - by projects.
- `"assignee"` - by assignees.
- `"label"` - by label.
- `"type"` - by type.
- `"state"` - by state.

It is also possible to create reports with more advanced grouping by providing an array of group configurations. Each group configuration is an object with following properties:

- `title` - title of the group.

And filtering properties described in [Filters](#filters) section above, but if omitted, the group will match all issues.

Example groups:

```json
{
  "name": "Closed Incidents and Issues",
  "type": ["incident", "issues"],
  "state": "closed"
}
```

```json
{
  "name": "Opened without assignee",
  "assignee": "None",
  "state": "opened"
}
```

```json
{
  "name": "All Issues"
}
```

#### Columns

By default, reports only show the total amount of issues in each group. Custom columns can be configured in a `columns` property. Each column configuration is an object with following properties:

- `title` - title of the column.

And filtering properties described in [Filters](#filters) section above, but if omitted, the column will count all issues.

Example:

```json
[
  {
    "title": "Total",
  },
  {
    "title": "Incidents",
    "type": "incident"
  }
]
```

### Example configuration

```json
{
  "url": "https://gitlab.com",
  "private_token": "glpat-EXAMPLe8EwWRx5yDxM5q",
  "title": "Example",
  "image": "https://example.com/image.jpg",
  "sections": [
    {
      "title": "Open Issues",
      "states": [
        "opened"
      ],
      "group_by": [
        {
          "title": "Incidents",
          "type": "incident"
        },
        {
          "title": "Issues",
          "types": "issue"
        }
      ],
      "columns": [
        {
          "title": "Assigned",
          "assignee": "Any"
        },
        {
          "title": "Unassigned",
          "assignees": "None"
        }
      ]
    },
    {
      "title": "Projects",
      "group_by": "project",
      "columns": [
        {
          "title": "Total"
        },
        {
          "title": "Incidents",
          "types": ["incident"]
        }
      ]
    }
  ]
}
```
