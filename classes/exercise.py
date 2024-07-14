from abc import ABC, abstractmethod
from dataclasses import dataclass
import mysql.connector
from mysql.connector import cursor


class Exercise:
    def __init__(
        self,
        bot,
        exercise_id=None,
        exercise_name=None,
        muscle_group=None,
    ):
        self.bot = bot
        self.exercise_name = exercise_name
        self.exercise_id = exercise_id
        self.muscle_group = muscle_group
        self.id_name_dict = {}

        if exercise_id:
            self.get_exercise_from_id(exercise_id=exercise_id)
        elif exercise_name:
            self.get_exercise_from_name(exercise_name=exercise_name)

    def get_exercise_from_id(self, exercise_id):

        query = "SELECT name, muscle_group_one FROM exercises WHERE exercise_id = %s"
        self.bot.cursor.execute(query, (exercise_id,))
        data = self.bot.cursor.fetchone()
        if data:
            self.exercise_id = exercise_id
            self.exercise_name = data[0]
            self.muscle_group = data[1]
            self.id_name_dict[exercise_id] = data[0]

    def get_exercise_from_name(self, exercise_name):

        query = "SELECT exercise_id, muscle_group_one FROM exercises WHERE name = %s"
        self.bot.cursor.execute(query, (exercise_name,))
        data = self.bot.cursor.fetchone()
        if data:
            self.exercise_id = data[0]
            self.exercise_name = exercise_name
            self.muscle_group = data[1]
            self.id_name_dict[self.exercise_id] = self.exercise_name
