import collections
import os
import csv
import yaml
import logging
from datetime import datetime
import openai
import string
from collections import deque, Counter  # Make sure deque is imported
print("deque and Counter imported successfully")
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize  
from nltk.stem import WordNetLemmatizer

from code.token_analysis.token_distribution_analyzer import calculate_entropy, compare_personas
from code.token_analysis.token_visualization import plot_token_distribution, plot_persona_comparison

class PersonaMediatedInterviewer:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.config = self.load_config(config_file)
        self.output_dir = self.config['output']['directory']
        self.model = self.config['advanced']['model']
        last_words_used = self.config['simulation'].get('last_words_used')
        self.token_tracker = TokenTracker(
            self.config['token_tracking']['output_directory'],
            self.config['token_tracking']['output_file'],
            last_words_used
        )    
        self.setup_logging()
        self.setup_openai_client()
        self.load_persona_pools()
        self.topic = self.load_topic()        
        self.results = []  # Initialize results as an empty list or the appropriate data structure
        print("Debug: Methods after initialization:", [method for method in dir(self) if not method.startswith("__")])
        print("PersonaMediatedInterviewer initialization complete")
        print("Methods after initialization:", [method for method in dir(self) if callable(getattr(self, method)) and not method.startswith("__")])
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    
        # Validate iterations and iterations_used
        total_iterations = config['simulation']['iterations']
        #iterations_used = config['simulation']['iterations_used']
    
        #if iterations_used > total_iterations:
        #    print(f"Warning: iterations_used ({iterations_used}) is greater than total iterations ({total_iterations}). Using all iterations.")
        #    config['simulation']['iterations_used'] = total_iterations
    
        return config
                 

    def get_ai_response(self, prompt):
        print(f"Sending prompt to AI for {prompt.split()[2]} role")  # This will print e.g., "Sending prompt to AI for Journalist role"
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "system", "content": prompt}],
                    timeout=300  # 5 minutes timeout
                )
                if response and 'choices' in response:
                    return response['choices'][0]['message']['content']
                else:
                    print(f"Invalid response format: {response}")
            except Exception as e:
                print(f"Error during AI response generation (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return "Error: Unable to generate response after multiple attempts."
        return "Error: Unable to generate response."



    def generate_header(self, personas):
        header = f"""Simulation Results
==================
Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Model: {self.model}
Number of Turns per Iteration: {self.config['advanced']['max_turns']}
Total Number of Personas: {len(personas)}
Number of Iterations: {self.config['simulation']['iterations']}
Topic: {self.topic}
Personas:
"""
        for persona in personas:
            header += f"- {persona['job']}: (Role: {persona['role']}, "
            header += f"Background: {persona.get('background', 'Not specified')}, "
            header += f"Education: {persona.get('education_level', 'Not specified')}, "
            header += f"Experience: {persona.get('years_of_coding_experience', 'Not specified')})\n"
        return header    


        
    def setup_logging(self):
        logging.basicConfig(filename=self.config['logging']['file'],
                            level=self.config['logging']['level'],
                            format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger()


    def setup_openai_client(self):
        """
        Setup the OpenAI API client using the API key from the environment variable.
        """
        #api_key = os.getenv('OPENAI_API_KEY')
        api_key = "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"

        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables.")
    
        openai.api_key = api_key  # Set the API key for the OpenAI client
    

    def analyze_and_visualize_tokens(self, group_index):
        # Load and analyze the token distribution after the simulation
        token_data = self.token_tracker.get_token_distribution()
        for persona, tokens in token_data.items():
            entropy = calculate_entropy(tokens)
            print(f"Entropy for {persona}: {entropy}")
            plot_token_distribution(tokens, persona)
        
        # Example comparison between two personas
        common, unique_p1, unique_p2 = compare_personas(token_data['AI Professor'], token_data['AI Software Developer'])
        plot_persona_comparison(common, unique_p1, unique_p2, 'AI Professor', 'AI Software Developer')


    def load_persona_pools(self):
        """
        Load personas from CSV files and return them as structured data.
        """
        self.persona_pools = []
        for persona_file in self.config['simulation']['persona_files']:
            try:
                with open(persona_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    personas = []
                    for i, row in enumerate(reader):
                        if row:
                            try:
                                cleaned_row = self.clean_row(row)
                                personas.append(cleaned_row)
                            except Exception as e:
                                print(f"Error processing row {i+1} in {persona_file}: {e}")
                                print(f"Problematic row: {row}")
                self.persona_pools.append(personas)
                print(f"Loaded {len(personas)} personas from {persona_file}")
            except FileNotFoundError:
                print(f"Warning: Persona file {persona_file} not found. Skipping.")
            except csv.Error as e:
                print(f"Error reading {persona_file}: {e}")


    # Make sure "expert" is replaced by "job""
    def clean_row(self, row):
        cleaned = {k.strip(): v.strip() if v is not None else '' for k, v in row.items()}
        # Replace 'job' with 'job' if it exists
        if 'job' in cleaned:
            cleaned['job'] = cleaned.pop('job')
        return cleaned    


    def load_topic(self):
        topic_file = self.config.get('topic_file')
        if not topic_file:
            raise ValueError("Topic file not specified in the configuration.")
        with open(topic_file, 'r') as f:
            topics = [line.strip() for line in f if line.strip()]
        return topics[0] if topics else "General discussion about technology"    

    def select_moderator(self, participants):
        moderators = [p for p in participants if p['role'] == 'moderator']
        if not moderators:
            raise ValueError("No moderator found in the persona pool")
        return moderators[0]


    def load_prompt(self, prompt_type):
        prompt_file = self.config['system_prompts'][prompt_type]
        with open(prompt_file, 'r') as f:
            return f.read().strip()

    def generate_participant_prompt(self, participant, conversation, is_focus_group):
        base_prompt = self.load_prompt('participant')
        prompt = base_prompt.format(
            job=participant['job'],
            interview_type='focus group' if is_focus_group else 'one-to-one interview',
            topic=self.topic,
            background=participant['background'],
            education_level=participant['education_level'],
            years_of_coding_experience=participant['years_of_coding_experience']
        )
        return prompt

    def generate_moderator_prompt(self, moderator, participants, conversation, is_focus_group):
        base_prompt = self.load_prompt('moderator')
        participants_str = ', '.join([p['job'] for p in participants]) if is_focus_group else participants[0]['job']
        prompt = base_prompt.format(
            job=moderator['job'],
            interview_type='focus group' if is_focus_group else 'one-to-one interview',
            topic=self.topic,
            participants=participants_str
        )
        return prompt


       
        

    def run_simulation_iterations(self, moderator, participants, output_file, is_focus_group=True, group_index=0):
        print(f"Starting simulation iterations for {'focus group' if is_focus_group else 'one-to-one interview'}")
        print(f"Writing to file: {output_file}")

        with open(output_file, 'w') as f:
            f.write(self.generate_header([moderator] + participants))
            for iteration in range(self.config['simulation']['iterations']):
                f.write(f"\n\n--- Iteration {iteration + 1} ---\n")
            
                # Moderator's question
                moderator_prompt = self.generate_moderator_prompt(moderator, participants, [], is_focus_group)
                moderator_response = self.get_ai_response(moderator_prompt)
                f.write(f"\nModerator: {moderator_response}\n")
            
                # Participants' responses
                for persona in participants:
                    prompt = self.generate_participant_prompt(persona, [moderator_response], is_focus_group)
                    response = self.get_ai_response(prompt)
                    f.write(f"\n{persona['job']}: {response}\n")
                
                    # Track tokens for this response
                    self.token_tracker.track_tokens(persona['job'], response)

        print(f"Finished writing to {output_file}")

        # Save token distribution after each simulation
        origin = "focus_group" if is_focus_group else "interview"
        self.token_tracker.save_token_distribution(origin)


    def run_one_to_one_interviews(self, participants, group_index):
        moderator = self.select_moderator(participants)
        job_counters = {}  # To keep track of job repetitions
    
        for participant in participants:
            if participant['role'] != 'moderator':
                job = participant['job'].lower().replace(' ', '_')
            
                # Update counter for this job
                job_counters[job] = job_counters.get(job, 0) + 1
            
                # Create a unique filename
                if job_counters[job] > 1:
                    filename = f"{job}_{job_counters[job]}_interview.txt"
                else:
                    filename = f"{job}_interview.txt"
            
                output_file = os.path.join(self.config['output']['directory'], filename)
            
                self.run_simulation_iterations(moderator, [participant], output_file, is_focus_group=False, group_index=group_index)
            

    def run_focus_groups(self, participants, group_index):
        print(f"Starting focus group for group {group_index+1}")
        moderator = self.select_moderator(participants)
        participants = [p for p in participants if p['role'] != 'moderator']
        output_file = os.path.join(self.config['output']['directory'], f"focus_group_{group_index+1}.txt")
        print(f"Output file: {output_file}")
        self.run_simulation_iterations(moderator, participants, output_file, is_focus_group=True, group_index=group_index)

    def run(self):
        print("Starting PersonaMediatedInterviewer simulation")
        for i, participants in enumerate(self.persona_pools):
            print(f"Running simulation for group {i+1}")
            self.token_tracker.reset()  # Reset token tracker before each group
            if self.config['one_to_one_interview']['enabled']:
                print("Running one-to-one interviews")
                self.run_one_to_one_interviews(participants, i)
            if self.config['focus_group']['enabled']:
                print("Running focus groups")
                self.run_focus_groups(participants, i)
    
        # Save combined token distribution after all simulations
        #self.token_tracker.save_token_distribution("combined")
        print("Simulation complete")  


        
# ------------------------------- DIVERSITY SCORING ------------------------------- #

    def assess_diversity(self, participants, conversation):
        """
        Use the LLM to assess the diversity of the group from each persona's perspective.
        """
        diversity_scores = {}
        for participant in participants:
            if participant['role'] != 'moderator':
                prompt = self.generate_persona_prompt(participant, participants, conversation)
                diversity_response = self.get_ai_response(prompt)


                # Debugging: Print the response from the LLM to see what it returns
                print(f"Raw LLM Response for {participant['job']}:\n{diversity_response}")

                try:
                    scores = self.parse_diversity_scores(diversity_response)
                    # Ensure scores are correctly parsed
                    print(f"Parsed scores for {participant['job']}: {scores}")
                    diversity_scores[participant['job']] = scores
                except ValueError as ve:
                    print(f"Error parsing diversity scores for {participant['job']}: {str(ve)}")

        # Debugging: Print the full diversity_scores dictionary
        print(f"Final diversity scores: {diversity_scores}")
        return diversity_scores


    def generate_diversity_assessment_prompt(self, assessor, participants, conversation, group_homogeneity=None):
        prompt = f"You are {assessor['job']} assessing the diversity of a group after a discussion. "
        prompt += f"The group consists of: {', '.join([p['job'] for p in participants if p['role'] != 'moderator'])}\n\n"

        if group_homogeneity is not None:
            prompt += f"The calculated group homogeneity is {group_homogeneity:.2f} (0 means completely diverse, 1 means completely homogeneous).\n\n"

        prompt += "Consider the following aspects:\n"
        prompt += "1. Way of Thinking (WT): Diversity in thought processes and problem-solving approaches.\n"
        prompt += "2. Knowledge and Skills (KS): Variety in areas of expertise and skill sets.\n"
        prompt += "3. Worldview (WV): Differences in perspectives on life, society, and the world.\n"
        prompt += "4. Beliefs about Right and Wrong (RW): Diversity in ethical and moral standpoints.\n\n"
        prompt += "Score each aspect from 1 (very low diversity) to 7 (very high diversity) based on these guidelines:\n"
        prompt += "1-2: Highly homogeneous\n3-4: Some diversity, but significant similarities\n"
        prompt += "5-6: Considerable diversity\n7: Extremely diverse\n\n"
        prompt += "IMPORTANT: This group has members from very different backgrounds. Scores should reflect this diversity.\n"
        prompt += "Avoid giving all aspects the same score unless truly warranted.\n"
        prompt += "Provide your scores in the format: WT:score, KS:score, WV:score, RW:score\n"
        prompt += "After the scores, briefly justify each score in 1-2 sentences.\n\n"
        prompt += "Key points from the conversation:\n" + self.extract_key_points(conversation)
        return prompt

    def extract_key_points(self, conversation):
        prompt = "Extract 3-5 key points from this conversation, focusing on diverse viewpoints and areas of disagreement:\n\n"
        prompt += "\n".join(conversation)
        key_points = self.get_ai_response(prompt)
        return key_points


    
    def generate_persona_prompt(self, persona, participants, group_diversity_score):
        prompt = f"You are a {persona['job']} participating in a group discussion.\n"
        prompt += "The group includes participants with the following roles and backgrounds:\n"

        for participant in participants:
            if participant['role'] != 'moderator':
                prompt += f"- {participant['job']} (Background: {participant.get('background', 'Not specified')}, "
                prompt += f"Education: {participant.get('education_level', 'Not specified')}, "
                prompt += f"Experience: {participant.get('years_of_coding_experience', 'Not specified')})\n"

        prompt += "\nBased on your perspective and professional background, please evaluate the diversity of the group as a whole in the following categories:\n"
        prompt += "1. Way of Thinking (WT): How diverse are the ways of thinking within the group?\n"
        prompt += "2. Knowledge and Skills (KS): How diverse is the group's knowledge and skillset?\n"
        prompt += "3. Worldview (WV): How diverse are the worldviews within the group?\n"
        prompt += "4. Beliefs about Right and Wrong (RW): How diverse are the beliefs and values in the group?\n"

        prompt += "\nRate each category on a scale from 1 (very low diversity) to 7 (very high diversity).\n"

        prompt += "Sure, everybody has different perspective and approaches. But note that participants with a similar background, e.g., academic, are usually more similar (less diverse). In particular, if in addition they deal with similar issues (e.g., technical, or social, or musical issues) in their job.\n"
        prompt += "In other words: If people come from a similar field, the diversity should be considered low and vice versa.\n"        
        prompt += "IMPORTANT: Please provide a numerical score for ALL FOUR categories (WT, KS, WV, RW) in your response.\n"
        prompt += "Format your response as follows:\n"
        prompt += "WT: [score]\nKS: [score]\nWV: [score]\nRW: [score]\n"
        prompt += "Then, provide a brief justification for each score.\n"

        return prompt


    def generate_persona_based_scores(self, persona, group_diversity_score):
        """
        Generate diversity scores for WT, KS, WV, RW based on how the persona's background compares with the group's diversity.
        The more distinct the group is from the persona's own background and experience, the higher the diversity score.
        """
        # Dynamic scaling based on group diversity
        wt_score = self.calculate_persona_score(persona, group_diversity_score, 'Way of Thinking')
        ks_score = self.calculate_persona_score(persona, group_diversity_score, 'Knowledge and Skills')
        wv_score = self.calculate_persona_score(persona, group_diversity_score, 'Worldview')
        rw_score = self.calculate_persona_score(persona, group_diversity_score, 'Beliefs about Right and Wrong')

        return [wt_score, ks_score, wv_score, rw_score]

    
    def calculate_group_diversity(self, participants):
        """
        Calculates a diversity score based on the variety of participants' attributes.
        The more unique combinations of attributes, the higher the diversity score.
        """
        attributes_set = set()

        # Combine key attributes (background, education, experience) for diversity comparison
        for participant in participants:
            if participant['role'] == 'participant':  # Ignore moderators
                key_attributes = (participant['background'], 
                                  participant['education_level'], 
                                  participant['years_of_coding_experience'])
                attributes_set.add(key_attributes)

        # Calculate diversity score as a fraction of unique attribute combinations
        diversity_score = len(attributes_set) / len(participants)
    
        # Scale the diversity score between 1 and 7
        return diversity_score * 7

        # Calculate diversity score as a fraction of unique attribute combinations relative to the group size
        diversity_score = len(attributes_set) / len(participants)  # Normalize diversity score

        # Scale to a score between 1 and 7
        return diversity_score * 7


    def calculate_group_diversity(self, participants):
        """
        Calculates a group diversity score based on the 'job' field and additional attributes (if available).
        """
        unique_experts = set(p['job'] for p in participants if p['role'] == 'participant')
    
        # Additional attributes
        unique_backgrounds = set(p['background'] for p in participants if p['role'] == 'participant' and p['background'])
        unique_education_levels = set(p['education_level'] for p in participants if p['role'] == 'participant' and p['education_level'])
        unique_years_of_experience = set(p['years_of_coding_experience'] for p in participants if p['role'] == 'participant' and p['years_of_coding_experience'])
    
        # Assign weights (adjust as needed)
        expert_weight = 0.6  # Main weight for the 'job' field
        background_weight = 0.2  # Weight for 'background' diversity
        education_weight = 0.1  # Weight for 'education_level' diversity
        experience_weight = 0.1  # Weight for 'years_of_coding_experience' diversity
    
        # Calculate a weighted diversity score
        diversity_score = (
            expert_weight * (len(unique_experts) / len(participants)) +
            background_weight * (len(unique_backgrounds) / len(participants)) +
            education_weight * (len(unique_education_levels) / len(participants)) +
            experience_weight * (len(unique_years_of_experience) / len(participants))
        )
    
        # Scale the diversity score to be between 1 and 7
        return max(1, min(7, diversity_score * 7))



    def extract_score_from_line(self, line):
        """
        Extract the score from a line in the LLM response.
        Example input: "Way of Thinking (WT): 5"
        Expected output: 5
        """
        try:
            # Split the line by ':' to get the score part
            if ':' in line:
                # Extract the score part and convert it to an integer
                key, value = line.split(':')
                score = int(value.strip().split()[0])  # Assuming the score is the first word after ':'
                return score
            else:
                raise ValueError("Line does not contain ':' to split key and value")
        except ValueError as e:
            raise ValueError(f"Failed to extract score from line: {line}. Error: {str(e)}")




    def parse_diversity_scores(self, response):
        """
        Parse the LLM response to extract the diversity scores for each category (WT, KS, WV, RW).
        """
        scores = {'WT': None, 'KS': None, 'WV': None, 'RW': None}
        categories = {
            'WT': ['Way of Thinking', 'WT'],
            'KS': ['Knowledge and Skills', 'KS'],
            'WV': ['Worldview', 'WV'],
            'RW': ['Beliefs about Right and Wrong', 'Beliefs', 'RW']
        }
    
        lines = response.split('\n')
        for i, line in enumerate(lines):
            for key, aliases in categories.items():
                if any(alias in line for alias in aliases):
                    try:
                        # Look for the score in this line and the next
                        score_text = line + ' ' + lines[i+1] if i+1 < len(lines) else line
                        score = int(''.join(filter(str.isdigit, score_text.split(':')[-1].split('/')[0])))
                        scores[key] = score
                        break
                    except ValueError:
                        continue
    
        return scores
        



        
    def write_diversity_csv(self, diversity_scores, group_index):
        """
        Writes the diversity scores for each persona to a CSV file.
        """
        try:
            diversity_file = self.config['output']['diversity_files'][group_index]
            os.makedirs(os.path.dirname(diversity_file), exist_ok=True)

            with open(diversity_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Persona', 'WT', 'KS', 'WV', 'RW'])

                for persona, scores in diversity_scores.items():
                    row = [persona]
                    for category in ['WT', 'KS', 'WV', 'RW']:
                        row.append(scores.get(category, 'N/A'))
                    writer.writerow(row)
                
            self.logger.info(f"Diversity scores written to {diversity_file}")
        except Exception as e:
            self.logger.error(f"Error writing diversity scores to CSV file: {str(e)}")
            raise



        self.model = self.config['advanced']['model']




class TokenTracker:
    def __init__(self, output_directory, output_file, last_words_used):
        self.output_directory = output_directory
        self.output_file = output_file
        self.last_words_used = last_words_used
        self.reset()
        
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def reset(self):
        self.token_data = {}
        self.recent_words = {}

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
        tokens = [token for token in tokens if token not in self.stop_words and len(token) > 1]
        return tokens

    def track_tokens(self, persona, text):
        tokens = self.preprocess_text(text)
        
        if persona not in self.recent_words:
            if self.last_words_used == -1:
                self.recent_words[persona] = []  # No limit
            else:
                self.recent_words[persona] = deque(maxlen=self.last_words_used)
        
        if self.last_words_used == -1:
            self.recent_words[persona].extend(tokens)
        else:
            self.recent_words[persona].extend(tokens)
        
        if persona not in self.token_data:
            self.token_data[persona] = Counter()
        
        self.token_data[persona] = Counter(self.recent_words[persona])


    def save_token_distribution(self, origin):
        os.makedirs(self.output_directory, exist_ok=True)
        token_file_path = os.path.join(self.output_directory, self.output_file)
    
        # Check if the file already exists
        file_exists = os.path.isfile(token_file_path)
    
        with open(token_file_path, 'a', newline='') as f:
            writer = csv.writer(f)
        
            # Write header only if the file is new
            if not file_exists:
                writer.writerow(['Origin', 'Persona', 'Token', 'Count'])
        
            for persona, token_counter in self.token_data.items():
                for token, count in token_counter.items():
                    writer.writerow([origin, persona, token, count])
    
        print(f"Token distribution for {origin} appended to {token_file_path}")
        print(f"Total unique tokens: {sum(len(tokens) for tokens in self.token_data.values())}")
        for persona, words in self.recent_words.items():
            print(f"Words tracked for {persona} in {origin}: {len(words)}")


if __name__ == "__main__":
    config_file = "config/config.yaml"
    interviewer = PersonaMediatedInterviewer(config_file)
    print(f"get_ai_response method exists: {'get_ai_response' in dir(interviewer)}")
    interviewer.run()
