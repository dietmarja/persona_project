# code/sub/chart_utilities.py

def format_persona_name(name):
    if name.lower() == 'no persona':
        return "Plain LLM"
    
    words = name.split()
    formatted_words = []
    for word in words:
        if word.lower() == 'ai':
            formatted_words.append('AI')
        elif word.lower() in ['and', 'of', 'in', 'at', 'the', 'for', 'to']:
            formatted_words.append(word.lower())
        else:
            formatted_words.append(word.capitalize())
    
    return ' '.join(formatted_words)