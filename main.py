from disnake.ext import commands
from dotenv import load_dotenv
import os
import asyncio
from classes.custom_bot import CustomBot

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot: commands.InteractionBot = CustomBot()


async def main():
    await bot.start(DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
