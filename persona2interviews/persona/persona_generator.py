# File: persona/persona_generator.py

import random
from collections import defaultdict
import uuid
import random

class PersonaGenerator:
    def __init__(self, persona_templates, random_config=None, stratified_config=None):
        self.persona_templates = persona_templates
        self.random_config = random_config
        self.stratified_config = stratified_config

    def generate_personas(self, num_personas, sampling_method='predefined'):
        if sampling_method == 'predefined':
            personas = self._sample_predefined_personas(num_personas)
        elif sampling_method == 'random':
            personas = self._random_persona_sampling(num_personas)
        elif sampling_method == 'stratified':
            personas = self._stratified_persona_sampling(num_personas)
        else:
            raise ValueError(f"Unknown sampling method: {sampling_method}")
        
        # Add an 'id' to each persona
        for persona in personas:
            persona['id'] = str(uuid.uuid4())
        
        return personas

    def _sample_predefined_personas(self, num_personas):
        if num_personas > len(self.persona_templates):
            raise ValueError("Requested number of personas exceeds available templates")
        return random.sample(self.persona_templates, num_personas)

    def _random_persona_sampling(self, num_personas):
        if not self.random_config:
            raise ValueError("Random configuration is not provided")
        
        personas = []
        for _ in range(num_personas):
            persona = {}
            for attr, values in self.random_config.items():
                if isinstance(values, list):
                    persona[attr] = random.choice(values)
                elif isinstance(values, tuple) and len(values) == 2:
                    persona[attr] = random.randint(values[0], values[1])
                else:
                    persona[attr] = values
            personas.append(persona)
        return personas

    def _stratified_persona_sampling(self, num_personas):
        if not self.stratified_config:
            raise ValueError("Stratified configuration is not provided")
        
        # Implementation for stratified sampling
        # This is a placeholder and should be implemented based on your specific requirements
        return self._random_persona_sampling(num_personas)  # Fallback to random sampling for now