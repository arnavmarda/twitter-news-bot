import click
import os
from cron_validator import CronValidator

def __give_yaml_text(self, cron: str, file: str) -> str:
    """Private: Build the .yaml file text for Github Actions to run the cron job
    
    Parameters
    ----------
    cron : str
        The cron job to run the pipeline.
        You can get a formatted cron job string from https://crontab.guru/
    file : str
        The file to run the pipeline from

    Returns
    -------
    str
        The .yaml file text for Github Actions to run the cron job
    """
    
    # Build the .yaml file text
    text = f"""---
name: "Twitter News Bot"
on:
schedule:
- cron: '{cron}'

jobs:
python-job:
name: "Python job"
runs-on: ubuntu-latest
steps:
    - name: Checkout repository
    uses: actions/checkout@v2
    - name: Setup python
    uses: actions/setup-python@v2
    with:
        python-version: '3.11.3'
    - name: Install dependencies
    run: pip install requests==2.31.0 requests-html==0.10.0 tweepy==4.14.0 google-generativeai==0.1.0 validators==0.20.0 cron-validator==1.0.8 python-dotenv==1.0.0
    - name: Run python script
    run: python {file}"""

    return text

@click.group()
def cli():
    pass

@cli.command(name="build-yaml")
@click.argument("cron")
@click.argument("filename")
def build_yaml(cron: str, filename: str) -> None:
    """Build a .yaml file for Github Actions to run the cron job
    
    Parameters
    ----------
    cron : str
        The cron job to run the pipeline.
        You can get a formatted cron job string from https://crontab.guru/
    filename : str
        The file to run the pipeline from

    Returns
    -------
    None

    Raises
    ------
    TypeError
        If cron is not a string
    TypeError
        If file_name is not a string
    ValueError
        If cron is not a valid cron job
    """

    # Check if cron is a string
    if not isinstance(cron, str):
        raise TypeError("cron must be a string")
    
    # Check if file is a string
    if not isinstance(filename, str):
        raise TypeError("file_name must be a string")
    
    # Check if cron is valid cron job
    if CronValidator.parse(cron) is None:
        raise ValueError("cron must be a valid cron job")
    
    # Build the .yml file
    text = __give_yaml_text(cron=cron, file=filename)

    try:
        os.mkdir(".github")
    except FileExistsError:
        pass

    try:
        os.mkdir(".github/workflows")
    except FileExistsError:
        pass

    file = open(".github/workflows/python-app.yml", "w")
    file.write(text)
    file.close()

if __name__ == "__main__":
    cli()