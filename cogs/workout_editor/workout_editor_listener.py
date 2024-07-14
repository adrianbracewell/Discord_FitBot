import disnake
from disnake.ext import commands
import utils.functions as util_func
from .add_exercise_modal import AddExerciseModal
from .update_exercise_modal import UpdateExerciseModal
from .replace_exercise_modal import ReplaceExerciseModal
from classes.fitness_program import FitnessProgram

workout_exercise_dict = {}


class WorkoutEditorListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in [
            "Add Exercise",
            "Edit Exercises",
            "Remove Exercise",
            "Edit Workouts",
            "Update Exercise",
            "Change Exercise Order",
            "Replace Exercise",
        ]:
            return

        if inter.component.custom_id == "Add Exercise":
            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["workout_day"]
            )[0]

            await inter.response.send_modal(
                AddExerciseModal(bot=self.bot, program_id=program_id)
            )
        elif inter.component.custom_id == "Update Exercise":
            await inter.response.defer(ephemeral=True)

            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            exercise_cycle_day = util_func.get_embed_info(
                message=inter.message, embed_properties=["workout_day"]
            )[0]
            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=exercise_cycle_day,
            )

            button_exercise_options = []
            for exercise in fitness_program.exercises:
                button = disnake.ui.Button(
                    label=exercise.exercise_name,
                    style=disnake.ButtonStyle.secondary,
                    custom_id=exercise.exercise_name,
                )
                button_exercise_options.append(button)

            exercise_menu = await inter.followup.send(
                content="Select an exercise to update:",
                components=button_exercise_options,
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            selected_exercise = interaction.data.custom_id

            for exercise in fitness_program.exercises:
                if exercise.exercise_name == selected_exercise:
                    exercise_obj = exercise
                    break

            if exercise_obj:
                exercise_id = exercise_obj.exercise_id
                sets = exercise_obj.sets
                reps = exercise_obj.reps

            await exercise_menu.delete()
            await interaction.response.send_modal(
                UpdateExerciseModal(
                    bot=self.bot,
                    program_id=program_id,
                    workout_day=exercise_cycle_day,
                    exercise_id=exercise_id,
                    exercise_name=exercise_obj.exercise_name,
                    reps=reps,
                    sets=sets,
                    action="update",
                )
            )

        elif inter.component.custom_id == "Remove Exercise":
            await inter.response.defer(ephemeral=True)

            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            exercise_cycle_day = util_func.get_embed_info(
                message=inter.message, embed_properties=["workout_day"]
            )[0]
            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=exercise_cycle_day,
            )
            exercise_options = {}
            for exercise in fitness_program.exercises:
                exercise_options.update(exercise.programmed_exercise_dict)
            print(exercise_options)

            menu_content = await util_func.dropdown(
                choices=list(exercise_options.keys()),
                min_choices=1,
            )
            message_menu = await inter.followup.send(
                "Select an exercise you wish to remove from the program:",
                components=menu_content,
                ephemeral=True,
            )
            exercise_to_remove = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            exercise_id = exercise_options[exercise_to_remove]["id"]

            exercise_order = exercise_options[exercise_to_remove][
                "session_order"
            ]
            print(exercise_order)
            components = [
                disnake.ui.Button(
                    label="Yes",
                    style=disnake.ButtonStyle.success,
                    custom_id="Yes",
                ),
                disnake.ui.Button(
                    label="No", style=disnake.ButtonStyle.danger, custom_id="No"
                ),
            ]

            exercise_menu = await inter.followup.send(
                content="Are you sure you want to remove this exercise from the program?",
                components=components,
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            confirm_removal = interaction.data.custom_id
            await exercise_menu.delete()

            if confirm_removal == "No":
                pass
            else:
                sql = """DELETE FROM program_exercises WHERE program_id = %s AND exercise_id = %s AND exercise_cycle_day = %s"""

                val = (program_id, exercise_id, exercise_cycle_day)

                self.bot.cursor.execute(sql, val)
                self.bot.db.commit()

                sql = """ UPDATE program_exercises
                            SET exercise_order = exercise_order - 1
                            WHERE program_id = %s
                            AND exercise_order > %s"""

                val = (program_id, exercise_order)

                self.bot.cursor.execute(sql, val)
                self.bot.db.commit()

                message, embed = await util_func.update_workout_embed(
                    inter=inter,
                    channel=inter.channel,
                    bot=self.bot,
                    exercise_cycle_day=exercise_cycle_day,
                    program_id=program_id,
                )

                await message.edit(embed=embed)

                await inter.followup.send(
                    "Order successfully updated.",
                    ephemeral=True,
                    delete_after=3,
                )

        elif inter.component.custom_id == "Replace Exercise":
            await inter.response.defer(ephemeral=True)

            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            exercise_cycle_day = util_func.get_embed_info(
                message=inter.message, embed_properties=["workout_day"]
            )[0]
            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=exercise_cycle_day,
            )
            exercise_options = {}
            for exercise in fitness_program.exercises:
                exercise_options.update(exercise.programmed_exercise_dict)
            print(exercise_options)

            menu_content = await util_func.dropdown(
                choices=list(exercise_options.keys()),
                min_choices=1,
            )
            message_menu = await inter.followup.send(
                "Select an exercise you wish to replace:",
                components=menu_content,
                ephemeral=True,
            )
            exercise_to_remove = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            exercise_id = exercise_options[exercise_to_remove]["id"]

            exercise_order = exercise_options[exercise_to_remove][
                "session_order"
            ]
            print(exercise_order)

            components = [
                disnake.ui.Button(
                    label="Yes",
                    style=disnake.ButtonStyle.success,
                    custom_id="Yes",
                ),
                disnake.ui.Button(
                    label="No", style=disnake.ButtonStyle.danger, custom_id="No"
                ),
            ]

            exercise_menu = await inter.followup.send(
                content="Are you sure you want to remove this exercise from the program?",
                components=components,
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            confirm_removal = interaction.data.custom_id
            await exercise_menu.delete()

            if confirm_removal == "No":
                pass
            else:

                sql = """DELETE FROM program_exercises WHERE program_id = %s AND exercise_id = %s AND exercise_cycle_day = %s"""

                val = (program_id, exercise_id, exercise_cycle_day)

                self.bot.cursor.execute(sql, val)
                self.bot.db.commit()

                sql = """ UPDATE program_exercises
                            SET exercise_order = exercise_order - 1
                            WHERE program_id = %s
                            AND exercise_order > %s"""

                val = (program_id, exercise_order)

                self.bot.cursor.execute(sql, val)
                self.bot.db.commit()

                await interaction.response.send_modal(
                    ReplaceExerciseModal(
                        bot=self.bot,
                        program_id=program_id,
                        workout_day=exercise_cycle_day,
                        exercise_id=None,
                        exercise_name=None,
                        sets=None,
                        reps=None,
                        action="replace",
                    )
                )

        elif inter.component.custom_id == "Change Exercise Order":
            await inter.response.defer(ephemeral=True)

            program_id = util_func.get_embed_info(
                message=inter.message, embed_properties=["program_id"]
            )[0]
            exercise_cycle_day = util_func.get_embed_info(
                message=inter.message, embed_properties=["workout_day"]
            )[0]

            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=exercise_cycle_day,
            )

            exercise_options = {}
            for exercise in fitness_program.exercises:
                exercise_options.update(exercise.programmed_exercise_dict)

            menu_content = await util_func.dropdown(
                choices=list(exercise_options.keys()),
                max_choices=len(list(exercise_options.keys())),
                min_choices=len(list(exercise_options.keys())),
            )
            message_menu = await inter.followup.send(
                "Select exercises in the order you would like them to appear:",
                components=menu_content,
                ephemeral=True,
            )
            selected_exercise_order: list = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu, return_list=True
            )
            await message_menu.delete()
            print(selected_exercise_order)

            for exercise_name in selected_exercise_order:
                self.bot.cursor.execute(
                    f"""UPDATE program_exercises
                                    SET exercise_order = {selected_exercise_order.index(exercise_name)+1}
                                    WHERE program_id = '{program_id}'
                                    AND exercise_id = '{exercise_options[exercise_name]['id']}'
                                    AND exercise_cycle_day = '{exercise_cycle_day}'
                                                            """
                )
            self.bot.db.commit()

            message, embed = await util_func.update_workout_embed(
                inter=inter,
                channel=inter.channel,
                bot=self.bot,
                exercise_cycle_day=exercise_cycle_day,
                program_id=program_id,
            )

            await message.edit(embed=embed)

            await inter.followup.send(
                "Order successfully updated.", ephemeral=True, delete_after=3
            )


def setup(bot):
    bot.add_cog(WorkoutEditorListener(bot))
