# Using Github-Actions

## Introduction
GitHub Actions are an essential part of GitHub's continuous integration and continuous deployment (CI/CD) platform. They allow you to automate various tasks, workflows, and processes directly within your GitHub repositories. With GitHub Actions, you can set up automated build, test, release, and deployment pipelines, enabling you to streamline your software development workflows and improve collaboration among team members.

Here's an explanation of GitHub Actions concepts and how they work, along with some examples in Markdown:

### Workflows
A workflow is a series of automated steps that are executed when specific events occur in your GitHub repository, such as a push to the repository, a pull request, or a new release. Workflows are defined in the `.github/workflows` directory in your repository, and they are written in YAML format.

Example workflow that runs automated tests on every push to the `main` branch:
```yaml linenums="1"
name: Automated Tests

on:
  push:
    branches:
      - main

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'

      - name: Install dependencies
        run: npm install

      - name: Run tests
        run: npm test
```

### Jobs
A job is a set of steps that run sequentially on the same runner. A workflow can have one or more jobs that run concurrently or sequentially, depending on the configuration.

Example job that builds the application, creates a production build, and then deploys it to a hosting service:
```yaml linenums="1"
jobs:
  build-and-deploy:
    name: Build and Deploy
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '12'

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Deploy
        run: npm run deploy
```

### Steps
Steps are individual tasks within a job. They represent the commands that will be executed on the runner.

Example step that installs dependencies:
```yaml linenums="1"
steps:
  - name: Install Dependencies
    run: npm install
```

### Actions
Actions are reusable units of code that can be used in steps. They encapsulate specific functionality and can be shared across multiple workflows and repositories.

Example action that sets up Node.js environment for the job:
```yaml linenums="1"
steps:
  - name: Setup Node.js
    uses: actions/setup-node@v2
    with:
      node-version: '14'
```

GitHub Actions provide a flexible and powerful automation platform that can significantly improve your development workflows, and you can find a wide range of community-contributed actions in the GitHub Marketplace to further enhance your automation capabilities.

## Using GitHub Actions to automate the Twitter News Bot

### Cron-Jobs
Cron-jobs are a time-based job scheduler in Unix-like computer operating systems. The name cron comes from the word "chronos", Greek for "time". Cron-jobs are used to schedule jobs (commands or shell scripts) to run periodically at fixed times, dates, or intervals. It typically automates system maintenance or administration—though its general-purpose nature makes it useful for things like downloading files from the Internet and downloading email at regular intervals.

Cron-jobs are composed of two parts: a cron expression and a shell command to execute. The cron expression is a string of five numbers separated by spaces. Each number represents a time unit (minutes, hours, days, months, years) and is followed by a slash and a number that indicates how often the command should be executed. For example, the cron expression `0 0 * * *` means that the command should be executed every day at midnight.

**Cron-jobs prove extremely useful for a Twitter news bot as we can use cron-jobs to schedule our script to scrape, summarize and post news blasts on twitter at particular times or intervals of the day. We now describe how to use Github-actions with cron-jobs to automatically schedule your customized tweets.**

### Setting up the workflow
A necessary pre-requisite for using github-actions would be to have a github account. If you do not have one, you can create one [here](https://github.com/pricing). 

To run github-actions, your script must be stored in a github repository. To create a repository, you can follow the steps [here](https://docs.github.com/en/get-started/quickstart/create-a-repo).

Once you have created a repository, you need to add your script to the repository by importing the twitter-news-bot library and building the script. 

Now, you have to create a `.yml` file in the `.github/workflows` directory of your repository. Luckily, the package provides a command for this. You can run the following command in the root directory of your project:
```bash
twitternewsbot build-yaml CRON FILENAME
```
where `CRON` is the cron expression and `FILENAME` is the name of the python script you have created. You can use [this](https://crontab.guru/) to help you build cron expressions. For example, if you want to run the script in `main.py` every day at 12:00 AM, you can run:
```bash
twitternewsbot build-yaml "0 0 * * *" "main.py"
```

This will create a `.yml` file in the `.github/workflows` directory of your repository. You can now commit and push the changes to your repository. This should create a github-action tweeting your news blasts at the specified time.