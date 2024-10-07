# File: code/sub/main_function.py
from code.sub.perform_llm_analysis import perform_llm_analysis
from code.sub.perform_focus_group_simulation import perform_focus_group_simulation

def main_focus_group(config, simulator):
    print("Starting focus group simulation in main_focus_group")
    perform_focus_group_simulation(config, simulator)
    print("Focus group simulation completed in main_focus_group")
    
def main_llm_only(config):
    print("Starting LLM-only analysis")
    llm_config = config['llm_analysis']
    question_file = llm_config['question_file']
    instruction_file = llm_config['instruction_file']
    output_file = llm_config['output_file']
    
    with open(question_file, 'r') as f:
        question = f.read().strip()
    
    print(f"Question: {question}")
    perform_llm_analysis(question, instruction_file, output_file)
    print("LLM analysis completed")

def main_focus_group(config, simulator):
    print("Starting focus group simulation in main_focus_group")
    perform_focus_group_simulation(config, simulator)
    print("Focus group simulation completed in main_focus_group")