import os
from datetime import datetime
from dotenv import load_dotenv
import json
import streamlit as st

load_dotenv()

# Get API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def save_content(content, filename):
    """Save generated content to file"""
    # Create outputs folder if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    with open(f"outputs/{filename}", "w", encoding="utf-8") as f:
        f.write(content)
    return f"outputs/{filename}"

def log_audit(stage, action, details):
    """Simple audit logging"""
    # Create outputs folder if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "stage": stage,
        "action": action,
        "details": details
    }
    
    # Append to log file
    try:
        with open("outputs/audit_log.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Error writing log: {e}")
    
    return log_entry

def calculate_time_saved(manual_hours, ai_minutes):
    """Calculate impact metrics"""
    manual_minutes = manual_hours * 60
    saved_minutes = manual_minutes - ai_minutes
    saved_percentage = (saved_minutes / manual_minutes) * 100 if manual_minutes > 0 else 0
    return {
        "manual_minutes": manual_minutes,
        "ai_minutes": ai_minutes,
        "saved_minutes": saved_minutes,
        "saved_percentage": saved_percentage
    }

def load_brand_guidelines():
    """Load brand guidelines from file"""
    try:
        with open("data/brand_guidelines.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        # Return default guidelines if file doesn't exist
        return """Brand Guidelines:
- Use professional, authoritative tone
- Avoid jargon - keep it accessible
- Use inclusive language
- No negative language about competitors
- No absolute claims like "best" or "guaranteed"""