import disnake


class ProgramEditorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Edit Program Type",
        style=disnake.ButtonStyle.secondary,
        custom_id="Edit Program Type",
    )
    async def add_to_program(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Edit Workouts",
        style=disnake.ButtonStyle.secondary,
        custom_id="Edit Workouts",
    )
    async def edit_prog_workouts(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Delete Program",
        style=disnake.ButtonStyle.danger,
        custom_id="Delete Program",
    )
    async def update_program(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return
