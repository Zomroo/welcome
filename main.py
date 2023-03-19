import os
import requests
from PIL import Image, ImageDraw, ImageFont
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Define the font for the welcome message
font = ImageFont.truetype('arial.ttf', 40)

def welcome(bot, update):
    user = update.message.new_chat_members[0]
    name = user.first_name
    username = user.username
    user_id = user.id

    # Download the welcome image
    image_url = 'https://example.com/welcome.jpg'
    image_path = 'welcome.jpg'
    response = requests.get(image_url)
    with open(image_path, 'wb') as f:
        f.write(response.content)

    # Open the image and add the text
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    draw.text((100, 100), f'Welcome {name}!', fill='white', font=font)
    draw.text((100, 200), f'Username: {username}', fill='white', font=font)
    draw.text((100, 300), f'ID: {user_id}', fill='white', font=font)

    # Save the modified image
    image.save('welcome_modified.jpg')

    # Send the modified image as a reply to the welcome message
    bot.send_photo(chat_id=update.message.chat_id, photo=open('welcome_modified.jpg', 'rb'))

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
