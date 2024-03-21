import os
from pinecone import Pinecone as pine, ServerlessSpec
from langchain_community.vectorstores import Pinecone as Cone
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
# Update the import statement for OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
import os


# Assuming langchain_community and langchain packages are installed and accessible
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Pinecone setup
pc = pine(
    api_key=os.environ.get("PINECONE_API_KEY")
)

index_name = "physical-therapy"

# Directory containing your documents
directory = 'content/PhysicalTherapyAssistant'

def load_docs(directory):
    loader = DirectoryLoader(directory)
    documents = loader.load()
    return documents

def split_docs(documents, chunk_size=500, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# Load and split documents
documents = load_docs(directory)
docs = split_docs(documents)
text_documents = [doc.page_content for doc in docs]

embeddings = OpenAIEmbeddings()

# Generate embeddings for each document
model = SentenceTransformer("all-MiniLM-L6-v2")
#embeddings = [model.encode(doc.page_content) for doc in docs]

vector_store = Cone.from_texts(text_documents, embeddings, index_name=index_name)
