# File: output_generators/focus_group_generator.py

import random
import openai
from datetime import datetime

class FocusGroupResponseGenerator:
    def __init__(self, model="gpt-3.5-turbo", max_tokens=500):
        self.model = model
        self.max_tokens = max_tokens
        self.client = openai.OpenAI()

    def generate(self, processed_inputs, config):
        question = processed_inputs['question']
        instructions = processed_inputs.get('instructions', '')
        
        # Use personas from config instead of processed_inputs
        personas = config.get('personas', [])
        if not personas:
            raise ValueError("No personas found in the configuration")

        non_leader_personas = [p for p in personas if "Discussion leader" not in p['role']]
        maverick = random.choice(non_leader_personas)
        maverick['is_maverick'] = True

        conversation = [
            {"role": "system", "content": "You are simulating a focus group discussion. Generate diverse responses varying in length, but limit to a maximum of 10 sentences. Participants should often react directly to each other. Use opening phrases sparingly, only 40-60% of the time. One participant is a maverick who voices provocative statements. The discussion leader should guide and summarize occasionally."},
            {"role": "user", "content": f"The topic of discussion is: {question}\n\nInstructions: {instructions}"}
        ]

        all_outputs = []
        for _ in range(len(personas) * 2):  # Each persona speaks twice on average
            current_persona = random.choice(personas)
            prompt = self.get_prompt(current_persona, maverick)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation + [{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            
            output = {
                "role": current_persona['role'],
                "content": response.choices[0].message.content
            }
            all_outputs.append(output)
            conversation.append({"role": "assistant", "content": output['content']})

        # Generate summary
        summary_prompt = "Summarize the key points of the discussion, focusing on the content and disregarding who said what or any rhetorical phrases. Provide a concise, factual summary."
        summary_response = self.client.chat.completions.create(
            model=self.model,
            messages=conversation + [{"role": "user", "content": summary_prompt}],
            max_tokens=250
        )
        summary = summary_response.choices[0].message.content

        return all_outputs, personas, question, summary

    def get_prompt(self, persona, maverick):
        if persona.get('is_maverick'):
            return f"As {persona['role']}, who is a maverick, provide a provocative or contrarian perspective. Use natural, spoken language. Vary your response length."
        elif "Discussion leader" in persona['role']:
            return f"As the {persona['role']}, guide the discussion or summarize key points. Be brief and neutral."
        else:
            return f"As {persona['role']}, contribute to the discussion. Use natural, spoken language. Vary your response length. Sometimes provide detailed, specific information."

# You may need to implement write_focus_group_results function here or import it