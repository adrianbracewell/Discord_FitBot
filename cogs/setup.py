import disnake
from disnake.ext import commands
import re
from cogs.program_manager.program_manager_buttons import (
    ProgramManagerButtons,
)
from cogs.session_manager.session_manager_buttons import (
    SessionManagerButtons,
)


class SetupBot(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Automatic Setup (Recommended)",
        style=disnake.ButtonStyle.primary,
        custom_id="Auto Setup",
    )
    async def auto_setup_button(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Custom Setup",
        style=disnake.ButtonStyle.secondary,
        custom_id="Custom Setup",
    )
    async def custom_setup_button(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return


class SetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="setup")
    async def setup(self, inter: disnake.ApplicationCommandInteraction):

        # embed_account_overview = disnake.Embed(title='', description='Welcome to setup')

        try:

            self.bot.cursor.execute(
                "INSERT INTO users (id, premium) VALUES (%s, %s)",
                (str(inter.author.id), "0"),
            )

            self.bot.db.commit()
            await inter.response.send_message(
                "Choose a setup option:", view=SetupBot()
            )

        except:
            await inter.response.send_message(
                "You have already set up the bot."
            )

    @commands.slash_command(name="delete_all_users")
    async def delete_setup(self, inter: disnake.ApplicationCommandInteraction):

        # embed_account_overview = disnake.Embed(title='', description='Welcome to setup')

        try:

            self.bot.cursor.execute("DELETE FROM users")

            self.bot.db.commit()
            await inter.response.send_message(
                "Choose a setup option:", view=SetupBot()
            )

        except:
            await inter.response.send_message(
                "You have already set up the bot."
            )

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in ["Auto Setup", "Custom Setup"]:
            return

        if inter.component.custom_id == "Auto Setup":
            await inter.response.defer(ephemeral=True)
            member_overwrite = disnake.PermissionOverwrite(
                view_channel=True, send_messages=True
            )
            overwrite_dict = {inter.user: member_overwrite}
            category = await inter.guild.create_category(
                "Training", overwrites=overwrite_dict, position=0
            )
            program_creator_channel = await inter.guild.create_text_channel(
                name="program creator",
                category=category,
                position=0,
                overwrites=overwrite_dict,
            )
            session_manager_channel = await inter.guild.create_text_channel(
                name="session manager",
                category=category,
                position=1,
                overwrites=overwrite_dict,
            )

            program_embed = disnake.Embed(title="Program Creator")
            session_embed = disnake.Embed(title="Session Manager")
            await program_creator_channel.send(
                embed=program_embed, view=ProgramManagerButtons()
            )

            await session_manager_channel.send(
                embed=session_embed, view=SessionManagerButtons()
            )

            await inter.followup.send("Setup successful.", ephemeral=True)

        elif inter.component.custom_id == "Custom Setup":
            pass


def setup(bot):
    bot.add_cog(SetupCommands(bot))
