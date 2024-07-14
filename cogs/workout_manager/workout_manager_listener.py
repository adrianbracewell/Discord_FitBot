import disnake
from disnake.ext import commands
import utils.functions as util_func
from .workout_manager_buttons import WorkoutManagerButtons

workout_exercise_dict = {}


class WorkoutManagerListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in [
            "Edit Exercises",
        ]:
            return

        if inter.component.custom_id == "Edit Exercises":

            program_info = util_func.get_embed_info(
                message=inter.message,
                embed_properties=["program_id", "workout_day"],
            )

            embed = disnake.Embed(
                title=f"Day {program_info[1]} - Edit Exercises",
                description="Choose an option below:",
            )
            embed.set_author(name=f"Program ID: {program_info[0]}")
            await inter.response.send_message(
                embed=embed, view=WorkoutManagerButtons(), ephemeral=True
            )
        elif inter.component.custom_id == "Add Exercise":
            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["workout_day"]
            )[0]

            await inter.response.send_modal(
                ExerciseModal(bot=self.bot, program_id=program_id)
            )


def setup(bot):
    bot.add_cog(WorkoutManagerListener(bot))
