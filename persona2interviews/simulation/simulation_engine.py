import importlib
from openai import OpenAI
from persona.persona_generator import generate_persona
from persona.persona_mediator import PersonaMediator
from code.json_to_csv_converter import convert_json_to_csv


class SimulationEngine:
    def __init__(self, config):
        self.config = config
        self.input_processor = self._load_processor(config['input_processor'])
        self.output_generator = self._load_generator(config['output_generator'])
        self.openai_client = OpenAI(api_key=config.get('openai_api_key'))

    def run_simulation(self):
        input_data = self.input_processor.process_input()
        if input_data is None:
            print("Error: No input data available. Simulation cannot proceed.")
            return

        personas = self._generate_personas()

        results = []
        for persona in personas:
            mediator = PersonaMediator(persona)
            processed_input = mediator.mediate_response(input_data)
            if processed_input is None:
                print(f"Warning: processed_input is None for persona {persona}")
                continue
            output = self.output_generator.generate_output(persona, processed_input)
            results.append({
                'persona': persona,
                'responses': output
            })

        if not results:
            print("Error: No results generated. Check if input data is being processed correctly.")
        else:
            json_file = self.config['output_path']
            self.output_generator.save_output(results, json_file)

            # Convert JSON to CSV
            csv_file = json_file.rsplit('.', 1)[0] + '.csv'
            convert_json_to_csv(json_file, csv_file)

    def _load_processor(self, processor_config):
        module = importlib.import_module(f"input_processors.{processor_config['type']}")
        processor_class = getattr(module, processor_config['class'])
        processor = processor_class()
        processor.load_input(processor_config['input_path'])
        return processor

    def _load_generator(self, generator_config):
        module = importlib.import_module(f"output_generators.{generator_config['type']}")
        generator_class = getattr(module, generator_config['class'])
        return generator_class()

# Generate a persona for each knowledge level
    def _generate_personas(self):
        personas = []
        persona_config = self.config['persona_generator']
        num_personas = persona_config['num_personas']
        knowledge_levels = persona_config['knowledge_levels']

        for _ in range(num_personas):
            for level in knowledge_levels:
                persona = generate_persona(self.openai_client, level)
                personas.append(persona)

        return personas

""""
# Generate only spicified number of persona
    def _generate_personas(self):
        personas = []
        persona_config = self.config['persona_generator']
        num_personas = persona_config['num_personas']
        knowledge_levels = persona_config['knowledge_levels']

        for _ in range(num_personas):
            for level in knowledge_levels:
                persona = generate_persona(self.openai_client, level)
                personas.append(persona)

        return personas
"""