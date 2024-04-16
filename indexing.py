import os
from dotenv import load_dotenv
from pinecone import Pinecone as Pine
from langchain_community.vectorstores import Pinecone as Cone
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pine(api_key=os.environ.get("PINECONE_API_KEY"))

# Specify Pinecone index name
index_name = "physical-therapy"
index = pc.Index(index_name)

# Directory with documents
directory = 'content/PhysicalTherapyAssistant'

def load_docs(directory):
    """Load documents from the specified directory."""
    loader = DirectoryLoader(directory)
    return loader.load()

def split_docs(documents, chunk_size=500, chunk_overlap=20):
    """Split documents into chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# Load and split documents
documents = load_docs(directory)
docs = split_docs(documents)
text_documents = [doc.page_content for doc in docs]

# Initialize embeddings generator
embeddings = OpenAIEmbeddings()

# Store each document chunk with metadata in Pinecone
for i, text in enumerate(text_documents):
    vector = embeddings.embed_query(text)  # Generate text embeddings
    metadata = {"text": text}  # Prepare metadata
    # Upsert document into Pinecone with metadata
    index.upsert(vectors=[{
        "id": f"doc_{i}", 
        "values": vector, 
        "metadata": metadata
    }])
