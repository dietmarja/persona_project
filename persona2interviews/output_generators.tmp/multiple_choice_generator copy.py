# output_generators/multiple_choice_generator.py

import random

class MultipleChoiceResponseGenerator:
    def generate(self, processed_inputs, persona):
        responses = []
        for question in processed_inputs['questions']:
            response = self.generate_single_response(question, persona)
            responses.append(response)
        return responses

    def generate_single_response(self, question, persona):
        # Simulate choosing 1-4 options randomly
        num_choices = random.randint(1, 4)
        choices = [0, 0, 0, 0]
        for _ in range(num_choices):
            index = random.randint(0, 3)
            choices[index] = 1
        
        return {
            'persona_id': persona.get('id', 'unknown'),  # Use 'unknown' if 'id' is not present
            'question_id': question['Question ID'],
            'choices': choices
        }

