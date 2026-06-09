# database.py
from .intents import INTENT_PHRASES

def init_db():
    # No more heavy downloads! Runs instantly with 0MB memory overhead.
    print("✅ System initialized successfully.")

def match_intent_pure_python(user_text: str):
    """A lightweight, zero-RAM keyword matching fallback"""
    user_text = user_text.lower().strip()
    
    # Check for exact or keyword matches safely
    for action, phrases in INTENT_PHRASES.items():
        for phrase in phrases:
            if phrase in user_text or user_text in phrase:
                return action
    return "UNKNOWN"