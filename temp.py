from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Initialize Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")  # Make sure you've set this environment variable
pc = Pinecone(api_key=pinecone_api_key)

index_name = "physical-therapy"

# Delete the index if it exists
if index_name in pc.list_indexes().names():
    pc.delete_index(name=index_name)
    print(f"Index {index_name} deleted successfully.")

# Recreate the index (assuming you want to reuse the same name and default settings)
# Specify the dimension of the vectors and the metric ('cosine' or 'euclidean')
dimension = 1536  # Example dimension, adjust according to your needs
metric = "cosine"  # or 'euclidean'

# Recreate the index
pc.create_index(
    name=index_name,
    dimension=dimension,
    metric=metric,
    spec=ServerlessSpec(
        cloud='GCP',  # or your cloud provider
        region='us-central1'  # adjust to your preferred region
    )
)
print(f"Index {index_name} has been recreated.")