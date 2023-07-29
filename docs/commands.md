# Command Line Interface Commands

## twitternewsbot
The main command for the CLI.

Usage:
```bash
twitternewsbot COMMAND [ARGS]...
```

### build-yaml

Build a .yaml file for Github Actions to run the cron job

Usage: 
```bash
twitternewsbot build-yaml CRON FILENAME
```

Arguments:

 - `CRON`: str - Cron expression for the job
 - `FILENAME`: str - Name of the file of the script to run

 Example:
```bash
twitternewsbot build-yaml "0 0 * * *" "main.py"
```