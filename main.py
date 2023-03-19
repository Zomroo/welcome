import os
import requests
from PIL import Image, ImageDraw, ImageFont
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'
FONT_NAME = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

# Define the font for the welcome message
font = ImageFont.truetype(FONT_NAME, 40)

def welcome(update, context):
    bot = context.bot
    user = update.message.new_chat_members[0]
    name = user.first_name
    username = user.username
    user_id = user.id

    # Download the welcome image
    image_url = 'https://te.legra.ph/file/0517921ee0a53c72f28f5.jpg'
    response = requests.get(image_url)
    with Image.open(requests.get(image_url, stream=True).raw) as image:
        # Open the image and add the text
        draw = ImageDraw.Draw(image)
        draw.text((100, 100), f'Welcome {name}!', fill='white', font=font)
        draw.text((100, 200), f'Username: {username}', fill='white', font=font)
        draw.text((100, 300), f'ID: {user_id}', fill='white', font=font)

        # Save the modified image
        image.save('welcome_modified.jpg')

        # Send the modified image as a reply to the welcome message
        with open('welcome_modified.jpg', 'rb') as f:
            bot.send_photo(chat_id=update.effective_chat.id, photo=f)

def start(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Hello! I'm a welcome bot.")

def main():
    bot = telegram.Bot(token=TOKEN)

    # Start the bot
    updater = Updater(bot=bot)
    dispatcher = updater.dispatcher

    # Add handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.status_update.new_chat_members, welcome))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
