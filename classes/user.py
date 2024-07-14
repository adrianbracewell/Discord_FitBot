from abc import ABC, abstractmethod
from dataclasses import dataclass
import mysql.connector
from mysql.connector import cursor
from .session_exercise import SessionExercise
from .fitness_program import FitnessProgram


class User:
    def __init__(self, bot, user_id):
        self.bot = bot
        self.user_id = str(user_id)
        self.weight = None
        self.measurements = {}
        self.active_session_id = None
        self.active_program_id = None
        self.user_programs = []

    @property
    def programs(self):
        if not self.user_programs:
            self.get_user_programs()
        return self.user_programs

    def get_user_programs(self):
        query = """SELECT program_id
                 FROM custom_programs
                 WHERE user_id = %s"""
        val = (self.user_id,)
        print(val)

        self.bot.cursor.execute(query, val)
        program_ids = self.bot.cursor.fetchall()
        print(program_ids)
        if program_ids:
            for program_id in program_ids:
                self.user_programs.append(
                    FitnessProgram(bot=self.bot, program_id=program_id[0])
                )
