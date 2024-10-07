# File: code/main.py
import yaml
import sys
import os
# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from code.sub.main_function import main_llm_only, main_focus_group
from focus_group_simulator import FocusGroupSimulator, print_persona_pool


Then, in your Python code, you can load the API key from an environment variable:


def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    config['openai_api_key'] = os.getenv('OPENAI_API_KEY')
    
    return config

if __name__ == "__main__":  # Corrected this line
    config = load_config()
    mode = config.get('mode', 'llm_only')
    print(f"Mode: {mode}")
    
    if mode == 'llm_only':
        main_llm_only(config)
    elif mode == 'focus_group':
        focus_group_config = config['focus_group']
        persona_pool_file = focus_group_config.get('persona_pool_file')
        num_iterations = focus_group_config.get('num_iterations')
        num_mavericks = focus_group_config.get('num_mavericks')
        personas_config = focus_group_config.get('personas')
        
        print(f"Creating simulator with: {persona_pool_file}, {num_iterations}, {num_mavericks}")
        
        print("Debugging: Printing persona pool")
        print_persona_pool(persona_pool_file)
        
        simulator = FocusGroupSimulator(persona_pool_file, num_iterations, num_mavericks, personas_config)
        
        print("Created personas:")
        simulator.print_personas()
        
        print("Calling main_focus_group")
        main_focus_group(config, simulator)
    else:
        print(f"Unknown mode: {mode}")