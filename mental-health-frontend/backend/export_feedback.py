import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Export feedback data
query = "SELECT user_id, prompt, response, rating FROM feedback"
feedback_data = pd.read_sql_query(query, conn)

# Save to CSV
feedback_data.to_csv('feedback_dataset.csv', index=False)

print("✅ Feedback data exported successfully!")
