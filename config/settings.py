"""
Configuration settings for the application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Configuration
    API_KEY = os.getenv("API_KEY", "")
    API_BASE_URL = os.getenv("API_BASE_URL", "")
    
    # Application Settings
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Data Configuration
    DATA_DIR = os.getenv("DATA_DIR", "./data")
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", 3600))
    
    # Visualization Settings
    PLOT_BACKEND = os.getenv("PLOT_BACKEND", "plotly")
