import os
import requests
from PIL import Image, ImageDraw, ImageFont
import telegram

TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Define the font for the welcome message
font = ImageFont.truetype('arial.ttf', 40)

def welcome(update, context):
    bot = context.bot
    user = update.message.new_chat_members[0]
    name = user.first_name
    username = user.username
    user_id = user.id

    # Download the welcome image
    image_url = 'https://te.legra.ph/file/0517921ee0a53c72f28f5.jpg'
    image_path = '0517921ee0a53c72f28f5.jpg'
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
    with open('welcome_modified.jpg', 'rb') as f:
        bot.send_photo(chat_id=CHAT_ID, photo=f)

def start(update, context):
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Hello! I'm a welcome bot.")

def main():
    bot = telegram.Bot(token=TOKEN)
    updater = telegram.ext.Dispatcher(bot, None, workers=0)

    updater.add_handler(CommandHandler('start', start))
    updater.add_handler(MessageHandler(telegram.ext.Filters.status_update.new_chat_members, welcome))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
