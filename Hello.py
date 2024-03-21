import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the OpenAI API key
print(os.getenv("OPENAI_API_KEY"))  # This should print your API key if it's loaded correctly
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to get a solution to a math problem using OpenAI
def get_math_solution(question):
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can change this to a different model if needed
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can solve math problems."},
            {"role": "user", "content": question}
        ])
        # Extract the text of the first (and in this case, only) completion
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit UI
st.title("Math Tutor Chatbot")

# Text input for the question
user_question = st.text_input("Enter your math question:")

# Button to send the question
if st.button("Ask the Math Tutor"):
    if user_question:
        # Call the function to interact with the chatbot
        response = get_math_solution(user_question)
        # Display the response
        st.write(response)
    else:
        st.write("Please enter a question.")
