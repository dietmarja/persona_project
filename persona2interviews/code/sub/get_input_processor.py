# File: code/sub/get_input_processor.py

def get_input_processor(config):
    input_processor_config = config['input_processor']
    processor_type = input_processor_config['type']
    
    if processor_type == 'questionnaire':
        from input_processors.questionnaire_processor import QuestionnaireProcessor
        return QuestionnaireProcessor(config['question_file'])
    elif processor_type == 'vanilla_text':
        from input_processors.vanilla_text_processor import VanillaTextProcessor
        return VanillaTextProcessor(config['question_file']['vanilla_text'], config['instruction_file'])
    elif processor_type == 'focus_group':
        from input_processors.focus_group_processor import FocusGroupProcessor
        return FocusGroupProcessor(config['question_file']['focus_group'], config['instruction_file'])
    else:
        raise ValueError(f"Unknown input processor type: {processor_type}")