# File: input_processors/focus_group_processor.py

import csv

class FocusGroupProcessor:
    def __init__(self, question_file, instruction_file):
        self.question_file = question_file
        self.instruction_file = instruction_file
        self.question = self.load_question()
        self.instructions = self.load_instructions()

    def load_question(self):
        with open(self.question_file, 'r') as f:
            reader = csv.reader(f)
            # Assuming the question is in the first row, first column
            return next(reader)[0]

    def load_instructions(self):
        with open(self.instruction_file, 'r') as f:
            return f.read()

    def process(self):
        return {
            'question': self.question,
            'instructions': self.instructions
        }