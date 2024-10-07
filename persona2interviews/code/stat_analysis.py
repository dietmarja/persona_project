import pandas as pd
import matplotlib.pyplot as plt
import argparse

def analyze_results(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Sum up the entries for each persona
    question_columns = [col for col in df.columns if col.startswith('Q')]
    df['Total_Score'] = df[question_columns].sum(axis=1)

    # Group by expert level and calculate mean score
    grouped_scores = df.groupby('Expert_Level')['Total_Score'].mean()

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    grouped_scores.plot(kind='bar')
    plt.title('Average Score by Expertise Level')
    plt.xlabel('Expertise Level')
    plt.ylabel('Average Score')
    plt.xticks(rotation=0)
    plt.tight_layout()
    
    # Save the plot
    plot_path = 'expertise_level_scores.png'
    plt.savefig(plot_path)
    print(f"Bar chart saved as {plot_path}")

    # Print summary statistics
    print("\nSummary Statistics:")
    print(df.groupby('Expert_Level')['Total_Score'].describe())

    # Print individual scores
    print("\nIndividual Scores:")
    print(df[['Persona', 'Expert_Level', 'Total_Score']])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze simulated questionnaire responses")
    parser.add_argument('csv_file', type=str, help='Path to the CSV file with simulated responses')
    args = parser.parse_args()
    analyze_results(args.csv_file)