import disnake
import utils.functions as util_func


class EditSetModal(disnake.ui.Modal):
    def __init__(
        self,
        bot,
        program_id,
        exercise_id,
        session_id,
        exercise_name,
        set_count,
        workout_day,
        session_reps,
        session_load,
    ):
        self.bot = bot
        self.program_id = program_id
        self.session_id = session_id
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.set_count = set_count
        self.workout_day = workout_day
        self.session_reps = session_reps
        self.session_load = session_load

        components = [
            disnake.ui.TextInput(
                custom_id="set_weight",
                label="Weight",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                value=self.session_load,
                max_length=4,
            ),
            disnake.ui.TextInput(
                custom_id="exercise_reps",
                label="Number of Reps Completed",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                value=self.session_reps,
                max_length=3,
            ),
        ]
        title = f"{self.exercise_name} - Edit Set {self.set_count}"

        super().__init__(title=title, components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        await inter.response.defer(ephemeral=True)
        # print(inter.user.name)

        exercise_load_amount = int(list(inter.text_values.values())[0])
        exercise_rep_count = int(list(inter.text_values.values())[1])

        insert_info = (
            exercise_load_amount,
            exercise_rep_count,
            self.session_id,
            self.exercise_id,
            self.set_count,
        )

        self.bot.cursor.execute(
            """UPDATE session_exercises
            SET amount = %s,
                reps = %s
            WHERE session_id = %s
            AND exercise_id = %s
            AND set_order = %s""",
            insert_info,
        )
        self.bot.db.commit()

        message, embed = await util_func.update_session_embed(
            inter=inter,
            bot=self.bot,
            exercise_cycle_day=self.workout_day,
            program_id=self.program_id,
            session_id=self.session_id,
        )

        await message.edit(embed=embed)

        await inter.followup.send(
            f"Set data for {self.exercise_name} updated.",
            ephemeral=True,
            delete_after=5,
        )
