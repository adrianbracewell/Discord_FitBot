from abc import ABC, abstractmethod
from dataclasses import dataclass
import mysql.connector
from mysql.connector import cursor
from classes.programmed_exercise import ProgrammedExercise


class SessionExercise(ProgrammedExercise):
    def __init__(
        self,
        bot,
        session_id,
        exercise_id,
        program_id,
        exercise_cycle_day=None,
    ):
        super().__init__(bot, exercise_id, program_id, exercise_cycle_day=None)
        self.bot = bot
        self.program_id = program_id
        self.exercise_id = exercise_id
        self.session_id = session_id
        self.current_set_count = None
        self.session_set_info = {}
        self.last_session_info = {}
        self.exercise_cycle_day = exercise_cycle_day

        if session_id:
            self.get_current_set_count()
            self.get_session_exercise_info()
        if exercise_cycle_day:
            self.get_last_session_exercise_info()

    def get_current_set_count(self):
        query = """SELECT COUNT(exercise_id)
                    FROM session_exercises
                    WHERE session_id = %s
                    AND exercise_id = %s"""
        val = (self.session_id, self.exercise_id)
        self.bot.cursor.execute(query, val)
        session_exercise_info = self.bot.cursor.fetchone()
        if session_exercise_info:
            self.current_set_count = session_exercise_info[0]

    def get_session_exercise_info(self):
        query = """SELECT set_order, reps, amount
                        FROM session_exercises
                        WHERE session_id = %s
                        AND exercise_id = %s
                        ORDER BY set_order"""
        val = (self.session_id, self.exercise_id)
        self.bot.cursor.execute(query, val)
        exercise_info_data = self.bot.cursor.fetchall()
        if exercise_info_data:
            print(exercise_info_data)
            for exercise_set in exercise_info_data:
                self.session_set_info[exercise_set[0]] = {
                    "set_reps": exercise_set[1],
                    "set_load": exercise_set[2],
                }

    def get_last_session_exercise_info(self):
        query = """SELECT set_order, reps, amount
                        FROM session_exercises
                        WHERE session_id = (SELECT session_id FROM sessions WHERE cycle_day = %s ORDER BY date_created DESC LIMIT 1 OFFSET 1)
                        AND exercise_id = %s
                        ORDER BY set_order"""
        val = (self.exercise_cycle_day, self.exercise_id)
        self.bot.cursor.execute(query, val)
        exercise_info_data = self.bot.cursor.fetchall()
        if exercise_info_data:
            print(exercise_info_data)
            for exercise_set in exercise_info_data:
                self.last_session_info[exercise_set[0]] = {
                    "past_set_reps": exercise_set[1],
                    "past_set_load": exercise_set[2],
                }
