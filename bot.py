import os
from pyrogram import Client, filters
#from pyrogram.types import ChatMemberAdministrator, ChatMemberOwner
from pyrogram.errors import RPCError

# Initialize the bot
api_id = "12799559"  # Replace with your API ID
api_hash = "077254e69d93d08357f25bb5f4504580"  # Replace with your API Hash
bot_token = "7202657465:AAEq59opThMwH-i2rLMpurRL9y1F43MgOdw"  # Replace with your bot token

app = Client("media_delete_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Function to check if the bot has admin privileges and can delete messages
media_count = {}

# Function to check if the bot has admin privileges with delete permission
async def is_bot_admin(client, chat_id):
    member = await client.get_chat_member(chat_id, "me")
    
    # Check if the bot is an admin or owner
    if member.status in ("administrator", "owner"):
        return member.privileges.can_delete_messages if hasattr(member, 'privileges') else True
    return False

# Handler for media messages
@app.on_message(filters.media)
async def handle_media(client, message):
    chat_id = message.chat.id

    # Check if bot has admin privileges in the chat
    if not await is_bot_admin(client, chat_id):
        print(f"Bot is not an admin in chat {chat_id}, can't delete messages.")
        return

    # Initialize media count for the chat if not already set
    if chat_id not in media_count:
        media_count[chat_id] = 0

    # Increment the media message count
    media_count[chat_id] += 1

    # Check if 10 media messages have been sent
    if media_count[chat_id] >= 10:
        try:
            # Delete the message
            await client.delete_messages(chat_id, message.message_id)
            print(f"Deleted media message {message.message_id} in chat {chat_id}")
        except Exception as e:
            print(f"Failed to delete message {message.message_id}: {e}")
        
        # Reset the media count
        media_count[chat_id] = 0
    else:
        print(f"Media count in chat {chat_id}: {media_count[chat_id]}")

# Start the bot
app.run()
