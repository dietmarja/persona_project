# COMPLETE FILE CONTENT
# File: code/sub/perform_llm_analysis.py

import openai
from typing import Dict, Any, List

def perform_analysis(conversation_data: List[Dict[str, str]], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform analysis on the focus group conversation data using LLM.
    
    :param conversation_data: List of dictionaries containing the conversation data
    :param config: Configuration dictionary containing API keys and other settings
    :return: Dictionary containing analysis results
    """
    # Ensure OpenAI API key is set
    openai.api_key = config['openai_api_key']
    
    # Prepare the conversation for analysis
    conversation_text = "\n".join([f"{turn['speaker']}: {turn['text']}" for turn in conversation_data])
    
    # Prepare the prompt for the LLM
    prompt = f"""
    Analyze the following focus group conversation about {config['topic']}:

    {conversation_text}

    Please provide:
    1. A summary of the main points discussed
    2. Key insights or themes that emerged
    3. Any notable agreements or disagreements among participants
    4. Suggestions for further exploration based on the discussion
    """

    try:
        # Make API call to OpenAI
        response = openai.ChatCompletion.create(
            model=config['model_name'],
            messages=[
                {"role": "system", "content": "You are an AI assistant skilled in analyzing focus group discussions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract and structure the analysis
        analysis_text = response.choices[0].message['content'].strip()
        
        # Here you might want to further process the analysis_text
        # For simplicity, we'll return it as is
        analysis_results = {
            "raw_analysis": analysis_text,
            "model_used": config['model_name'],
            "topic": config['topic']
        }

        return analysis_results

    except Exception as e:
        print(f"An error occurred during LLM analysis: {str(e)}")
        return {"error": str(e)}

# If you need to test the function independently, you can add:
if __name__ == "__main__":
    # Test data
    test_conversation = [
        {"speaker": "Moderator", "text": "What are your thoughts on AI's impact on jobs?"},
        {"speaker": "Participant1", "text": "I think AI will create new job opportunities."},
        {"speaker": "Participant2", "text": "I'm worried AI might replace many existing jobs."}
    ]
    test_config = {
        "openai_api_key": "your-api-key-here",
        "model_name": "gpt-3.5-turbo",
        "topic": "AI's impact on the job market"
    }
    
    # Run test analysis
    test_results = perform_analysis(test_conversation, test_config)
    print(test_results)
