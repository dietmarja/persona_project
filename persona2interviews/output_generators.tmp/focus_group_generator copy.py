# File: output_generators/focus_group_generator.py

import random
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

        contributions = []
        last_speaker = None
        for i in range(self.num_contributions):
            if i == 0 or i == self.num_contributions - 1:
                current_persona = next(p for p in personas if "Discussion leader" in p['role'])
            else:
                current_persona = random.choice([p for p in personas if p != last_speaker])
            
            prompt = self.get_prompt(current_persona, i == 0, i == self.num_contributions - 1)
            
            conversation.append({"role": "user", "content": prompt})
            
            variation_factor = random.choice([0.1, 0.3, 0.5, 0.8, 1.0])  # More distinct variation
            current_max_tokens = int(self.max_tokens * variation_factor)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=conversation,
                max_tokens=current_max_tokens
            )
            
            contribution = response.choices[0].message.content.strip()
            contributions.append({"role": current_persona['role'], "content": contribution})
            conversation.append({"role": "assistant", "content": contribution})
            
            last_speaker = current_persona
            self.update_drift_factor()

        # Generate summary
        summary_prompt = "Summarize the key points of the discussion, focusing on the content and disregarding who said what or any rhetorical phrases. Provide a concise, factual summary."
        conversation.append({"role": "user", "content": summary_prompt})
        summary_response = self.client.chat.completions.create(
            model=self.model,
            messages=conversation,
            max_tokens=250
        )
        summary = summary_response.choices[0].message.content.strip()

        return contributions, personas, question, summary

    def get_prompt(self, persona, is_opening, is_closing):
        if is_opening:
            return f"As the discussion leader, provide a brief opening statement introducing the topic."
        elif is_closing:
            return f"As the discussion leader, summarize the key points and conclude the discussion."
        elif "Discussion leader" in persona['role']:
            if self.drift_factor > 0.7:
                return f"As the discussion leader, gently guide the conversation back to the main topic."
            else:
                return f"As the discussion leader, facilitate the discussion with a brief comment or question."
        elif persona.get('is_maverick'):
            return f"As {persona['role']}, provide a provocative or contrarian perspective. Use natural, spoken language. Vary your response length."
        else:
            return f"As {persona['role']}, {self.get_response_instruction()} Use natural, spoken language. Vary your response length. Sometimes provide detailed, specific information."

    def get_response_instruction(self):
        if random.random() < 0.6:  # 60% chance of no specific instruction
            return "contribute to the discussion."
        
        instructions = [
            "ask for clarification on a previous point",
            "share a specific, detailed personal experience related to the topic",
            "propose a unique solution or approach, going into technical details if appropriate",
            "play devil's advocate to a previous statement",
            "bring up a related subtopic for discussion, providing specific examples or data"
        ]
        return random.choice(instructions)

    def update_drift_factor(self):
        drift_change = random.uniform(-0.2, 0.2)
        self.drift_factor = max(0, min(1, self.drift_factor + drift_change))

def write_focus_group_results(conversation, personas, question, summary, output_file):
    with open(output_file, 'w') as f:
        f.write(f"Discussion on: {question}\n\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y')}\n\n")
        f.write("Focus Group Participants:\n")
        for persona in personas:
            maverick_mark = " (M)" if persona.get('is_maverick') else ""
            f.write(f"- {persona['role']}{maverick_mark}\n")
        f.write("\n" + "-" * 40 + "\n\n")
        for message in conversation:
            f.write(f"{message['role']}: {message['content']}\n\n")
        f.write("-" * 40 + "\n\n")
        f.write("Summary of Key Points:\n\n")
        f.write(summary)