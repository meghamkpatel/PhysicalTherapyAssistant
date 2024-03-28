from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# Name of your Pinecone index
index_name = "physical-therapy"

# Initialize the Pinecone index
index = Pinecone.Index(index_name)

# Fetch all vector IDs (conceptual; implementation depends on available methods)
# This step assumes there's a method to fetch or list all IDs, which might not be directly available.
# You might need to maintain a separate list of IDs or use queries/filters to retrieve them.
vector_ids = [...]  # You need to determine how to fetch or list all vector IDs

# Delete vectors by IDs
for vector_id in vector_ids:
    index.delete(ids=[vector_id])

# Note: Consider batching deletes if you have a large number of vectors to delete for efficiency
