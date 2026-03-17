import streamlit as st
import theme_manager
import sidebar
import ai

# Initialize page config first
st.set_page_config(
    page_title="Gordon RamsAi", 
    page_icon="🏎️", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 1. INITIALIZE SESSION STATES
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Listen to me! I'm Gordon RamsAi. We're not doing fads, we're doing the standard. Pressure is a privilege, so turn it into energy. What are we grinding today? LFG!"
    }]

if "chats" not in st.session_state:
    st.session_state.chats = {"default": {}}

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = "default"

if "profile" not in st.session_state:
    st.session_state.profile = {
        "goal": "Utilitarian Health", 
        "weight": 70, 
        "height": 170, 
        "workout_days": 4, 
        "diet": "High Protein"
    }

# ==========================================
# 2. INJECT THE DESIGN ENGINE
# ==========================================
# Applies Bianco Fuji theme, adaptive modes, and interactive animations
theme_manager.apply_bianco_fuji_theme()

# ==========================================
# 3. RENDER SIDEBAR & HEADER
# ==========================================
sidebar.render()
theme_manager.render_main_header()

# ==========================================
# 4. CHAT HISTORY
# ==========================================
for msg in st.session_state.messages:
    avatar_img = "🏎️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_img):
        st.markdown(msg["content"])

# ==========================================
# 5. QUICK ACTIONS & INPUT
# ==========================================
# Interactive 2x3 Grid of buttons from Report 2
buttons = theme_manager.get_quick_action_buttons()

ui_prompt = None
if buttons["workout"]: ui_prompt = "Give me a brutal 15-minute quick workout using only bodyweight or household items."
if buttons["rest"]: ui_prompt = "I am exhausted. I need a proper rest and recovery protocol for today."
if buttons["cheap_meal"]: ui_prompt = "I need cheap meal ideas for a broke student. Keep it strictly 5 ingredients and show the cost in PHP."
if buttons["hell_week"]: ui_prompt = "LFG! Initiate Hell Week. Give me the most grueling endurance routine you have."
if buttons["fuel"]: ui_prompt = "I need a 'Fuel & Sweat' meal plan. Use a hypercar metaphor to explain the nutrition."
if buttons["snack"]: ui_prompt = "Give me a fast, utilitarian pre-workout snack idea."

# Handle the standard chat input with "Action Creates Energy" glow
if text_input := st.chat_input("Action creates energy. Log your grind or ask for fuel..."):
    ui_prompt = text_input

# ==========================================
# 6. AI RESPONSE GENERATION
# ==========================================
if ui_prompt:
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(ui_prompt)
    st.session_state.messages.append({"role": "user", "content": ui_prompt})
    
    # Fetch AI Response using the compliant logic in ai.py
    with st.chat_message("assistant", avatar="🏎️"):
        with st.spinner("Assessing this absolute disaster..."):
            response_text, _ = ai.generate_response(st.session_state.messages, st.session_state.profile)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            # Scripted safety response stop
            if response_text == "Drop and give me 10 pushups!":
                st.stop()