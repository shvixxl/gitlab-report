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

- `--url` or `-u` - URL of the GitLab instance. Defaults to `https://gitlab.com`.
- `--access-token` - either personal, project or group access token for the GitLab API.
- `--oauth-token` - OAuth 2.0 access token for the GitLab API.
- `--output-dir` or `-o` - path to a directory where all created reports will be saved, by default all reports will be saved in current directory.
- `--prefix` or `-p` - prefix for the report filenames, by default current date is used as prefix.
- `--format` or `-f` - format of the report (`pdf`, `excel`, `html`, `markdown`, `json`). Multiple formats can be specified by using this option multiple times, e.g. `-f pdf -f json -f markdown`. By default script produces reports in PDF format.
- `--ca-file` - path to a custom CA file for SSL verification.
- `--skip-ssl` - skip SSL verification.

### Environment variables

This script also supports some configuration via environment variables:

- `GITLAB_URL` - URL of the GitLab instance.
- `GITLAB_ACCESS_TOKEN` - either personal, project or group access token for the GitLab API.
- `GITLAB_OAUTH_TOKEN` - OAuth 2.0 access token for the GitLab API.

## Configuration

Report configuration is a JSON file with following properties:

- `title` - title for the report, it could be your company name.
- `image` - image attached the report, for example your company logo.

Optionally, you set a period for the report:

- `period_from` - starting period.
- `period_to` - ending period.

### Sections

Report consists of sections. They are configured in `sections` property as array of section configurations. Each section configuration is an object with following properties:

- `title` - title of the section.

#### Filters

You can narrow report results using following properties for filtering.

- `type` - an issue type or an array of issue types (`"issue"`, `"incident"`, `"test_case"` or `"task"`).
- `state` - an issue state or an array of issue states (`"opened"`, `"closed"`).
- `author` - an author ID or an array of author user IDs.
- `assignee` - an assignee ID or an array of assignee IDs.
- `label` - a label name or an array of label names.
- `group` - a group ID or an array of group IDs.
- `project` - a project ID or an array of project paths, e.g. `my-group/my-project`.
- `overdue` - either `true` or `false`.

`"None"` and `"Any"` keywords can be used as values to match issues with either no values for selected key or with at least some value, e.g. issues with no assignees or with issues with any labels.

#### Groups

Since by default all issues are grouped into a single group, you would probably want to change it by specifying `group_by` property. There are a few basic groupings available:

- `"group"` - by groups.
- `"project"` - by projects.
- `"author"` - by author.
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
  "type": ["incident", "issue"],
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
    "title": "Incidents",
    "type": "incident"
  },
  {
    "title": "Overdue",
    "overdue": true
  }
]
```

### Example configuration

```json
{
  "title": "My Company - Issues Report",
  "image": "https://example.com/image.png",
  "period_from": "2024-04-01",
  "sections": [
    {
      "title": "All Issues",
      "group_by": [
        {
          "title": "Active issues (Assigned)",
          "assignee": "Any"
        },
        {
          "title": "Incidents",
          "type": "incident"
        },
        {
          "title": "Closed",
          "state": "closed"
        },
        {
          "title": "On going",
          "label": "Any"
        },
        {
          "title": "Pending",
          "label": "None"
        },
        {
          "title": "Overdue",
          "overdue": true
        }
      ]
    },
    {
      "title": "Groups ranking",
      "group_by": "group",
      "columns": [
        {
          "title": "Number of Incidents",
          "type": "incident"
        }
      ]
    },
    {
      "title": "Top 10 Projects",
      "group_by": "project",
      "limit": 10,
      "columns": [
        {
          "title": "Number of Incidents",
          "type": "incident"
        }
      ]
    },
    {
      "title": "Selected Groups",
      "group_by": [
        {
          "title": "Group 1",
          "project": 85655869
        },
        {
          "title": "Subgroup 1",
          "project": 85836532
        },
        {
          "title": "Total"
        }
      ],
      "columns": [
        {
          "title": "Number of Incidents",
          "type": "incident"
        }
      ]
    },
    {
      "title": "Selected Projects",
      "group_by": [
        {
          "title": "Project 2",
          "project": 56844097
        },
        {
          "title": "Project 3",
          "project": 56844101
        },
        {
          "title": "Total"
        }
      ],
      "columns": [
        {
          "title": "Number of Incidents",
          "type": "incident"
        }
      ]
    }
  ]
}

```
