import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from pinecone import Pinecone
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as Cone
from langchain_community.document_loaders import DirectoryLoader

# Load environment variables
load_dotenv()

# Initialize Pinecone and OpenAI services
pinecone_api_key = st.secrets["PINECONE_API_KEY"]
pc = Pinecone(api_key=pinecone_api_key)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Pinecone index configuration
index_name = "physical-therapy"
index = pc.Index(index_name)

# Set Streamlit page configuration
st.set_page_config(
    page_title="PhysioPhrame",
    page_icon=":rocket:",
    layout="wide",
)

# --------------------------------Uploading files to Pinecone---------------------------------------------------
def pdf_to_text(file):  
    """Function to extract text from a PDF file."""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to push uploaded file to Pinecone
def push_to_pinecone(file):
    text = pdf_to_text(file)
    
    vector = embeddings.embed_query(text)  # Generate text embeddings
    metadata = {"text": text}  # Prepare metadata
    # Upsert document into Pinecone with metadata
    index.upsert(vectors=[{
        "id": f"doc_{file.name}", 
        "values": vector, 
        "metadata": metadata
    }])

# Initialize embeddings generator
embeddings = OpenAIEmbeddings()

# Sidebar for file uploading
filetoimport = st.sidebar.file_uploader("Upload file to push into Pinecone", type="pdf")

if filetoimport:
    push_to_pinecone(filetoimport)
    st.sidebar.success(f"File {filetoimport.name} uploaded and processed!")

# -------------------------------Main Chat with PhysioPhrame---------------------------------

st.title("PhysioPhrame")

if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

uploaded_file = st.file_uploader("Upload your file", type="pdf")

# File uploader
text_data = ""

# Initialize or load message history
if 'message_history' not in st.session_state:
    st.session_state.message_history = []

def clear_text_input():
    """Function to clear text input."""
    st.session_state.text_input = ''
    
def search_similar_documents(query, top_k=5):
    """Searches for documents in Pinecone that are similar to the query."""
    query_vector = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    vector = query_vector.data[0].embedding
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)
    contexts = [x['metadata']['text'] for x in results['matches']]
    return contexts

def generate_prompt(query):
    """Generates a comprehensive prompt including contexts from similar documents."""
    prompt_start = "Answer the question based on the context below.\n\nContext:\n"
    prompt_end = f"\n\nQuestion: {query}\nAnswer:"
    similar_docs = search_similar_documents(query)
    
    # Compile contexts into a single prompt, respecting character limits
    prompt = prompt_start
    for doc in similar_docs:
        if len(prompt + doc + prompt_end) < 3750:
            prompt += "\n\n---\n\n" + doc
        else:
            break
    prompt += prompt_end
    return prompt

def generate_openai_response(prompt, temperature=0.7):
    """Generates a response from OpenAI based on a structured prompt."""
    try:
        full_prompt = f"{prompt}\n\nAdditional Docs: {text_data}"
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant designed to support physical therapists by offering quick access to information on possible diagnoses, suggesting appropriate tests for accurate diagnosis, highlighting important considerations during patient assessment, and serving as a database for physical therapy knowledge. This tool is intended for use by physical therapists and healthcare professionals, not patients. Your guidance should facilitate the identification of potential conditions based on symptoms and clinical findings, recommend evidence-based tests and measures for diagnosis, and provide key observations that physical therapists should consider when evaluating patients. Always emphasize the importance of professional judgment and the necessity of individualized patient evaluation. Your advice is based on up-to-date physical therapy practices and evidence-based research. Remember, you are here to augment the expertise of physical therapists by providing quick, relevant, and research-backed information to assist in patient care. Do not offer medical diagnoses but rather support the decision-making process with actionable insights and references to authoritative sources when applicable."},
                {"role": "user", "content": full_prompt}
            ] + [
                {"role": "user" if msg['role'] == 'You' else "assistant", "content": msg['content']}
                for msg in st.session_state.message_history
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# User input for chat
user_input = st.chat_input("Ask me a question")

if user_input:
    # Add user's message to history
    st.session_state.message_history.append({"role": "user", "content": user_input})

    if uploaded_file is not None:
        text_data = pdf_to_text(uploaded_file)
        uploaded_file = None  # Clear out the uploaded file

    final_prompt = generate_prompt(user_input)
    bot_response = generate_openai_response(final_prompt)
    
    # Add Aidin's response to history
    st.session_state.message_history.append({"role": "assistant", "content": bot_response})

    # Clear text input
    clear_text_input()

    # Display chat messages from history on app rerun
    for message in st.session_state.message_history:
        role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.markdown(message["content"])
