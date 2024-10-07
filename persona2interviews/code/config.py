import yaml
from openai import OpenAI

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Set up OpenAI client
    if 'openai_api_key' in config:
        OpenAI.api_key = config['openai_api_key']
    
    return config
