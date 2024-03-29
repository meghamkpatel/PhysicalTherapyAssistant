# PhysioPhrame

## Description
PhysioPhrame is a domain-specific application designed to assist physical therapists and healthcare professionals by providing quick access to information through natural language queries. Leveraging the power of Large Language Models (LLM) for semantic understanding and a vector database for efficient data storage and retrieval, PhysioPhrame offers an innovative way to access a wealth of physical therapy knowledge. Whether you're looking for possible diagnoses, appropriate tests, or key considerations during patient assessment, PhysioPhrame is your go-to assistant.

## Features
- **Semantic Search**: Utilizes a vector database to index and retrieve data based on semantic similarity, ensuring that responses are relevant and accurate.
- **Natural Language Interface**: Powered by OpenAI's LLM, the application processes natural language queries, allowing for intuitive interaction.
- **Real-time Response Generation**: Generates responses in real-time, offering quick access to information without navigating through traditional databases.
- **Chat History**: Maintains a session-based chat history for the continuity of interaction, enhancing the user experience by keeping track of the conversation flow.

## How to Run

### Prerequisites
- Python 3.8 or higher
- Streamlit
- OpenAI API Key
- Pinecone API Key
- `dotenv` package for managing environment variables

### Setup
1. **Clone the Repository**: Start by cloning the repository where PhysioPhrame is stored to your local machine.

2. **Install Dependencies**: Install the required Python packages by running the following command in your terminal:
   ```
    pip install streamlit openai pinecone-client python-dotenv
   ```

3. **Set Up Environment Variables**: Create a `.env` file in the root directory of the project and add your OpenAI and Pinecone API keys as follows:
   ```   
   OPENAI_API_KEY='your_openai_api_key'
   PINECONE_API_KEY='your_pinecone_api_key'
   ```

### Running the Application
1. Navigate to the project directory in your terminal.

2. Run the Streamlit application using the command:
```streamlit run PTRAG.py```

4. Streamlit will start the application and provide you with a local URL to access PhysioPhrame.

5. Open the provided URL in your web browser to interact with the application. Input your queries related to physical therapy, and PhysioPhrame will assist you with relevant information.

### Testing
Test the application thoroughly with various natural language queries to evaluate its performance. Ensure that the system returns relevant and accurate responses.

---

**Note**: Replace placeholders (e.g., `'your_openai_api_key'`, `'your_pinecone_api_key'`) with your actual API keys. Ensure that your Pinecone account and index are correctly configured to match the script's requirements.

For any issues or further customization, refer to the official documentation of the used APIs and libraries.
