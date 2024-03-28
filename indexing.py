import os
from dotenv import load_dotenv
from pinecone import Pinecone as Pine, ServerlessSpec
from langchain_community.vectorstores import Pinecone as Cone
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Load environment variables, particularly for Pinecone API key
load_dotenv()

# Initialize Pinecone with your API key
pc = Pine(api_key=os.environ.get("PINECONE_API_KEY"))

# Name of your Pinecone index
index_name = "physical-therapy"
index = pc.Index(index_name)

# Path to the directory containing your documents
directory = 'content/PhysicalTherapyAssistant'

def load_docs(directory):
    """Loads documents from a specified directory using DirectoryLoader."""
    loader = DirectoryLoader(directory)
    return loader.load()

def split_docs(documents, chunk_size=500, chunk_overlap=20):
    """Splits loaded documents into chunks of specified size and overlap."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

# Load documents and split them into manageable chunks
documents = load_docs(directory)
docs = split_docs(documents)
# Extract text content from each document chunk
text_documents = [doc.page_content for doc in docs]

# Initialize embeddings object - OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

# Utilize Cone (langchain_community's wrapper for Pinecone) to store text documents
# along with their embeddings into the Pinecone index specified
####vector_store = Cone.from_texts(text_documents, embeddings, index_name=index_name)
# At this point, your documents are processed to generate embeddings
# and stored in a Pinecone vector store for future retrieval and similarity search.

# Process and store each document chunk with metadata
for i, text in enumerate(text_documents):
    # Generate embeddings for the text
    vector = embeddings.embed_query(text)
    # Include the original text as metadata
    metadata = {"original_text": text}
    # Upsert the document into Pinecone
    index.upsert(vectors=[{
        "id": f"doc_{i}", 
        "values": vector, 
        "metadata": metadata
    }]
