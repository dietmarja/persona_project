# File: input_processors/questionnaire_processor.py

import csv
from .base_processor import BaseInputProcessor

class MultipleChoiceProcessor(BaseInputProcessor):
    def __init__(self, question_file):
        self.question_file = question_file

        
        
    def load_input(self, input_path):
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                headers = next(reader)  # Skip the header row
                for row in reader:
                    if len(row) < 9:  # Ensure we have all required fields
                        print(f"Warning: Skipping malformed row: {row}")
                        continue
                    question = {
                        'id': row[0],
                        'text': row[1],
                        'options': {
                            'A': row[2],
                            'B': row[3],
                            'C': row[4],
                            'D': row[5]
                        },
                        'correct_options': set(row[6].split(',')),
                        'difficulty': int(row[7]),
                        'topic': row[8]
                    }
                    self.questions.append(question)
            print(f"Loaded {len(self.questions)} questions from {input_path}")
        except FileNotFoundError:
            print(f"Error: Input file not found at {input_path}")
        except Exception as e:
            print(f"Error loading input file: {str(e)}")

    def process_input(self):
        if not self.questions:
            print("Error: No questions loaded. Make sure to call load_input() before process_input().")
            return None

        processed_questions = []
        for question in self.questions:
            processed_question = self._process_question(question)
            if processed_question:
                processed_questions.append(processed_question)

        print(f"Processed {len(processed_questions)} questions")
        return processed_questions

    def _process_question(self, question):
        try:
            # Here you can add any additional processing logic
            # For example, you might want to validate the question format,
            # normalize difficulties, or apply any other transformations

            # For now, we'll just do a basic validation
            if not all(key in question for key in ['id', 'text', 'options', 'correct_options', 'difficulty', 'topic']):
                print(f"Warning: Question {question.get('id', 'Unknown')} is missing required fields")
                return None

            if question['difficulty'] < 0 or question['difficulty'] > 10:
                print(
                    f"Warning: Question {question['id']} has invalid difficulty {question['difficulty']}. Setting to 5.")
                question['difficulty'] = 5

            return question
        except Exception as e:
            print(f"Error processing question {question.get('id', 'Unknown')}: {str(e)}")
            return None