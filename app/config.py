from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Langflow
    BASE_API_URL = os.getenv("LANGFLOW_BASE_API_URL")
    FLOW_ID = os.getenv("LANGFLOW_FLOW_ID")
    API_KEY = os.getenv("LANGFLOW_API_KEY")
    
    # Feedback DB
    ASTRA_DB_TOKEN = os.getenv("ASTRA_FEEDBACK_DB_TOKEN")
    ASTRA_DB_ENDPOINT = os.getenv("ASTRA_FEEDBACK_DB_ENDPOINT")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_FEEDBACK_DB_KEYSPACE", "chat_feedback")
    ASTRA_DB_TABLE = os.getenv("ASTRA_FEEDBACK_DB_TABLE", "messages")
    
    # Uvicorn
    DEBUG = True
    RELOAD = True
    HOST = "0.0.0.0"
    PORT = 8000
    DEFAULT_TWEAKS = {
        "ChatInput-YZIsE": {},
        "ParseData-N6Rge": {},
        "Prompt-tYQ5F": {},
        "SplitText-CQ17M": {},
        "OpenAIModel-ACgfu": {},
        "ChatOutput-nc48v": {},
        "AstraDB-gooPu": {},
        "OpenAIEmbeddings-VPu7G": {},
        "AstraDB-Hpv50": {},
        "OpenAIEmbeddings-cJJzX": {},
        "File-0Guiq": {}
    }
    
    def validate_astra_config(self):
        """Validate that all required Astra DB settings are present"""
        if not self.ASTRA_DB_TOKEN:
            raise ValueError("ASTRA_DB_TOKEN must be set in environment variables")
        if not self.ASTRA_DB_ENDPOINT:
            raise ValueError("ASTRA_DB_ENDPOINT must be set in environment variables")

settings = Settings()