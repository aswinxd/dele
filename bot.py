import os
from pyrogram import Client, filters

# Initialize the bot
api_id = "YOUR_API_ID"  # Replace with your API ID
api_hash = "YOUR_API_HASH"  # Replace with your API Hash
bot_token = "YOUR_BOT_TOKEN"  # Replace with your bot token

app = Client("media_delete_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Dictionary to keep track of media messages count per chat
media_count = {}

# Function to check if the message contains media
def is_media(message):
    return message.photo or message.video or message.document or message.audio or message.voice or message.animation

# Handler for media messages
@app.on_message(filters.media)
def handle_media(client, message):
    chat_id = message.chat.id
    
    # Initialize media count for the chat if not already set
    if chat_id not in media_count:
        media_count[chat_id] = 0
    
    # Increment the media message count
    media_count[chat_id] += 1

    # Check if 10 media messages have been sent
    if media_count[chat_id] >= 10:
        # Delete the message
        app.delete_messages(chat_id, message.message_id)
        # Reset the media count
        media_count[chat_id] = 0

    print(f"Media count in chat {chat_id}: {media_count[chat_id]}")

# Start the bot
app.run()
