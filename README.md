# Telegram Bot for Giphy Views Tracker

This Telegram bot allows you to track daily views of specific Giphy projects and receive updates directly in your Telegram chat.

## Assignment Overview

The assignment is to create a Telegram bot that performs the following functions:

- Create a Telegram bot that interacts with users.
- Allow users to set and manage Giphy project IDs for tracking.
- Automate fetching daily view counts of Giphy projects.
- Send daily updates to users with the view counts.

## Features

- **Bot Commands:**
  - `/start`: Begin interacting with the bot and view available commands.
  - `/set_project <project_id>`: Set your Giphy project ID for tracking.
  - `/get_views`: Get the daily views of your tracked Giphy project.
  - `/search <search_term>`: Search for a Giphy project based on a search term and set it for tracking.
  - `/url <giphy_url>`: Set a Giphy project ID based on a Giphy URL.
  - `/help`: Display available commands and usage instructions.

- **Daily Updates:**
  - Automated daily updates of Giphy project views sent to users via Telegram.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
cd your-repository
```

### 2. Install Dependencies

Ensure you have Python and pip installed. Install required Python packages using:
```bash
pip install -r requirements.txt
```
### 3. Set Up Telegram Bot

To use this Telegram bot, you'll need to create a new bot using the BotFather on Telegram and obtain the bot token.

1. **Create a New Telegram Bot:**
   - Open Telegram and search for the BotFather (https://t.me/BotFather).
   - Start a chat with BotFather and use the `/newbot` command to create a new bot.
   - Follow the prompts to choose a name and username for your bot, and you will receive a token for your bot.

2. **Set Bot Token as Environment Variable:**
   - Copy the bot token provided by BotFather.
   - Set the token as an environment variable named `TELEGRAM_BOT_API` in your system:
     ```bash
     export TELEGRAM_BOT_API="your_bot_token_here"
     ```
   Alternatively, you can set the environment variable in your preferred way (e.g., using a `.env` file).

### 4. Set Up Giphy API Key

To fetch Giphy project views, you'll need to obtain a Giphy API key.

1. **Sign Up for Giphy API Key:**
   - Sign up for a Giphy Developer account and obtain an API key at https://developers.giphy.com/.
   
2. **Set Giphy API Key as Environment Variable:**
   - Copy your Giphy API key.
   - Set the API key as an environment variable named `GIPHY_API_KEY` in your system:
     ```bash
     export GIPHY_API_KEY="your_giphy_api_key_here"
     ```
   Alternatively, store the API key securely in your preferred way (e.g., using a `.env` file).

### 5. Run the Bot

Once you have set up the required environment variables, you can run the Telegram bot:

```bash
python bot.py
```
### 6. Interact with the Bot

1. **Start a Chat with Your Telegram Bot:**
   - Open Telegram and search for your bot using its username.
   - Start a chat with the bot by clicking on the "Start" button.

2. **Use Bot Commands:**
   - Use the `/set_project <project_id>` command to set a Giphy project ID for tracking.
   - Use the `/get_views` command to get the daily views of your tracked Giphy project.
   - Use the `/search <search_term>` command to search for a Giphy project and set it for tracking.
   - Use the `/url <giphy_url>` command to set a Giphy project ID based on a Giphy URL.

### Additional Notes

- Make sure to handle environment variables securely, especially sensitive keys like API tokens.
- Customize the bot functionality and commands according to your project requirements by modifying the `bot.py` script.
- Refer to the script comments and documentation for detailed implementation details.
