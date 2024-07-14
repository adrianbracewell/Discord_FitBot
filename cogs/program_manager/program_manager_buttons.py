import disnake


class ProgramManagerButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Create Program",
        style=disnake.ButtonStyle.success,
        custom_id="Create Program",
    )
    async def create_program(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Edit Program",
        style=disnake.ButtonStyle.primary,
        custom_id="Edit Program",
    )
    async def edit_program(
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
    async def delete_program(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="My Programs",
        style=disnake.ButtonStyle.secondary,
        custom_id="My Programs",
    )
    async def my_program(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return
