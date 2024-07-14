import disnake
import utils.functions as util_func
from classes.fitness_program import FitnessProgram
from classes.exercise import Exercise


async def is_added_exercise_correct(
    bot,
    inter: disnake.MessageInteraction,
    program: FitnessProgram,
    exercise: Exercise,
    num_sets: int,
    num_reps: int,
) -> bool:

    embed = disnake.Embed(title=f"{program.name} - Add Exercise")
    embed.add_field(
        name="Exercise Name", value=exercise.exercise_name, inline=False
    )
    embed.add_field(name="# of Sets", value=num_sets, inline=False)
    embed.add_field(name="# of Reps", value=num_reps, inline=False)
    embed.set_footer(text=f"Program ID: {program.program_id}")

    menu_content = await util_func.dropdown(
        choices=["Yes", "No"],
    )
    message_menu = await inter.followup.send(
        "Does this look correct?",
        embed=embed,
        components=menu_content,
        ephemeral=True,
    )
    confirm_addition = await util_func.get_dropdown_value(
        bot=bot, message=message_menu
    )
    await message_menu.delete()

    if confirm_addition == "No":
        return False
    else:
        return True
