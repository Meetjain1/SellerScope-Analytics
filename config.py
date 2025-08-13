import os

# Database configuration
DB_CONFIG = {
    'dbname': os.environ.get('DB_NAME', 'seller_analytics'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', 'postgres'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', '5432'))
}

# Application configuration
APP_CONFIG = {
    'debug': os.environ.get('DEBUG', 'False').lower() == 'true',
    'cache_ttl': int(os.environ.get('CACHE_TTL', '3600'))
}

# Deployment mode
IS_PRODUCTION = os.environ.get('ENVIRONMENT', 'development') == 'production'

# Demo mode configuration
DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() == 'true'

# Detect Streamlit Cloud environment
IS_STREAMLIT_CLOUD = any([
    'STREAMLIT_SHARING' in os.environ,  # Streamlit sharing
    'IS_STREAMLIT_CLOUD' in os.environ,  # Custom flag
    os.environ.get('HOSTNAME', '').startswith('ip-'),  # Streamlit Cloud hostname pattern
    os.environ.get('SERVER_SOFTWARE', '').startswith('uvicorn'),  # Streamlit Cloud server
])

# Force demo mode when on Streamlit Cloud
if IS_STREAMLIT_CLOUD:
    DEMO_MODE = True
