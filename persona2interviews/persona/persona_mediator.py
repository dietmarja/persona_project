class PersonaMediator:
    def __init__(self, persona):
        self.persona = persona

    def mediate_response(self, input_data):
        if not input_data:
            return None

        mediated_data = []
        for question in input_data:
            mediated_question = self._adjust_question_difficulty(question)
            mediated_data.append(mediated_question)

        return mediated_data

    def _adjust_question_difficulty(self, question):
        knowledge_level = self.persona['knowledge_level']
        original_difficulty = question['difficulty']

        if knowledge_level == 'high':
            adjusted_difficulty = min(original_difficulty + 2, 10)
        elif knowledge_level == 'medium':
            adjusted_difficulty = original_difficulty
        else:  # low knowledge level
            adjusted_difficulty = max(original_difficulty - 2, 1)

        adjusted_question = question.copy()
        adjusted_question['difficulty'] = adjusted_difficulty

        return adjusted_question