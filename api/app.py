from telegram import Update, ParseMode
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from googletrans import Translator
import re
from flask import Flask, request

# Initialize the translator
translator = Translator()

# Initialize Flask app
app = Flask(__name__)

# Function to handle /start command
def start(update: Update, context) -> None:
    update.message.reply_text('Welcome to the Headline Translator Bot!\n\n'
                              'Please enter your headline in Persian.')

# Function to handle messages
def handle_message(update: Update, context) -> None:
    # Get the user's message
    headline = update.message.text.strip()

    # Translate and format the headline
    formatted_headline = translate_and_format(headline)

    # Reply to the user with the formatted headline in a code block
    update.message.reply_text(f"\n{formatted_headline}\n", parse_mode=ParseMode.MARKDOWN)

# Function to translate and format the headline
def translate_and_format(headline):
    try:
        # Translate the headline to English
        english_headline = translator.translate(headline, dest='en').text

        # Convert the headline to lowercase and replace spaces with hyphens
        formatted_headline = english_headline.lower().replace(' ', '-')

        # Remove special characters except alphanumeric and hyphens
        formatted_headline = re.sub(r'[^a-zA-Z0-9\-]', '', formatted_headline)

        return formatted_headline
    except Exception as e:
        print(f"Error translating headline: {e}")
        return "Error translating headline."

# Set up the dispatcher
dispatcher = Dispatcher(None, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), None)
    dispatcher.process_update(update)
    return 'OK'

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
