# File: code/sub/prompts.py

class Prompts:
    @staticmethod
    def generate_moderator_prompt(moderator, participant, topic, conversation):
        prompt = f"You are a {moderator['expert']} moderating a discussion on the topic: '{topic}'. "
        prompt += f"You're speaking with a {participant['expert']}. "
        prompt += "Based on the conversation so far, ask a relevant question or make a comment to further the discussion.\n\n"
        prompt += "Conversation so far:\n"
        prompt += "\n".join(conversation)
        return prompt

    @staticmethod
    def generate_participant_prompt(participant, topic, conversation):
        if participant['expert'] == 'No Persona':
            prompt = f"You are participating in a discussion on the topic: '{topic}'. "
        else:
            prompt = f"You are a {participant['expert']} participating in a discussion on the topic: '{topic}'. "
            prompt += f"Your background is in {participant['background']}. "
        prompt += "Based on the conversation so far, provide a response or insight.\n\n"
        prompt += "Conversation so far:\n"
        prompt += "\n".join(conversation)
        return prompt

    @staticmethod
    def generate_summary_prompt(conversation):
        prompt = "Summarize the key points of the following conversation:\n\n"
        prompt += "\n".join(conversation)
        return prompt
