# File: output_generators/free_text_generator.py

from .base_generator import BaseOutputGenerator
import openai

class FreeTextResponseGenerator(BaseOutputGenerator):
    def __init__(self, model, max_tokens):
        self.model = model
        self.max_tokens = max_tokens
        self.client = openai.OpenAI()

    def generate(self, input_data, persona):
        responses = []
        for input_item in input_data:
            response = self.generate_single_response(input_item, persona)
            responses.append(response)
        return responses

    def generate_single_response(self, input_item, persona):
        full_prompt = f"""
        Instructions: {input_item['instructions']}

        Question: {input_item['question']}

        Please answer as a person with the following characteristics:
        Description: {persona['description']}
        Knowledge Level: {persona['knowledge_level']}
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt}
            ],
            max_tokens=self.max_tokens
        )
        
        return {
            "persona": persona['description'],
            "question": input_item['question'],
            "response": response.choices[0].message.content.strip()
        }