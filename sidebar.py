import streamlit as st
import theme_manager
import auth_manager

def render():
    with st.sidebar:
        # Check authentication first
        if not st.session_state.get("authenticated", False):
            st.markdown("<p style='color: var(--text-muted); font-size: 0.95rem; font-weight: 600;'>Please login to view profile.</p>", unsafe_allow_html=True)
            return

        # ============================================================
        # 1. USER PROFILE
        # ============================================================
        st.markdown(f"<h3 style='color: var(--accent); margin-bottom: 0px;'>Chef {st.session_state.username.capitalize()}</h3>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.8rem; color: var(--text-muted); margin-bottom: 20px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>Kitchen Active</p>", unsafe_allow_html=True)
        
        st.subheader("Profile")
        
        # Load profile from global state
        profile = st.session_state.profile
        
        goals_list = [
            "Endurance (Ironman Prep)", 
            "Resilience (Injury Recovery)", 
            "Focus (BJJ / Martial Arts)",
            "Utilitarian Health"
        ]
        goal_idx = goals_list.index(profile.get("goal", "Utilitarian Health")) if profile.get("goal") in goals_list else 3

        diets_list = ["High Protein", "Low Carb", "Vegetarian", "Utilitarian Balanced"]
        diet_idx = diets_list.index(profile.get("diet", "High Protein")) if profile.get("diet") in diets_list else 0

        heats_list = ["Low (Simmering)", "Medium (Boiling)", "Hell's Kitchen (Inferno)"]
        heat_idx = heats_list.index(profile.get("heat_level", "Medium (Boiling)")) if profile.get("heat_level") in heats_list else 1

        goal = st.selectbox("The Objective", goals_list, index=goal_idx)
        weight = st.number_input("Weight (kg)", 40, 200, int(profile.get("weight", 70)))
        height = st.number_input("Height (cm)", 140, 220, int(profile.get("height", 170)))
        workout_days = st.slider("Grind Days per Week", 1, 7, int(profile.get("workout_days", 4)))
        diet = st.selectbox("Dietary Constraints", diets_list, index=diet_idx)
        heat_level = st.selectbox("Gordon's Mood", heats_list, index=heat_idx)
        
        # Save changes directly back
        new_profile = {
            "goal": goal, 
            "weight": weight, 
            "height": height, 
            "workout_days": workout_days, 
            "diet": diet, 
            "heat_level": heat_level
        }
        st.session_state.profile = new_profile
        
        # Save to file persistence
        auth_manager.save_user_data(
            st.session_state.username,
            new_profile,
            st.session_state.tracker,
            st.session_state.messages
        )
        
        st.divider()
        if st.button("Wipe Slate Clean", use_container_width=True):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Clean slate! No excuses now. LFG!"
            }]
            st.session_state.tracker = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
            auth_manager.save_user_data(
                st.session_state.username,
                st.session_state.profile,
                st.session_state.tracker,
                st.session_state.messages
            )
            st.rerun()
            
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.messages = []
            st.session_state.profile = {}
            st.session_state.tracker = {}
            st.rerun()
            
        theme_manager.render_daily_roast_widget()