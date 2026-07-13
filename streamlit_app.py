"""
Streamlit entry point for SOLO ROCK deployment.

Streamlit Cloud automatically runs streamlit_app.py if it exists in the root,
regardless of the "Main file path" setting. This file delegates to dashboard.py,
ensuring the correct cross-platform app runs on any platform (Windows, Linux, macOS).
"""

import os
import sys

# Add repo root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run all dashboard functionality
# This executes dashboard.py's Streamlit app code directly
exec(open("dashboard.py").read())