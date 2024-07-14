import disnake
import utils.functions as util_func
from classes.exercise import Exercise


muscle_groups = [
    "Upper Back",
    "Lower Back",
    "Lats",
    "Chest",
    "Front Deltoid",
    "Middle Deltoid",
    "Rear Deltoid",
    "Upper Traps",
    "Lower Traps",
    "Rectus Abdominis",
    "Transverse Adbominis",
    "Obliques",
    "Triceps",
    "Biceps",
    "Forearms",
    "Quadriceps",
    "Hamstrings",
    "Calves",
    "Serratus Anterior",
    "Glutes",
    "Hips",
]


async def add_new_exercise(
    bot,
    inter: disnake.MessageInteraction,
    exercise_name: str,
    return_object=False,
):
    await inter.response.defer(ephemeral=True)
    menu_content = await util_func.dropdown(
        choices=muscle_groups,
        sort_choices=False,
        max_choices=1,
    )

    nonexistent_exercise_msg = (
        "It looks this exercise has not yet been added to our database. "
        "We will add it now!\n\n"
        "What is the primary muscle group trained during this exercise?"
    )

    message_menu = await inter.followup.send(
        content=nonexistent_exercise_msg,
        components=menu_content,
        ephemeral=True,
    )
    selected_muscle_group = await util_func.get_dropdown_value(
        bot=bot, message=message_menu
    )
    await message_menu.delete()

    exercise_info_insert = (exercise_name, selected_muscle_group)

    bot.cursor.execute(
        """INSERT INTO exercises (
        name,
        muscle_group_one
        ) VALUES (%s, %s)""",
        exercise_info_insert,
    )
    bot.db.commit()

    if return_object:

        exercise_id = bot.cursor.execute(
            """SELECT exercise_id
                    FROM exercises
                    WHERE name = %s""",
            (exercise_name,),
        )

        exercise_id = util_func.sql_select_handler(
            cursor=bot.cursor,
            res=exercise_id,
            fetch_type="fetchone",
        )

        return Exercise(bot=bot, exercise_id=exercise_id)
