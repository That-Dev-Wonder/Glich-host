import discord
from discord.ext import commands
import traceback
from keep_alive import keep_alive
import asyncio

# Set your bot token directly here
TOKEN = ''  # Replace with your actual bot token

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user.name}')

async def main():
    try:
        keep_alive()  # Start the Flask server to keep the bot alive
        await bot.start(TOKEN)  # Use the hardcoded token
    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
