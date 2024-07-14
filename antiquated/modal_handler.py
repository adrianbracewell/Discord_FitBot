# import disnake
# from disnake.ext import commands
# import utils.functions as util_func
# from classes.fitness_program import FitnessProgram


# exercise_button_dict = {}

# weekday_bitfield_dict = {
#     "Monday": 1,
#     "Tuesday": 2,
#     "Wednesday": 4,
#     "Thursday": 8,
#     "Friday": 16,
#     "Saturday": 32,
#     "Sunday": 64,
# }


# class ProgramManagerModal(disnake.ui.Modal):
#     def __init__(self, bot):
#         self.bot = bot
#         print(self.bot)

#         components = [
#             disnake.ui.TextInput(
#                 custom_id="program_name",
#                 label="What is the name of your program?",
#                 placeholder="-",
#                 style=disnake.TextInputStyle.short,
#                 max_length=30,
#             )
#         ]
#         super().__init__(title="Create a Program", components=components)

#     async def callback(self, inter: disnake.ModalInteraction):

#         await inter.response.defer(ephemeral=True)
#         # print(inter.user.name)

#         program_name = list(inter.text_values.values())[0]

#         print(program_name)

#         program_type = "Yes"

#         split_list = [
#             "Bro Split",
#             "Push-Pull-Legs",
#             "Full Body",
#             "PHAT",
#             "German Volumne Training",
#             "DC Training (DoggCrapp)",
#             "PHUL Powerbuilding",
#             "FST-7 Training",
#             "Upper/Lower Split",
#             "5 x 5",
#             "Soviet Powerlifting",
#             "Auto-Regulation",
#             "Shortcut to Shred",
#             "Shortcut to Size",
#             "Shortcut to Stupidity",
#             "John Meadows Taskmaster",
#             "John Meadows Intensification",
#             "YOLO",
#             "Sure",
#             "OK",
#             "OH NO",
#             "HELP",
#             "SURPRISE",
#             "FUNNY",
#             "GHOSH",
#             "Sweet",
#             "Done",
#         ]
#         menu_content = await util_func.dropdown(
#             bot=self.bot, inter=inter, menu_desc="Test", choices=split_list
#         )

#         message_menu = await inter.followup.send(
#             "Choose a type of split:", components=menu_content, ephemeral=True
#         )
#         program_split = await util_func.get_dropdown_value(
#             bot=self.bot, message=message_menu
#         )
#         await message_menu.delete()

#         menu_content = await util_func.dropdown(
#             bot=self.bot,
#             inter=inter,
#             menu_desc="Test",
#             choices=[x for x in range(1, 15)],
#         )
#         message_menu = await inter.followup.send(
#             "How many days is one microcycle for this program?",
#             components=menu_content,
#             ephemeral=True,
#         )
#         program_microcycle_length = await util_func.get_dropdown_value(
#             bot=self.bot, message=message_menu
#         )
#         await message_menu.delete()

#         program_insert = (
#             program_name,
#             program_microcycle_length,
#             str(inter.author.id),
#         )

#         self.bot.cursor.execute(
#             "INSERT INTO custom_programs (program_name, microcycle_length, user_id) VALUES (%s, %s, %s)",
#             (program_insert),
#         )
#         self.bot.db.commit()

#         await inter.followup.send(
#             "Program created!", ephemeral=True, delete_after=3
#         )


# class SessionLogModal(disnake.ui.Modal):
#     def __init__(
#         self,
#         bot,
#         program_id,
#         exercise_id,
#         session_id,
#         exercise_name,
#         target_sets,
#         target_reps,
#         set_count,
#         workout_day,
#         last_session_info=None,
#     ):
#         self.bot = bot
#         self.program_id = program_id
#         self.session_id = session_id
#         self.exercise_id = exercise_id
#         self.exercise_name = exercise_name
#         self.target_sets = target_sets
#         self.target_reps = target_reps
#         self.set_count = set_count
#         self.workout_day = workout_day
#         self.last_session_info = last_session_info

#         if last_session_info:
#             last_session_set_weight = last_session_info[self.set_count][
#                 "past_set_load"
#             ]
#             last_session_set_reps = last_session_info[self.set_count][
#                 "past_set_reps"
#             ]
#             weight_label = f"Weight [Last Session: {last_session_set_weight}]"
#             reps_label = f"Number of Reps Completed [Last Session: {last_session_set_reps}]"
#         else:
#             weight_label = f"Weight"
#             reps_label = f"Number of Reps Completed [Goal: {self.target_reps}]"

#         components = [
#             disnake.ui.TextInput(
#                 custom_id="exercise_amount",
#                 label=weight_label,
#                 placeholder="-",
#                 style=disnake.TextInputStyle.short,
#                 max_length=4,
#             ),
#             disnake.ui.TextInput(
#                 custom_id="exercise_reps",
#                 label=reps_label,
#                 placeholder="-",
#                 style=disnake.TextInputStyle.short,
#                 max_length=3,
#             ),
#         ]
#         title = (
#             f"{self.exercise_name} - Set {self.set_count}/{self.target_sets}"
#         )

#         super().__init__(title=title, components=components)

#     async def callback(self, inter: disnake.ModalInteraction):

#         await inter.response.defer(ephemeral=True)
#         # print(inter.user.name)

#         exercise_load_amount = int(list(inter.text_values.values())[0])
#         exercise_rep_count = int(list(inter.text_values.values())[1])

#         insert_info = (
#             self.session_id,
#             self.exercise_id,
#             exercise_rep_count,
#             exercise_load_amount,
#             self.set_count,
#         )

#         self.bot.cursor.execute(
#             """INSERT INTO session_exercises (
#                                 session_id,
#                                 exercise_id,
#                                 reps,
#                                 amount,
#                                 set_order) VALUES (%s, %s, %s, %s, %s)""",
#             insert_info,
#         )
#         self.bot.db.commit()

#         message, embed = await util_func.update_session_embed(
#             inter=inter,
#             bot=self.bot,
#             channel=inter.channel,
#             exercise_cycle_day=self.workout_day,
#             program_id=self.program_id,
#             session_id=self.session_id,
#         )

#         await message.edit(embed=embed)

#         await inter.followup.send(
#             "Exercise successfully added.", ephemeral=True, delete_after=5
#         )


# class ExerciseModal(disnake.ui.Modal):
#     def __init__(
#         self,
#         bot,
#         program_id,
#         workout_day,
#         exercise_id,
#         exercise_name,
#         action,
#         sets=None,
#         reps=None,
#     ):
#         self.bot = bot
#         self.program_id = program_id
#         self.workout_day = workout_day
#         self.action = action
#         self.exercise_id = exercise_id
#         self.exercise_name = exercise_name
#         self.sets = sets
#         self.reps = reps
#         print("reps", reps)

#         components = [
#             disnake.ui.TextInput(
#                 custom_id="exercise_name",
#                 label="What is the name of this exercise?",
#                 placeholder="-",
#                 style=disnake.TextInputStyle.short,
#                 max_length=30,
#             ),
#             disnake.ui.TextInput(
#                 custom_id="exercise_sets",
#                 label="How many sets?",
#                 placeholder="-",
#                 style=disnake.TextInputStyle.short,
#                 value=sets,
#                 max_length=3,
#             ),
#             disnake.ui.TextInput(
#                 custom_id="exercise_reps",
#                 label="How many reps per set?",
#                 placeholder="-",
#                 style=disnake.TextInputStyle.short,
#                 value=reps,
#                 max_length=3,
#             ),
#         ]
#         if action == "add":
#             title = "Add Exercise"
#             custom_id = action
#         elif action == "update":
#             title = f"Update Exercise - {self.exercise_name}"
#             components = components[1:]
#             custom_id = action
#         elif action == "replace":
#             title = f"Replace Exercise - {self.exercise_name}"
#             custom_id = action

#         super().__init__(
#             title=title, components=components, custom_id=custom_id
#         )

#     async def callback(self, inter: disnake.ModalInteraction):

#         await inter.response.defer(ephemeral=True)
#         # print(inter.user.name)
#         print(inter.custom_id)

#         if inter.custom_id == "add":

#             exercise_name = list(inter.text_values.values())[0].title()
#             exercise_sets = list(inter.text_values.values())[1]
#             exercise_reps = list(inter.text_values.values())[2]

#             # program_days = self.bot.cursor.execute(f"""SELECT DISTINCT exercise_cycle_day
#             #                                        FROM program_exercises
#             #                                        WHERE program_id = {self.program_id}""")

#             # program_days = util_func.sql_select_handler(bot=self.bot, res=program_days, fetch_type='fetchall')

#             # menu_content = await util_func.dropdown(bot=self.bot,
#             #                                                           inter=inter,
#             #                                                           menu_desc='To which days of the program do you want to add this exercise?',
#             #                                                           choices=program_days,
#             #                                                           sort_choices=False,
#             #                                                           max_choices=7)
#             # message_menu = await inter.followup.send('To which days of the program do you want to add this exercise?', components=menu_content, ephemeral=True)
#             # selected_program_days = await util_func.get_dropdown_value(bot=self.bot, message=message_menu, return_list=True)
#             # await message_menu.delete()

#             # print(selected_program_days)

#             # weekdays_bit_val = util_func.weekdays_to_bit(weekdays=selected_weekdays,
#             #                                              weekday_bitfield_dict=weekday_bitfield_dict)
#             # print(weekdays_bit_val)
#             # weekday_vals = util_func.bit_to_weekdays(
#             #     weekdays_bit_val, weekday_bitfield_dict=weekday_bitfield_dict)
#             # print(weekday_vals)
#             # exercise_name_matches = get_col_val_matches(bot=self.bot, word_to_match=exercise_name,
#             #                                             tbl_name='exercises', col_name='name')
#             # print(exercise_name_matches)

#             exercise_name_matches = util_func.levenshtein_distance(
#                 bot=self.bot,
#                 word_to_match=exercise_name,
#                 tbl_name="exercises",
#                 col_name="name",
#                 constraint_col_name=None,
#                 constraint_col_val=None,
#             )

#             print(exercise_name_matches)
#             if exercise_name_matches == []:
#                 muscle_groups = [
#                     "Upper Back",
#                     "Lower Back",
#                     "Lats",
#                     "Chest",
#                     "Front Deltoid",
#                     "Middle Deltoid",
#                     "Rear Deltoid",
#                     "Upper Traps",
#                     "Lower Traps",
#                     "Rectus Abdominis",
#                     "Transverse Adbominis",
#                     "Obliques",
#                     "Triceps",
#                     "Biceps",
#                     "Forearms",
#                     "Quadriceps",
#                     "Hamstrings",
#                     "Calves",
#                     "Serratus Anterior",
#                     "Glutes",
#                     "Hips",
#                 ]

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="What is the primary muscle group trained during this exercise?",
#                     choices=muscle_groups,
#                     sort_choices=False,
#                     max_choices=1,
#                 )

#                 nonexistent_exercise_msg = (
#                     "It looks this exercise has not yet been added to our database. "
#                     "We will add it now!\n\n"
#                     "What is the primary muscle group trained during this exercise?"
#                 )

#                 message_menu = await inter.followup.send(
#                     content=nonexistent_exercise_msg,
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 selected_muscle_group = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 await message_menu.delete()

#                 program_name = self.bot.cursor.execute(
#                     f"""SELECT program_name FROM custom_programs WHERE program_id = '{self.program_id}'"""
#                 )
#                 embed = disnake.Embed(title=f"{program_name} - Add Exercise")
#                 embed.add_field(
#                     name="Exercise Name", value=exercise_name, inline=False
#                 )
#                 embed.add_field(
#                     name="Primary Muscle Group",
#                     value=selected_muscle_group,
#                     inline=False,
#                 )
#                 embed.add_field(
#                     name="# of Sets", value=exercise_sets, inline=False
#                 )
#                 embed.add_field(
#                     name="# of Reps", value=exercise_reps, inline=False
#                 )
#                 embed.set_footer(text=f"Program ID: {self.program_id}")

#                 print("This is the program_id", self.program_id)
#                 fitness_program = FitnessProgram(
#                     bot=self.bot,
#                     program_id=self.program_id,
#                     exercise_cycle_day=self.workout_day,
#                 )

#                 print("Lenoo", len(fitness_program.exercises))

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="Does this look correct?",
#                     choices=["Yes", "No"],
#                 )
#                 message_menu = await inter.followup.send(
#                     "Does this look correct?",
#                     embed=embed,
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 confirm_addition = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 await message_menu.delete()

#                 exercise_info_insert = (exercise_name, selected_muscle_group)

#                 self.bot.cursor.execute(
#                     """INSERT INTO exercises (  name,
#                                                                     muscle_group_one
#                                                                     ) VALUES (%s, %s)""",
#                     exercise_info_insert,
#                 )
#                 self.bot.db.commit()
#                 exercise_id = self.bot.cursor.execute(
#                     """SELECT exercise_id
#                                         FROM exercises
#                                         WHERE name = %s""",
#                     (exercise_name,),
#                 )

#                 exercise_id = util_func.sql_select_handler(
#                     bot=self.bot,
#                     res=exercise_id,
#                     fetch_type="fetchone",
#                 )
#                 print("Workout Day", self.workout_day)

#                 program_exercise_info = (
#                     self.program_id,
#                     exercise_id,
#                     self.workout_day,
#                     exercise_sets,
#                     exercise_reps,
#                     len(fitness_program.exercises),
#                 )

#                 self.bot.cursor.execute(
#                     """INSERT INTO program_exercises (program_id,
#                                                                             exercise_id,
#                                                                             exercise_cycle_day,
#                                                                             exercise_target_sets,
#                                                                             exercise_target_reps,
#                                                                             exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
#                     program_exercise_info,
#                 )
#                 self.bot.db.commit()

#                 channel_history = await inter.channel.history(limit=5).flatten()
#                 for msg in channel_history:
#                     if (
#                         len(msg.embeds) != 0
#                         and msg.embeds[0].title
#                         == f"Day {self.workout_day} - Edit Workout"
#                     ):
#                         message_to_edit = msg

#                 workout_info, title = util_func.display_workout(
#                     bot=self.bot,
#                     program_id=self.program_id,
#                     exercise_cycle_day=self.workout_day,
#                 )
#                 embed = disnake.Embed(
#                     title=f"Day {self.workout_day}{title}",
#                     description=workout_info,
#                 )
#                 embed.set_author(name=f"Program ID: {self.program_id}")

#                 message_to_edit, embed = await util_func.update_workout_embed(
#                     inter=inter,
#                     bot=self.bot,
#                     channel=inter.channel,
#                     exercise_cycle_day=self.workout_day,
#                     program_id=self.program_id,
#                 )

#                 await message_to_edit.edit(embed=embed)

#                 await inter.followup.send(
#                     "Exercise successfully added.",
#                     ephemeral=True,
#                     delete_after=5,
#                 )

#             else:
#                 button_exercise_options = []
#                 for i, exercise in enumerate(exercise_name_matches):
#                     button_component = disnake.ui.Button(
#                         label=exercise,
#                         style=disnake.ButtonStyle.secondary,
#                         row=i + 1,
#                         custom_id=exercise,
#                     )
#                     button_exercise_options.append(button_component)
#                     exercise_button_dict[exercise] = button_component

#                 exercise_check = await inter.followup.send(
#                     content="Did you mean one of these exercises?",
#                     components=button_exercise_options,
#                 )

#                 def check(m):
#                     return m.channel == inter.channel

#                 interaction: disnake.MessageInteraction = (
#                     await self.bot.wait_for("button_click", check=check)
#                 )
#                 print(interaction.data.custom_id)

#                 await exercise_check.delete()

#                 exercise_buttons = list(exercise_button_dict.keys())

#                 exercise_name = interaction.data.custom_id
#                 print("This is the program_id", self.program_id)
#                 fitness_program = FitnessProgram(
#                     bot=self.bot,
#                     program_id=self.program_id,
#                     exercise_cycle_day=self.workout_day,
#                 )

#                 print("Lenoo", len(fitness_program.exercises))

#                 program_name = self.bot.cursor.execute(
#                     f"""SELECT program_name FROM custom_programs WHERE program_id = '{self.program_id}'"""
#                 )
#                 embed = disnake.Embed(title=f"{program_name} - Add Exercise")
#                 embed.add_field(
#                     name="Exercise Name", value=exercise_name, inline=False
#                 )
#                 embed.add_field(
#                     name="# of Sets", value=exercise_sets, inline=False
#                 )
#                 embed.add_field(
#                     name="# of Reps", value=exercise_reps, inline=False
#                 )
#                 embed.set_footer(text=f"Program ID: {self.program_id}")

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="Does this look correct?",
#                     choices=["Yes", "No"],
#                 )
#                 message_menu = await inter.followup.send(
#                     "Does this look correct?",
#                     embed=embed,
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 confirm_addition = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 await message_menu.delete()

#                 if confirm_addition == "No":
#                     pass
#                 else:
#                     print(exercise_name)
#                     exercise_id = self.bot.cursor.execute(
#                         f"""SELECT exercise_id FROM exercises WHERE name = '{exercise_name}'"""
#                     )
#                     print(exercise_id)
#                     exercise_id = util_func.sql_select_handler(
#                         res=exercise_id,
#                         bot=self.bot,
#                         fetch_type="fetchone",
#                     )
#                     print(exercise_id)

#                     cycle_day_num_exercises = len(fitness_program.exercises) + 1

#                     insert_info = (
#                         self.program_id,
#                         exercise_id,
#                         self.workout_day,
#                         exercise_sets,
#                         exercise_reps,
#                         cycle_day_num_exercises,
#                     )
#                     self.bot.cursor.execute(
#                         """INSERT INTO program_exercises (program_id,
#                                                                             exercise_id,
#                                                                             exercise_cycle_day,
#                                                                             exercise_target_sets,
#                                                                             exercise_target_reps,
#                                                                             exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
#                         insert_info,
#                     )
#                     self.bot.db.commit()
#                     print("Successs")
#                     channel_history = await inter.channel.history(
#                         limit=5
#                     ).flatten()
#                     for msg in channel_history:
#                         if len(msg.embeds) != 0 and (
#                             msg.embeds[0].title
#                             == f"Day {self.workout_day} - Edit Workout"
#                             or msg.embeds[0].title
#                             == f"Day {self.workout_day} - Rest Day"
#                         ):
#                             message_to_edit = msg
#                     try:
#                         workout_info, title = util_func.display_workout(
#                             bot=self.bot,
#                             program_id=self.program_id,
#                             exercise_cycle_day=self.workout_day,
#                         )
#                         embed = disnake.Embed(
#                             title=f"Day {self.workout_day}{title}",
#                             description=workout_info,
#                         )
#                         embed.set_author(name=f"Program ID: {self.program_id}")

#                         await message_to_edit.edit(embed=embed)
#                     except:
#                         print("Could not find workout embed to refresh.")

#                     await inter.followup.send(
#                         "Exercise successfully added.",
#                         ephemeral=True,
#                         delete_after=5,
#                     )
#         elif inter.custom_id == "update":
#             exercise_sets = list(inter.text_values.values())[0]
#             exercise_reps = list(inter.text_values.values())[1]
#             print(self.exercise_id)

#             insert_info = (
#                 exercise_sets,
#                 exercise_reps,
#                 self.program_id,
#                 self.workout_day,
#                 self.exercise_id,
#             )

#             self.bot.cursor.execute(
#                 """UPDATE program_exercises
#                                     SET exercise_target_sets = %s,
#                                         exercise_target_reps = %s
#                                     WHERE program_id = %s
#                                     AND exercise_cycle_day = %s
#                                     AND exercise_id = %s""",
#                 insert_info,
#             )
#             self.bot.db.commit()

#             channel_history = await inter.channel.history(limit=5).flatten()
#             for msg in channel_history:
#                 if (
#                     len(msg.embeds) != 0
#                     and msg.embeds[0].title
#                     == f"Day {self.workout_day} - Edit Workout"
#                 ):
#                     message_to_edit = msg
#             try:
#                 workout_info, title = util_func.display_workout(
#                     bot=self.bot,
#                     program_id=self.program_id,
#                     exercise_cycle_day=self.workout_day,
#                 )
#                 embed = disnake.Embed(
#                     title=f"Day {self.workout_day}{title}",
#                     description=workout_info,
#                 )
#                 embed.set_author(name=f"Program ID: {self.program_id}")

#                 await message_to_edit.edit(embed=embed)
#             except:
#                 print("Could not find workout embed to refresh.")

#             await inter.followup.send(
#                 "Workout successfully updated.", ephemeral=True, delete_after=5
#             )
#         elif inter.custom_id == "replace":
#             exercise_name = list(inter.text_values.values())[0].title()
#             exercise_sets = list(inter.text_values.values())[1]
#             exercise_reps = list(inter.text_values.values())[2]

#             # program_days = self.bot.cursor.execute(f"""SELECT DISTINCT exercise_cycle_day
#             #                                        FROM program_exercises
#             #                                        WHERE program_id = {self.program_id}""")

#             # program_days = util_func.sql_select_handler(bot=self.bot, res=program_days, fetch_type='fetchall')

#             # menu_content = await util_func.dropdown(bot=self.bot,
#             #                                                           inter=inter,
#             #                                                           menu_desc='To which days of the program do you want to add this exercise?',
#             #                                                           choices=program_days,
#             #                                                           sort_choices=False,
#             #                                                           max_choices=7)
#             # message_menu = await inter.followup.send('To which days of the program do you want to add this exercise?', components=menu_content, ephemeral=True)
#             # selected_program_days = await util_func.get_dropdown_value(bot=self.bot, message=message_menu, return_list=True)
#             # await message_menu.delete()

#             # print(selected_program_days)

#             # weekdays_bit_val = util_func.weekdays_to_bit(weekdays=selected_weekdays,
#             #                                              weekday_bitfield_dict=weekday_bitfield_dict)
#             # print(weekdays_bit_val)
#             # weekday_vals = util_func.bit_to_weekdays(
#             #     weekdays_bit_val, weekday_bitfield_dict=weekday_bitfield_dict)
#             # print(weekday_vals)
#             # exercise_name_matches = get_col_val_matches(bot=self.bot, word_to_match=exercise_name,
#             #                                             tbl_name='exercises', col_name='name')
#             # print(exercise_name_matches)

#             exercise_name_matches = util_func.levenshtein_distance(
#                 bot=self.bot,
#                 word_to_match=exercise_name,
#                 tbl_name="exercises",
#                 col_name="name",
#                 constraint_col_name=None,
#                 constraint_col_val=None,
#             )

#             print(exercise_name_matches)
#             if not exercise_name_matches:
#                 muscle_groups = [
#                     "Upper Back",
#                     "Lower Back",
#                     "Lats",
#                     "Chest",
#                     "Front Deltoid",
#                     "Middle Deltoid",
#                     "Rear Deltoid",
#                     "Upper Traps",
#                     "Lower Traps",
#                     "Rectus Abdominis",
#                     "Transverse Adbominis",
#                     "Obliques",
#                     "Triceps",
#                     "Biceps",
#                     "Forearms",
#                     "Quadriceps",
#                     "Hamstrings",
#                     "Calves",
#                     "Serratus Anterior",
#                     "Glutes",
#                     "Hips",
#                 ]

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="What is the primary muscle group trained during this exercise?",
#                     choices=muscle_groups,
#                     sort_choices=False,
#                     max_choices=1,
#                 )
#                 message_menu = await inter.followup.send(
#                     "It looks this exercise has not yet been added to our database. We will add it now!\n\nWhat is the primary muscle group trained during this exercise?",
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 selected_muscle_group = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 await message_menu.delete()

#                 program_name = self.bot.cursor.execute(
#                     f"""SELECT program_name FROM custom_programs WHERE program_id = '{self.program_id}'"""
#                 )
#                 embed = disnake.Embed(title=f"{program_name} - Add Exercise")
#                 embed.add_field(
#                     name="Exercise Name", value=exercise_name, inline=False
#                 )
#                 embed.add_field(
#                     name="Primary Muscle Group",
#                     value=selected_muscle_group,
#                     inline=False,
#                 )
#                 embed.add_field(
#                     name="# of Sets", value=exercise_sets, inline=False
#                 )
#                 embed.add_field(
#                     name="# of Reps", value=exercise_reps, inline=False
#                 )
#                 embed.set_footer(text=f"Program ID: {self.program_id}")

#                 print("This is the program_id", self.program_id)
#                 fitness_program = FitnessProgram(
#                     bot=self.bot,
#                     program_id=self.program_id,
#                     exercise_cycle_day=self.workout_day,
#                 )

#                 print("Lenoo", len(fitness_program.exercises))

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="Does this look correct?",
#                     choices=["Yes", "No"],
#                 )
#                 message_menu = await inter.followup.send(
#                     "Does this look correct?",
#                     embed=embed,
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 confirm_addition = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 await message_menu.delete()

#                 exercise_info_insert = (exercise_name, selected_muscle_group)

#                 self.bot.cursor.execute(
#                     """INSERT INTO exercises (  name,
#                                                                     muscle_group_one
#                                                                     ) VALUES (%s, %s)""",
#                     exercise_info_insert,
#                 )
#                 self.bot.db.commit()
#                 exercise_id = self.bot.cursor.execute(
#                     """SELECT exercise_id
#                                         FROM exercises
#                                         WHERE name = %s""",
#                     (exercise_name,),
#                 )

#                 exercise_id = util_func.sql_select_handler(
#                     bot=self.bot,
#                     res=exercise_id,
#                     fetch_type="fetchone",
#                 )
#                 print("Workout Day", self.workout_day)

#                 program_exercise_info = (
#                     self.program_id,
#                     exercise_id,
#                     self.workout_day,
#                     exercise_sets,
#                     exercise_reps,
#                     len(fitness_program.exercises),
#                 )

#                 self.bot.cursor.execute(
#                     """INSERT INTO program_exercises (program_id,
#                                                                             exercise_id,
#                                                                             exercise_cycle_day,
#                                                                             exercise_target_sets,
#                                                                             exercise_target_reps,
#                                                                             exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
#                     program_exercise_info,
#                 )
#                 self.bot.db.commit()

#                 message, embed = await util_func.update_workout_embed(
#                     inter=inter,
#                     bot=self.bot,
#                     channel=inter.channel,
#                     exercise_cycle_day=self.workout_day,
#                     program_id=self.program_id,
#                 )

#                 await message.edit(embed=embed)

#                 await inter.followup.send(
#                     "Exercise successfully added.",
#                     ephemeral=True,
#                     delete_after=5,
#                 )

#             else:
#                 button_exercise_options = []
#                 for i, exercise in enumerate(exercise_name_matches):
#                     button_component = disnake.ui.Button(
#                         label=exercise,
#                         style=disnake.ButtonStyle.secondary,
#                         row=i + 1,
#                         custom_id=exercise,
#                     )
#                     button_exercise_options.append(button_component)
#                     exercise_button_dict[exercise] = button_component

#                 exercise_check = await inter.followup.send(
#                     content="Did you mean one of these exercises?",
#                     components=button_exercise_options,
#                 )

#                 def check(m):
#                     return m.channel == inter.channel

#                 interaction: disnake.MessageInteraction = (
#                     await self.bot.wait_for("button_click", check=check)
#                 )
#                 print(interaction.data.custom_id)

#                 await exercise_check.delete()

#                 exercise_buttons = list(exercise_button_dict.keys())

#                 exercise_name = interaction.data.custom_id
#                 print("This is the program_id", self.program_id)
#                 fitness_program = FitnessProgram(
#                     bot=self.bot,
#                     program_id=self.program_id,
#                     exercise_cycle_day=self.workout_day,
#                 )

#                 print("Lenoo", len(fitness_program.exercises))

#                 program_name = self.bot.cursor.execute(
#                     f"""SELECT program_name FROM custom_programs WHERE program_id = '{self.program_id}'"""
#                 )
#                 embed = disnake.Embed(title=f"{program_name} - Add Exercise")
#                 embed.add_field(
#                     name="Exercise Name", value=exercise_name, inline=False
#                 )
#                 embed.add_field(
#                     name="# of Sets", value=exercise_sets, inline=False
#                 )
#                 embed.add_field(
#                     name="# of Reps", value=exercise_reps, inline=False
#                 )
#                 embed.set_footer(text=f"Program ID: {self.program_id}")

#                 menu_content = await util_func.dropdown(
#                     bot=self.bot,
#                     inter=inter,
#                     menu_desc="Does this look correct?",
#                     choices=["Yes", "No"],
#                 )
#                 message_menu = await inter.followup.send(
#                     "Does this look correct?",
#                     embed=embed,
#                     components=menu_content,
#                     ephemeral=True,
#                 )
#                 confirm_addition = await util_func.get_dropdown_value(
#                     bot=self.bot, message=message_menu
#                 )
#                 await message_menu.delete()

#                 if confirm_addition == "No":
#                     pass
#                 else:
#                     print(exercise_name)
#                     exercise_id = self.bot.cursor.execute(
#                         f"""SELECT exercise_id FROM exercises WHERE name = '{exercise_name}'"""
#                     )
#                     print(exercise_id)
#                     exercise_id = util_func.sql_select_handler(
#                         res=exercise_id,
#                         bot=self.bot,
#                         fetch_type="fetchone",
#                     )
#                     print(exercise_id)

#                     cycle_day_num_exercises = len(fitness_program.exercises) + 1

#                     insert_info = (
#                         self.program_id,
#                         exercise_id,
#                         self.workout_day,
#                         exercise_sets,
#                         exercise_reps,
#                         cycle_day_num_exercises,
#                     )
#                     self.bot.cursor.execute(
#                         """INSERT INTO program_exercises (program_id,
#                                                                             exercise_id,
#                                                                             exercise_cycle_day,
#                                                                             exercise_target_sets,
#                                                                             exercise_target_reps,
#                                                                             exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
#                         insert_info,
#                     )
#                     self.bot.db.commit()
#                     print("Successs")
#                     message, embed = await util_func.update_workout_embed(
#                         inter=inter,
#                         bot=self.bot,
#                         channel=inter.channel,
#                         exercise_cycle_day=self.workout_day,
#                         program_id=self.program_id,
#                     )

#                     await message.edit(embed=embed)

#                     await inter.followup.send(
#                         "Exercise successfully added.",
#                         ephemeral=True,
#                         delete_after=5,
#                     )


# # class ExerciseButtons(commands.Cog):
# #     def __init__(self, bot):
# #         self.bot = bot

# #     @commands.Cog.listener("on_button_click")
# #     async def help_listener(self, inter: disnake.MessageInteraction):
# #         exercise_buttons = list(exercise_button_dict.keys())

# #         if inter.component.custom_id in exercise_button_dict:
# #             if inter.message.content == 'Did you mean one of these exercises?':
# #                 await inter.response.send_modal()

# #         elif inter.component.custom_id == 'Edit Program':
# #             await inter.response.defer()

# #             self.bot.cursor.execute(f"""SELECT program_id, program_name
# #                                     FROM custom_programs
# #                                     WHERE user_id = '{inter.author.id}'""")

# #             programs = self.bot.cursor.fetchall()
# #             programs = sql_select_handler(programs)
# #             program_dict = detupler_to_dict(programs)

# #             menu_content = await dropdown(bot=self.bot,
# #                                                         inter=inter,
# #                                                         menu_desc='Select a Program',
# #                                                         choices=list(program_dict.values()))
# #             message_menu = await inter.followup.send('Which program would you like to edit?', components=menu_content, ephemeral=True)
# #             selected_program = await get_dropdown_value(bot=self.bot, message=message_menu)
# #             selected_program_id = key_from_value(selected_program, program_dict)
# #             await message_menu.delete()

# #             program_info = display_program(bot=self.bot, program_id=selected_program_id)

# #             embed = disnake.Embed(title=selected_program, description=program_info)
# #             embed.set_footer(text=f'Program ID: {selected_program_id}')

# #             await inter.followup.send(embed=embed, view=ProgramEditor())
# #         elif inter.component.custom_id == 'Add Exercise':

# #             await inter.response.send_modal(AddExerciseModal(self.bot))


# #             program_id = get_embed_info(message=inter.message, embed_property='program_id')


# # def setup(bot):
# #     bot.add_cog(EmbedButtons(bot))
