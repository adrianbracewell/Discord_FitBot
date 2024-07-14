import disnake
import utils.functions as util_func


class SessionLogModal(disnake.ui.Modal):
    def __init__(
        self,
        bot,
        program_id,
        exercise_id,
        session_id,
        exercise_name,
        target_sets,
        target_reps,
        set_count,
        workout_day,
        last_session_info=None,
    ):
        self.bot = bot
        self.program_id = program_id
        self.session_id = session_id
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.target_sets = target_sets
        self.target_reps = target_reps
        self.set_count = set_count
        self.workout_day = workout_day
        self.last_session_info = last_session_info

        if last_session_info:
            last_session_set_weight = last_session_info[self.set_count][
                "past_set_load"
            ]
            last_session_set_reps = last_session_info[self.set_count][
                "past_set_reps"
            ]
            weight_label = f"Weight [Last Session: {last_session_set_weight}]"
            reps_label = f"Number of Reps Completed [Last Session: {last_session_set_reps}]"
        else:
            weight_label = f"Weight"
            reps_label = f"Number of Reps Completed [Goal: {self.target_reps}]"

        components = [
            disnake.ui.TextInput(
                custom_id="exercise_amount",
                label=weight_label,
                placeholder="-",
                style=disnake.TextInputStyle.short,
                max_length=4,
            ),
            disnake.ui.TextInput(
                custom_id="exercise_reps",
                label=reps_label,
                placeholder="-",
                style=disnake.TextInputStyle.short,
                max_length=3,
            ),
        ]
        title = (
            f"{self.exercise_name} - Set {self.set_count}/{self.target_sets}"
        )

        super().__init__(title=title, components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        await inter.response.defer(ephemeral=True)
        # print(inter.user.name)

        exercise_load_amount = int(list(inter.text_values.values())[0])
        exercise_rep_count = int(list(inter.text_values.values())[1])

        insert_info = (
            self.session_id,
            self.exercise_id,
            exercise_rep_count,
            exercise_load_amount,
            self.set_count,
        )

        self.bot.cursor.execute(
            """INSERT INTO session_exercises (
                                session_id,
                                exercise_id,
                                reps,
                                amount,
                                set_order) VALUES (%s, %s, %s, %s, %s)""",
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
            "Exercise successfully added.", ephemeral=True, delete_after=5
        )
