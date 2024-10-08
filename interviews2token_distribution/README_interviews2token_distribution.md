# interviews2token_distribution

## Overview
The interviews2token_distribution application processes interview data to generate and analyze token distributions per persona. It calculates distance and similarity metrics (KL Divergence and Cosine Similarity) between token distributions and visualizes them for comparison.

## Key Features
- Processes token distribution data from interviews
- Calculates KL Divergence and Cosine Similarity between distributions
- Visualizes token distributions per persona
- Uses TF-IDF for selecting relevant tokens
- Supports multiple calculation types: interview vs. focus group, persona vs. non-persona

## Dependencies
- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- scikit-learn
- PyYAML

## File Structure
```
interviews2token_distribution/
├── README.md
├── code/
│   ├── interviews2token_distribution.py
│   ├── run_interviews2token_distribution.sh
│   └── sub/
│       ├── similarity.py
│       ├── visualization.py
│       ├── data_transformation.py
│       ├── config_utility.py
│       ├── matrix_visualization.py
│       └── divergence_line_chart.py
├── config/
│   └── config.yaml
├── input/
│   └── token_distribution.csv
└── output/
    ├── kl_divergence_matrix.csv
    ├── cosine_similarity_matrix.csv
    └── plots/
        ├── kl_divergence_line_chart.png
        ├── js_divergence_line_chart.png
        └── [persona]_token_distribution.png
```

## Configuration
The `config.yaml` file specifies input/output paths and calculation parameters:

```yaml
input_files:
  - file: '/path/to/token_distribution_5.csv'
    iterations: 5
  - file: '/path/to/token_distribution_20.csv'
    iterations: 20

output_dir: '/path/to/output'
kl_divergence_file: '/path/to/output/kl_divergence_matrix.csv'
cosine_similarity_file: '/path/to/output/cosine_similarity_matrix.csv'
js_divergence_file: '/path/to/output/js_divergence_matrix.csv'
png_output_dir: '/path/to/output/plots'
kl_divergence_line_chart: '/path/to/output/plots/kl_divergence_line_chart.png'
js_divergence_line_chart: '/path/to/output/plots/js_divergence_line_chart.png'

divergence_calculations:
  - type: "interview_focus_group"
  - type: "persona_nonpersona"
    origin: "interview"
  - type: "persona_nonpersona"
    origin: "focus_group"
```

## Implementation Details

### Main Script (interviews2token_distribution.py)
- Loads configuration from `config.yaml`
- Processes each input file
- Calculates divergences using TF-IDF selected tokens
- Generates rectangular data for plotting
- Creates KL and JS divergence line charts

### Data Transformation (data_transformation.py)
- `calculate_divergences`: Calculates KL and JS divergences using TF-IDF selected tokens
- `create_distribution`: Creates token distribution with zero-padding for missing tokens
- `generate_rectangular_data`: Prepares data for plotting

### Similarity Calculations (similarity.py)
- `calculate_kl_divergence`: Computes KL divergence between two distributions
- `calculate_js_divergence`: Computes Jensen-Shannon divergence
- `calculate_cosine_similarity`: Computes cosine similarity

### Visualization (visualization.py, divergence_line_chart.py)
- `plot_token_distribution`: Creates bar charts of token distributions
- `create_divergence_line_chart`: Generates line charts for KL and JS divergences

### Divergence Analysis
- Creates pairwise JS and KL divergence scores for n distributions.
- Builds an n x n matrix of divergence scores.
- Finds the v closest and w farthest distribution pairs.
- Keeps the new code modular by placing it in the sub directory.
- Allows for configuration of parameters through the config.yaml file.



## Running the Application
1. Install dependencies: `pip install pandas numpy matplotlib seaborn scipy scikit-learn PyYAML`
2. Configure `config.yaml` with appropriate paths and parameters
3. Run: `./code/run_interviews2token_distribution.sh` or `python code/interviews2token_distribution.py`

## Key Concepts
- **Common Token Grid**: All distributions use a unified set of tokens (union of all tokens across personas)
- **TF-IDF Token Selection**: Relevant tokens are selected using TF-IDF scores
- **Zero-Padding**: Missing tokens in a distribution are assigned zero count
- **Multiple Comparison Types**: Supports interview vs. focus group and persona vs. non-persona comparisons

## Output
- CSV files with KL Divergence and Cosine Similarity matrices
- PNG visualizations of token distributions per persona
- Line charts showing KL and JS divergences across iterations

This application provides comprehensive analysis of token distributions from interview data, offering insights into differences between personas and data collection methods.
