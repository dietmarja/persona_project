# File: code/sub/perform_focus_group_simulation.py

import re
from typing import List, Dict, Any
import openai
import logging
from .prompts import Prompts

def perform_simulation(moderator: Dict[str, str], participants: List[Dict[str, str]], config: Dict[str, Any]) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=config['openai_api_key'])
    prompts = Prompts(config)
    conversation = []
    
    for question in config['questions']:
        moderator_prompt = prompts.get_moderator_prompt(moderator, question, is_followup=False)
        moderator_response = generate_response(client, moderator_prompt, config['max_tokens'])
        conversation.append({"speaker": moderator['abbreviation'], "text": moderator_response, "question": question})
        
        for participant in participants:
            participant_prompt = prompts.get_participant_prompt(participant, question, is_focus_group=len(participants) > 1)
            participant_response = generate_response(client, participant_prompt, config['max_tokens'])
            conversation.append({"speaker": participant['abbreviation'], "text": participant_response, "question": question})
    
    summary = generate_summary(client, conversation, config['questions'], prompts, config['max_tokens'])
    return {
        "conversation": conversation,
        "summary": summary,
        "config": config
    }

def perform_no_persona_simulation(moderator: Dict[str, str], participants: List[Dict[str, str]], config: Dict[str, Any]) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=config['openai_api_key'])
    prompts = Prompts(config)
    conversation = []
    
    for question in config['questions']:
        moderator_prompt = prompts.get_moderator_prompt(moderator, question, is_followup=False)
        moderator_response = generate_response(client, moderator_prompt, config['max_tokens'])
        conversation.append({"speaker": moderator['abbreviation'], "text": moderator_response, "question": question})

        for participant in participants:
            participant_prompt = prompts.get_participant_prompt(participant, question, config['is_focus_group'])
            participant_response = generate_response(client, participant_prompt, config['max_tokens'])
            conversation.append({"speaker": participant['abbreviation'], "text": participant_response, "question": question})

    summary = generate_summary(client, conversation, config['questions'], prompts, config['max_tokens'])

    return {
        "conversation": conversation,
        "summary": summary,
        "config": config
    }


def generate_response(client: openai.OpenAI, prompt: str, max_tokens: int) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        # Remove redundant speaker labels
        content = response.choices[0].message.content.strip()
        content = re.sub(r'^(Moderator: |AI Ethicist: |Participant: )+', '', content, flags=re.MULTILINE)
        return content
    except Exception as e:
        logging.error(f"Error generating response: {str(e)}")
        return f"[Error generating response]"

def generate_summary(client: openai.OpenAI, conversation: List[Dict[str, str]], questions: List[str], prompts: Prompts, max_tokens: int) -> str:
    conversation_text = "\n\n".join([
        f"Question: {question}\n" + "\n".join([f"{turn['speaker']}: {turn['text']}" for turn in conversation if turn['question'] == question])
        for question in questions
    ])
    summary_prompt = prompts.get_summary_prompt(conversation_text)
    summary = generate_response(client, summary_prompt, max_tokens * 2)
    # Remove any potential redundant labels from the summary
    summary = re.sub(r'^(Moderator: |AI Ethicist: |Participant: )+', '', summary, flags=re.MULTILINE)
    return summary