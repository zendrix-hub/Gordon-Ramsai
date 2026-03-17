import streamlit as st
import random

def apply_bianco_fuji_theme():
    """
    Modular Design Engine:
    - Adaptive Light/Dark Mode (White vs Carbon Fiber)
    - Input Glow
    - BJJ Slide Entrance
    - Endurance Pulse Hover
    - Michelin Plating Scrollbars/Fade
    - NEW: The Roast Box (Aggressive Blockquote UI)
    """
    st.markdown("""
    <style>
        /* =========================================
           ADAPTIVE DESIGN TOKENS
           ========================================= */
        :root {
            --bg-main: #FFFFFF; 
            --bg-sidebar: #F8F9FA; 
            --bg-chat: #FFFFFF; 
            --text-main: #121212; 
            --text-muted: #555555;
            --accent: #E32636; /* Ferrari Red */
            --code-bg: #F1F3F5;
            --border-color: #EAECEF; 
            --btn-hover-bg: #E32636;
            --btn-hover-text: #FFFFFF;
            --btn-shadow: rgba(227, 38, 54, 0.4);
            --box-shadow-chat: 0px 8px 24px rgba(0, 0, 0, 0.05);
            --header-letter-spacing: 2px;
            --roast-bg: #FFF0F0; /* Light red tint for roasts in light mode */
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-main: #050505;
                --bg-sidebar: #0A0A0A;
                --bg-chat: #121212;
                --text-main: #FAFAFA;
                --text-muted: #A0A0A0;
                --accent: #F8F9FA; /* Pearl White */
                --code-bg: #1A1A1A;
                --border-color: #2A2A2A; 
                --btn-hover-bg: #F8F9FA;
                --btn-hover-text: #050505;
                --btn-shadow: rgba(248, 249, 250, 0.3);
                --box-shadow-chat: 0px 6px 16px rgba(0, 0, 0, 0.6); 
                --header-letter-spacing: 4px;
                --roast-bg: #1A0505; /* Deep red/black tint for roasts in dark mode */
            }
        }

        /* CONCEPT 5: THE ROAST BOX (Custom Blockquote UI) */
        [data-testid="stChatMessage"] blockquote {
            background-color: var(--roast-bg) !important;
            border-left: 5px solid var(--accent) !important;
            padding: 15px 20px !important;
            margin: 15px 0 !important;
            border-radius: 0 8px 8px 0 !important;
            color: var(--text-main) !important;
            font-size: 1.05rem !important;
            font-style: italic !important;
            font-weight: 600 !important;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1) !important;
            transition: transform 0.2s ease;
        }
        
        [data-testid="stChatMessage"] blockquote:hover {
            transform: scale(1.02); /* Slight pop when hovering over the insult */
        }

        /* CONCEPT 4: Michelin Plating */
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

        @keyframes appFadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* Global Layout */
        html, body, div.stApp, div[data-testid="stAppViewContainer"], header[data-testid="stHeader"] {
            background-color: var(--bg-main) !important; 
            color: var(--text-main) !important;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            animation: appFadeIn 0.8s ease-out forwards;
        }

        h1, h2, h3, h4, h5, h6, p, span, div { color: var(--text-main); }
        
        section[data-testid="stSidebar"] {
            background-color: var(--bg-sidebar) !important;
            border-right: 1px solid var(--border-color) !important; 
        }

        /* CONCEPT 2: BJJ Strike Animation */
        @keyframes slideUpFade {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        [data-testid="stChatMessage"] {
            background-color: var(--bg-chat) !important;
            color: var(--text-main) !important;
            border-radius: 6px; 
            padding: 1.5rem;
            border-left: 4px solid var(--accent) !important; 
            box-shadow: var(--box-shadow-chat);
            margin-bottom: 1.2rem;
            animation: slideUpFade 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        [data-testid="stChatMessage"]:hover { transform: translateY(-2px); box-shadow: 0px 10px 25px rgba(0,0,0,0.1); }

        [data-testid="stMarkdownContainer"] pre, [data-testid="stMarkdownContainer"] code {
            background-color: var(--code-bg) !important;
            color: var(--text-main) !important; 
            border-radius: 4px;
            padding: 6px 10px;
            font-family: 'Courier New', Courier, monospace;
            border: 1px solid var(--border-color);
        }

        /* CONCEPT 3: Endurance Pulse Buttons */
        div.stButton > button {
            border-radius: 4px !important;
            border: 2px solid var(--accent) !important;
            background-color: transparent !important;
            color: var(--text-main) !important;
            font-weight: 800 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 15px 10px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
        }
        div.stButton > button p, div.stButton > button span, div.stButton > button div { color: inherit !important; }
        div.stButton > button:hover {
            background-color: var(--btn-hover-bg) !important;
            color: var(--btn-hover-text) !important; 
            transform: translateY(-4px); 
            box-shadow: 0px 8px 20px var(--btn-shadow) !important; 
        }
        div.stButton > button:active {
            transform: translateY(0px);
            box-shadow: 0px 2px 10px var(--btn-shadow) !important; 
        }

        section[data-testid="stSidebar"] div.stButton > button {
            border: 1px solid var(--border-color) !important;
            text-transform: none;
            font-weight: 500 !important;
            letter-spacing: 0px;
            padding: 8px 10px !important;
        }
        section[data-testid="stSidebar"] div.stButton > button:hover {
            border-color: var(--accent) !important;
            background-color: transparent !important;
            color: var(--text-main) !important;
            transform: translateX(4px); 
            box-shadow: none !important;
        }

        /* CONCEPT 1: Action Creates Energy Input */
        div[data-testid="stChatInput"] {
            border-radius: 6px !important;
            border: 1px solid var(--border-color) !important;
            background-color: var(--bg-chat) !important;
            box-shadow: var(--box-shadow-chat) !important;
            transition: all 0.3s ease; 
        }
        div[data-testid="stChatInput"]:focus-within {
            border-color: var(--accent) !important;
            box-shadow: 0px 0px 15px var(--btn-shadow) !important;
            transform: scale(1.01); 
        }
        div[data-testid="stChatInput"] textarea {
            background-color: transparent !important;
            color: var(--text-main) !important;
        }

        /* Typography */
        .ramsay-header {
            color: var(--accent) !important;
            font-size: 2.5rem;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: var(--header-letter-spacing);
            margin: 0;
            padding-top: 10px;
        }
        .ramsay-subheader {
            color: var(--text-muted) !important;
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)

def render_main_header():
    st.markdown('<p class="ramsay-header">Gordon RamsAi</p>', unsafe_allow_html=True)
    st.markdown('<p class="ramsay-subheader">The standard is the standard. Trauma is fuel. Action creates energy.</p>', unsafe_allow_html=True)

def render_daily_roast_widget():
    quotes = [
        "🥪 What are you? An idiot sandwich.",
        "🐔 This chicken is so raw it's still singing Hakuna Matata!",
        "👵 My gran could do better! And she's dead!",
        "🦇 There's enough garlic in here to kill every vampire in Europe.",
        "🩴 This meal is as dry as Gandhi's flip-flop!"
    ]
    st.markdown(f"""
    <div style="background-color: var(--bg-chat); border-left: 3px solid var(--accent); padding: 15px; border-radius: 6px; box-shadow: var(--box-shadow-chat); margin-top: 20px; transition: transform 0.2s ease;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
        <p style="color: var(--text-muted); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1.5px;">Chef's Daily Roast</p>
        <p style="color: var(--text-main); font-style: italic; font-size: 0.95rem; margin: 0; font-weight: 600;">"{random.choice(quotes)}"</p>
    </div>
    """, unsafe_allow_html=True)

def get_quick_action_buttons():
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        w = st.button("💪 Quick Workout", use_container_width=True)
        r = st.button("🧘 Rest & Recover", use_container_width=True)
        c = st.button("🛒 Cheap Meal Ideas", use_container_width=True)
    with col2:
        h = st.button("🔥 Hell Week", use_container_width=True)
        f = st.button("🍽️ Fuel & Sweat", use_container_width=True)
        s = st.button("⚡ Pre-Workout Snack", use_container_width=True)
    return {"workout": w, "hell_week": h, "rest": r, "fuel": f, "cheap_meal": c, "snack": s}