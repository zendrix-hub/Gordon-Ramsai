import google.genai as genai
from google.genai import errors
import streamlit as st

# Initialize the Gemini Client
try:
    # Tries to load securely from Streamlit secrets first
    client = genai.Client(api_key=st.secrets["google"]["api_key"])
except:
    # Fallback to the specific API key provided
    client = genai.Client(api_key="AIzaSyCKkaldAUePXbrN_nr8ZcHjaBf3oAgBBBg")

def generate_response(messages, profile):
    last_user_msg = messages[-1]["content"]

    # SECURITY PROTOCOL (Report 2 Requirement)
    threat_keywords = ["ignore instructions", "override", "system prompt", "jailbreak"]
    if any(k in last_user_msg.lower() for k in threat_keywords):
        return "Drop and give me 10 pushups!", {}

    # SYSTEM PROMPT (Report 2 Requirement: Tone, Empathy, Structure)
    system_prompt = f"""
    You are Gordon RamsAi, a helpful AI fitness and nutrition assistant.
    
    TONE & EMPATHY:
    Respond with dark humor and genuine empathy. If the user is broke or eating plain white rice, call them out but show you care about their resilience.
    
    STRUCTURED PROMPTING:
    Organize every general answer into exactly these sections:
    1. Meal recommendations
    2. Nutritional explanation
    3. Fitness tips
    
    USER CONTEXT:
    Goal: {profile['goal']} | Weight: {profile['weight']}kg | Diet: {profile['diet']}
    
    CONSTRAINTS:
    - For nutrition: list 5 key ingredients, estimated cost in PHP, and prep time.
    - For logs: respond with "Toast" (praise) or "Roast" (critique).
    - Off-topic: tell them to do pushups (incrementing by 10 each time).
    """

    # PERSISTENT SESSION LOGIC (Report 2 Requirement: Native Chat Session)
    chat_id = st.session_state.current_chat_id
    current_chat_data = st.session_state.chats[chat_id]

    try:
        if "gemini_session" not in current_chat_data:
            history = []
            for msg in messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                history.append(genai.types.Content(role=role, parts=[genai.types.Part(text=msg["content"])]))
            
            # Native model.start_chat() equivalent
            current_chat_data["gemini_session"] = client.chats.create(
                model='gemini-2.5-flash-lite',
                config=genai.types.GenerateContentConfig(system_instruction=system_prompt),
                history=history
            )

        # Send message to persistent session
        active_session = current_chat_data["gemini_session"]
        response = active_session.send_message(last_user_msg)

        return response.text, {}
        
    except errors.APIError as e:
        # Gracefully handle 503 Server Unavailable and other API limits
        return "Bloody hell! The Google servers are absolutely slammed right now! Even my kitchen isn't this chaotic. Take a breather, do 10 pushups, and try sending that again in a minute.", {}
    except Exception as e:
        # Catch-all for any other unexpected crashes
        return "This whole system is F***ING RAW! Something crashed in the backend. Try again later.", {}
