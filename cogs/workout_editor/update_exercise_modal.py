import disnake
import utils.functions as util_func


exercise_button_dict = {}


class UpdateExerciseModal(disnake.ui.Modal):
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

        super().__init__(
            title=f"Update Exercise - {self.exercise_name}",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):

        exercise_sets = list(inter.text_values.values())[0]
        exercise_reps = list(inter.text_values.values())[1]

        insert_info = (
            exercise_sets,
            exercise_reps,
            self.program_id,
            self.workout_day,
            self.exercise_id,
        )

        self.bot.cursor.execute(
            """UPDATE program_exercises
                SET exercise_target_sets = %s,
                    exercise_target_reps = %s
                WHERE program_id = %s
                AND exercise_cycle_day = %s
                AND exercise_id = %s""",
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
            "Workout successfully updated.", ephemeral=True, delete_after=5
        )
