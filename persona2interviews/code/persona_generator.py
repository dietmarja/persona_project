import json
import random
from openai import OpenAI

def load_traits(file_path='persona_traits.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_persona(client, knowledge_level, traits_file='persona_traits.json'):
    traits = load_traits(traits_file)
    
    prompt = f"Create a persona with {knowledge_level} AI knowledge. Describe their background and current role in 2-3 sentences."
    
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    
    persona = {
        "description": completion.choices[0].message.content.strip(),
        "knowledge_level": knowledge_level
    }
    
    # Assign job
    persona['job'] = random.choice(traits['jobs'][knowledge_level])
    
    # Assign hobbies
    if knowledge_level == 'high':
        persona['hobbies'] = random.sample(traits['hobbies']['ai'], 2) + random.sample(traits['hobbies']['general'], 1)
    elif knowledge_level == 'medium':
        persona['hobbies'] = random.sample(traits['hobbies']['ai'], 1) + random.sample(traits['hobbies']['general'], 2)
    else:
        persona['hobbies'] = random.sample(traits['hobbies']['general'], 3)
    
    return persona

def main():
    client = OpenAI()  # Make sure to set up your OpenAI API key
    
    knowledge_levels = ['high', 'medium', 'low']
    
    for level in knowledge_levels:
        persona = generate_persona(client, level)
        print(f"Generated persona with {level} knowledge:")
        print(f"Description: {persona['description']}")
        print(f"Job: {persona['job']}")
        print(f"Hobbies: {', '.join(persona['hobbies'])}")
        print()

if __name__ == "__main__":
    main()