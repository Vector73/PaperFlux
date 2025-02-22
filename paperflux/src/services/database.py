from pymongo import MongoClient
from src.config.settings import MONGODB_URI, DB_NAME, COLLECTION_NAME
from src.models.paper import Paper

class DatabaseService:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def clear_collection(self):
        self.collection.delete_many({})

    def insert_paper(self, paper: Paper):
        return self.collection.insert_one(paper.to_dict())

    def get_all_papers(self):
        return list(self.collection.find())

    def get_paper_by_id(self, paper_id: str):
        return self.collection.find_one({"paper_id": paper_id})