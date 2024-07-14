import disnake


class WorkoutManagerButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Prior Workout",
        style=disnake.ButtonStyle.primary,
        custom_id="Prior Workout",
    )
    async def prior_workout(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Edit Exercises",
        style=disnake.ButtonStyle.primary,
        custom_id="Edit Exercises",
    )
    async def edit_exercises(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Next Workout",
        style=disnake.ButtonStyle.danger,
        custom_id="Next Workout",
    )
    async def next_workout(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return
