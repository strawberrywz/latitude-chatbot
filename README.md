# Latitude Chatbot

A chatbot interface for handling apartment-related queries and interactions.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Langflow installed locally

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Langflow:
You can install and run Langflow using either pip or uv:

Using pip:
```bash
pip install langflow
langflow run
```

Using uv (recommended for faster installation):
```bash
uv pip install langflow
langflow run
```

Langflow will start on http://127.0.0.1:7860

3. Configure environment variables:
Copy `.env.example` to `.env` and fill in the following:

- `OPENAI_API_KEY`: Your OpenAI API key for the language model
- `LANGFLOW_API_KEY`: API key from your Langflow instance
- `LANGFLOW_FLOW_ID`: Flow ID from your Langflow configuration
- `LANGFLOW_BASE_API_URL`: Default is http://127.0.0.1:7860

### Database Setup

The chatbot uses two Astra DB databases:

1. Documentation Database:
- Configure using `ASTRA_DB_DOCS_TOKEN` and `ASTRA_DB_DOCS_ENDPOINT`
- Used for storing apartment documentation and knowledge base

2. Feedback Database:
- Configure using `ASTRA_FEEDBACK_DB_*` variables
- Uses AstraPy's Document API
- A `messages` collection will be automatically created on first run
- No manual table creation needed - the application handles this

## Running the Chatbot

1. Start Langflow if not already running:
```bash
langflow run
```

2. Start the chatbot:
```bash
python main.py
```

## Environment Variables

Create a `.env` file with the following structure:
```
OPENAI_API_KEY=           # OpenAI API key
LANGFLOW_API_KEY=         # Your Langflow API key
LANGFLOW_FLOW_ID=         # Your Langflow flow ID
LANGFLOW_BASE_API_URL=    # Langflow URL (default: http://127.0.0.1:7860)

ASTRA_DB_DOCS_TOKEN=      # Astra DB token for documentation database
ASTRA_DB_DOCS_ENDPOINT=   # Astra DB endpoint for documentation

ASTRA_FEEDBACK_DB_TOKEN=  # Astra DB token for feedback database
ASTRA_FEEDBACK_DB_ENDPOINT= # Astra DB endpoint for feedback
ASTRA_FEEDBACK_DB_KEYSPACE=chat_feedback
ASTRA_FEEDBACK_DB_TABLE=messages