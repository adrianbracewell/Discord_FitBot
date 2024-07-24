from abc import ABC, abstractmethod
from dataclasses import dataclass
import mysql.connector
from mysql.connector import cursor
from classes.session_exercise import SessionExercise


class Session:
    def __init__(self, bot, session_id, program_id, user_id):
        self.program_id = program_id
        self.bot = bot
        self.session_id = session_id
        self.session_date = None
        self.session_duration = None
        self.programmed_session_exercises = []
        self.session_notes = None
        self.user_id = user_id
        self.cycle_day = None
        if self.session_id:
            self.get_session_info()

    @property
    def session_exercises(self):
        if not self.programmed_session_exercises:
            self.get_session_exercises()
        return self.programmed_session_exercises

    def get_session_exercises(self):
        query = """SELECT exercise_id, reps, amount, set_order
                 FROM session_exercises
                 WHERE session_id = %s
                 and program_id = %s
                 and user_id = %s"""
        val = (self.session_id, self.program_id, self.user_id)

        self.bot.cursor.execute(query, val)
        session_exercise_data = self.bot.cursor.fetchall()
        if session_exercise_data:
            for _ in session_exercise_data:
                self.programmed_session_exercises.append(SessionExercise)

    def get_session_info(self):
        query = """SELECT date_created,
                        session_minutes,
                        session_notes,
                        cycle_day
                        FROM sessions
                        WHERE session_id = %s
                        AND program_id = %s
                        AND user_id = %s"""
        val = (self.session_id, self.program_id, self.user_id)

        self.bot.cursor.execute(query, val)
        session_info = self.bot.cursor.fetchone()
        if session_info:
            self.session_date = session_info[0]
            self.session_duration = session_info[1]
            self.session_notes = session_info[2]
            self.cycle_day = session_info[3]
