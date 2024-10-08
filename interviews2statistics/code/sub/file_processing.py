# sub/file_processing.py

import os
import re
from typing import List, Tuple
from collections import namedtuple

Contribution = namedtuple('Contribution', ['text'])

def read_interviews_from_directory(directory_path: str) -> List[Tuple[str, List[Tuple[int, Contribution]]]]:
    interviews = []
    print(f"Searching for interviews in: {directory_path}")
    
    all_files = os.listdir(directory_path)
    print(f"Total files in directory: {len(all_files)}")
    
    for filename in all_files:
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            print(f"\nProcessing file: {filename}")
            file_contributions = []
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    print(f"File content length: {len(content)} characters")
                    
                    # Find all summary blocks
                    summary_blocks = re.findall(r"--- Summary Start \(Iteration (\d+)\) ---\s*(.*?)\s*(?=--- Summary Start|$)", content, re.DOTALL)
                    
                    for iteration, summary_text in summary_blocks:
                        iteration = int(iteration)
                        summary_text = summary_text.strip()
                        print(f"Found summary for iteration {iteration}, length: {len(summary_text)} characters")
                        file_contributions.append((iteration, Contribution(summary_text)))
                
                if file_contributions:
                    interviews.append((filename, file_contributions))
                    print(f"Added interview from {filename} with {len(file_contributions)} summary blocks")
                else:
                    print(f"No valid summary blocks found in {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
        else:
            print(f"Skipping non-txt file: {filename}")
    
    print(f"\nTotal valid files found: {len(interviews)}")
    print("List of processed interview files:")
    for filename, contributions in interviews:
        print(f"- {filename}: {len(contributions)} contributions")
    
    if 'no_persona_interview.txt' in all_files:
        if any(filename == 'no_persona_interview.txt' for filename, _ in interviews):
            print("'no_persona_interview.txt' was successfully processed.")
        else:
            print("WARNING: 'no_persona_interview.txt' exists in the directory but was not processed successfully.")
    else:
        print("WARNING: 'no_persona_interview.txt' does not exist in the directory.")
    
    return interviews


def process_interview_content(content: str) -> List[dict]:
    """
    Process the content of a single interview file.
    """
    summary_blocks = re.findall(r"--- Summary Start \(Iteration (\d+)\) ---\s*(.*?)\s*(?=--- Summary Start|$)", content, re.DOTALL)
    
    processed_content = []
    for iteration, summary_text in summary_blocks:
        processed_content.append({
            'iteration': int(iteration),
            'text': summary_text.strip()
        })
    
    return processed_content

# Keep this for backwards compatibility if needed
read_discussions_from_directory = read_interviews_from_directory