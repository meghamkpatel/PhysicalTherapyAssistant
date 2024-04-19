import streamlit as st
import pytest
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import docx
from pinecone import Pinecone
from langchain_community.document_loaders import DirectoryLoader

# Initialize Pinecone and OpenAI services
pinecone_api_key = st.secrets["PINECONE_API_KEY"]
pc = Pinecone(api_key=pinecone_api_key)

# Initialize embeddings generator
embeddings = OpenAIEmbeddings()

# Function to process PDF files
def pdf_to_text(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to process DOCX files
def docx_to_text(file):
    doc = docx.Document(file)
    text = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(text)

# Function to push uploaded file to Pinecone
def push_to_pinecone(file):
    if file.type == "pdf":
        text = pdf_to_text(file)
    elif file.type == "docx":
        text = docx_to_text(file)
    
    vector = embeddings.embed_query(text)
    metadata = {"text": text}
    index_name = "physical-therapy"
    index = pc.Index(index_name)
    index.upsert(vectors=[{
        "id": f"doc_{file.name}", 
        "values": vector, 
        "metadata": metadata
    }])

# Mock file upload function for testing
def mock_file_upload(file_path):
    class MockFile:
        def __init__(self, file_path):
            self.name = file_path.split("/")[-1]
            self.type = file_path.split(".")[-1]
    
    return MockFile(file_path)

# Process file for testing
def process_file(file):
    if file.type == "pdf":
        return pdf_to_text(file)
    elif file.type == "docx":
        return docx_to_text(file)

# Generate bot response for testing
def generate_bot_response(user_input):
    return "Bot response for: " + user_input

# Unit Test Example: Text Extraction from PDF
def test_pdf_to_text():
    test_file_path = "test_file.pdf"
    expected_text = "Sample text extracted from PDF."
    
    with open(test_file_path, "rb") as file:
        extracted_text = pdf_to_text(file)
    
    assert extracted_text == expected_text, f"Expected text: {expected_text}, Actual text: {extracted_text}"

# Integration Test Example: File Upload and Processing
def test_file_upload_and_processing():
    test_file_path = "sample_file.pdf"
    
    uploaded_file = mock_file_upload(test_file_path)
    processed_text = process_file(uploaded_file)
    
    assert processed_text is not None, "File processing failed."

# UI Test Example: Chatbot Interaction
def test_chatbot_interaction():
    user_input = "What is up?"
    bot_response = generate_bot_response(user_input)
    
    assert bot_response is not None, "Chatbot response generation failed."

# Main Streamlit Application
def main():
    st.title("PhysioPhrame")
    
    # Sidebar for file uploading
    filetoimport = st.sidebar.file_uploader("Upload file to push into Pinecone", type=["pdf", "docx"])
    
    if filetoimport:
        push_to_pinecone(filetoimport)
        st.sidebar.success(f"File {filetoimport.name} uploaded and processed!")
    
    # User input for chat
    user_input = st.chat_input("What is up?")
    
    if user_input:
        bot_response = generate_bot_response(user_input)
        st.chat_message("Assistant", bot_response)

# Run Streamlit application
if __name__ == "__main__":
    main()
