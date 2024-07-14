from abc import ABC, abstractmethod
from dataclasses import dataclass
import mysql.connector
from mysql.connector import cursor
from classes.exercise import Exercise


class ProgrammedExercise(Exercise):
    def __init__(self, bot, exercise_id, program_id, exercise_cycle_day=None):
        super().__init__(bot, exercise_id, muscle_group=None)
        self.program_id = program_id
        self.sets = None
        self.reps = None
        self.rep_type = None
        self.session_order = None
        self.exercise_cycle_day = exercise_cycle_day
        self.programmed_exercise_dict = {}
        self.programmed_exercise_name = None

        if program_id:
            self.get_programmed_exercise(
                program_id=program_id, exercise_cycle_day=exercise_cycle_day
            )

    def get_programmed_exercise(self, program_id, exercise_cycle_day):

        if not exercise_cycle_day:
            query = """SELECT
                            exercise_target_sets,
                            exercise_target_reps,
                            exercise_rep_type,
                            exercise_order,
                            exercise_cycle_day
                            FROM program_exercises
                            WHERE exercise_id = %s
                            AND program_id = %s"""
            val = (self.exercise_id, program_id)
        else:
            query = """SELECT
                            exercise_target_sets,
                            exercise_target_reps,
                            exercise_rep_type,
                            exercise_order,
                            exercise_cycle_day
                            FROM program_exercises
                            WHERE exercise_id = %s
                            AND program_id = %s
                            AND exercise_cycle_day = %s"""
            val = (self.exercise_id, program_id, exercise_cycle_day)

        self.bot.cursor.execute(query, val)
        data = self.bot.cursor.fetchone()
        if data:
            self.sets = data[0]
            self.reps = data[1]
            self.rep_type = data[2]
            self.session_order = data[3]
            self.exercise_cycle_day = data[4]
            programmed_exercise_name = Exercise(
                bot=self.bot, exercise_id=self.exercise_id
            ).exercise_name
            self.programmed_exercise_dict[programmed_exercise_name] = {
                "id": self.exercise_id,
                "sets": data[0],
                "reps": data[1],
                "rep_type": data[2],
                "session_order": data[3],
                "cycle_day": self.exercise_cycle_day,
            }
