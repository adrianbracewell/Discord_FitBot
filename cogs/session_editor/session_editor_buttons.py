import disnake


class SessionEditorButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        label="Log Set",
        style=disnake.ButtonStyle.primary,
        custom_id="Log Exercise Data",
    )
    async def log_exercise_data(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Change Session Exercise Order",
        style=disnake.ButtonStyle.secondary,
        custom_id="Change Session Exercise Order",
    )
    async def change_session_order(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Edit Session Info",
        style=disnake.ButtonStyle.secondary,
        custom_id="Edit Session Info",
    )
    async def edit_session_info(
        self,
        inter: disnake.ApplicationCommandInteraction,
        button: disnake.ui.Button,
    ):
        return

    @disnake.ui.button(
        label="Complete Session",
        style=disnake.ButtonStyle.success,
        custom_id="Complete Session",
    )
    async def end_session(
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
