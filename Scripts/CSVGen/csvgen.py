import pandas as pd
import requests

# Function to generate questions and answers using Gemini API
def generate_questions_answers(policy_text, num_questions=10):
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=AIzaSyDf-Wwx-pXeM3rdfjzKMvJMsXf-4vmyH8Q'
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        'content': policy_text,
        'numQuestions': num_questions
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Read the CSV file
input_csv = 'data.csv'  # Replace with the path to your input CSV file
df = pd.read_csv(input_csv)

# Initialize a list to store the generated Q&A pairs
qa_pairs = []

# Generate questions and answers for each policy
for index, row in df.iterrows():
    policy = row['Policy']
    qa_list = generate_questions_answers(policy)
    
    if qa_list:
        for qa in qa_list.get('generatedQuestions', []):
            question = qa.get('question', '')
            answer = qa.get('answer', '')
            qa_pairs.append([policy, question, answer])

# Create a DataFrame with the generated Q&A pairs
qa_df = pd.DataFrame(qa_pairs, columns=['Policy', 'Question', 'Answer'])

# Save the Q&A pairs to a new CSV file
output_csv = 'generated_qa_pairs.csv'
qa_df.to_csv(output_csv, index=False)

print(f"Generated Q&A pairs saved to {output_csv}")