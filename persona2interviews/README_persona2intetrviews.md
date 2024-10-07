# persona2interviews -- A Persona-Mediated AI Interview System for 1:1 Interviews and 1:many interviews (focus groups)

## Overview
This system conducts AI-driven interviews using predefined personas and a no persona condition, viz. a standard LLM condition. It supports both one-on-one interviews and focus group simulations. 
In addition persona2interviews come with a range of interview-related features, e.g., diversity scoring of the groups as a whole and token tracking in line withe scoring method of Van der Vegt & Janssen (2005). 
The system uses OpenAI's GPT models to generate responses based on the characteristics of the personas involved (persona-mediated AI) or without any persona influence (standard AI). 

## Folder Structure
```
project_root/
├── code/
│   ├── token_analysis/
│   │   ├── token_distribution_analyzer.py
│   │   ├── token_tracking.py
│   │   └── token_analysis.py
│   ├── sub/
│   │   ├── perform_focus_group_simulation.py
│   │   ├── __init__.py
│   │   └── (other utility scripts)
│   └── run_persona2interviews.sh
├── config/.csv
│   └── config.yaml
├── data/
│   ├── inputs/
│   │   ├── persona/
│   │   │   └── persona_pool.csv
│   │   ├── prompts/
│   │   │   ├── moderator_prompt.txt
│   │   │   └── participant_prompt.txt
│   │   └── topics/
│   │       └── topics4discussion.csv
│   ├── outputs/
│   │   └── results/
│   │       └── 4analysis/
│   └── logs/
├── persona2interviews.py
└── README.md
```

## Key Scripts
1. `persona2interviews.py`: The main script that orchestrates the simulation.
2. `code/sub/perform_focus_group_simulation.py`: Contains core logic for running simulations and generating responses.
3. `code/sub/prompts.py`: Centralizes all prompts used in the system.
4. `code/run_persona2interviews.sh`: Shell script to run the simulator.

## New Feature: No Persona Condition
We've introduced a "no persona" condition to our simulator. This condition allows for a baseline comparison where the AI processes queries the LLM used 
without the influence of any specific persona characteristics.







### Purpose
The no persona condition serves as a control group, helping researchers understand how persona-mediated responses differ from standard AI processing. This can provide insights into the impact of personas on the generated content and opinions.

### Implementation
When the no persona condition is activated, the system bypasses the persona selection process and directly processes the input queries using the base AI model without any additional context or character traits.

### Usage
To use the no persona condition, specify it in your configuration file or use the appropriate flag when running the simulator. This will generate responses without applying any persona-specific modifications.

## Customizing Prompts
All prompts are now centralized in `code/sub/prompts.py`. To customize the behavior of the AI:
1. Edit the base prompts in `data/inputs/prompts/moderator_prompt.txt` and `data/inputs/prompts/participant_prompt.txt`.
2. For more advanced customization, modify the prompt generation methods in the `Prompts` class in `code/sub/prompts.py`.

## System Configuration
The system is parameterized using the `config/config.yaml` file. Key configuration options include:
- `simulation`: Settings for persona file and criteria
- `one_to_one_interview`: Enable/disable one-on-one interviews
- `focus_group`: Enable/disable focus group simulations
- `no_persona`: Enable/disable the no persona condition
- `output`: Directory for result files
- `advanced`: Settings like max turns, tokens, and language model
- `logging`: Log file location and level
- `system_prompts`: Locations of moderator and participant prompt files
- `topic_file`: "data/inputs/topics/topics4discussion.csv" - Location of the file with the topics discussed

## Persona Definition
Personas are defined via a csv file in `data/inputs/persona/`. Each persona has attributes like job, background, gender, age, hobbies, and style, but the persona attributes can be changed. 

## Running the System
1. Ensure you have Python 3.7+ installed.
2. Install required packages:
   ```
   pip install openai pyyaml
   ```
3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```
4. Navigate to the project root directory.
5. Run the simulator:
   ```
   ./code/run_persona2interviews.sh
   ```


## Participant Handling

- All participants, including those with "maverick" roles, are included in both 1:1 interviews and focus group discussions (1:n interviews).
- In 1:1 interviews, the system generates separate interview files for each participant, regardless of their role.
- In focus groups, all participants are included in the discussion, with the group size determined by the configuration or defaulting to a single group with all participants.
- Mavericks have the opportunity to interject with provocative statements in both 1:1 and focus group settings, based on the configured interjection probability.

This approach ensures a diverse range of perspectives in all interview types, with mavericks adding an element of unpredictability and challenge to the discussions.

## Maverick Role in Discussions
The system supports designating one or more participants as "mavericks" in the discussion. 
This feature may adds dynamism and challenge to the group interactions.

### Maverick Behavior
- Mavericks are designed to shake up group discussions by asking blunt and provocative questions.
- They challenge assumptions and introduce alternative viewpoints to the conversation.





### Implementation
- Maverick status is assigned in the `persona_pool.csv` file by setting the 'role' attribute to 'maverick'.
- The system identifies maverick participants and generates special prompts for them.

### Maverick Interjections
- During discussions, mavericks have a chance to interject with provocative statements or questions.
- The frequency of maverick interjections is currently hardcoded in the `persona2interviews.py` file.

### Impact on Discussions
- Mavericks help prevent groupthink and encourage more diverse perspectives.
- They can lead to more dynamic and unpredictable conversation flows.

### Customizing Maverick Behavior
- Modify the `generate_maverick_prompt` method in `persona2interviews.py` to adjust maverick behavior.
- To change the probability of maverick interjections, update the `run_single_iteration` method in `persona2interviews.py`.

When one or more participants are assigned the maverick role:
1. Discussions become more challenging and dynamic.
2. The AI generates more provocative and questioning responses for maverick personas.
3. Other participants may need to defend their viewpoints more rigorously.
4. The overall discussion may cover a broader range of perspectives and ideas.

### Maverick Interjections
- During discussions, mavericks have a chance to interject with provocative statements or questions.
- The frequency of maverick interjections is configurable in the `config.yaml` file under the `maverick` section.


### Customizing Maverick Behavior
- The default probability how often mavericks interject is set in __init__ in persona2interviews. 
- This default can be overwritten. To do so adjust the `interjection_probability` in the `maverick` section of `config.yaml`
- Modify the `generate_maverick_prompt` method in `persona2interviews.py` to adjust the content of maverick interjections.

## Customizing Simulations
1. Edit `config/config.yaml` to change simulation parameters, including enabling/disabling one-on-one interviews and focus groups.
2. Modify `data/inputs/persona/persona_pool.csv` to add or change personas. To add a maverick, set the 'role' attribute to 'maverick' for the desired persona(s).
3. Update `data/inputs/topics/topics4discussion.csv` to change interview topics.
4. Adjust prompts in `data/inputs/prompts/` to fine-tune AI behavior.
5. To modify maverick behavior, edit the `persona2interviews.py` file:
   - Adjust the `generate_maverick_prompt` method to change how maverick prompts are generated.
   - Modify the maverick interjection probability in the `run_single_iteration` method.
   
## Output
Results are saved in `data/outputs/results/4analysis/` as text files. Each file contains:
- Simulation metadata (date, model, turns, personas or no persona condition)
- Full conversation transcript
- AI-generated summary
The output of persona2interviews becomes the input for interviews2statistics

## Analysis
The simulator generates output files for each session, which can be analyzed to compare responses across different personas and the no persona condition. This allows for insights into how persona-mediated responses differ from the baseline no persona condition.

## Troubleshooting
- Check `data/logs/simulation.log` for detailed error messages and debugging information.
- Ensure all file paths in the config file are correct.
- Verify that the OpenAI API key is set correctly.

## Token Tracking
The system facilitakes token tracking, run simulations, and analyze the token distributions using the  modular methods.

Sub-folder Structure: A dedicated token_analysis sub-folder for all token-related methods.
### Token Trakin Methods
Token Tracking: Token counting and tracking moved to token_tracking.py.
Token Analysis: Entropy, comparison, and token distribution statistics in token_distribution_analyzer.py.
Token Visualization: Visualization methods in token_visualization.py.
Modular Integration: The main application calls these methods, keeping it lean and well-organized.
This approach maintains Persona2Interviews as a lightweight framework while allowing new token distribution features to be easily added and modified in a modular fashion.


## New System Features

### Self-Introductions
At the beginning of each interview or focus group, each persona (including the moderator) will briefly introduce themselves. 
This introduction is based on their persona characteristics and provides context for the discussion.

### Post-Discussion Questionnaire
After each discussion, participants will "fill out" a questionnaire about the other participants. 
The questionnaire is the cognitive Team Diversity Questionnaire (van der Vegt & Janssen, 2003)


The questionnaire assesses the perceived differences in:
- Way of Thinking (WT)
- Knowledge and Skills (KS)
- Worldview (WV)
- Beliefs about What is Right or Wrong (RW)

Scores are given on a 7-point rating scale ranging from 1 (to a very small extent) to 7 (to a very large extent).

The questionnaire results are saved in a CSV file named `diversity.csv` in the `data/outputs/questionnaire/` directory. The file format is as follows:

```
Persona,WT,KS,WV,RW
AI Professor,3,7,1,7
```

These features can be enabled or disabled in the `config.yaml` file under the `features` section.

## Output
Results are saved in `data/outputs/results/4analysis/` as text files. Each file contains:
- Simulation metadata (date, model, turns, personas or no persona condition)
- Full conversation transcript
- AI-generated summary
- Self-introductions of participants
- Questionnaire results

Additionally, the questionnaire results are saved in `data/outputs/questionnaire/diversity.csv`.

The output of persona2interviews becomes the input for other modules that carry out further analysis, e.g. interviews2statistics.


## Other modules that work on the basis of persona2interviews
There are several other modules that analyse the text output of persona2interviews. These modules include

### persona2statistics
### persona2disributions
### persona2graphics

The modules cooperate via data files typically provided by persona2interviews


## Extending the System
To add new features:
1. Modify the module `persona2interviews.py` for high-level changes.
2. Update `perform_focus_group_simulation.py` for changes to simulation logic.
3. Add new configuration options to `config.yaml` as needed.
4. Update this README to reflect any significant changes.

## License
[Specify your license here]

## Contact
[Your contact information]
