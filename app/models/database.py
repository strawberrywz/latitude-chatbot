from astrapy import DataAPIClient
from config import settings

class Database:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.client = DataAPIClient(settings.ASTRA_DB_TOKEN)
        self.db = self.client.get_database(settings.ASTRA_DB_ENDPOINT)
        
        try:
            collections = self.db.list_collection_names()
            
            if "messages" not in collections:
              self.messages = self.db.create_collection('messages')
              print("Created 'messages' collection")
            else:
              self.messages = self.db["messages"] 
        except Exception as e:
            print(f"Collection access error: {e}")
    
    def test_connection(self):
        """Test the database connection"""
        try:
            db_info = self.db.info()
            return f"Connected to Astra DB. Database name: {db_info.name}"
        except Exception as e:
            return f"Connection error: {str(e)}"