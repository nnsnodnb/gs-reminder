# github-pr-slack-reminder

Notify Slack of a review of Pull Requests in the GitHub repository.

## Environments

- Python 3.10
  - poetry

## Usage

```shell
pip install gs-reminder
gs_reminder -r nnsnodnb/github-pr-slack-reminder -u examples/username.json
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
