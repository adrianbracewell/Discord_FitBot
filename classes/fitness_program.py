from abc import ABC, abstractmethod
from dataclasses import dataclass
import mysql.connector
from mysql.connector import cursor
from classes.programmed_exercise import ProgrammedExercise
from classes.session import Session


class FitnessProgram:
    def __init__(self, bot, program_id, exercise_cycle_day=None, user_id=None):
        self.bot = bot
        self.program_id = program_id
        self.name = None
        self.program_length = None
        self.description = None
        self.program_type = None
        self.program_split_type = None
        self.program_exercises = []
        self.exercise_cycle_day = exercise_cycle_day
        self.user_id = user_id
        self.user_sessions = []

        if program_id:
            self.get_program_info(program_id=program_id)

        if user_id:
            self.load_user_sessions()

    @property
    def exercises(self):
        if not self.program_exercises:
            self.load_exercises()
        return self.program_exercises

    def get_program_info(self, program_id):
        query = """SELECT program_name,
                    microcycle_length,
                    program_description,
                    program_type,
                    split_type
                    FROM custom_programs
                    WHERE program_id = %s"""
        val = (program_id,)
        self.bot.cursor.execute(query, val)
        program_data = self.bot.cursor.fetchone()
        if program_data:
            self.name = program_data[0]
            self.program_length = program_data[1]
            self.program_description = program_data[2]
            self.program_type = program_data[3]
            self.program_split_type = program_data[4]

    def load_exercises(self):
        if not self.exercise_cycle_day:
            query = """SELECT exercise_id FROM program_exercises WHERE program_id = %s ORDER BY exercise_order"""
            val = (self.program_id,)
        else:
            query = """SELECT exercise_id FROM program_exercises WHERE program_id = %s AND exercise_cycle_day = %s ORDER BY exercise_order"""
            val = (self.program_id, self.exercise_cycle_day)
        self.bot.cursor.execute(query, val)
        exercise_data = self.bot.cursor.fetchall()
        print("here is the", self.exercise_cycle_day)
        if exercise_data:
            for exercise in exercise_data:
                self.program_exercises.append(
                    ProgrammedExercise(
                        bot=self.bot,
                        exercise_id=exercise[0],
                        program_id=self.program_id,
                        exercise_cycle_day=self.exercise_cycle_day,
                    )
                )

    def load_user_sessions(self):
        query = """
        SELECT session_id
        FROM sessions
        WHERE program_id = %s
        AND user_id = %s
        """
        val = (self.program_id, self.user_id)

        self.bot.cursor.execute(query, val)
        sessions_data = self.bot.cursor.fetchall()
        if sessions_data:
            for session in sessions_data:
                self.user_sessions.append(
                    Session(
                        bot=self.bot,
                        program_id=self.program_id,
                        session_id=session[0],
                        user_id=self.user_id,
                    )
                )
