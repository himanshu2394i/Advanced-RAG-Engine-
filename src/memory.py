import json
import os
MAX_HISTORY=20
HISTORY_FILE="history.json"




conversation_history=[]

def add_history(role,content):
    conversation_history.append({
        "role":role,
        "content":content
        }
    )
    if len(conversation_history)>MAX_HISTORY:
        conversation_history[:]=conversation_history[-MAX_HISTORY:]
    save_history()

def get_history():
    return conversation_history
def clear_history():
    conversation_history.clear()
    save_history()

def save_history():
    with open(HISTORY_FILE,"w") as f:
        json.dump(conversation_history,f,indent=2)

def load_history():
    global conversation_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE,"r") as f:
            conversation_history=json.load(f)
        print(f"Loaded {len(conversation_history)} messages from history")
    else:
        print("No history found.")

