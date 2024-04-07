import os
import argparse
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from get_view_count_script import *
import schedule
import pytz
from datetime import datetime
import re
from dotenv import load_dotenv

#Load dotenv file (ensure .env is present)
load_dotenv()

# Set up API keys
TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_BOT_API')
GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY')

# Dictionary to store project IDs for users (replace with database in production)
user_project_map = {}

#Setup arguments 
parser = argparse.ArgumentParser(description='Daily Giphy Views Tracker Bot')
parser.add_argument('--time', default='9:30', help='Set the time of update (format: HH:MM)')
parser.add_argument('--path', default='', help='Set the path of ChromeDriver installation')
args = parser.parse_args()
path = args.path if args.path else ''

# Initialize driver 
driver = initialize_driver(path=path) 

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to Daily Giphy Views Tracker Bot!\n"
        "Use /set_project <project_id> to set your Giphy project ID.\n"
        "Use /get_views to get the daily views of your project.\n"
        "Use /search <search_term> to set the project ID based on Giphy search.\n"
        "Use /url <giphy_url> to set the project ID from a Giphy URL.\n"  # Updated line for /url command
        "Use /help to see available commands and usage."
    )


def set_project_from_url(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide a URL.")
        return

    url = context.args[0]

    # Extract Giphy ID from the URL
    match = re.search(r'/gifs/([\w-]+)', url)
    if match:
        giphy_id = match.group(1)
        user_id = update.effective_chat.id
        user_project_map[user_id] = giphy_id
        print('Printing the URL USER PROJECT MAP')
        print(user_project_map)
        update.message.reply_text(f"Project ID set to: {giphy_id}")
    else:
        update.message.reply_text("Invalid Giphy URL format.")


def convert_ist_to_utc(ist_time_str):
    try:
        # Parse the input time string in IST
        ist_time = datetime.strptime(ist_time_str, '%H:%M')

        # Assume today's date for IST time (you may adjust as needed)
        ist_time = ist_time.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

        # Create IST timezone object
        ist_tz = pytz.timezone('Asia/Kolkata')

        # Localize the IST time
        ist_time = ist_tz.localize(ist_time)

        # Convert localized IST time to UTC
        utc_time = ist_time.astimezone(pytz.utc)

        # Format the UTC time string
        utc_time_str = utc_time.strftime('%H:%M')

        return utc_time_str

    except ValueError:
        print("Invalid time format. Please provide time in HH:MM format (e.g., 01:48)")
        return None


def send_daily_updates(context: CallbackContext):
    print("Running send_daily_updates...")
    job_queue = context.job_queue  # Get the job_queue from the context
    bot = context.bot  # Get the bot from the context

    for user_id, project_id in user_project_map.items():
        views_count = fetch_views(project_id)
        if views_count != -1:
            bot.send_message(chat_id=user_id, text=f"📊 Daily views update for project {project_id}: {views_count}")
        else:
            bot.send_message(chat_id=user_id, text=f"Failed to fetch views for project {project_id}")

    # Reschedule the job for the next day
    time = convert_ist_to_utc(args.time)
    daily_time = datetime.strptime(time, "%H:%M").time()
    job_queue.run_daily(send_daily_updates, time=daily_time, context=context)


def set_project(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide a Giphy project ID.")
        return

    project_id = context.args[0]
    user_id = update.effective_chat.id
    user_project_map[user_id] = project_id
    print(user_project_map)
    update.message.reply_text(f"Project ID set to: {project_id}")

def get_views(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_chat.id
    if user_id not in user_project_map:
        update.message.reply_text("Please set a project ID using /set_project <project_id>.")
        return

    project_id = user_project_map[user_id]
    print('Project id:', project_id)
    views_count = fetch_views(project_id)

    update.message.reply_text(f"Total views for project {project_id}: {views_count}")

def fetch_views(project_id: str) -> str:
    """Fetch views count by scraping the Giphy page."""
    giphy_url = f"https://giphy.com/gifs/{project_id}"
    count = -1
    try:
        count = get_views_selenium(driver=driver, url=giphy_url, debug=True)
    except:
        count = -1 
        pass
    return count

def search_giphy(update: Update, context: CallbackContext) -> None:
    if len(context.args) == 0:
        update.message.reply_text("Please provide a search term.")
        return

    search_term = ' '.join(context.args)
    giphy_id = get_top_giphy_id(search_term)

    if giphy_id:
        user_id = update.effective_chat.id
        user_project_map[user_id] = giphy_id
        print(user_project_map)
        update.message.reply_text(f"Project ID set to: {giphy_id}")
    else:
        update.message.reply_text("No results found for the search term.")

def get_top_giphy_id(search_term: str) -> str:
    endpoint = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_API_KEY,
        "q": search_term,
        "limit": 1
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if "data" in data and data["data"]:
        return data["data"][0]["id"]
    else:
        return None

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "This is a Daily Giphy Views Tracker Bot.\n"
        "Available commands:\n"
        "/start - Start the bot and get usage instructions.\n"
        "/set_project <project_id> - Set your Giphy project ID.\n"
        "/get_views - Get the daily views of your project.\n"
        "/search <search_term> - Search for a Giphy and set the project ID.\n"
        "/url <giphy_url> - Set the project ID from a Giphy URL.\n"  # Updated line for /url command
        "/help - Display available commands and usage."
    )

def main() -> None:
    updater = Updater(TELEGRAM_API_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("set_project", set_project))
    dispatcher.add_handler(CommandHandler("get_views", get_views))
    dispatcher.add_handler(CommandHandler("search", search_giphy))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("url", set_project_from_url)) 


    #Convert IST to UTC 
    time = convert_ist_to_utc(args.time)
    # Parse the provided time argument
    daily_time = datetime.strptime(time, "%H:%M").time()
    # Get the job queue instance from the updater
    job_queue = updater.job_queue
    # Schedule the daily job to send updates
    job_queue.run_daily(send_daily_updates, time=daily_time, context=updater)
    # Start the bot
    updater.start_polling()
    # Start the bot
    print('Bot is running...')
    print('Scheduled Time:', args.time)
    updater.idle()
    

if __name__ == "__main__":
    main()
