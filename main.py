import os
import requests
from PIL import Image, ImageDraw, ImageFont
import pyrogram
from pyrogram import Client, filters


API_ID = 15849735 # Your API ID
API_HASH = 'b8105dc4c17419dfd4165ecf1d0bc100' # Your API Hash
BOT_TOKEN = '6145559264:AAEkUH_znhpaTdkbnndwP1Vy2ppv-C9Zf4o'

# Create a Pyrogram client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the font for the welcome message
font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf' # Path to your custom font file
font_size = 70
font_color = (255, 255, 255)
font = ImageFont.truetype(font_path, font_size)

# Define the welcome image URL
image_url = 'https://i.postimg.cc/Hsggt1hn/photo-2023-03-20-01-40-46-7212352388177380352.png'

def generate_welcome_image(name, username, user_id):
    # Download the welcome image
    response = requests.get(image_url)
    with Image.open(requests.get(image_url, stream=True).raw) as image:
        # Open the image and add the text
        draw = ImageDraw.Draw(image)
        draw.text((120, 250), f'Welcome {name}!', fill=font_color, font=font)
        draw.text((120, 350), f'Username: @{username}', fill=font_color, font=font)
        draw.text((120, 450), f'ID: {user_id}', fill=font_color, font=font)

        # Save the modified image
        modified_image_path = 'images/welcome_modified.jpg'
        image.save(modified_image_path)
        
        return modified_image_path
@app.on_message(filters.new_chat_members)
def handle_new_chat_members(client, message):
    user = message.new_chat_members[0]
    name = user.first_name
    username = user.username
    user_id = user.id

    # Generate the welcome image
    modified_image_path = generate_welcome_image(name, username, user_id)

    # Send the modified image as a reply to the welcome message
    with open(modified_image_path, 'rb') as f:
        client.send_photo(chat_id=message.chat.id, photo=f)

@app.on_message(filters.command('start'))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hello! I'm a welcome bot.")

# Start the client
app.run()
