from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'twitternewsbot',         # How you named your package folder (MyLib)
  packages = ['twitternewsbot'],   # Chose the same as "name"
  version = '2.0.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python API allowing you to automize a personalized news delivery system.',   # Give a short description about your library
  author = 'Arnav Marda',                   # Type in your name
  author_email = 'arnavmarda@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/arnavmarda/twitter-news-bot/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/arnavmarda/twitter-news-bot/archive/refs/tags/v2.0.tar.gz',    # I explain this later on
  keywords = ['AI', 'Twitter', 'News', 'Automation'],   # Keywords that define your package best
  long_description = long_description,
  long_description_content_type="text/markdown",
  install_requires=[            # I get to this in a second
          'requests==2.31.0',
          'requests-html==0.10.0',
          'tweepy==4.14.0',
          'google-generativeai==0.1.0',
          'validators==0.20.0',
          'cron-validator==1.0.8',
          'python-dotenv==1.0.0'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.11',
  ],
)