import disnake
from disnake.ext import commands
import utils.functions as util_func
from classes.user import User
from classes.fitness_program import FitnessProgram
from .create_program_modal import CreateProgramModal
from cogs.program_editor.program_editor_buttons import (
    ProgramEditorButtons,
)


class ProgramManagerListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in [
            "Create Program",
            "Edit Program",
            "Delete Program",
            "My Programs",
        ]:
            return

        if inter.component.custom_id == "Create Program":
            await inter.response.send_modal(CreateProgramModal(self.bot))

        elif inter.component.custom_id == "Edit Program":
            await inter.response.defer(ephemeral=True)

            user = User(bot=self.bot, user_id=inter.user.id)

            user_programs: list[FitnessProgram] = user.programs

            if not user_programs:
                await inter.followup.send(
                    content="You have no programs to edit! Create one first.",
                    ephemeral=True,
                    delete_after=10,
                )
                return

            user_program_names = [program.name for program in user_programs]

            dropdown = await util_func.dropdown(
                choices=user_program_names,
            )
            dropdown_message = await inter.followup.send(
                content="Which program would you like to edit?",
                components=dropdown,
                ephemeral=True,
            )
            program_name = await util_func.get_dropdown_value(
                bot=self.bot, message=dropdown_message
            )
            program_id = next(
                (
                    program.program_id
                    for program in user_programs
                    if getattr(program, "name") == program_name
                ),
                None,
            )

            await dropdown_message.delete()

            program_info = util_func.display_program(
                bot=self.bot, program_id=program_id
            )

            embed = disnake.Embed(title=program_name, description=program_info)
            embed.set_author(name=f"Program ID: {program_id}")

            await inter.followup.send(embed=embed, view=ProgramEditorButtons())


def setup(bot):
    bot.add_cog(ProgramManagerListener(bot))
