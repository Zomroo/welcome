import os
import requests
from PIL import Image, ImageDraw, ImageFont
import pyrogram

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
FONT_NAME = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

# Define the font for the welcome message
font = ImageFont.truetype(FONT_NAME, 40)

app = pyrogram.Client('my_bot', bot_token=TOKEN)

def welcome(client, message):
    bot = client
    user = message.new_chat_members[0]
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
            bot.send_photo(chat_id=message.chat.id, photo=f)

def start(client, message):
    bot = client
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id, text="Hello! I'm a welcome bot.")

@app.on_message()
def message_handler(client, message):
    if message.new_chat_members:
        welcome(client, message)
    else:
        start(client, message)

if __name__ == '__main__':
    app.run()
