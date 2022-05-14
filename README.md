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

## Example Result

<img src="https://user-images.githubusercontent.com/9856514/168425744-bcfd0510-3ec3-433e-82c1-4d8d2d1940d8.png" alt="example result" width="500px">

## License

This software is licensed under the MIT License.
