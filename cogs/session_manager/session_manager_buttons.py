import disnake


class SessionManagerButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Change Program",
        style=disnake.ButtonStyle.secondary,
        custom_id="Change Program",
    )
    async def change_program_session(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="New Session",
        style=disnake.ButtonStyle.success,
        custom_id="Start Session",
    )
    async def create_session(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Edit Session",
        style=disnake.ButtonStyle.primary,
        custom_id="Edit Session",
    )
    async def edit_session(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Delete Session",
        style=disnake.ButtonStyle.danger,
        custom_id="Delete Session",
    )
    async def delete_session(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="My Sessions",
        style=disnake.ButtonStyle.secondary,
        custom_id="My Sessions",
    )
    async def my_sessions(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return
