import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

class LeadMemoryAgent:
    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        self.vector_store = None

    def add_lead_context(self, lead_id: int, context_text: str):
        """লিডের ডেটা বা স্ক্র্যাপ করা তথ্য মেমোরিতে সেভ করবে"""
        doc = Document(page_content=context_text, metadata={"lead_id": lead_id})
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents([doc], self.embeddings)
        else:
            self.vector_store.add_documents([doc])
            
    def get_relevant_context(self, query: str, lead_id: int = None, k: int = 2):
        """নতুন মেসেজ লেখার সময় আগের প্রাসঙ্গিক তথ্য খুঁজে বের করবে"""
        if self.vector_store is None:
            return "No previous context found."
            
        results = self.vector_store.similarity_search(
            query, 
            k=k, 
            filter={"lead_id": lead_id} if lead_id else None
        )
        return "\n".join([res.page_content for res in results])

memory_agent = LeadMemoryAgent()