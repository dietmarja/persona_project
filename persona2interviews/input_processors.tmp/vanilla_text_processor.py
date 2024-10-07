# File: input_processors/vanilla_text_processor.py

import csv
from .base_processor import BaseInputProcessor

class VanillaTextProcessor:
    def __init__(self, question_file, instruction_file):
        self.question_file = question_file
        self.instruction_file = instruction_file
        self.instructions = self.read_instructions()
        self.questions = self.read_questions()
        
    def read_instructions(self):
        with open(self.instruction_file, 'r') as f:
            return '\n'.join(line.strip() for line in f if not line.strip().startswith('#'))
    
    def read_questions(self):
        questions = []
        with open(self.question_file, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                questions.append(row[0])  # Assuming questions are in the first column
        return questions

    def process(self):
        processed_inputs = []
        for question in self.questions:
            processed_input = {
                "instructions": self.instructions,
                "question": question
            }
            processed_inputs.append(processed_input)
        return processed_inputs