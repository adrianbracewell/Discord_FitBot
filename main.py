import pymongo
import logging
import disnake
from disnake.ext import commands
import mysql.connector
from dotenv import load_dotenv
import os
import asyncio

USER = os.getenv("USER")
PASS = os.getenv('PASS')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

load_dotenv()

cog_extensions = ['cogs.setup']

async def main():

    intents = disnake.Intents.all()
    intents.members = True
    intents.messages = True
    intents.message_content = True

    bot = commands.InteractionBot(intents=intents)

    db = mysql.connector.connect(
         host='localhost',
         user=USER,
         password=PASS,
         database='discfit'

    )

    bot.db = db

    cursor = db.cursor()

    bot.cursor = cursor

    bot.cursor.execute("CREATE TABLE IF NOT EXISTS users (id VARCHAR(20) PRIMARY KEY, premium VARCHAR(20))")

    bot.cursor.execute("CREATE TABLE IF NOT EXISTS exercises (exercise_id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50))")

    for extension in cog_extensions:
        bot.load_extension(extension)

    await bot.start(DISCORD_TOKEN)

if __name__=="__main__":
        asyncio.run(main())
    

