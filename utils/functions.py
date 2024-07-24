import disnake
import math
from mysql.connector import cursor
from difflib import get_close_matches
from classes.session_exercise import SessionExercise
from classes.fitness_program import FitnessProgram
from datetime import datetime
import time

description_dict = {
    'Bro Split': 'Each major muscle group is trained once per microcycle',
    'Full Body': 'Major muscle groups are trained within the same workout multiples time across a microcycle',
    'Push-Pull-Legs': 'Workouts are divided by pushing, pulling, and lower-body-emphasis movements',
}


async def get_dropdown_value(bot, message: disnake.Message=None, return_list=False) -> str | list[str]:
    async def reveal_choices(inter):
        return inter

    def check(inter: disnake.MessageInteraction):
        return inter.message.id == message.id

    inter: disnake.MessageInteraction = await bot.wait_for('message_interaction', check=check, timeout=60)

    value = await reveal_choices(inter=inter)
    if return_list is True:
        return value.data.values
    else:
        return value.data.values[0]


async def dropdown(choices: list, sort_choices=False, 
                   max_choices=1, min_choices=1) -> list[str]:
    if sort_choices is True:
        choices.sort()

    if (len(choices) % 25) != 0:
        num_menus = math.ceil(len(choices) / 25)
    else:
        num_menus = math.ceil(len(choices) / 25)

    all_quarters = [[]*num_menus]

    for e in choices:
        for j in all_quarters:
            if len(j) == 25:
                continue
            else:
                j.append(disnake.SelectOption(label=e, value=e))
                break

    choices_selection_list = []
    for quarter in all_quarters:
        first_letter = str(quarter[0].label)[0].upper()
        last_letter = str(quarter[-1].label)[0].upper()
        placeholder_text = f'Options: {first_letter} - {last_letter}'
        choices_selection_list.append(disnake.ui.ActionRow(disnake.ui.StringSelect(options=quarter,
                                                                                   placeholder=placeholder_text, max_values=max_choices,
                                                                                   min_values=min_choices)))
    return choices_selection_list


def sql_select_handler(res, bot, fetch_type: str):
    if fetch_type not in ['fetchone', 'fetchall']:
        return "Invalid fetch_type parameter"
    if fetch_type == 'fetchone':
        res = bot.cursor.fetchone()
    else:
        res = bot.cursor.fetchall()
    result = None
    if res is None:
        pass
    elif res == [] or res == ():
        pass
    elif isinstance(res[0], tuple) is False:
        if len(res) > 1:
            result = [x for x in res]
        else:
            result = res[0]
    else:
        # ZIP here?
        if len(res[0]) > 1:
            result = res
        else:
            result = [x[0] for x in res]
    return result


def detupler_to_dict(list_of_tuples):
    new_dict = {}
    for tup in list_of_tuples:
        new_dict[tup[0]] = tup[1]
    return new_dict


def key_from_value(value, dictionary: dict):
    for k, v in dictionary.items():
        if value == v:
            return k
    return "Corresponding key not found for value."


def display_program(bot, program_id):
    exercise_info = bot.cursor.execute(f"""SELECT exercises.name,
                       exercise_cycle_day,
                       exercise_weekday,
                       exercise_target_sets,
                       exercise_target_reps,
                       exercise_rep_type
                       FROM program_exercises
                       INNER JOIN exercises ON program_exercises.exercise_id = exercises.exercise_id
                       WHERE program_id = '{program_id}'""")
    exercise_info = sql_select_handler(res=exercise_info, bot=bot, fetch_type="fetchall")

    program_info = bot.cursor.execute(f"""SELECT program_name,
                                  microcycle_length,
                                  program_description,
                                  program_type
                                  FROM custom_programs
                                  WHERE program_id = '{program_id}'""")
    program_info = sql_select_handler(res=program_info, bot=bot, fetch_type="fetchone")

    if program_info:
        microcycle_length = int(program_info[1])

    training_days = bot.cursor.execute(f"""SELECT DISTINCT exercise_cycle_day
                                   FROM program_exercises
                                   WHERE program_id = '{program_id}'""")
    training_days = sql_select_handler(res=training_days, bot=bot, fetch_type="fetchall")
    if training_days is None:
        embed_text = 'Looks like no exercises have been added yet! Click **Edit Workouts** to add some!'
    else:
        training_days.sort()

        training_days_dict = {}

        for training_day in training_days:
            muscle_groups = bot.cursor.execute(f"""SELECT DISTINCT muscle_group_one
                                        FROM exercises
                                        WHERE exercise_id in (SELECT exercise_id
                                                                FROM program_exercises
                                                                WHERE program_id = '{program_id}'
                                                                AND exercise_cycle_day = '{training_day}')""")
            muscle_groups = sql_select_handler(res=muscle_groups, bot=bot, fetch_type="fetchall")
            training_days_dict[int(training_day)] = muscle_groups
            print(muscle_groups)

        embed_text = []
        microcycle_days = [*range(1, microcycle_length+1)]
        print(microcycle_days)
        print(list(training_days_dict.keys()))
        for day in microcycle_days:
            if day not in list(training_days_dict.keys()):
                embed_text.append(f"**Day {day} - Rest**")
            else:
                for k, v in training_days_dict.items():
                    if k == day:
                        embed_text.append(f"**Day {k}**\n{'\n'.join(v)}")
        embed_text = '\n\n'.join(embed_text)

    return embed_text


def display_workout(bot, program_id, exercise_cycle_day):
    exercise_info = bot.cursor.execute(f"""SELECT exercises.name,
                       exercise_target_sets,
                       exercise_target_reps,
                       exercise_rep_type
                       FROM program_exercises
                       INNER JOIN exercises ON program_exercises.exercise_id = exercises.exercise_id
                       WHERE program_id = '{program_id}'
                       AND exercise_cycle_day = '{exercise_cycle_day}'
                       ORDER BY program_exercises.exercise_order""")
    exercise_info = sql_select_handler(res=exercise_info, bot=bot, fetch_type="fetchall")
    if exercise_info is None:
        embed_text = 'It looks like this day is current a **Rest Day**! Click **Edit Exercises** and add some exercises to make this a workout day!'
        title = ' - Rest Day'
    else:
        embed_text = []
        for exercise in exercise_info:
            exercise_str = f"{exercise[0]} - {exercise[1]}x{exercise[2]} ({exercise[3]})"
            embed_text.append(exercise_str)

        embed_text = '\n\n'.join(embed_text)
        title = ' - Edit Workout'
    return embed_text, title


def get_embed_info(message: disnake.Message, embed_properties: list):
    valid_properties = ['embed', 'title', 'footer', 'program_id', 'workout_day', 'session_id']
    for embed_property in embed_properties:
        if embed_property not in valid_properties:
            raise ValueError("Invalid embed property in list.")

    requested_properties = []
    for embed_property in embed_properties:
        if embed_property == 'embed':
            embed_info = [embed for embed in message.embeds][0]
            requested_properties.append(embed_info)
        elif embed_property == 'title':
            embed_info = [embed.title for embed in message.embeds][0]
            requested_properties.append(embed_info)
        elif embed_property == 'footer':
            embed_info = [embed.footer for embed in message.embeds][0]
            requested_properties.append(embed_info)
        elif embed_property == 'program_id':
            embed_author = [embed.author for embed in message.embeds][0]
            embed_info = embed_author.name.split()[2]
            requested_properties.append(embed_info)
        elif embed_property == 'workout_day':
            embed_title = [embed.title for embed in message.embeds][0]
            embed_info = int(embed_title.split()[1])
            requested_properties.append(embed_info)
        elif embed_property == 'session_id':
            embed_author = [embed.author for embed in message.embeds][0]
            embed_info = embed_author.name.split()[5]
            requested_properties.append(embed_info)
    return tuple(requested_properties)


def get_col_val_matches(bot, word_to_match: str, tbl_name: str, col_name: str, constraint_col_name: str, constraint_col_val):
    select_statement = f"SELECT {col_name} FROM {tbl_name}"
    if constraint_col_name is not None:
        constraint_statement = f"WHERE {
            constraint_col_name} = '{constraint_col_val}'"
        select_statement = ' '.join([select_statement, constraint_statement])
    print(select_statement)

    patterns = bot.cursor.execute(select_statement)
    patterns = sql_select_handler(
        res=patterns, bot=bot, fetch_type='fetchall')

    close_matches = get_close_matches(
        word=word_to_match, possibilities=patterns, n=10, cutoff=0.7)

    return close_matches


def levenshtein_distance(
        bot, word_to_match: str,
        tbl_name: str, col_name: str,
        constraint_col_name, constraint_col_val):
    select_statement = f"SELECT {col_name} FROM {tbl_name}"
    if constraint_col_name is not None:
        constraint_statement = f"WHERE {
            constraint_col_name} = '{constraint_col_val}'"
        select_statement = ' '.join([select_statement, constraint_statement])
    print(select_statement)

    patterns = bot.cursor.execute(select_statement)
    patterns = sql_select_handler(
        res=patterns, bot=bot, fetch_type='fetchall')

    len_word = len(word_to_match)
    matches = {}
    for pattern in patterns:
        len_pattern = len(pattern)
        dp = [[0 for _ in range(len_pattern + 1)] for _ in range(len_word + 1)]

    # Initialize the first row and column with values from 0 to m and 0 to n respectively
        for i in range(len_word + 1):
            dp[i][0] = i
        for j in range(len_pattern + 1):
            dp[0][j] = j

        # Fill the matrix using dynamic programming to compute edit distances
        for i in range(1, len_word + 1):
            for j in range(1, len_pattern + 1):
                if word_to_match[i - 1] == pattern[j - 1]:
                    # Characters match, no operation needed
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    # Characters don't match, choose minimum cost among insertion, deletion, or substitution
                    dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1]
                                       [j], dp[i - 1][j - 1])

        # Return the edit distance between the strings
        distance = dp[len_word][len_pattern]
        if distance < 4:
            matches[distance] = pattern
            print(matches)
    dict_keys = list(matches.keys())
    dict_keys.sort()
    matches = {i: matches[i] for i in dict_keys}
    return list(matches.values())[:4]


def weekdays_to_bit(weekdays: list, weekday_bitfield_dict: dict):
    bit_sum = 0
    for weekday in weekdays:
        bit_sum += weekday_bitfield_dict[weekday]
    return bit_sum


def bit_to_weekdays(bit_val, weekday_bitfield_dict: dict):
    assigned_bit_values = list(weekday_bitfield_dict.values())
    assigned_bit_values.sort(reverse=True)
    weekdays = []
    counter = bit_val
    for assigned_bit in assigned_bit_values:
        diff = counter - assigned_bit
        if diff < 0:
            continue
        elif diff > 0:
            weekdays.insert(0, key_from_value(assigned_bit, weekday_bitfield_dict))
            counter = diff
        else:
            weekdays.insert(0, key_from_value(assigned_bit, weekday_bitfield_dict))
            break
    return weekdays


async def update_workout_embed(inter: disnake.Interaction, bot, channel: disnake.TextChannel, exercise_cycle_day,
                               program_id):
    channel_history = await inter.channel.history(limit=5).flatten()
    for message in channel_history:
        if len(message.embeds) != 0 and (message.embeds[0].title == f'Day {exercise_cycle_day} - Edit Workout' or message.embeds[0].title == f'Day {exercise_cycle_day} - Rest Day'):
            message_to_edit = message
            break
    workout_info, title = display_workout(bot=bot,
                                          program_id=program_id,
                                          exercise_cycle_day=exercise_cycle_day)
    embed = disnake.Embed(title=f"Day {exercise_cycle_day}{title}",
                          description=workout_info)
    embed.set_author(name=f'Program ID: {program_id}')

    return message_to_edit, embed


def display_session_workout(bot, program_id, exercise_cycle_day, session_id):

    fitness_program = FitnessProgram(bot=bot, program_id=program_id, exercise_cycle_day=exercise_cycle_day)

    session_info = []
    for programmed_exercise in fitness_program.exercises:
        session_exercise = SessionExercise(bot=bot, session_id=session_id,
                                           exercise_id=programmed_exercise.exercise_id,
                                           program_id=program_id
                                           )

        exercise_name = programmed_exercise.exercise_name
        exercise_programmed_sets = programmed_exercise.sets
        exercise_programmed_reps = programmed_exercise.reps
        exercise_rep_type = programmed_exercise.rep_type

        header_text = f"__**{exercise_name} - {exercise_programmed_sets}x{
            exercise_programmed_reps} ({exercise_rep_type})**__"

        if not session_exercise:
            session_text = None

        else:
            exercise_session_info = session_exercise.session_set_info
            session_text = []
            for set_num, set_info in exercise_session_info.items():
                set_str = f" Set {set_num} - {set_info['set_reps']} reps @ {set_info['set_load']}lbs"
                session_text.append(set_str)

        if not session_text:
            exercise_text = header_text
        else:
            if exercise_programmed_sets == len(session_text):
                header_text = ':white_check_mark: ' + header_text

            session_text = '\n'.join(session_text)
            exercise_text = '\n'.join([header_text, session_text])
        session_info.append(exercise_text)

    session_text = '\n\n'.join(session_info)

    return session_text


def get_now_datetime_int():
    now = datetime.now()
    now = now.strftime('%Y-%m-%d %H:%M:%S')
    print(type(now))
    return now

# def datetime_int_to_str(timestamp):
#     time_stamp_format = '%Y-%m-%d %H:%M:%S'
#     date_format = '%m%d%Y'
#     dt_obj = datetime.strptime(timestamp, time_stamp_format)
#     return 


async def update_session_embed(bot, inter: disnake.Interaction,program_id,
                               exercise_cycle_day, session_id):
    channel_history = await inter.channel.history(limit=1).flatten()
    for message in channel_history:
        message_to_edit = message
        break
    program_name = FitnessProgram(bot=bot, program_id=program_id,
                                  exercise_cycle_day=exercise_cycle_day).name

    workout_info = display_session_workout(bot=bot,
                                           program_id=program_id,
                                           exercise_cycle_day=exercise_cycle_day,
                                           session_id=session_id)
    embed = disnake.Embed(title=f"Day {exercise_cycle_day} - {program_name} Session",
                          description=workout_info)
    embed.set_author(name=f'Program ID: {program_id}\nSession ID: {session_id}')

    return message_to_edit, embed

def post_session_embed(bot, inter: disnake.Interaction,program_id,
                               exercise_cycle_day, session_id):
    program_name = FitnessProgram(bot=bot, program_id=program_id,
                                  exercise_cycle_day=exercise_cycle_day).name

    workout_info = display_session_workout(bot=bot,
                                           program_id=program_id,
                                           exercise_cycle_day=exercise_cycle_day,
                                           session_id=session_id)
    embed = disnake.Embed(title=f"Day {exercise_cycle_day} - {program_name} Session",
                          description=workout_info)
    embed.set_author(name=f'Program ID: {program_id}\nSession ID: {session_id}')

    return embed
