import streamlit as st
import openai
import os
import time
from dotenv import load_dotenv
# Assuming the Pinecone SDK has been updated, adjust imports as needed
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# Initialize OpenAI with your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pinecone setup
pinecone_api_key = os.getenv("PINECONE_API_KEY")
# Create a Pinecone client instance
pc = Pinecone(api_key=pinecone_api_key)

index_name = "canopy--document-uploader"

# Attempt to connect to the index directly
try:
    vector_database = pc.Index(index_name)
except Exception as e:
    # If the index doesn't exist, create it
    pc.create_index(
        name=index_name,
        dimension=1536,  # Make sure this matches your embeddings' dimension
        metric="cosine",
        spec=ServerlessSpec(cloud='gcp', region='us-central1')
    )
    # Then connect to the newly created index
    vector_database = pc.Index(index_name)

def generate_response(user_input):
    response = openai.Completion.create(
        model="text-davinci-003",  # Or whichever model you're intending to use
        prompt=user_input,
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def generate_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-ada-002"  # Adjust based on your specific needs
    )
    embedding = response['data'][0]['embedding']
    return embedding

def log_conversation(question, answer):
    combined_text = f"Q: {question} A: {answer}"
    conversation_embedding = generate_embedding(combined_text)
    conversation_id = f"conversation_{int(time.time())}"
    vector_database.upsert(vectors=[(conversation_id, conversation_embedding)])

def main():
    st.title("Chatbot with Pinecone and OpenAI")
    user_input = st.text_input("Your question:")

    if user_input:
        with st.spinner("Thinking..."):
            bot_response = generate_response(user_input)
            log_conversation(user_input, bot_response)
            st.text_area("Bot:", value=bot_response, height=100, max_chars=None, key="bot_response")

if __name__ == "__main__":
    main()
