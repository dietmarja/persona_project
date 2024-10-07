# File: code/sub/get_output_generator.py

def get_output_generator(config):
    output_generator_config = config['output_generator']
    generator_type = output_generator_config['type']
    
    if generator_type == 'multiple_choice_generator':
        from output_generators.multiple_choice_generator import MultipleChoiceResponseGenerator
        return MultipleChoiceResponseGenerator()
    elif generator_type == 'free_text_generator':
        from output_generators.free_text_generator import FreeTextResponseGenerator
        model_config = config.get('model', {})
        model_name = model_config.get('name', 'gpt-3.5-turbo')
        max_tokens = model_config.get('max_tokens', 150)
        return FreeTextResponseGenerator(model=model_name, max_tokens=max_tokens)
    elif generator_type == 'focus_group_generator':
        from output_generators.focus_group_generator import FocusGroupResponseGenerator
        model_config = config.get('model', {})
        model_name = model_config.get('name', 'gpt-3.5-turbo')
        max_tokens = model_config.get('max_tokens', 500)
        return FocusGroupResponseGenerator(model=model_name, max_tokens=max_tokens)
    else:
        raise ValueError(f"Unknown output generator type: {generator_type}")