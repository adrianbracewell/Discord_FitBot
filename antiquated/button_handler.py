# import disnake
# from disnake.ext import commands
# from utils.modal_handler import (
#     ProgramManagerModal,
#     ExerciseModal,
#     SessionLogModal,
# )
# import utils.functions as util_func
# from datetime import datetime

# workout_exercise_dict = {}


# class ProgramManager(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(
#         label="Create Program",
#         style=disnake.ButtonStyle.success,
#         custom_id="Create Program",
#     )
#     async def create_program(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Edit Program",
#         style=disnake.ButtonStyle.primary,
#         custom_id="Edit Program",
#     )
#     async def edit_program(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Delete Program",
#         style=disnake.ButtonStyle.danger,
#         custom_id="Delete Program",
#     )
#     async def delete_program(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="My Programs",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="My Programs",
#     )
#     async def my_program(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return


# class SessionManager(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(
#         label="Change Program",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Change Program",
#     )
#     async def change_program_session(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="New Session",
#         style=disnake.ButtonStyle.success,
#         custom_id="Start Session",
#     )
#     async def create_session(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Edit Session",
#         style=disnake.ButtonStyle.primary,
#         custom_id="Edit Session",
#     )
#     async def edit_session(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Delete Session",
#         style=disnake.ButtonStyle.danger,
#         custom_id="Delete Session",
#     )
#     async def delete_session(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="My Sessions",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="My Sessions",
#     )
#     async def my_sessions(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return


# class ProgramEditor(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(
#         label="Edit Program Type",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Edit Program Type",
#     )
#     async def add_to_program(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Edit Workouts",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Edit Workouts",
#     )
#     async def edit_prog_workouts(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Delete Program",
#         style=disnake.ButtonStyle.danger,
#         custom_id="Delete Program",
#     )
#     async def update_program(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return


# class SessionEditor(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(
#         label="Log Set",
#         style=disnake.ButtonStyle.primary,
#         custom_id="Log Exercise Data",
#     )
#     async def log_exercise_data(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Change Session Exercise Order",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Change Session Exercise Order",
#     )
#     async def change_session_order(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Edit Session Info",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Edit Session Info",
#     )
#     async def edit_session_info(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Complete Session",
#         style=disnake.ButtonStyle.success,
#         custom_id="Complete Session",
#     )
#     async def end_session(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Delete Session",
#         style=disnake.ButtonStyle.danger,
#         custom_id="Delete Session",
#     )
#     async def delete_session(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return


# class WorkoutEditor(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(
#         label="Prior Workout",
#         style=disnake.ButtonStyle.primary,
#         custom_id="Prior Workout",
#     )
#     async def prior_workout(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Edit Exercises",
#         style=disnake.ButtonStyle.primary,
#         custom_id="Edit Exercises",
#     )
#     async def edit_exercises(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Next Workout",
#         style=disnake.ButtonStyle.danger,
#         custom_id="Next Workout",
#     )
#     async def next_workout(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return


# class ExercisesEditor(disnake.ui.View):
#     def __init__(self):
#         super().__init__(timeout=None)

#     @disnake.ui.button(
#         label="Add Exercise",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Add Exercise",
#     )
#     async def add_exercise(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Update Exercise",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Update Exercise",
#     )
#     async def update_exercise(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Replace Exercise",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Replace Exercise",
#     )
#     async def replace_exercise(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Remove Exercise",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Remove Exercise",
#     )
#     async def remove_exercise(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return

#     @disnake.ui.button(
#         label="Change Exercise Order",
#         style=disnake.ButtonStyle.secondary,
#         custom_id="Change Exercise Order",
#     )
#     async def change_exercise_order(
#         self,
#         inter: disnake.ApplicationCommandInteraction,
#         button: disnake.ui.Button,
#     ):
#         return


# class EmbedButtons(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.Cog.listener("on_button_click")
#     async def help_listener(self, inter: disnake.MessageInteraction):
#         if inter.component.custom_id not in [
#             "Create Program",
#             "Edit Program",
#             "Delete Program",
#             "My Programs",
#             "Add Exercise",
#             "Edit Exercises",
#             "Remove Exercise",
#             "Edit Workouts",
#             "Update Exercise",
#             "Change Exercise Order",
#             "Replace Exercise",
#             "Start Session",
#             "Edit Session",
#             "Delete Session",
#             "My Sessions",
#             "Change Program",
#             "Log Exercise Data",
#             "Mark Rest Day",
#             "Complete Session",
#         ]:
#             return

#         if inter.component.custom_id == "Create Program":
#             await inter.response.send_modal(ProgramManagerModal(self.bot))

#         elif inter.component.custom_id == "Edit Program":
#             await inter.response.defer()

#             programs = self.bot.cursor.execute(
#                 f"""SELECT program_id, program_name
#                                     FROM custom_programs
#                                     WHERE user_id = '{inter.author.id}'"""
#             )

#             programs = util_func.sql_select_handler(
#                 res=programs, bot=self.bot, fetch_type="fetchall"
#             )
#             program_dict = util_func.detupler_to_dict(programs)
#             print(program_dict)

#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Program",
#                 choices=list(program_dict.values()),
#             )
#             message_menu = await inter.followup.send(
#                 "Which program would you like to edit?",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             selected_program = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu
#             )
#             selected_program_id = util_func.key_from_value(
#                 selected_program, program_dict
#             )
#             await message_menu.delete()

#             program_info = util_func.display_program(
#                 bot=self.bot, program_id=selected_program_id
#             )

#             embed = disnake.Embed(
#                 title=selected_program, description=program_info
#             )
#             embed.set_author(name=f"Program ID: {selected_program_id}")

#             await inter.followup.send(embed=embed, view=ProgramEditor())
#         elif inter.component.custom_id == "Add Exercise":
#             program_info = util_func.get_embed_info(
#                 message=inter.message,
#                 embed_properties=["program_id", "workout_day"],
#             )

#             await inter.response.send_modal(
#                 ExerciseModal(
#                     bot=self.bot,
#                     program_id=program_info[0],
#                     workout_day=program_info[1],
#                     exercise_id=None,
#                     exercise_name=None,
#                     sets=None,
#                     reps=None,
#                     action="add",
#                 )
#             )
#         elif inter.component.custom_id == "Edit Workouts":
#             await inter.response.defer()
#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["program_id"]
#             )[0]
#             # workout_days = self.bot.cursor.execute(f"""SELECT DISTINCT exercise_cycle_day
#             #                                        FROM program_exercises
#             #                                        WHERE program_id = '{program_id}'""")
#             # workout_days = util_func.sql_select_handler(res=workout_days, bot=self.bot, fetch_type='fetchall')

#             workout_days = self.bot.cursor.execute(
#                 f"""SELECT microcycle_length
#                                                     FROM custom_programs
#                                                     WHERE program_id = '{program_id}'"""
#             )
#             workout_days = util_func.sql_select_handler(
#                 res=workout_days, bot=self.bot, fetch_type="fetchall"
#             )
#             print(workout_days)
#             workout_days = [*range(1, workout_days[0] + 1)]
#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Day:",
#                 choices=workout_days,
#                 sort_choices=True,
#             )
#             message_menu = await inter.followup.send(
#                 "Which workout day would you like to edit?",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             selected_day = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu
#             )
#             await message_menu.delete()

#             workout_info, title = util_func.display_workout(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=selected_day,
#             )
#             embed = disnake.Embed(
#                 title=f"Day {selected_day}{title}", description=workout_info
#             )
#             embed.set_author(name=f"Program ID: {program_id}")

#             await inter.message.edit(embed=embed, view=WorkoutEditor())
#         elif inter.component.custom_id == "Edit Exercises":

#             program_info = util_func.get_embed_info(
#                 message=inter.message,
#                 embed_properties=["program_id", "workout_day"],
#             )

#             embed = disnake.Embed(
#                 title=f"Day {program_info[1]} - Edit Exercises",
#                 description="Choose an option below:",
#             )
#             embed.set_author(name=f"Program ID: {program_info[0]}")
#             await inter.response.send_message(
#                 embed=embed, view=ExercisesEditor(), ephemeral=True
#             )
#         elif inter.component.custom_id == "Add Exercise":
#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["program_id"]
#             )[0]
#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["workout_day"]
#             )[0]

#             await inter.response.send_modal(
#                 ExerciseModal(bot=self.bot, program_id=program_id)
#             )
#         elif inter.component.custom_id == "Update Exercise":
#             await inter.response.defer(ephemeral=True)

#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["program_id"]
#             )[0]
#             exercise_cycle_day = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["workout_day"]
#             )[0]
#             fitness_program = FitnessProgram(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=exercise_cycle_day,
#             )

#             button_exercise_options = []
#             for exercise in fitness_program.exercises:
#                 button = disnake.ui.Button(
#                     label=exercise.exercise_name,
#                     style=disnake.ButtonStyle.secondary,
#                     custom_id=exercise.exercise_name,
#                 )
#                 button_exercise_options.append(button)

#             exercise_menu = await inter.followup.send(
#                 content="Select an exercise to update:",
#                 components=button_exercise_options,
#             )

#             def check(m):
#                 return m.channel == inter.channel

#             interaction: disnake.MessageInteraction = await self.bot.wait_for(
#                 "button_click", check=check
#             )
#             selected_exercise = interaction.data.custom_id

#             for exercise in fitness_program.exercises:
#                 if exercise.exercise_name == selected_exercise:
#                     exercise_obj = exercise
#                     break

#             if exercise_obj:
#                 exercise_id = exercise_obj.exercise_id
#                 sets = exercise_obj.sets
#                 reps = exercise_obj.reps

#             await exercise_menu.delete()
#             await interaction.response.send_modal(
#                 ExerciseModal(
#                     bot=self.bot,
#                     program_id=program_id,
#                     workout_day=exercise_cycle_day,
#                     exercise_id=exercise_id,
#                     exercise_name=exercise_obj.exercise_name,
#                     reps=reps,
#                     sets=sets,
#                     action="update",
#                 )
#             )

#         elif inter.component.custom_id == "Remove Exercise":
#             await inter.response.defer(ephemeral=True)

#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["program_id"]
#             )[0]
#             exercise_cycle_day = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["workout_day"]
#             )[0]
#             fitness_program = FitnessProgram(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=exercise_cycle_day,
#             )
#             exercise_options = {}
#             for exercise in fitness_program.exercises:
#                 exercise_options.update(exercise.programmed_exercise_dict)
#             print(exercise_options)

#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Program",
#                 choices=list(exercise_options.keys()),
#                 min_choices=1,
#             )
#             message_menu = await inter.followup.send(
#                 "Select an exercise you wish to remove from the program:",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             exercise_to_remove = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu
#             )
#             await message_menu.delete()

#             exercise_id = exercise_options[exercise_to_remove]["id"]

#             exercise_order = exercise_options[exercise_to_remove][
#                 "session_order"
#             ]
#             print(exercise_order)
#             components = [
#                 disnake.ui.Button(
#                     label="Yes",
#                     style=disnake.ButtonStyle.success,
#                     custom_id="Yes",
#                 ),
#                 disnake.ui.Button(
#                     label="No", style=disnake.ButtonStyle.danger, custom_id="No"
#                 ),
#             ]

#             exercise_menu = await inter.followup.send(
#                 content="Are you sure you want to remove this exercise from the program?",
#                 components=components,
#             )

#             def check(m):
#                 return m.channel == inter.channel

#             interaction: disnake.MessageInteraction = await self.bot.wait_for(
#                 "button_click", check=check
#             )
#             confirm_removal = interaction.data.custom_id
#             await exercise_menu.delete()

#             if confirm_removal == "No":
#                 pass
#             else:
#                 sql = """DELETE FROM program_exercises WHERE program_id = %s AND exercise_id = %s AND exercise_cycle_day = %s"""

#                 val = (program_id, exercise_id, exercise_cycle_day)

#                 self.bot.cursor.execute(sql, val)
#                 self.bot.db.commit()

#                 sql = """ UPDATE program_exercises
#                             SET exercise_order = exercise_order - 1
#                             WHERE program_id = %s
#                             AND exercise_order > %s"""

#                 val = (program_id, exercise_order)

#                 self.bot.cursor.execute(sql, val)
#                 self.bot.db.commit()

#                 message, embed = await util_func.update_workout_embed(
#                     inter=inter,
#                     channel=inter.channel,
#                     bot=self.bot,
#                     exercise_cycle_day=exercise_cycle_day,
#                     program_id=program_id,
#                 )

#                 await message.edit(embed=embed)

#                 await inter.followup.send(
#                     "Order successfully updated.",
#                     ephemeral=True,
#                     delete_after=3,
#                 )

#         elif inter.component.custom_id == "Replace Exercise":
#             await inter.response.defer(ephemeral=True)

#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["program_id"]
#             )[0]
#             exercise_cycle_day = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["workout_day"]
#             )[0]
#             fitness_program = FitnessProgram(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=exercise_cycle_day,
#             )
#             exercise_options = {}
#             for exercise in fitness_program.exercises:
#                 exercise_options.update(exercise.programmed_exercise_dict)
#             print(exercise_options)

#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Program",
#                 choices=list(exercise_options.keys()),
#                 min_choices=1,
#             )
#             message_menu = await inter.followup.send(
#                 "Select an exercise you wish to replace:",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             exercise_to_remove = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu
#             )
#             await message_menu.delete()

#             exercise_id = exercise_options[exercise_to_remove]["id"]

#             exercise_order = exercise_options[exercise_to_remove][
#                 "session_order"
#             ]
#             print(exercise_order)

#             components = [
#                 disnake.ui.Button(
#                     label="Yes",
#                     style=disnake.ButtonStyle.success,
#                     custom_id="Yes",
#                 ),
#                 disnake.ui.Button(
#                     label="No", style=disnake.ButtonStyle.danger, custom_id="No"
#                 ),
#             ]

#             exercise_menu = await inter.followup.send(
#                 content="Are you sure you want to remove this exercise from the program?",
#                 components=components,
#             )

#             def check(m):
#                 return m.channel == inter.channel

#             interaction: disnake.MessageInteraction = await self.bot.wait_for(
#                 "button_click", check=check
#             )
#             confirm_removal = interaction.data.custom_id
#             await exercise_menu.delete()

#             if confirm_removal == "No":
#                 pass
#             else:

#                 sql = """DELETE FROM program_exercises WHERE program_id = %s AND exercise_id = %s AND exercise_cycle_day = %s"""

#                 val = (program_id, exercise_id, exercise_cycle_day)

#                 self.bot.cursor.execute(sql, val)
#                 self.bot.db.commit()

#                 sql = """ UPDATE program_exercises
#                             SET exercise_order = exercise_order - 1
#                             WHERE program_id = %s
#                             AND exercise_order > %s"""

#                 val = (program_id, exercise_order)

#                 self.bot.cursor.execute(sql, val)
#                 self.bot.db.commit()

#                 await interaction.response.send_modal(
#                     ExerciseModal(
#                         bot=self.bot,
#                         program_id=program_id,
#                         workout_day=exercise_cycle_day,
#                         exercise_id=None,
#                         exercise_name=None,
#                         sets=None,
#                         reps=None,
#                         action="replace",
#                     )
#                 )

#         elif inter.component.custom_id == "Change Exercise Order":
#             await inter.response.defer(ephemeral=True)

#             program_id = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["program_id"]
#             )[0]
#             exercise_cycle_day = util_func.get_embed_info(
#                 message=inter.message, embed_properties=["workout_day"]
#             )[0]

#             fitness_program = FitnessProgram(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=exercise_cycle_day,
#             )

#             exercise_options = {}
#             for exercise in fitness_program.exercises:
#                 exercise_options.update(exercise.programmed_exercise_dict)

#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Program",
#                 choices=list(exercise_options.keys()),
#                 max_choices=len(list(exercise_options.keys())),
#                 min_choices=len(list(exercise_options.keys())),
#             )
#             message_menu = await inter.followup.send(
#                 "Select exercises in the order you would like them to appear:",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             selected_exercise_order: list = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu, return_list=True
#             )
#             await message_menu.delete()
#             print(selected_exercise_order)

#             for exercise_name in selected_exercise_order:
#                 self.bot.cursor.execute(
#                     f"""UPDATE program_exercises
#                                     SET exercise_order = {selected_exercise_order.index(exercise_name)+1}
#                                     WHERE program_id = '{program_id}'
#                                     AND exercise_id = '{exercise_options[exercise_name]['id']}'
#                                     AND exercise_cycle_day = '{exercise_cycle_day}'
#                                                             """
#                 )
#             self.bot.db.commit()

#             message, embed = await util_func.update_workout_embed(
#                 inter=inter,
#                 channel=inter.channel,
#                 bot=self.bot,
#                 exercise_cycle_day=exercise_cycle_day,
#                 program_id=program_id,
#             )

#             await message.edit(embed=embed)

#             await inter.followup.send(
#                 "Order successfully updated.", ephemeral=True, delete_after=3
#             )

#         elif inter.component.custom_id == "Start Session":
#             await inter.response.defer(ephemeral=True)
#             try:
#                 program_id = util_func.get_embed_info(
#                     message=inter.message, embed_properties=["program_id"]
#                 )[0]
#                 print("here gg", program_id)
#             except:
#                 programs = self.bot.cursor.execute(
#                     f"""SELECT program_id, program_name
#                                     FROM custom_programs
#                                     WHERE user_id = '{inter.author.id}'"""
#                 )

#                 programs = util_func.sql_select_handler(
#                     res=programs, bot=self.bot, fetch_type="fetchall"
#                 )
#                 program_dict = util_func.detupler_to_dict(programs)
#                 print(program_dict)

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="Select a Program",
#                     choices=list(program_dict.values()),
#                 )
#                 message_menu = await inter.followup.send(
#                     "It looks like you have not set a current Program. Which program would you like to set to current?",
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 selected_program = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 program_id = util_func.key_from_value(
#                     selected_program, program_dict
#                 )
#                 await message_menu.delete()

#             fitness_program = FitnessProgram(
#                 bot=self.bot, program_id=program_id
#             )

#             program_info = util_func.display_program(
#                 bot=self.bot, program_id=program_id
#             )

#             embed = disnake.Embed(
#                 title=f"Session Manager\n{fitness_program.program_name}",
#                 description=program_info,
#             )
#             embed.set_author(name=f"Program ID: {program_id}")

#             await inter.message.edit(embed=embed)

#             self.bot.cursor.execute(
#                 """SELECT session_id,
#                                     program_id,
#                                     cycle_day
#                                     FROM sessions
#                                     WHERE active = 1
#                                     LIMIT 1"""
#             )
#             active_session = self.bot.cursor.fetchone()
#             if active_session:
#                 active_session_id = active_session[0]
#                 active_program_id = active_session[1]
#                 active_cycle_day = active_session[2]
#                 fitness_program_name = FitnessProgram(
#                     bot=self.bot, program_id=active_program_id
#                 ).program_name

#                 components = [
#                     disnake.ui.Button(
#                         label="Continue Active Session",
#                         style=disnake.ButtonStyle.primary,
#                         custom_id="Continue",
#                     ),
#                     disnake.ui.Button(
#                         label="Start New Session",
#                         style=disnake.ButtonStyle.success,
#                         custom_id="Start New",
#                     ),
#                 ]

#                 active_session_menu = await inter.followup.send(
#                     f"It looks like you already have a currently active session for {fitness_program_name}. Do you wish to continue this active session or mark it complete and start a new session?",
#                     components=components,
#                 )

#                 def check(m):
#                     return m.channel == inter.channel

#                 interaction: disnake.MessageInteraction = (
#                     await self.bot.wait_for("button_click", check=check)
#                 )

#                 active_session_action = interaction.data.custom_id
#                 await active_session_menu.delete()

#                 if active_session_action == "Continue":
#                     message, embed = await util_func.update_session_embed(
#                         inter=inter,
#                         bot=self.bot,
#                         channel=inter.channel,
#                         exercise_cycle_day=active_cycle_day,
#                         program_id=active_program_id,
#                         session_id=active_session_id,
#                     )

#                     await inter.followup.send(embed=embed, view=SessionEditor())
#                     return

#             workout_days = fitness_program.program_length

#             workout_days = [*range(1, workout_days + 1)]
#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Day:",
#                 choices=workout_days,
#                 sort_choices=True,
#             )
#             message_menu = await inter.followup.send(
#                 "For workout day would you like to start a session?",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             selected_day = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu
#             )
#             await message_menu.delete()

#             session_date = util_func.get_now_datetime_int()
#             print(session_date)

#             self.bot.cursor.execute(
#                 """CREATE TABLE IF NOT EXISTS sessions(
#                                                                 session_id INT PRIMARY KEY,
#                                                                 program_id INT,
#                                                                 user_id INT,
#                                                                 session_minutes INT,
#                                                                 date_created BIGINT,
#                                                                 session_notes VARCHAR(500))"""
#             )
#             self.bot.cursor.execute(
#                 """SELECT COUNT(session_id)
#                                     FROM sessions"""
#             )
#             session_id = self.bot.cursor.fetchone()[0] + 1

#             self.bot.cursor.execute(
#                 """INSERT INTO sessions (session_id, program_id, date_created, active, cycle_day) VALUES (%s, %s, %s, %s, %s)""",
#                 (session_id, program_id, session_date, 1, int(selected_day)),
#             )

#             self.bot.db.commit()

#             workout_info, embed_title = util_func.display_workout(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=selected_day,
#             )
#             embed = disnake.Embed(
#                 title=f"Day {selected_day} - {fitness_program.program_name} Session",
#                 description=workout_info,
#             )
#             embed.set_author(
#                 name=f"Program ID: {program_id}\nSession ID: {session_id}"
#             )

#             # self.bot.cursor.execute("""CREATE TABLE IF NOT EXISTS session_exercises(
#             #                                                     session_id INT,
#             #                                                     exercise_id INT,
#             #                                                     reps INT,
#             #                                                     load FLOAT)""")

#             await inter.followup.send(embed=embed, view=SessionEditor())

#         elif inter.component.custom_id == "Log Exercise Data":
#             await inter.response.defer(ephemeral=True)

#             program_info = util_func.get_embed_info(
#                 message=inter.message,
#                 embed_properties=["program_id", "workout_day", "session_id"],
#             )
#             program_id = program_info[0]
#             exercise_cycle_day = program_info[1]
#             session_id = program_info[2]

#             fitness_program = FitnessProgram(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=exercise_cycle_day,
#             )

#             button_exercise_options = []
#             for exercise in fitness_program.exercises:
#                 button = disnake.ui.Button(
#                     label=exercise.exercise_name,
#                     style=disnake.ButtonStyle.secondary,
#                     custom_id=exercise.exercise_name,
#                 )
#                 button_exercise_options.append(button)

#             embed = disnake.Embed(
#                 title=f"Day {exercise_cycle_day} - Log Exercise Data",
#                 description="Choose an option below:",
#             )
#             embed.set_author(
#                 name=f"Program ID: {program_id}\nSession ID: {session_id}"
#             )

#             exercise_menu = await inter.followup.send(
#                 embed=embed, components=button_exercise_options
#             )

#             def check(m):
#                 return m.channel == inter.channel

#             interaction: disnake.MessageInteraction = await self.bot.wait_for(
#                 "button_click", check=check
#             )
#             selected_exercise = interaction.data.custom_id

#             for exercise in fitness_program.exercises:
#                 if exercise.exercise_name == selected_exercise:
#                     exercise_obj: ProgrammedExercise = exercise
#                     break

#             if exercise_obj:

#                 exercise_id = exercise_obj.exercise_id
#                 session_exercise = SessionExercise(
#                     bot=self.bot,
#                     session_id=session_id,
#                     exercise_id=exercise_id,
#                     program_id=program_id,
#                     exercise_cycle_day=exercise_cycle_day,
#                 )
#                 programmed_sets = session_exercise.sets
#                 programmed_reps = session_exercise.reps
#                 session_set_info = session_exercise.session_set_info
#                 session_last_set = session_exercise.current_set_count
#                 session_current_set = session_last_set + 1
#                 last_session_info = session_exercise.last_session_info
#                 print(
#                     programmed_sets,
#                     programmed_reps,
#                     session_last_set,
#                     session_set_info,
#                     last_session_info,
#                 )

#             if programmed_sets != session_last_set:
#                 await exercise_menu.delete()
#                 await interaction.response.send_modal(
#                     SessionLogModal(
#                         bot=self.bot,
#                         program_id=program_id,
#                         session_id=session_id,
#                         exercise_id=exercise_id,
#                         exercise_name=exercise_obj.exercise_name,
#                         target_reps=programmed_reps,
#                         set_count=session_current_set,
#                         target_sets=programmed_sets,
#                         workout_day=exercise_cycle_day,
#                         last_session_info=last_session_info,
#                     )
#                 )
#             else:
#                 components = [
#                     disnake.ui.Button(
#                         label="Yes",
#                         style=disnake.ButtonStyle.success,
#                         custom_id="Yes",
#                     ),
#                     disnake.ui.Button(
#                         label="No",
#                         style=disnake.ButtonStyle.danger,
#                         custom_id="No",
#                     ),
#                 ]

#                 add_set_menu = await inter.followup.send(
#                     content=f"You have already completed the {programmed_sets} sets programmed for the **{exercise_obj.exercise_name}**. Do you want to do another set of this exercise for this session?",
#                     components=components,
#                 )

#                 interaction: disnake.MessageInteraction = (
#                     await self.bot.wait_for("button_click", check=check)
#                 )

#                 add_set = interaction.data.custom_id
#                 await exercise_menu.delete()

#                 await add_set_menu.delete()

#                 if add_set == "No":
#                     pass
#                 else:
#                     await interaction.response.send_modal(
#                         SessionLogModal(
#                             bot=self.bot,
#                             program_id=program_id,
#                             session_id=session_id,
#                             exercise_id=exercise_id,
#                             exercise_name=exercise_obj.exercise_name,
#                             target_reps=programmed_reps,
#                             set_count=session_current_set,
#                             target_sets=programmed_sets,
#                             workout_day=exercise_cycle_day,
#                             last_session_info=last_session_info,
#                         )
#                     )

#         elif inter.component.custom_id == "Change Program":
#             await inter.response.defer(ephemeral=True)
#             programs = self.bot.cursor.execute(
#                 f"""SELECT program_id, program_name
#                                     FROM custom_programs
#                                     WHERE user_id = '{inter.author.id}'"""
#             )

#             programs = util_func.sql_select_handler(
#                 res=programs, bot=self.bot, fetch_type="fetchall"
#             )
#             program_dict = util_func.detupler_to_dict(programs)
#             print(program_dict)

#             menu_content = await util_func.dropdown(
#                 bot=self.bot,
#                 inter=inter,
#                 menu_desc="Select a Program",
#                 choices=list(program_dict.values()),
#             )
#             message_menu = await inter.followup.send(
#                 "To which program would you like to switch?",
#                 components=menu_content,
#                 ephemeral=True,
#             )
#             selected_program = await util_func.get_dropdown_value(
#                 bot=self.bot, message=message_menu
#             )
#             program_id = util_func.key_from_value(
#                 selected_program, program_dict
#             )
#             await message_menu.delete()

#             fitness_program = FitnessProgram(
#                 bot=self.bot, program_id=program_id
#             )

#             program_info = util_func.display_program(
#                 bot=self.bot, program_id=program_id
#             )

#             embed = disnake.Embed(
#                 title=f"Session Manager\n{fitness_program.program_name}",
#                 description=program_info,
#             )
#             embed.set_author(name=f"Program ID: {program_id}")

#             await inter.message.edit(embed=embed)

#         elif inter.component.custom_id == "Complete Session":
#             await inter.response.defer(ephemeral=True)

#             program_info = util_func.get_embed_info(
#                 message=inter.message,
#                 embed_properties=["program_id", "workout_day", "session_id"],
#             )
#             program_id = program_info[0]
#             exercise_cycle_day = program_info[1]
#             session_id = program_info[2]

#             components = [
#                 disnake.ui.Button(
#                     label="Yes",
#                     style=disnake.ButtonStyle.success,
#                     custom_id="Yes",
#                 ),
#                 disnake.ui.Button(
#                     label="No", style=disnake.ButtonStyle.danger, custom_id="No"
#                 ),
#             ]

#             exercise_menu = await inter.followup.send(
#                 content="Are you sure you want to mark this session as complete?",
#                 components=components,
#             )

#             def check(m):
#                 return m.channel == inter.channel

#             interaction: disnake.MessageInteraction = await self.bot.wait_for(
#                 "button_click", check=check
#             )
#             confirm_removal = interaction.data.custom_id
#             await exercise_menu.delete()

#             if confirm_removal == "No":
#                 return

#             query = """UPDATE sessions SET active = 0 WHERE session_id = %s"""
#             val = (session_id,)
#             self.bot.cursor.execute(query, val)
#             self.bot.db.commit()

#             fitness_program = FitnessProgram(
#                 bot=self.bot,
#                 program_id=program_id,
#                 exercise_cycle_day=exercise_cycle_day,
#             )

#             await inter.message.delete()

#             await inter.followup.send(
#                 "Session marked complete!", ephemeral=True, delete_after=3
#             )


# def setup(bot):
#     bot.add_cog(EmbedButtons(bot))
