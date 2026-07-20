# Gordon RamsAi: Utilitarian Fitness & Nutrition Tracker

Gordon RamsAi is an empirical, utilitarian fitness and nutrition coaching platform powered by Google Gemini and Streamlit. It combines strict macronutrient tracking, real-time feedback (the "Michelin Star" Accountability Rating), a multi-level personality engine (Gordon's Simmering, Boiling, and Inferno Moods), and a local RAG (Retrieval-Augmented Generation) lookup system.

Designed with a high-fidelity red glowing aesthetic, the app features a fully functional user authentication system, data isolation, and persistence.

## Key Features

- **Functional User Authentication:** Create an account, login, and logout. User profile settings, calorie logs, and chat histories are isolated and saved to a persistent database (`users.json`).
- **Dynamic Michelin Accountability:** A real-time rating widget that evaluates daily calorie logs against target macros. Earn `*** Rating` for perfect logs, or get `Disapproved (0 Stars)` and roasted by Chef Gordon!
- **Interactive Intake Logger:** Easily log daily Calories, Protein, Carbs, and Fats. View goals, tracking progress, and a progress bar directly on the dashboard.
- **Gordon's Mood Engine:** Scale the coach's strictness dynamically:
  - *Low (Simmering):* Construction guidance with dry sarcasm.
  - *Medium (Boiling):* Strict metrics tracking and humorous coaching.
  - *Hell's Kitchen (Inferno):* High-intensity motivation! Capitalized shouting, direct roasts, and zero tolerance for slacking.
- **Context-Aware Coaching (RAG):** Retains custom training knowledge (e.g. hydration rules, cheap nutrition tips, endurance guidelines) from a local knowledge base (`knowledge.txt`).

## Tech Stack

- **Frontend/Backend:** Python & Streamlit
- **Generative AI:** Google Gemini API (`google-genai` SDK)
- **Database/Persistence:** Local JSON DB (structured user serialization)
- **Vector Embeddings (RAG):** Local semantic vector lookup

## Directory Structure

```
├── .streamlit/
│   └── secrets.toml          # Secret API Keys (Git ignored)
├── auth_manager.py           # Persistence & verification engine
├── app.py                    # Main app page & authentication views
├── sidebar.py                # Profile settings & controls sidebar
├── theme_manager.py          # Custom CSS style injection & theme engine
├── ai.py                     # AI model interaction & instruction sets
├── rag.py                    # RAG document chunking & vector search
├── knowledge.txt             # Domain rules for retrieval queries
├── requirements.txt          # Package dependencies
└── run.py                    # Startup console helper
```

## Setup & Configuration

This project uses Google Gemini API. Follow these steps to configure your local environment:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zendrix-hub/Gordon-Ramsai.git
   cd Gordon-Ramsai
   ```

2. **Create local secrets configuration:**
   Create a `.streamlit/` folder and a `secrets.toml` file inside it:
   ```toml
   [google]
   api_key = "YOUR_GOOGLE_GEMINI_API_KEY_HERE"
   ```
   *Note: `.streamlit/secrets.toml` is added to `.gitignore` and will never be pushed to version control.*

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```
   or
   ```bash
   streamlit run app.py
   ```

## Development & Best Practices

- **Security first:** Password storage is managed inside the persistence engine, and user configurations are decoupled from remote version control.
- **Responsive Theme:** The interface features a custom dark glassmorphism theme, fire-orange inputs, glowing titles, and responsive metric cards.
