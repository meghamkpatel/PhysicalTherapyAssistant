import streamlit as st
import openai
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Initialize OpenAI and Pinecone
openai.api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
client = openai.Client()

# Specify your Pinecone index name
index_name = "physical-therapy"
index = pc.Index(index_name)

def generate_openai_response(prompt, temperature=0.7):
    """Generate a response using OpenAI based on the given prompt."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust the model as necessary
        messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                  {"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def search_similar_documents(query, top_k=3):
    """Search for top_k similar documents in Pinecone based on the query."""
    model = OpenAIEmbeddings(model="text-embedding-3-large")
    query_vector = OpenAIEmbeddings().embed_text(query)
    results = index.query(query_vector, top_k=top_k)
    return results["matches"]

st.title("AI Chatbot")

user_input = st.text_input("You: ", "")

if user_input:
    # Generate a response using OpenAI
    bot_response = generate_openai_response(user_input)
    
    # Optionally search for similar documents
    similar_docs = search_similar_documents(user_input)
    similar_docs_text = "\n\n".join([doc["metadata"]["text"] for doc in similar_docs])

    # Display the chatbot's response and similar documents
    st.text_area("Chatbot:", value=bot_response, height=150)
    st.text_area("Similar Documents:", value=similar_docs_text, height=150)
