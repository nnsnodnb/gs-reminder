# github-pr-slack-reminder

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/380a539992d941f0a6d9c045c48c580c)](https://www.codacy.com/gh/nnsnodnb/github-pr-slack-reminder/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nnsnodnb/github-pr-slack-reminder&amp;utm_campaign=Badge_Grade)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![PyPI Package version](https://badge.fury.io/py/gs-reminder.svg)](https://pypi.org/project/gs-reminder)
[![Python Supported versions](https://img.shields.io/pypi/pyversions/gs-reminder.svg)](https://pypi.org/project/gs-reminder)
[![format](https://img.shields.io/pypi/format/gs-reminder.svg)](https://pypi.org/project/gs-reminder)
[![implementation](https://img.shields.io/pypi/implementation/gs-reminder.svg)](https://pypi.org/project/gs-reminder)
[![LICENSE](https://img.shields.io/pypi/l/gs-reminder.svg)](https://pypi.org/project/gs-reminder)

Notify Slack of a review of Pull Requests in the GitHub repository.

## Environments

- Python 3.7 or later
  - poetry

## Usage

```shell
pip install gs-reminder
gs-reminder -r nnsnodnb/github-pr-slack-reminder -u examples/username.json
```

### Environment variables

- `GITHUB_TOKEN`
  - Required
  - Your GitHub Personal Access Token.
    - Create https://github.com/settings/tokens
- `SLACK_URL`
  - Required
  - Incoming webhook's url of Slack app.

### Options

- `-r` or `--repo`
  - Required
  - Your GitHub repository name. (ex. `nnsnodnb/github-pr-slack-reminder`)
- `--file-username` or `-u`
  - Required 
  - Corresponding files for GitHub and Slack usernames. (ex. `examples/username.json`)
    ```json
    [
      {
        "github": "nnsnodnb",
        "slack": "yuya.oka"    
      }
    ]
    ```

- `--limit` or `-l`
  - Optional
  - Number of Pull Requests to notify Slack. Max: 20 (default: 20)

## Example Result

<img src="https://user-images.githubusercontent.com/9856514/168442310-af165e75-7329-4a37-8e67-3f2635c549ac.png" alt="example result" width="500px">

## License

This software is licensed under the MIT License.
