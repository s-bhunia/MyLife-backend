# database.py
import chromadb
from .intents import INTENT_PHRASES


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="portfolio_intents")

def init_db():
    """Validates and synchronizes the local vector database with intents.py."""
    global chroma_client, collection
    total_phrases = sum(len(phrases) for phrases in INTENT_PHRASES.values())

    if collection.count() != total_phrases:
        print("🔄 Synchronizing database with latest intents file...")
        try:
            chroma_client.delete_collection(name="portfolio_intents")
        except Exception:
            pass
        
        collection = chroma_client.create_collection(name="portfolio_intents")
        
        docs, metas, ids = [], [], []
        for action, phrases in INTENT_PHRASES.items():
            for i, phrase in enumerate(phrases):
                docs.append(phrase)
                metas.append({"action": action})
                ids.append(f"{action}_{i}")
                
        collection.add(documents=docs, metadatas=metas, ids=ids)
        print("✅ ChromaDB intents synced successfully.")
    else:
        print("✅ ChromaDB database is already up to date. ok")