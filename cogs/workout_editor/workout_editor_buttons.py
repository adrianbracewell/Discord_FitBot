import disnake


class WorkoutEditorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Add Exercise",
        style=disnake.ButtonStyle.secondary,
        custom_id="Add Exercise",
    )
    async def add_exercise(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Update Exercise",
        style=disnake.ButtonStyle.secondary,
        custom_id="Update Exercise",
    )
    async def update_exercise(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Replace Exercise",
        style=disnake.ButtonStyle.secondary,
        custom_id="Replace Exercise",
    )
    async def replace_exercise(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Remove Exercise",
        style=disnake.ButtonStyle.secondary,
        custom_id="Remove Exercise",
    )
    async def remove_exercise(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Change Exercise Order",
        style=disnake.ButtonStyle.secondary,
        custom_id="Change Exercise Order",
    )
    async def change_exercise_order(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return
