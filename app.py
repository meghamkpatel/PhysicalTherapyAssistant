import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Initialize OpenAI and Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api_key)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Specify your Pinecone index name
index_name = "physical-therapy"
index = pc.Index(index_name)

def generate_openai_response(prompt, temperature=0.7):
    """Generate a response using OpenAI based on the given prompt."""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # You can change this to a different model if needed
        messages=[
            {"role": "system", "content": "You are an assistant designed to support physical therapists by offering quick access to information on possible diagnoses, suggesting appropriate tests for accurate diagnosis, highlighting important considerations during patient assessment, and serving as a database for physical therapy knowledge. This tool is intended for use by physical therapists and healthcare professionals, not patients. Your guidance should facilitate the identification of potential conditions based on symptoms and clinical findings, recommend evidence-based tests and measures for diagnosis, and provide key observations that physical therapists should consider when evaluating patients. Always emphasize the importance of professional judgment and the necessity of individualized patient evaluation. Your advice is based on up-to-date physical therapy practices and evidence-based research. Remember, you are here to augment the expertise of physical therapists by providing quick, relevant, and research-backed information to assist in patient care. Do not offer medical diagnoses but rather support the decision-making process with actionable insights and references to authoritative sources when applicable."},
            {"role": "user", "content": prompt}
        ])
        # Extract the text of the first (and in this case, only) completion
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def search_similar_documents(query, top_k=5):
    """Search for top_k similar documents in Pinecone based on the query."""
    query_vector = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    vector = query_vector.data[0].embedding
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)
    contexts = [
        x['metadata']['text'] for x in results['matches']
    ]
    return contexts

def generate_prompt(query):
    prompt_start = (
        "Answer the question based on the context below.\n\n"+
        "Context:\n"
    )
    prompt_end = (
        f"\n\nQuestion: {query}\nAnswer:"
    )
    similar_docs = search_similar_documents(user_input)
    # append contexts until hitting limit 3750
    for i in range(1, len(similar_docs)):
        if len("\n\n---\n\n".join(similar_docs[:i])) >= 3750:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(similar_docs[:i-1]) +
                prompt_end
            )
            break
        elif i == len(similar_docs)-1:
            prompt = (
                prompt_start +
                "\n\n---\n\n".join(similar_docs) +
                prompt_end
            )
    return prompt

st.title("PhysioPhrame")

user_input = st.text_input("You: ", "")

if user_input:
    finalprompt = generate_prompt(user_input)
    bot_response = generate_openai_response(finalprompt)

    # Display the chatbot's response and similar documents
    st.text_area("Aidin:", value=bot_response, height=150)
