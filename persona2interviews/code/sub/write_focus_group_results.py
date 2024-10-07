# File: code/sub/write_focus_group_results.py

def write_results(results, output_file):
    """
    Write the focus group results to the specified output file.
    
    :param results: The results of the focus group simulation
    :param output_file: The path to the output file
    """
    with open(output_file, 'w') as f:
        f.write(results)