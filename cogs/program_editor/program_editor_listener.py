import disnake
from disnake.ext import commands
import utils.functions as util_func
from .program_editor_buttons import ProgramEditorButtons
from cogs.workout_editor.workout_editor_buttons import (
    WorkoutEditorButtons,
)

workout_exercise_dict = {}


class ProgramEditorListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in [
            "Edit Workouts",
        ]:
            return

        if inter.component.custom_id == "Edit Workouts":
            await inter.response.defer()
            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            # workout_days = self.bot.cursor.execute(f"""SELECT DISTINCT exercise_cycle_day
            #                                        FROM program_exercises
            #                                        WHERE program_id = '{program_id}'""")
            # workout_days = util_func.sql_select_handler(res=workout_days, bot=self.bot, fetch_type='fetchall')

            workout_days = self.bot.cursor.execute(
                f"""SELECT microcycle_length
                                                    FROM custom_programs
                                                    WHERE program_id = '{program_id}'"""
            )
            workout_days = util_func.sql_select_handler(
                res=workout_days, bot=self.bot, fetch_type="fetchall"
            )
            print(workout_days)
            workout_days = [*range(1, workout_days[0] + 1)]
            menu_content = await util_func.dropdown(
                choices=workout_days,
                sort_choices=True,
            )
            message_menu = await inter.followup.send(
                "Which workout day would you like to edit?",
                components=menu_content,
                ephemeral=True,
            )
            selected_day = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            workout_info, title = util_func.display_workout(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=selected_day,
            )
            embed = disnake.Embed(
                title=f"Day {selected_day}{title}", description=workout_info
            )
            embed.set_author(name=f"Program ID: {program_id}")

            await inter.message.edit(embed=embed, view=WorkoutEditorButtons())


def setup(bot):
    bot.add_cog(ProgramEditorListener(bot))
