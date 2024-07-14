import disnake
from disnake.ext import commands
import utils.functions as util_func
from classes.fitness_program import FitnessProgram
from classes.exercise import Exercise
from .workout_editor_utils.add_new_exercise import add_new_exercise
from .workout_editor_utils.is_added_exercise_correct import (
    is_added_exercise_correct,
)


class AddExerciseModal(disnake.ui.Modal):
    def __init__(
        self,
        bot,
        program_id,
        workout_day,
        exercise_id,
        exercise_name,
        action,
        sets=None,
        reps=None,
    ):
        self.bot = bot
        self.program_id = program_id
        self.workout_day = workout_day
        self.action = action
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.sets = sets
        self.reps = reps

        components = [
            disnake.ui.TextInput(
                custom_id="exercise_name",
                label="What is the name of this exercise?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                max_length=30,
            ),
            disnake.ui.TextInput(
                custom_id="exercise_sets",
                label="How many sets?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                value=sets,
                max_length=3,
            ),
            disnake.ui.TextInput(
                custom_id="exercise_reps",
                label="How many reps per set?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                value=reps,
                max_length=3,
            ),
        ]

        super().__init__(title="Add Exercise", components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        await inter.response.defer(ephemeral=True)

        exercise_name = list(inter.text_values.values())[0].title()
        exercise_sets = list(inter.text_values.values())[1]
        exercise_reps = list(inter.text_values.values())[2]

        exercise_name_matches = util_func.levenshtein_distance(
            bot=self.bot,
            word_to_match=exercise_name,
            tbl_name="exercises",
            col_name="name",
            constraint_col_name=None,
            constraint_col_val=None,
        )

        if not exercise_name_matches:

            exercise: Exercise = await add_new_exercise(
                bot=self.bot,
                inter=inter,
                exercise_name=exercise_name,
                return_object=True,
            )

        else:
            button_exercise_options = []
            for i, exercise in enumerate(exercise_name_matches):
                button_component = disnake.ui.Button(
                    label=exercise,
                    style=disnake.ButtonStyle.secondary,
                    row=i + 1,
                    custom_id=exercise,
                )
                button_exercise_options.append(button_component)

            exercise_check = await inter.followup.send(
                content="Did you mean one of these exercises?",
                components=button_exercise_options,
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )

            exercise_name = interaction.data.custom_id

            await exercise_check.delete()

            exercise = Exercise(bot=self.bot, exercise_name=exercise_name)

        program = FitnessProgram(
            bot=self.bot,
            program_id=self.program_id,
            exercise_cycle_day=self.workout_day,
        )

        correct_addition = await is_added_exercise_correct(
            bot=self.bot,
            inter=inter,
            program=program,
            exercise=exercise,
            num_sets=exercise_sets,
            num_reps=exercise_reps,
        )

        if not correct_addition:
            return

        cycle_day_num_exercises = len(program.exercises) + 1

        insert_info = (
            self.program_id,
            exercise.exercise_id,
            self.workout_day,
            exercise_sets,
            exercise_reps,
            cycle_day_num_exercises,
        )
        self.bot.cursor.execute(
            """INSERT INTO program_exercises (
            program_id,
            exercise_id,
            exercise_cycle_day,
            exercise_target_sets,
            exercise_target_reps,
            exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
            insert_info,
        )
        self.bot.db.commit()

        message_to_edit, embed = await util_func.update_workout_embed(
            inter=inter,
            bot=self.bot,
            channel=inter.channel,
            exercise_cycle_day=self.workout_day,
            program_id=self.program_id,
        )

        await message_to_edit.edit(embed=embed)

        await inter.followup.send(
            "Exercise successfully added.",
            ephemeral=True,
            delete_after=5,
        )
