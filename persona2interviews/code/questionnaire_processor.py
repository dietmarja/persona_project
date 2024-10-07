# File: input_processors/questionnaire_processor.py

import csv
from .base_processor import InputProcessor

class QuestionnaireProcessor(InputProcessor):
    def __init__(self, questionnaire_file):
        self.questionnaire_file = questionnaire_file
        self.questions = self.load_questions()

    def load_questions(self):
        questions = []
        with open(self.questionnaire_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                questions.append({
                    'id': row.get('id', ''),
                    'text': row.get('question', ''),
                    'options': [
                        row.get('option_a', ''),
                        row.get('option_b', ''),
                        row.get('option_c', ''),
                        row.get('option_d', '')
                    ]
                })
        return questions

    def process(self):
        processed_questions = []
        for question in self.questions:
            processed_question = {
                'id': question['id'],
                'text': question['text'],
                'options': [option for option in question['options'] if option]
            }
            processed_questions.append(processed_question)
        return processed_questions

    def get_question_by_id(self, question_id):
        for question in self.questions:
            if question['id'] == question_id:
                return question
        return None

    def get_all_questions(self):
        return self.questions