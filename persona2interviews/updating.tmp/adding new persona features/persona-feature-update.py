# In focus_group_simulator.py

class FocusGroupSimulator:
    def load_persona_pool(self):
        with open(self.config['simulation']['persona_file'], 'r') as f:
            reader = csv.DictReader(f)
            self.persona_pool = list(reader)
        
        # Verify all expected columns are present
        expected_columns = ['expert', 'role', 'background', 'gender', 'age', 'hobbies', 'style', 'new_feature1', 'new_feature2']  # Add your new features here
        for column in expected_columns:
            if column not in self.persona_pool[0]:
                raise ValueError(f"Expected column '{column}' not found in persona pool CSV")

    # Rest of the class...

# In code/sub/prompts.py

class Prompts:
    @staticmethod
    def generate_persona_prompt(persona):
        prompt = f"You are a {persona['age']} year old {persona['gender']} {persona['expert']} with a background in {persona['background']}. "
        prompt += f"Your hobbies include {persona['hobbies']} and your communication style is {persona['style']}. "
        
        # Add new features to the prompt
        if 'new_feature1' in persona:
            prompt += f"Your new_feature1 is {persona['new_feature1']}. "
        if 'new_feature2' in persona:
            prompt += f"Your new_feature2 is {persona['new_feature2']}. "
        
        return prompt

    # Rest of the class...
