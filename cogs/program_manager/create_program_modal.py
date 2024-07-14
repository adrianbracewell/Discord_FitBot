import disnake
import utils.functions as util_func


exercise_button_dict = {}

split_list = [
    "Bro Split",
    "Push-Pull-Legs",
    "Full Body",
    "PHAT",
    "German Volumne Training",
    "DC Training (DoggCrapp)",
    "PHUL Powerbuilding",
    "FST-7 Training",
    "Upper/Lower Split",
    "5 x 5",
    "Soviet Powerlifting",
    "Auto-Regulation",
    "Shortcut to Shred",
    "Shortcut to Size",
    "Shortcut to Stupidity",
    "John Meadows Taskmaster",
    "John Meadows Intensification",
    "YOLO",
    "Sure",
    "OK",
    "OH NO",
    "HELP",
    "SURPRISE",
    "FUNNY",
    "GHOSH",
    "Sweet",
    "Done",
]


class CreateProgramModal(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        print(self.bot)

        components = [
            disnake.ui.TextInput(
                custom_id="program_name",
                label="What is the name of your program?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                max_length=30,
            )
        ]
        super().__init__(title="Create a Program", components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        await inter.response.defer(ephemeral=True)

        program_name = list(inter.text_values.values())[0]

        menu_content = await util_func.dropdown(
            bot=self.bot, inter=inter, menu_desc="Test", choices=split_list
        )

        message_menu = await inter.followup.send(
            content="Choose a type of split:",
            components=menu_content,
            ephemeral=True,
        )
        program_split = await util_func.get_dropdown_value(
            bot=self.bot, message=message_menu
        )
        await message_menu.delete()

        dropdown = await util_func.dropdown(
            bot=self.bot,
            inter=inter,
            menu_desc="Test",
            choices=[x for x in range(1, 15)],
        )
        dropdown_message = await inter.followup.send(
            content="How many days is one microcycle for this program?",
            components=dropdown,
            ephemeral=True,
        )
        program_microcycle_length = await util_func.get_dropdown_value(
            bot=self.bot, message=message_menu
        )
        await dropdown_message.delete()

        program_insert = (
            program_name,
            program_microcycle_length,
            str(inter.author.id),
        )

        self.bot.cursor.execute(
            "INSERT INTO custom_programs (program_name, microcycle_length, user_id) VALUES (%s, %s, %s)",
            (program_insert),
        )

        self.bot.db.commit()

        await inter.followup.send(
            "Program created!", ephemeral=True, delete_after=3
        )
