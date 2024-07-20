import disnake
from disnake.ext import commands
import utils.functions as util_func
from classes.fitness_program import FitnessProgram
from classes.programmed_exercise import ProgrammedExercise
from classes.session_exercise import SessionExercise
from .log_set_modal import SessionLogModal
from .edit_set_modal import EditSetModal


workout_exercise_dict = {}


class SessionEditorListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in [
            "Log Exercise Data",
            "Complete Session",
            "Edit Session",
        ]:
            return

        if inter.component.custom_id == "Log Exercise Data":
            await inter.response.defer(ephemeral=True)

            program_info = util_func.get_embed_info(
                message=inter.message,
                embed_properties=["program_id", "workout_day", "session_id"],
            )
            program_id = program_info[0]
            exercise_cycle_day = program_info[1]
            session_id = program_info[2]

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

            embed = disnake.Embed(
                title=f"Day {exercise_cycle_day} - Log Exercise Data",
                description="Choose an option below:",
            )
            embed.set_author(
                name=f"Program ID: {program_id}\nSession ID: {session_id}"
            )

            exercise_menu = await inter.followup.send(
                embed=embed, components=button_exercise_options
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            selected_exercise = interaction.data.custom_id

            for exercise in fitness_program.exercises:
                if exercise.exercise_name == selected_exercise:
                    exercise_obj: ProgrammedExercise = exercise
                    break

            if exercise_obj:

                exercise_id = exercise_obj.exercise_id
                session_exercise = SessionExercise(
                    bot=self.bot,
                    session_id=session_id,
                    exercise_id=exercise_id,
                    program_id=program_id,
                    exercise_cycle_day=exercise_cycle_day,
                )
                programmed_sets = session_exercise.sets
                programmed_reps = session_exercise.reps
                session_set_info = session_exercise.session_set_info
                session_last_set = session_exercise.current_set_count
                session_current_set = session_last_set + 1
                last_session_info = session_exercise.last_session_info
                print(
                    programmed_sets,
                    programmed_reps,
                    session_last_set,
                    session_set_info,
                    last_session_info,
                )

            if programmed_sets != session_last_set:
                await exercise_menu.delete()
                await interaction.response.send_modal(
                    SessionLogModal(
                        bot=self.bot,
                        program_id=program_id,
                        session_id=session_id,
                        exercise_id=exercise_id,
                        exercise_name=exercise_obj.exercise_name,
                        target_reps=programmed_reps,
                        set_count=session_current_set,
                        target_sets=programmed_sets,
                        workout_day=exercise_cycle_day,
                        last_session_info=last_session_info,
                    )
                )
            else:
                components = [
                    disnake.ui.Button(
                        label="Yes",
                        style=disnake.ButtonStyle.success,
                        custom_id="Yes",
                    ),
                    disnake.ui.Button(
                        label="No",
                        style=disnake.ButtonStyle.danger,
                        custom_id="No",
                    ),
                ]

                add_set_menu = await inter.followup.send(
                    content=f"You have already completed the {programmed_sets} sets programmed for the **{exercise_obj.exercise_name}**. Do you want to do another set of this exercise for this session?",
                    components=components,
                )

                interaction: disnake.MessageInteraction = (
                    await self.bot.wait_for("button_click", check=check)
                )

                add_set = interaction.data.custom_id
                await exercise_menu.delete()

                await add_set_menu.delete()

                if add_set == "No":
                    pass
                else:
                    await interaction.response.send_modal(
                        SessionLogModal(
                            bot=self.bot,
                            program_id=program_id,
                            session_id=session_id,
                            exercise_id=exercise_id,
                            exercise_name=exercise_obj.exercise_name,
                            target_reps=programmed_reps,
                            set_count=session_current_set,
                            target_sets=programmed_sets,
                            workout_day=exercise_cycle_day,
                            last_session_info=last_session_info,
                        )
                    )

        elif inter.component.custom_id == "Complete Session":
            await inter.response.defer(ephemeral=True)

            program_info = util_func.get_embed_info(
                message=inter.message,
                embed_properties=["program_id", "workout_day", "session_id"],
            )
            program_id = program_info[0]
            exercise_cycle_day = program_info[1]
            session_id = program_info[2]

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
                content="Are you sure you want to mark this session as complete?",
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
                return

            query = """UPDATE sessions SET active = 0 WHERE session_id = %s"""
            val = (session_id,)
            self.bot.cursor.execute(query, val)
            self.bot.db.commit()

            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=exercise_cycle_day,
            )

            await inter.message.delete()

            await inter.followup.send(
                "Session marked complete!", ephemeral=True, delete_after=3
            )

        elif inter.component.custom_id == "Edit Session":
            await inter.response.defer(ephemeral=True)

            program_info = util_func.get_embed_info(
                message=inter.message,
                embed_properties=["program_id", "workout_day", "session_id"],
            )
            program_id = program_info[0]
            exercise_cycle_day = program_info[1]
            session_id = program_info[2]

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

            embed = disnake.Embed(
                title=f"Day {exercise_cycle_day} - Edit Session",
                description="Which session exercise would you like to edit?",
            )
            embed.set_author(
                name=f"Program ID: {program_id}\nSession ID: {session_id}"
            )

            exercise_menu = await inter.followup.send(
                embed=embed, components=button_exercise_options, ephemeral=True
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            selected_exercise = interaction.data.custom_id

            await exercise_menu.delete()

            for exercise in fitness_program.exercises:
                if exercise.exercise_name == selected_exercise:
                    exercise_obj: ProgrammedExercise = exercise
                    break

            if not exercise_obj:
                return

            exercise_id = exercise_obj.exercise_id
            session_exercise = SessionExercise(
                bot=self.bot,
                session_id=session_id,
                exercise_id=exercise_id,
                program_id=program_id,
                exercise_cycle_day=exercise_cycle_day,
            )
            session_set_info = session_exercise.session_set_info
            session_last_set = session_exercise.current_set_count
            session_current_set = session_last_set + 1

            choices = ["Edit a Set", "Delete Set"]

            dropdown = await util_func.dropdown(choices=choices)

            dropdown_message = await inter.followup.send(
                content="Choose an option:",
                components=dropdown,
                ephemeral=True,
            )
            edit_session_action = await util_func.get_dropdown_value(
                bot=self.bot, message=dropdown_message
            )
            await dropdown_message.delete()

            set_button_options = []
            for session_set in list(session_set_info.keys()):
                session_reps = session_set_info[session_set]["set_reps"]
                session_load = session_set_info[session_set]["set_load"]
                label = f"Set {session_set} -> {session_reps} reps @ {session_load}lbs"
                button = disnake.ui.Button(
                    label=label,
                    style=disnake.ButtonStyle.secondary,
                    custom_id=session_set,
                )
                set_button_options.append(button)

            if edit_session_action == "Edit a Set":
                title_action = "Edit"
            else:
                title_action = "Delete"

            embed = disnake.Embed(
                title=f"Day {exercise_cycle_day} - {title_action} {selected_exercise} Set",
                description="Choose a set:",
            )
            embed.set_author(
                name=f"Program ID: {program_id}\nSession ID: {session_id}"
            )

            exercise_menu = await inter.followup.send(
                embed=embed, components=set_button_options, ephemeral=True
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            selected_set = int(interaction.data.custom_id)

            await exercise_menu.delete()

            if edit_session_action == "Edit a Set":

                await interaction.response.send_modal(
                    EditSetModal(
                        bot=self.bot,
                        program_id=program_id,
                        session_id=session_id,
                        exercise_id=exercise_id,
                        exercise_name=exercise_obj.exercise_name,
                        set_count=selected_set,
                        workout_day=exercise_cycle_day,
                        session_load=session_set_info[selected_set]["set_load"],
                        session_reps=session_set_info[selected_set]["set_reps"],
                    )
                )

            elif edit_session_action == "Delete Set":
                query = """DELETE FROM session_exercises
                    WHERE session_id = %s
                    AND exercise_id = %s
                    AND set_order = %s"""

                val = (
                    session_id,
                    exercise_id,
                    selected_set,
                )

                self.bot.cursor.execute(query, val)
                self.bot.db.commit()

                query = """ UPDATE session_exercises
                            SET set_order = set_order - 1
                            WHERE session_id = %s
                            AND exercise_id = %s
                            AND set_order > %s"""

                self.bot.cursor.execute(query, val)

                self.bot.db.commit()

                message, embed = await util_func.update_session_embed(
                    inter=inter,
                    bot=self.bot,
                    exercise_cycle_day=exercise_cycle_day,
                    program_id=program_id,
                    session_id=session_id,
                )

                await message.edit(embed=embed)

                await inter.followup.send(
                    f"Set {selected_set} deleted for {selected_exercise}.",
                    ephemeral=True,
                    delete_after=3,
                )


def setup(bot):
    bot.add_cog(SessionEditorListener(bot))
