import streamlit as st
import theme_manager

def render():
    with st.sidebar:
        st.subheader("Profile")
        goal = st.selectbox("The Objective", [
            "Endurance (Ironman Prep)", 
            "Resilience (Injury Recovery)", 
            "Focus (BJJ / Martial Arts)",
            "Utilitarian Health"
        ])
        weight = st.number_input("Weight (kg)", 40, 200, st.session_state.profile["weight"])
        height = st.number_input("Height (cm)", 140, 220, st.session_state.profile["height"])
        workout_days = st.slider("Grind Days per Week", 1, 7, st.session_state.profile["workout_days"])
        diet = st.selectbox("Dietary Constraints", ["High Protein", "Low Carb", "Vegetarian", "Utilitarian Balanced"])
        
        st.session_state.profile = {
            "goal": goal, "weight": weight, "height": height, 
            "workout_days": workout_days, "diet": diet
        }
        
        st.divider()
        if st.button("↻ Wipe Slate Clean", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.current_chat_id in st.session_state.chats:
                st.session_state.chats[st.session_state.current_chat_id] = {}
            st.rerun()
            
        theme_manager.render_daily_roast_widget()