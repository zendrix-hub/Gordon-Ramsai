import sys
import subprocess

print("========================================")
print("🔧 GORDON RAMSAI: PRE-FLIGHT CHECK")
print("========================================")

print("⏳ Forcing Langfuse v3.14.6 sync to prevent upstream breaking changes...")
# Force install the stable v3 SDK where .trace() exists
subprocess.check_call([
    sys.executable, "-m", "pip", "install", "langfuse==3.14.6", "--force-reinstall", "--quiet"
])
print("✅ Environment locked and stable.")

print("🚀 Launching application...")
print("========================================")
# Boot Streamlit directly from this exact Python executable
subprocess.check_call([sys.executable, "-m", "streamlit", "run", "app.py"])