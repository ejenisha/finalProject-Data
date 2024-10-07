import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker()

# Constants
num_employees = 5000
num_skills = 15
num_emp_skills = 5700
num_job_performance = 5500
num_training = 250

# Helper functions
def get_random_experience_and_salary(age):
    if age < 25:
        return random.choice([0, 1, 2]), random.randint(20000, 35000)
    elif 25 <= age < 30:
        return random.choice([3, 4, 5]), random.randint(35000, 50000)
    elif 30 <= age < 40:
        return random.choice([6, 10]), random.randint(50000, 80000)
    else:
        return random.choice([11, 20]), random.randint(80000, 120000)

# Employee Table
departments = ["HR", "Engineering", "Marketing", "Finance", "Sales"]
designations = ["Junior Developer", "Mid-level Developer", "Senior Developer", "Lead Developer", "Manager"]
education_levels = ["Bachelors", "Masters", "MBA"]

employees = []
for i in range(num_employees):
    emp_id = f"E{str(i+1).zfill(3)}"
    emp_name = fake.name()
    department = random.choice(departments)
    age = random.randint(22, 50)
    experience, salary = get_random_experience_and_salary(age)
    designation = designations[min(experience // 5, 4)]  # Logical designation based on experience
    doj = fake.date_between(start_date='-20y', end_date='today')
    no_of_promotions = random.choice([0, 1, 2, 3]) if experience > 2 else 0
    education = random.choice(education_levels)
    
    # Introduce some nulls
    if random.random() < 0.03:
        experience = None
    if random.random() < 0.03:
        no_of_promotions = None
    if random.random() < 0.03:
        salary = None
    
    employees.append({
        "emp_id": emp_id,
        "emp_name": emp_name,
        "department": department,
        "designation": designation,
        "DOJ": doj,
        "age": age,
        "experience": experience,
        "salary": salary,
        "no_of_promotions": no_of_promotions,
        "education": education
    })

employees_df = pd.DataFrame(employees)

# Skill Table
skill_categories = ["full_stack", "data", "consulting"]
skills = [
    {"skill_id": f"S{str(i+1).zfill(3)}", "skill_name": skill, "skill_category": category}
    for i, (skill, category) in enumerate(
        [
            ("JavaScript", "full_stack"), 
            ("React", "full_stack"), 
            ("Node.js", "full_stack"), 
            ("Docker", "full_stack"), 
            ("HTML/CSS", "full_stack"),
            ("Python", "data"), 
            ("SQL", "data"), 
            ("Machine Learning", "data"), 
            ("Data Visualization", "data"), 
            ("Big Data", "data"),
            ("Consulting Basics", "consulting"), 
            ("Project Management", "consulting"), 
            ("Financial Modeling", "consulting"), 
            ("Client Management", "consulting"), 
            ("Risk Management", "consulting")
        ]
    )
]

skills_df = pd.DataFrame(skills)

# Employee Skill Table
employee_skills = []
for i in range(num_emp_skills):
    emp_id = random.choice(employees_df['emp_id'])
    emp_name = employees_df[employees_df['emp_id'] == emp_id]['emp_name'].values[0]
    skill_id = random.choice(skills_df['skill_id'])
    skill_name = skills_df[skills_df['skill_id'] == skill_id]['skill_name'].values[0]
    proficiency_level = random.randint(1, 10)
    no_of_projects_done = random.randint(1, 50)
    certifications = random.choice(["Yes", "No"])
    
    employee_skills.append({
        "emp_id": emp_id,
        "emp_name": emp_name,
        "skill_id": skill_id,
        "skill_name": skill_name,
        "proficiency_level": proficiency_level,
        "no_of_projects_done_in_that_skill": no_of_projects_done,
        "certifications": certifications
    })

employee_skills_df = pd.DataFrame(employee_skills)

# Job Performance Table
job_performance = []
for index, employee in employees_df.iterrows():
    emp_id = employee['emp_id']
    emp_name = employee['emp_name']
    
    # Generate job performance details
    no_of_projects = random.randint(1, 30)
    manager_rating = random.choice([None] + [random.randint(1, 5)] * 10)  # Allow some nulls
    promotion = random.choice([0, 1])
    
    # Append the record to the job_performance list
    job_performance.append({
        "emp_id": emp_id,
        "emp_name": emp_name,
        "no_of_projects": no_of_projects,
        "manager_rating": manager_rating,
        "promotion": promotion
    })

job_performance_df = pd.DataFrame(job_performance)

# Training Table
full_stack_trainings = [
    "Full-Stack Web Development", "Advanced JavaScript", "React and Redux", 
    "Node.js Masterclass", "DevOps with Docker"
]
data_trainings = [
    "Data Science Bootcamp", "Python for Data Analysis", "Machine Learning Basics", 
    "SQL Mastery", "Advanced Data Visualization"
]
consulting_trainings = [
    "Consulting Essentials", "Business Process Management", "Financial Modeling", 
    "Project Management for Consultants", "Client Relationship Management"
]

training_names = full_stack_trainings + data_trainings + consulting_trainings
training_id_mapping = {name: f"T{str(i+1).zfill(3)}" for i, name in enumerate(training_names)}

# Create the training table
training = []
for i in range(num_training):
    emp_id = random.choice(employees_df['emp_id'])  # Foreign Key Reference
    emp_name = employees_df[employees_df['emp_id'] == emp_id]['emp_name'].values[0]
    
    # Select a random training name and get its corresponding unique T_id
    t_name = random.choice(training_names)
    t_id = training_id_mapping[t_name]

    project_score = random.randint(0, 100)
    hackerrank_score = random.randint(0, 100)
    completed = random.choice([0, 1])
    date_completed = fake.date_between(start_date='-5y', end_date='today') if completed == 1 else None
    
    # If not completed, set low scores
    if completed == 0:
        if random.random() > 0.1:
            project_score = random.randint(0, 40)
            hackerrank_score = random.randint(0, 40)

    training.append({
        "emp_id": emp_id,
        "emp_name": emp_name,
        "T_id": t_id,
        "T_name": t_name,
        "project_score": project_score,
        "hackerrank_score": hackerrank_score,
        "completed": completed,
        "date_completed": date_completed
    })

training_df = pd.DataFrame(training)
# Save DataFrames to CSV
employees_df.to_csv('employee_data.csv', index=False)
skills_df.to_csv('skills_data.csv', index=False)
employee_skills_df.to_csv('employee_skills_data.csv', index=False)
job_performance_df.to_csv('job_performance_data.csv', index=False)
training_df.to_csv('training_data.csv', index=False)

print("All CSV files have been generated successfully!")

