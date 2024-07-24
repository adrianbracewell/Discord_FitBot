import mysql.connector

import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()


USER = os.getenv("USER")
PASS = os.getenv("PASS")


cog_extensions = [
    "cogs.setup",
    "cogs.program_editor.program_editor_listener",
    "cogs.program_manager.program_manager_listener",
    "cogs.session_editor.session_editor_listener",
    "cogs.session_manager.session_manager_listener",
    "cogs.workout_manager.workout_manager_listener",
    "cogs.workout_editor.workout_editor_listener",
]


class CustomBot(commands.InteractionBot):
    def __init__(self):
        intents = disnake.Intents.all()
        intents.members = True
        intents.messages = True
        intents.message_content = True
        super().__init__(intents=intents)

        self.db = mysql.connector.connect(
            host="localhost", user=USER, password=PASS, database="discfit"
        )

        self.cursor = self.db.cursor(buffered=True)

        for extension in cog_extensions:
            self.load_extension(extension)
