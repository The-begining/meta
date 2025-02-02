import pandas as pd
import json

# Load the feedback CSV
df = pd.read_csv('feedback_dataset.csv')

# Filter for positive feedback
positive_feedback = df[df['rating'] >= 4]

# Convert to JSONL
with open('fine_tuning_data.jsonl', 'w') as f:
    for _, row in positive_feedback.iterrows():
        json_line = {"prompt": row['prompt'], "completion": row['response']}
        f.write(json.dumps(json_line) + '\n')

print("✅ Data formatted for LLaMA fine-tuning!")
