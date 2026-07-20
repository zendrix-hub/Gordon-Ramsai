import streamlit as st
import theme_manager
import sidebar
import ai
import auth_manager

# Initialize page config first
st.set_page_config(
    page_title="Gordon RamsAi", 
    page_icon=None, 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 0. HELPER: MACRO CALCULATIONS FOR DASHBOARD
# ==========================================
def get_macro_targets(weight, diet, goal):
    goal_lower = goal.lower()
    if "endurance" in goal_lower:
        mapped_goal = "cut"
    elif "resilience" in goal_lower:
        mapped_goal = "maintain"
    elif "focus" in goal_lower:
        mapped_goal = "bulk"
    else:
        mapped_goal = "maintain"
        
    protein_multiplier = {"maintain": 1.8, "cut": 2.2, "bulk": 2.0}.get(mapped_goal, 1.8)
    kcal_per_kg = {"maintain": 33, "cut": 27, "bulk": 38}.get(mapped_goal, 33)

    total_kcal = round(weight * kcal_per_kg)
    protein_g  = round(weight * protein_multiplier)
    protein_kcal = protein_g * 4

    diet_lower = diet.lower()
    normalized_diet = "standard"
    if "low carb" in diet_lower or "keto" in diet_lower: normalized_diet = "keto"
    elif "vegetarian" in diet_lower or "vegan" in diet_lower: normalized_diet = "vegan"

    if normalized_diet == "keto":
        fat_kcal  = round((total_kcal - protein_kcal) * 0.85)
        carb_kcal = total_kcal - protein_kcal - fat_kcal
    elif normalized_diet == "vegan":
        carb_kcal = round((total_kcal - protein_kcal) * 0.60)
        fat_kcal  = total_kcal - protein_kcal - carb_kcal
    else:  # standard
        carb_kcal = round((total_kcal - protein_kcal) * 0.50)
        fat_kcal  = total_kcal - protein_kcal - carb_kcal

    return {
        "calories": total_kcal,
        "protein": protein_g,
        "carbs": max(0, round(carb_kcal / 4)),
        "fat": max(0, round(fat_kcal / 9)),
    }

# ==========================================
# 1. INITIALIZE SESSION STATES & AUTHENTICATION
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

# Inject Design engine styling
theme_manager.apply_bianco_fuji_theme()

# ==========================================
# 2. AUTHENTICATION PAGES (LOGIN / REGISTER)
# ==========================================
if not st.session_state.authenticated:
    theme_manager.render_main_header()
    st.markdown("<p style='font-size: 1.2rem; font-weight: 700; color: var(--text-muted); margin-bottom: 20px;'>AUTHENTICATION REQUIRED</p>", unsafe_allow_html=True)
    
    tab_login, tab_register = st.tabs(["Login", "Register"])
    
    with tab_login:
        username_login = st.text_input("Username", key="username_login")
        password_login = st.text_input("Password", type="password", key="password_login")
        if st.button("Login", use_container_width=True):
            if auth_manager.authenticate_user(username_login, password_login):
                st.session_state.authenticated = True
                st.session_state.username = username_login.strip().lower()
                user_data = auth_manager.get_user_data(st.session_state.username)
                st.session_state.messages = user_data.get("messages", [])
                st.session_state.profile = user_data.get("profile", {})
                st.session_state.tracker = user_data.get("tracker", {"calories": 0, "protein": 0, "carbs": 0, "fat": 0})
                st.success(f"Welcome back, Chef {st.session_state.username.capitalize()}!")
                st.rerun()
            else:
                st.error("Invalid username or password. Get out of my kitchen!")
                
    with tab_register:
        username_reg = st.text_input("Create Username", key="username_reg")
        password_reg = st.text_input("Create Password", type="password", key="password_reg")
        
        st.markdown("<p style='font-weight: 700; margin-top: 15px;'>Initial Profile Setup</p>", unsafe_allow_html=True)
        goals_list = [
            "Endurance (Ironman Prep)", 
            "Resilience (Injury Recovery)", 
            "Focus (BJJ / Martial Arts)",
            "Utilitarian Health"
        ]
        goal_reg = st.selectbox("Objective", goals_list, index=3, key="goal_reg")
        weight_reg = st.number_input("Weight (kg)", 40, 200, 70, key="weight_reg")
        height_reg = st.number_input("Height (cm)", 140, 220, 170, key="height_reg")
        days_reg = st.slider("Grind Days per Week", 1, 7, 4, key="days_reg")
        diets_list = ["High Protein", "Low Carb", "Vegetarian", "Utilitarian Balanced"]
        diet_reg = st.selectbox("Dietary Constraints", diets_list, index=0, key="diet_reg")
        
        if st.button("Register Account", use_container_width=True):
            user_reg_clean = username_reg.strip().lower()
            if not user_reg_clean or not password_reg:
                st.error("Username and password are required, donkey!")
            else:
                default_profile = {
                    "goal": goal_reg,
                    "weight": weight_reg,
                    "height": height_reg,
                    "workout_days": days_reg,
                    "diet": diet_reg,
                    "heat_level": "Medium (Boiling)"
                }
                if auth_manager.register_user(user_reg_clean, password_reg, default_profile):
                    st.session_state.authenticated = True
                    st.session_state.username = user_reg_clean
                    user_data = auth_manager.get_user_data(user_reg_clean)
                    st.session_state.messages = user_data.get("messages", [])
                    st.session_state.profile = user_data.get("profile", {})
                    st.session_state.tracker = user_data.get("tracker", {"calories": 0, "protein": 0, "carbs": 0, "fat": 0})
                    st.success("Account registered! Let's get to work!")
                    st.rerun()
                else:
                    st.error("Username already exists. Be original!")
    st.stop()

# ==========================================
# 3. RENDER MAIN VIEWS (If Authenticated)
# ==========================================
# Render the sidebar (which loads active user settings and handles change-saves)
sidebar.render()
theme_manager.render_main_header()

tracker = st.session_state.tracker

# Calculate Targets based on current profile
targets = get_macro_targets(
    weight=st.session_state.profile.get("weight", 70),
    diet=st.session_state.profile.get("diet", "High Protein"),
    goal=st.session_state.profile.get("goal", "Utilitarian Health")
)

# Michelin Stars calculation
logged_cals = tracker.get("calories", 0)
target_cals = targets.get("calories", 2000)

if logged_cals == 0:
    rating_stars = "*** Rating"
    rating_msg = "A fresh, clean kitchen. Keep the standard high today!"
    rating_color = "var(--text-muted)"
else:
    diff_pct = (abs(logged_cals - target_cals) / target_cals) * 100
    if diff_pct <= 10:
        rating_stars = "*** Rating"
        rating_msg = "Perfect execution. Michelin-star standard!"
        rating_color = "#FFD700" # Gold
    elif diff_pct <= 25:
        rating_stars = "** Rating"
        rating_msg = "Solid effort, but you can plate this better."
        rating_color = "#E6C229" # Darker Gold
    elif diff_pct <= 50:
        rating_stars = "* Rating"
        rating_msg = "Messy presentation. You're testing my patience!"
        rating_color = "#D27D2D" # Copper
    else:
        rating_stars = "Disapproved (0 Stars)"
        rating_msg = "An absolute disaster! GET OUT OF MY KITCHEN!"
        rating_color = "#E32636" # Flame Red
        
st.markdown(f"""
<div style="background-color: var(--bg-chat); border-left: 5px solid {rating_color}; padding: 15px; border-radius: 6px; box-shadow: var(--box-shadow-chat); margin-bottom: 25px;">
    <p style="color: var(--text-muted); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1.5px;">Chef's Kitchen Rating</p>
    <h3 style="color: {rating_color}; font-size: 1.6rem; font-weight: 900; margin: 0 0 5px 0;">{rating_stars}</h3>
    <p style="color: var(--text-main); font-size: 0.95rem; font-weight: 600; margin: 0;">"{rating_msg}"</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size:1.5rem; font-weight:800; text-transform:uppercase; margin-bottom:10px; margin-top:20px; color:var(--accent);'>Today's Fuel Stats</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        label="Calories",
        value=f"{tracker.get('calories', 0)} / {targets['calories']} kcal",
        delta=f"{targets['calories'] - tracker.get('calories', 0)} left" if targets['calories'] > tracker.get('calories', 0) else "Goal Met!"
    )
with col2:
    st.metric(
        label="Protein",
        value=f"{tracker.get('protein', 0)} / {targets['protein']} g",
        delta=f"{targets['protein'] - tracker.get('protein', 0)} left" if targets['protein'] > tracker.get('protein', 0) else "Goal Met!"
    )
with col3:
    st.metric(
        label="Carbs",
        value=f"{tracker.get('carbs', 0)} / {targets['carbs']} g",
        delta=f"{targets['carbs'] - tracker.get('carbs', 0)} left" if targets['carbs'] > tracker.get('carbs', 0) else "Goal Met!"
    )
with col4:
    st.metric(
        label="Fat",
        value=f"{tracker.get('fat', 0)} / {targets['fat']} g",
        delta=f"{targets['fat'] - tracker.get('fat', 0)} left" if targets['fat'] > tracker.get('fat', 0) else "Goal Met!"
    )

# Progress bar
progress_val = min(1.0, max(0.0, tracker.get('calories', 0) / (targets['calories'] or 1)))
st.progress(progress_val, text=f"Daily Caloric Goal Progress: {int(progress_val*100)}%")

# Simplified Logging row directly visible
st.markdown("<p style='font-size:1.1rem; font-weight:700; text-transform:uppercase; margin-top:20px; margin-bottom:10px;'>Quick Intake Logger</p>", unsafe_allow_html=True)
col_l1, col_l2, col_l3, col_l4 = st.columns(4)
with col_l1:
    log_cal = st.number_input("Log Calories", 0, 5000, 0, step=50, key="log_cal_input")
with col_l2:
    log_prot = st.number_input("Log Protein (g)", 0, 300, 0, step=5, key="log_prot_input")
with col_l3:
    log_carb = st.number_input("Log Carbs (g)", 0, 500, 0, step=5, key="log_carb_input")
with col_l4:
    log_fat = st.number_input("Log Fat (g)", 0, 200, 0, step=5, key="log_fat_input")
    
log_col1, log_col2 = st.columns(2)
with log_col1:
    if st.button("Add Log", use_container_width=True):
        st.session_state.tracker["calories"] += log_cal
        st.session_state.tracker["protein"] += log_prot
        st.session_state.tracker["carbs"] += log_carb
        st.session_state.tracker["fat"] += log_fat
        # Persist immediately
        auth_manager.save_user_data(
            st.session_state.username,
            st.session_state.profile,
            st.session_state.tracker,
            st.session_state.messages
        )
        st.success("Log updated successfully!")
        st.rerun()
with log_col2:
    if st.button("Reset Today's Log", use_container_width=True):
        st.session_state.tracker = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        # Persist immediately
        auth_manager.save_user_data(
            st.session_state.username,
            st.session_state.profile,
            st.session_state.tracker,
            st.session_state.messages
        )
        st.warning("Reset today's logs.")
        st.rerun()

st.markdown("<hr style='border: 1px solid var(--border-color); margin: 30px 0;'>", unsafe_allow_html=True)

# ==========================================
# 4. CHAT HISTORY
# ==========================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 5. QUICK ACTIONS & INPUT
# ==========================================
# Interactive 2x3 Grid of buttons
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
    with st.chat_message("user"):
        st.markdown(ui_prompt)
    st.session_state.messages.append({"role": "user", "content": ui_prompt})
    
    # Save user message to file persistence
    auth_manager.save_user_data(
        st.session_state.username,
        st.session_state.profile,
        st.session_state.tracker,
        st.session_state.messages
    )
    
    # Fetch AI Response using the compliant logic in ai.py
    with st.chat_message("assistant"):
        with st.spinner("Assessing this absolute disaster..."):
            response_text, _ = ai.generate_response(st.session_state.messages, st.session_state.profile)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            # Save assistant response to file persistence
            auth_manager.save_user_data(
                st.session_state.username,
                st.session_state.profile,
                st.session_state.tracker,
                st.session_state.messages
            )
            
            # Scripted safety response stop
            if response_text == "Drop and give me 10 pushups!":
                st.stop()