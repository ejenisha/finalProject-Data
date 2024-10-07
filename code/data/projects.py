import pandas as pd
import numpy as np

# Load the CSV file
file_path = r'F:\finalProjectData\finalprojectData\employee_skills_data.csv'
df = pd.read_csv(file_path)

# Update the 'no_of_projects_done_in_that_skill' column based on 'proficiency_level'
df['no_of_projects_done_in_that_skill'] = np.where(
    df['proficiency_level'] > 5,
    np.random.randint(5, 13, size=len(df)),
    np.random.randint(1, 5, size=len(df))
)

# Save the updated DataFrame to a new CSV file
output_path = r'F:\finalProjectData\finalprojectData\employee_skills_data.csv'
df.to_csv(output_path, index=False)

print(f"Updated file saved to {output_path}")
