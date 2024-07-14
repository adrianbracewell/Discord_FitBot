import disnake
from disnake.ext import commands
import utils.functions as util_func
from classes.fitness_program import FitnessProgram
from .session_manager_buttons import SessionManagerButtons
from ..session_editor.session_editor_buttons import SessionEditorButtons

workout_exercise_dict = {}


class SessionManagerListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id not in [
            "Start Session",
            "Edit Session",
            "Delete Session",
            "My Sessions",
        ]:
            return

        if inter.component.custom_id == "Start Session":
            await inter.response.defer(ephemeral=True)
            try:
                program_id = util_func.get_embed_info(
                    message=inter.message, embed_properties=["program_id"]
                )[0]
                print("here gg", program_id)
            except:
                programs = self.bot.cursor.execute(
                    f"""SELECT program_id, program_name
                                    FROM custom_programs
                                    WHERE user_id = '{inter.author.id}'"""
                )

                programs = util_func.sql_select_handler(
                    res=programs, bot=self.bot, fetch_type="fetchall"
                )
                program_dict = util_func.detupler_to_dict(programs)
                print(program_dict)

                menu_content = await util_func.dropdown(
                    choices=list(program_dict.values()),
                )
                message_menu = await inter.followup.send(
                    "It looks like you have not set a current Program. Which program would you like to set to current?",
                    components=menu_content,
                    ephemeral=True,
                )
                selected_program = await util_func.get_dropdown_value(
                    bot=self.bot, message=message_menu
                )
                program_id = util_func.key_from_value(
                    selected_program, program_dict
                )
                await message_menu.delete()

            fitness_program = FitnessProgram(
                bot=self.bot, program_id=program_id
            )

            program_info = util_func.display_program(
                bot=self.bot, program_id=program_id
            )

            embed = disnake.Embed(
                title=f"Session Manager\n{fitness_program.name}",
                description=program_info,
            )
            embed.set_author(name=f"Program ID: {program_id}")

            await inter.message.edit(embed=embed)

            self.bot.cursor.execute(
                """SELECT session_id,
                                    program_id,
                                    cycle_day
                                    FROM sessions
                                    WHERE active = 1
                                    LIMIT 1"""
            )
            active_session = self.bot.cursor.fetchone()
            if active_session:
                active_session_id = active_session[0]
                active_program_id = active_session[1]
                active_cycle_day = active_session[2]
                fitness_program_name = FitnessProgram(
                    bot=self.bot, program_id=active_program_id
                ).name

                components = [
                    disnake.ui.Button(
                        label="Continue Active Session",
                        style=disnake.ButtonStyle.primary,
                        custom_id="Continue",
                    ),
                    disnake.ui.Button(
                        label="Start New Session",
                        style=disnake.ButtonStyle.success,
                        custom_id="Start New",
                    ),
                ]

                active_session_menu = await inter.followup.send(
                    f"It looks like you already have a currently active session for {fitness_program_name}. Do you wish to continue this active session or mark it complete and start a new session?",
                    components=components,
                )

                def check(m):
                    return m.channel == inter.channel

                interaction: disnake.MessageInteraction = (
                    await self.bot.wait_for("button_click", check=check)
                )

                active_session_action = interaction.data.custom_id
                await active_session_menu.delete()

                if active_session_action == "Continue":
                    message, embed = await util_func.update_session_embed(
                        inter=inter,
                        bot=self.bot,
                        exercise_cycle_day=active_cycle_day,
                        program_id=active_program_id,
                        session_id=active_session_id,
                    )

                    await inter.followup.send(
                        embed=embed, view=SessionEditorButtons()
                    )
                    return

            workout_days = fitness_program.program_length

            workout_days = [*range(1, workout_days + 1)]
            menu_content = await util_func.dropdown(
                choices=workout_days,
                sort_choices=True,
            )
            message_menu = await inter.followup.send(
                "For workout day would you like to start a session?",
                components=menu_content,
                ephemeral=True,
            )
            selected_day = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu
            )
            await message_menu.delete()

            session_date = util_func.get_now_datetime_int()
            print(session_date)

            self.bot.cursor.execute(
                """SELECT COUNT(session_id)
                                    FROM sessions"""
            )
            session_id = self.bot.cursor.fetchone()[0] + 1

            self.bot.cursor.execute(
                """INSERT INTO sessions (session_id, program_id, date_created, active, cycle_day) VALUES (%s, %s, %s, %s, %s)""",
                (session_id, program_id, session_date, 1, int(selected_day)),
            )

            self.bot.db.commit()

            workout_info, embed_title = util_func.display_workout(
                bot=self.bot,
                program_id=program_id,
                exercise_cycle_day=selected_day,
            )
            embed = disnake.Embed(
                title=f"Day {selected_day} - {fitness_program.name} Session",
                description=workout_info,
            )
            embed.set_author(
                name=f"Program ID: {program_id}\nSession ID: {session_id}"
            )

            await inter.followup.send(embed=embed, view=SessionEditorButtons())

        elif inter.component.custom_id == "Change Program":
            await inter.response.defer(ephemeral=True)
            programs = self.bot.cursor.execute(
                f"""SELECT program_id, program_name
                                    FROM custom_programs
                                    WHERE user_id = '{inter.author.id}'"""
            )

            programs = util_func.sql_select_handler(
                res=programs, bot=self.bot, fetch_type="fetchall"
            )
            program_dict = util_func.detupler_to_dict(programs)
            print(program_dict)

            menu_content = await util_func.dropdown(
                choices=list(program_dict.values()),
            )
            message_menu = await inter.followup.send(
                "To which program would you like to switch?",
                components=menu_content,
                ephemeral=True,
            )
            selected_program = await util_func.get_dropdown_value(
                bot=self.bot, message=message_menu
            )
            program_id = util_func.key_from_value(
                selected_program, program_dict
            )
            await message_menu.delete()

            fitness_program = FitnessProgram(
                bot=self.bot, program_id=program_id
            )

            program_info = util_func.display_program(
                bot=self.bot, program_id=program_id
            )

            embed = disnake.Embed(
                title=f"Session Manager\n{fitness_program.name}",
                description=program_info,
            )
            embed.set_author(name=f"Program ID: {program_id}")

            await inter.message.edit(embed=embed)


def setup(bot):
    bot.add_cog(SessionManagerListener(bot))
