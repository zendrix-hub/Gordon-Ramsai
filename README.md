🏎️ Gordon RamsAi: Utilitarian Fitness & Nutrition Tracker

Gordon RamsAi is an empirical, utilitarian fitness and nutrition assistant powered by Google Gemini. It enforces strict accountability using dynamic contextual prompting, constraint-based safety hooks, and a dual-track psychological response system (The Roast & The Toast).

🔐 Setup & Configuration

This project uses Google Gemini via Streamlit's secrets management. Follow these steps to configure your local environment:

Create a .streamlit folder in the root directory of the project.

Create a secrets.toml file inside the .streamlit folder.

Add your API key to .streamlit/secrets.toml with the following contents:

[google]
api_key = "YOUR_GOOGLE_GEMINI_API_KEY_HERE"

Ensure .streamlit/secrets.toml is added to your .gitignore file so it is never committed to the repository.

🚀 Running Locally

Once your secrets are configured, install the dependencies and run the app:

pip install -r requirements.txt
streamlit run app.py
