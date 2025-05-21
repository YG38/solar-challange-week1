import os
import json

# Paths
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
notebook_path = os.path.join(project_dir, 'notebooks', 'benin_analysis.ipynb')

# Read the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Update the data loading cell
for cell in notebook['cells']:
    if cell['cell_type'] == 'code' and 'load_data' in ''.join(cell['source']):
        cell['source'] = [
            "# Load the dataset\n",
            "data_path = os.path.join('..', 'data', 'solar-measurements_benin-malanville_qc (1).csv')\n",
            "df = pd.read_csv(data_path, encoding='utf-8', parse_dates=['Timestamp'], low_memory=False)\n",
            "\n",
            "# Basic data exploration\n",
            "print(\"Dataset shape:\", df.shape)\n",
            "print(\"\\nFirst 5 rows:\")\n",
            "display(df.head())\n",
            "print(\"\\nData types and non-null counts:\")\n",
            "print(df.info())"
        ]
        break

# Save the updated notebook
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)
    
print(f"Updated notebook with correct data path: {notebook_path}")
