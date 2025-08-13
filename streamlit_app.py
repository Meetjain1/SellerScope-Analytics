#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
streamlit_app.py - Entry point for the Seller Performance Analytics Dashboard

This is the main entry point for the Streamlit Community Cloud deployment.
It imports and runs the main dashboard application.

Created by: Meet Jain
"""

import sys
import os

# Add the current directory to the Python path to ensure proper imports
sys.path.append(os.path.dirname(__file__))

# Import the main dashboard application
from dashboard.app import main

if __name__ == "__main__":
    # Run the main dashboard application
    main()