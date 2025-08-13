"""
Streamlit app entry point for the Seller Performance Analytics Dashboard
This file is used to run the dashboard from the root directory.
"""

# Import necessary modules
import os
import sys

# Add the project root to the path so we can import from dashboard/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set demo mode for Streamlit Cloud
os.environ['DEMO_MODE'] = 'true'

# Import and run the dashboard app
from dashboard.app import main

# Run the main function
main()
