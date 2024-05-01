# Twitter(x.com) Giveaway Hunting Bot

This is a Python script that automates various tasks related to Twitter, such as retweeting, following users, interacting with YouTube, Twitch, and Telegram, and replying to tweets related to various giveaways.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python
- Google Chrome

## Installation

1. Clone or download the repository.
2. Open the terminal or command prompt and navigate to the project directory.
3. Run the `setup.py` script to create a virtual environment, install the required dependencies, and set up the necessary directories and configuration files.

```
python setup.py
```

4. After the setup is complete, fill in the required information in the `config.ini` file.

## Usage

To run the script, you have two options:

1. Use the `app.py` script:

```
python app.py
```

This script will provide you with three choices:
- Scrape only: This option will scrape tweets based on the specified keywords and save them to a CSV file.
- Run app: This option will run the main script (`twittermain()` function) to perform the automated tasks.
- Both: This option will perform both scraping and running the automated tasks.

2. Use the `start.bat` script (for Windows):

```
start.bat
```

This script will run the `app.py` script within the virtual environment.

## Features

The script includes the following features:

- Scraping tweets based on specified keywords using the `tweet_scraper` function.
- Logging in to Twitter with your credentials.
- Retweeting tweets.
- Following users on Twitter.
- Interacting with YouTube videos (watching, commenting).
- Interacting with Twitch streams.
- Interacting with Telegram channels.
- Replying to tweets with custom messages and/or screenshots.
- Handling various exceptions and errors.
- Maintaining a CSV file to track the status of tasks and prevent duplicate actions.

## Configuration

The `config.ini` file contains configuration options for the script, such as Chrome options and other settings. You can modify this file according to your requirements.

## Contributing

Contributions to this project are welcome. If you find any issues or want to add new features, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).