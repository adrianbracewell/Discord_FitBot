import disnake
import utils.functions as util_func
from classes.fitness_program import FitnessProgram


class ReplaceExerciseModal(disnake.ui.Modal):
    def __init__(
        self,
        bot,
        program_id,
        workout_day,
        exercise_id,
        exercise_name,
        action,
        sets=None,
        reps=None,
    ):
        self.bot = bot
        self.program_id = program_id
        self.workout_day = workout_day
        self.action = action
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.sets = sets
        self.reps = reps

        components = [
            disnake.ui.TextInput(
                custom_id="exercise_name",
                label="What is the name of this exercise?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                max_length=30,
            ),
            disnake.ui.TextInput(
                custom_id="exercise_sets",
                label="How many sets?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                value=sets,
                max_length=3,
            ),
            disnake.ui.TextInput(
                custom_id="exercise_reps",
                label="How many reps per set?",
                placeholder="-",
                style=disnake.TextInputStyle.short,
                value=reps,
                max_length=3,
            ),
        ]

        super().__init__(
            title=f"Replace Exercise - {self.exercise_name}",
            components=components,
        )

    async def callback(self, inter: disnake.ModalInteraction):

        await inter.response.defer(ephemeral=True)

        exercise_name = list(inter.text_values.values())[0].title()
        exercise_sets = list(inter.text_values.values())[1]
        exercise_reps = list(inter.text_values.values())[2]

        exercise_name_matches = util_func.levenshtein_distance(
            bot=self.bot,
            word_to_match=exercise_name,
            tbl_name="exercises",
            col_name="name",
            constraint_col_name=None,
            constraint_col_val=None,
        )

        print(exercise_name_matches)
        if not exercise_name_matches:
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

            menu_content = await util_func.dropdown(
                choices=muscle_groups,
                sort_choices=False,
                max_choices=1,
            )
            message_menu = await inter.followup.send(
                "It looks this exercise has not yet been added to our database. We will add it now!\n\nWhat is the primary muscle group trained during this exercise?",
                components=menu_content,
                ephemeral=True,
            )
            selected_muscle_group = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            program_name = self.bot.cursor.execute(
                f"""SELECT program_name FROM custom_programs WHERE program_id = '{self.program_id}'"""
            )
            embed = disnake.Embed(title=f"{program_name} - Add Exercise")
            embed.add_field(
                name="Exercise Name", value=exercise_name, inline=False
            )
            embed.add_field(
                name="Primary Muscle Group",
                value=selected_muscle_group,
                inline=False,
            )
            embed.add_field(name="# of Sets", value=exercise_sets, inline=False)
            embed.add_field(name="# of Reps", value=exercise_reps, inline=False)
            embed.set_footer(text=f"Program ID: {self.program_id}")

            print("This is the program_id", self.program_id)
            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=self.program_id,
                exercise_cycle_day=self.workout_day,
            )

            print("Lenoo", len(fitness_program.exercises))

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
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            exercise_info_insert = (exercise_name, selected_muscle_group)

            self.bot.cursor.execute(
                """INSERT INTO exercises (  name,
                                                                muscle_group_one
                                                                ) VALUES (%s, %s)""",
                exercise_info_insert,
            )
            self.bot.db.commit()
            exercise_id = self.bot.cursor.execute(
                """SELECT exercise_id
                                    FROM exercises
                                    WHERE name = %s""",
                (exercise_name,),
            )

            exercise_id = util_func.sql_select_handler(
                bot=self.bot,
                res=exercise_id,
                fetch_type="fetchone",
            )
            print("Workout Day", self.workout_day)

            program_exercise_info = (
                self.program_id,
                exercise_id,
                self.workout_day,
                exercise_sets,
                exercise_reps,
                len(fitness_program.exercises),
            )

            self.bot.cursor.execute(
                """INSERT INTO program_exercises (program_id,
                                                                        exercise_id,
                                                                        exercise_cycle_day,
                                                                        exercise_target_sets,
                                                                        exercise_target_reps,
                                                                        exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
                program_exercise_info,
            )
            self.bot.db.commit()

            message, embed = await util_func.update_workout_embed(
                inter=inter,
                bot=self.bot,
                channel=inter.channel,
                exercise_cycle_day=self.workout_day,
                program_id=self.program_id,
            )

            await message.edit(embed=embed)

            await inter.followup.send(
                "Exercise successfully added.",
                ephemeral=True,
                delete_after=5,
            )

        else:
            button_exercise_options = []
            for i, exercise in enumerate(exercise_name_matches):
                button_component = disnake.ui.Button(
                    label=exercise,
                    style=disnake.ButtonStyle.secondary,
                    row=i + 1,
                    custom_id=exercise,
                )
                button_exercise_options.append(button_component)

            exercise_check = await inter.followup.send(
                content="Did you mean one of these exercises?",
                components=button_exercise_options,
            )

            def check(m):
                return m.channel == inter.channel

            interaction: disnake.MessageInteraction = await self.bot.wait_for(
                "button_click", check=check
            )
            print(interaction.data.custom_id)

            await exercise_check.delete()

            exercise_name = interaction.data.custom_id
            print("This is the program_id", self.program_id)
            fitness_program = FitnessProgram(
                bot=self.bot,
                program_id=self.program_id,
                exercise_cycle_day=self.workout_day,
            )

            print("Lenoo", len(fitness_program.exercises))

            program_name = self.bot.cursor.execute(
                f"""SELECT program_name FROM custom_programs WHERE program_id = '{self.program_id}'"""
            )
            embed = disnake.Embed(title=f"{program_name} - Add Exercise")
            embed.add_field(
                name="Exercise Name", value=exercise_name, inline=False
            )
            embed.add_field(name="# of Sets", value=exercise_sets, inline=False)
            embed.add_field(name="# of Reps", value=exercise_reps, inline=False)
            embed.set_footer(text=f"Program ID: {self.program_id}")

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
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            if confirm_addition == "No":
                pass
            else:
                print(exercise_name)
                exercise_id = self.bot.cursor.execute(
                    f"""SELECT exercise_id FROM exercises WHERE name = '{exercise_name}'"""
                )
                print(exercise_id)
                exercise_id = util_func.sql_select_handler(
                    res=exercise_id,
                    bot=self.bot,
                    fetch_type="fetchone",
                )
                print(exercise_id)

                cycle_day_num_exercises = len(fitness_program.exercises) + 1

                insert_info = (
                    self.program_id,
                    exercise_id,
                    self.workout_day,
                    exercise_sets,
                    exercise_reps,
                    cycle_day_num_exercises,
                )
                self.bot.cursor.execute(
                    """INSERT INTO program_exercises (program_id,
                                                                        exercise_id,
                                                                        exercise_cycle_day,
                                                                        exercise_target_sets,
                                                                        exercise_target_reps,
                                                                        exercise_order) VALUES (%s, %s, %s, %s, %s, %s)""",
                    insert_info,
                )
                self.bot.db.commit()
                print("Successs")
                message, embed = await util_func.update_workout_embed(
                    inter=inter,
                    bot=self.bot,
                    channel=inter.channel,
                    exercise_cycle_day=self.workout_day,
                    program_id=self.program_id,
                )

                await message.edit(embed=embed)

                await inter.followup.send(
                    "Exercise successfully added.",
                    ephemeral=True,
                    delete_after=5,
                )
