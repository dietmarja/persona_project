
# File: MyPersonaFlex/input_processors/multiple_choice_processor.py

import csv

class MultipleChoiceProcessor:
    def __init__(self, question_file, instruction_file):
        self.question_file = question_file
        self.instruction_file = instruction_file
        self.questions = self.load_questions()
        self.instructions = self.load_instructions()

    def load_questions(self):
        questions = []
        with open(self.question_file, 'r') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                questions.append(row)
        return questions

    def load_instructions(self):
        with open(self.instruction_file, 'r') as f:
            return f.read()

    def process(self):
        return {
            'questions': self.questions,
            'instructions': self.instructions
        }