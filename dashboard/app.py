#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
app.py - Streamlit dashboard for Seller Performance Analytics

This is the main application file for the Seller Performance Analytics Dashboard.
It provides an interactive interface for marketplace administrators to analyze
seller performance metrics through visualizations and data tables.

The dashboard includes:
- KPI metrics (total orders, revenue, average order value, ratings)
- Performance trends over time
- Seller comparisons and rankings
- Detailed seller profiles with historical data
- Custom filtering by date range, location, and category

Created by: Meet Jain
Last updated: 2023
"""

import streamlit as st

# Page configuration MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Seller Performance Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
import base64
from datetime import datetime, timedelta
from io import BytesIO
import importlib.util

# Get the absolute path to the database_connector.py file
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
connector_path = os.path.join(project_root, 'scripts', 'database_connector.py')

# Import database connector with debugging info
import_success = False
error_message = ""

try:
    # Dynamic import using the full file path
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    spec = importlib.util.spec_from_file_location("database_connector", connector_path)
    database_connector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(database_connector)
    DatabaseConnector = database_connector.DatabaseConnector
    import_success = True
except Exception as e:
    error_message = f"Could not import DatabaseConnector. Error: {str(e)}, Path: {connector_path}"

# Show database connector import status
if import_success:
    st.sidebar.success(f"Successfully imported DatabaseConnector")
else:
    st.error(error_message)
    st.error(f"Current directory: {os.getcwd()}")
    st.stop()

# Apply custom styling - using dark theme with responsive design elements
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
st.markdown("""
    <style>
    .main {
        padding: 1.5rem;
        max-width: 1400px;
        margin: 0 auto;
        background-color: #121212;
    }
    .title-container {
        background: linear-gradient(to right, #1E1E1E, #2A2A2A);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .stPlotlyChart {
        background-color: #1E1E1E;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #333;
    }
    /* Hide empty horizontal bars and ensure no empty divs */
    section.main > div:empty,
    div[data-testid="stVerticalBlock"] > div:empty,
    div[data-testid="stHorizontalBlock"] > div:empty {
        display: none !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        border-radius: 5px 5px 0 0;
        padding: 10px 20px;
        color: #ffffff;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2C2C2C !important;
        border-bottom: 2px solid #4285F4;
    }
    /* Button styling */
    .stButton > button {
        background-color: #2C2C2C;
        color: white;
        border: 1px solid #444;
        border-radius: 5px;
        padding: 10px 15px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #444;
        border-color: #666;
    }
    /* Dataframe styling */
    .dataframe {
        background-color: #1E1E1E !important;
        color: #DDD !important;
        border: 1px solid #333 !important;
    }
    .dataframe th {
        background-color: #2C2C2C !important;
        color: white !important;
        font-weight: 600 !important;
    }
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.5rem;
        }
        .metric-card {
            padding: 0.8rem;
            height: 100px;
        }
        .stPlotlyChart {
            padding: 0.8rem;
        }
    }
    /* Header styling */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    /* Text styling */
    p, div {
        color: #CCC;
    }
    .metric-card {
        background-color: #1E1E1E;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        padding: 1.2rem;
        text-align: center;
        margin: 0.5rem;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid #333;
        width: 100%;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #ffffff;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Make sure metrics section is visible */
    [data-testid="stHorizontalBlock"] {
        width: 100%;
        display: flex;
        flex-direction: row;
        gap: 10px;
    }
    /* Fix empty metric boxes */
    .metric-card {
        min-height: 120px;
        background-color: #1E1E1E;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #333;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Database connection parameters - modify as needed
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
@st.cache_resource
def get_database_connection():
    """
    Initialize and return a database connection
    
    This function establishes a connection to the PostgreSQL database using
    the DatabaseConnector class. It's cached to prevent multiple connections
    being created during dashboard interaction.
    
    Returns:
        DatabaseConnector: An active database connection object
    """
    # Get database connection parameters from environment variables or use defaults
    import os
    db_params = {
        'dbname': os.environ.get('DB_NAME', 'seller_analytics'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', 'postgres'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', '5432'))
    }
    
    # Check for DEMO_MODE environment variable
    import os
    demo_mode = os.environ.get('DEMO_MODE', 'false').lower() == 'true'
    
    # Use DemoDataProvider in demo mode or when database connection fails
    if demo_mode:
        from scripts.demo_data_provider import DemoDataProvider
        st.sidebar.success("Running in demo mode with sample data")
        return DemoDataProvider()
    
    # Try to connect to the database
    try:
        db = DatabaseConnector(db_params)
        connection_successful = db.connect()
        
        if not connection_successful:
            st.warning("Failed to connect to the database. Falling back to demo mode with sample data.")
            from scripts.demo_data_provider import DemoDataProvider
            return DemoDataProvider()
        else:
            # Log success for debugging
            st.sidebar.success("Database connection established successfully")
        
        return db
    except Exception as e:
        st.warning(f"Could not connect to the database: {str(e)}. Using demo data instead.")
        try:
            from scripts.demo_data_provider import DemoDataProvider
            return DemoDataProvider()
        except Exception as demo_error:
            st.error(f"Failed to initialize demo data: {str(demo_error)}")
            st.stop()

# Load data with caching
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
@st.cache_data(ttl=3600)
def load_initial_data(_db):
    """
    Load initial data needed for the dashboard
    
    This function retrieves lookup data that's needed for filters and selections.
    Results are cached for one hour to improve performance.
    
    Args:
        _db: DatabaseConnector instance or DemoDataProvider with active connection
        
    Returns:
        dict: Dictionary containing date range, locations, categories, and sellers
    """
    try:
        data = {
            'date_range': _db.get_date_range(),
            'locations': _db.get_locations(),
            'categories': _db.get_categories(),
            'sellers': _db.get_all_sellers()
        }
        
        # No widgets here to avoid CachedWidgetWarning
        return data
    except Exception as e:
        st.error(f"Error loading initial data: {str(e)}")
        # Return empty structures as fallback
        return {
            'date_range': pd.DataFrame([{'min_date': datetime.now() - timedelta(days=365), 'max_date': datetime.now()}]),
            'locations': pd.DataFrame({'seller_location': ['Default Location']}),
            'categories': pd.DataFrame({'product_category': ['Default Category']}),
            'sellers': pd.DataFrame({'seller_id': [0], 'seller_name': ['Default Seller']})
        }

# Load KPI data with filters
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
@st.cache_data(ttl=3600, show_spinner=False, max_entries=100)
def load_kpi_data(_db, filters=None):
    """
    Load KPI data with optional filters
    
    This function retrieves the key performance indicators for sellers,
    applying any filters selected by the user. Results are cached for one hour
    but will refresh when filter parameters change.
    
    Args:
        _db: DatabaseConnector instance with active connection
        filters: Dictionary of filter parameters (date range, location, category, etc.)
        
    Returns:
        DataFrame: KPI data for filtered sellers
    """
    # Convert filters to a hashable string for better caching
    # Including the timestamp in the filter hash to ensure fresh data on page reloads
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    filter_str = str(sorted((filters or {}).items())) + str(datetime.now().minute)
    # Get the data with filters
    return _db.get_seller_kpi_dashboard(filters)

# Load top sellers data with filters
@st.cache_data(ttl=3600, show_spinner=False)
def load_top_sellers(_db, limit=10, filters=None):
    """
    Load top sellers data with optional filters
    
    This function retrieves the top sellers by revenue, applying any filters
    selected by the user. Results are cached for one hour but will refresh 
    when filter parameters change.
    
    Args:
        _db: DatabaseConnector instance with active connection
        limit: Maximum number of top sellers to retrieve
        filters: Dictionary of filter parameters (date range, location, category, etc.)
        
    Returns:
        DataFrame: Top sellers data sorted by revenue
    """
    return _db.get_top_sellers_by_revenue(limit, filters)

# Load monthly trend data with filters
@st.cache_data(ttl=3600, show_spinner=False)
def load_monthly_trend(_db, seller_id=None, filters=None):
    """
    Load monthly trend data with optional filters
    
    Args:
        _db: DatabaseConnector instance
        seller_id: Specific seller to focus on (optional)
        filters: Dictionary of filter parameters
        
    Returns:
        DataFrame: Monthly sales trend data
    """
    return _db.get_monthly_sales_trend(seller_id, filters)

# Load order status distribution with filters
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
@st.cache_data(ttl=3600, show_spinner=False)
def load_order_status(_db, seller_id=None, filters=None):
    """
    Load order status distribution with optional filters
    
    Args:
        _db: DatabaseConnector instance
        seller_id: Specific seller to focus on (optional)
        filters: Dictionary of filter parameters
        
    Returns:
        DataFrame: Order status distribution data
    """
    return _db.get_order_status_distribution(seller_id, filters)

# Load ratings vs returns data with filters
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
@st.cache_data(ttl=3600, show_spinner=False)
def load_ratings_returns(_db, filters=None):
    """
    Load ratings vs returns data with optional filters
    
    Args:
        _db: DatabaseConnector instance
        filters: Dictionary of filter parameters
        
    Returns:
        DataFrame: Correlation data between ratings and return rates
    """
    return _db.get_ratings_returns_correlation(filters)

# Load seller breakdown data
@st.cache_data(ttl=3600)
def load_seller_breakdown(_db, seller_id, start_date=None, end_date=None):
    """Load comprehensive seller breakdown data"""
    return _db.get_full_seller_breakdown(seller_id, start_date, end_date)

# Load export data with filters
@st.cache_data(ttl=3600)
def load_export_data(_db, filters=None):
    """Load data for export with optional filters"""
    return _db.get_filtered_data_for_export(filters)

# Function to create a download link for dataframes
def get_download_link(df, filename, text):
    """Generate a download link for a dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

# Create a KPI metrics row
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
def display_kpi_metrics(kpi_data, filters=None):
    """
    Display a row of KPI metric cards
    
    This function calculates and displays the main KPI metrics at the top of the dashboard.
    It calculates aggregate values based on the filtered data and updates whenever filters change.
    
    Args:
        kpi_data: DataFrame containing KPI data for the current filters
        filters: Dictionary of filter parameters used for generating unique keys
    """
    if filters is None:
        filters = {}
    
    # Reset UI before displaying new metrics to ensure refresh
    st.markdown("### Key Performance Indicators")
    
    # Calculate aggregate KPIs with input validation
    try:
        # Ensure we have valid numeric data by converting columns to numeric types
        for col in ['total_orders', 'total_revenue', 'average_order_value', 'average_rating', 'total_review_count', 'return_rate']:
            if col in kpi_data.columns:
                kpi_data[col] = pd.to_numeric(kpi_data[col], errors='coerce').fillna(0)
        
        # Calculate total orders
        if 'total_orders' in kpi_data.columns and len(kpi_data) > 0:
            total_orders = kpi_data['total_orders'].sum()
        else:
            total_orders = 0
            
        # Calculate total revenue
        if 'total_revenue' in kpi_data.columns and len(kpi_data) > 0:
            total_revenue = kpi_data['total_revenue'].sum()
        else:
            total_revenue = 0
        
        # Calculate average order value directly from filtered data
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        
        # Calculate weighted average rating based on review counts
        if 'total_review_count' in kpi_data.columns and 'average_rating' in kpi_data.columns and len(kpi_data) > 0:
            # Use numpy for better handling of potential NaN values
            weights = kpi_data['total_review_count'].values
            ratings = kpi_data['average_rating'].values
            
            # Calculate weighted average only if we have reviews
            sum_weights = np.sum(weights)
            
            if sum_weights > 0:
                # Weight ratings by review count
                avg_rating = np.sum(ratings * weights) / sum_weights
            else:
                avg_rating = 0
        else:
            avg_rating = 0
        
        # Calculate weighted return rate based on order counts
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        if 'return_rate' in kpi_data.columns and 'total_orders' in kpi_data.columns and len(kpi_data) > 0:
            weights = kpi_data['total_orders'].values
            rates = kpi_data['return_rate'].values
            
            sum_weights = np.sum(weights)
            
            if sum_weights > 0:
                total_return_rate = np.sum(rates * weights) / sum_weights
            else:
                total_return_rate = 0
        else:
            total_return_rate = 0
            
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        total_orders = 0
        total_revenue = 0
        avg_order_value = 0
        avg_rating = 0
        total_return_rate = 0
    
    # Create a unique key for the metrics section to force a refresh when filters change
    # Use the entire filter dictionary as part of the key to ensure refresh when any filter changes
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    metrics_key = f"metrics_{hash(str(filters))}"
    
    # Create columns for KPI cards with unique keys to force refresh
    col1, col2, col3, col4 = st.columns(4, gap="small")
    
    with col1:
        st.markdown(f'''
            <div class="metric-card" id="order-metric-{metrics_key}">
                <div class="metric-value">{total_orders:,.0f}</div>
                <div class="metric-label">Total Orders</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="metric-card" id="revenue-metric-{metrics_key}">
                <div class="metric-value">${total_revenue:,.2f}</div>
                <div class="metric-label">Total Revenue</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <div class="metric-card" id="aov-metric-{metrics_key}">
                <div class="metric-value">${avg_order_value:.2f}</div>
                <div class="metric-label">Avg. Order Value</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
            <div class="metric-card" id="rating-metric-{metrics_key}">
                <div class="metric-value">{avg_rating:.2f}/5</div>
                <div class="metric-label">Avg. Rating</div>
            </div>
        ''', unsafe_allow_html=True)

# Create the top sellers chart
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
def display_top_sellers_chart(top_sellers):
    """
    Display a bar chart of top sellers by revenue
    
    Creates an interactive horizontal bar chart showing the top sellers
    ranked by their total revenue. Each bar also displays the total order count.
    
    Args:
        top_sellers (DataFrame): DataFrame containing seller data with columns:
                                 seller_name, total_revenue, total_orders
    
    Returns:
        None: Displays the chart directly in the Streamlit app
    """
    fig = px.bar(
        top_sellers,
        y='seller_name',
        x='total_revenue',
        title='Top 10 Sellers by Revenue',
        labels={'seller_name': 'Seller', 'total_revenue': 'Total Revenue ($)'},
        color='total_revenue',
        color_continuous_scale='Viridis',
        orientation='h',
        height=500
    )
    
    # Add order count as text
    fig.update_traces(
        text=top_sellers['total_orders'].apply(lambda x: f"{x:,} orders"),
        textposition='inside',
        textfont=dict(size=12, color='white')
    )
    
    # Update layout
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    fig.update_layout(
        xaxis_title='Total Revenue ($)',
        yaxis_title='',
        yaxis=dict(autorange="reversed"),  # Highest revenue at the top
        coloraxis_showscale=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Create the monthly trend chart
def display_monthly_trend_chart(monthly_trend):
    """Display a line chart of monthly sales trends"""
    # Pivot the data for easier plotting
    if 'seller_id' in monthly_trend.columns and 'seller_name' in monthly_trend.columns:
        # Multiple sellers
        monthly_pivot = monthly_trend.pivot_table(
            index='month',
            columns='seller_name', 
            values='monthly_revenue',
            aggfunc='sum'
        ).reset_index()
        
        # Sort by month
        monthly_pivot = monthly_pivot.sort_values('month')
        
        # Create a line chart
        fig = px.line(
            monthly_pivot,
            x='month',
            y=monthly_pivot.columns[1:],  # Skip the 'month' column
            title='Monthly Sales Trend by Seller',
            labels={'value': 'Revenue ($)', 'variable': 'Seller'},
            height=500
        )
    else:
        # Aggregate data
        monthly_pivot = monthly_trend.pivot_table(
            index='month', 
            values=['total_orders', 'monthly_revenue'],
            aggfunc='sum'
        ).reset_index()
        
        # Sort by month
        monthly_pivot = monthly_pivot.sort_values('month')
        
        # Create a line chart with dual y-axes
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add revenue line
        fig.add_trace(
            go.Scatter(
                x=monthly_pivot['month'],
                y=monthly_pivot['monthly_revenue'],
                name='Revenue',
                line=dict(color='rgb(0, 123, 255)', width=3)
            ),
            secondary_y=False
        )
        
        # Add orders line
        fig.add_trace(
            go.Scatter(
                x=monthly_pivot['month'],
                y=monthly_pivot['total_orders'],
                name='Orders',
                line=dict(color='rgb(220, 53, 69)', width=3, dash='dot')
            ),
            secondary_y=True
        )
        
        # Update layout
        fig.update_layout(
            title='Monthly Sales Trend',
            xaxis=dict(title='Month'),
            legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.8)'),
            height=500
        )
        
        # Update y-axes
        fig.update_yaxes(title_text='Revenue ($)', secondary_y=False)
        fig.update_yaxes(title_text='Number of Orders', secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

# Create the order status chart
# © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
def display_order_status_chart(status_distribution):
    """Display a pie chart of order status distribution"""
    if 'seller_id' in status_distribution.columns and len(status_distribution['seller_id'].unique()) > 1:
        # Aggregate across all sellers
        status_agg = status_distribution.groupby('order_status').agg(
            order_count=('order_count', 'sum')
        ).reset_index()
    else:
        # Already aggregated or single seller
        status_agg = status_distribution
    
    # Calculate percentages
    total_orders = status_agg['order_count'].sum()
    status_agg['percentage'] = status_agg['order_count'] / total_orders * 100 if total_orders > 0 else 0
    
    # Create a pie chart
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    fig = px.pie(
        status_agg,
        values='order_count',
        names='order_status',
        title='Order Status Distribution',
        color='order_status',
        color_discrete_map={
            'delivered': 'green',
            'cancelled': 'red',
            'returned': 'orange'
        },
        hole=0.4
    )
    
    # Update text information
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=14
    )
    
    # Update layout
    fig.update_layout(
        legend_title='Order Status',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Create the ratings vs returns chart
def display_ratings_returns_chart(ratings_returns):
    """Display a scatter plot of ratings vs returns correlation"""
    fig = px.scatter(
        ratings_returns,
        x='average_rating',
        y='return_rate',
        title='Correlation: Average Rating vs Return Rate',
        size='total_orders',  # Size points by number of orders
        color='average_rating',  # Color points by rating
        hover_name='seller_name',
        color_continuous_scale='Viridis',
        labels={
            'average_rating': 'Average Rating (1-5)',
            'return_rate': 'Return Rate (%)',
            'total_orders': 'Total Orders',
            'total_revenue': 'Total Revenue ($)'
        },
        height=600
    )
    
    # Add a trend line
    fig.update_layout(
        xaxis=dict(range=[1, 5]),
        yaxis=dict(range=[0, max(ratings_returns['return_rate']) * 1.1 if len(ratings_returns) > 0 else 10])
    )
    
    # Add annotations for correlation
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    if len(ratings_returns) > 5:  # Only calculate if we have enough data
        correlation = ratings_returns['average_rating'].corr(ratings_returns['return_rate'])
        fig.add_annotation(
            x=4.5,
            y=max(ratings_returns['return_rate']) * 0.9 if len(ratings_returns) > 0 else 5,
            text=f"Correlation: {correlation:.2f}",
            showarrow=False,
            font=dict(size=14)
        )
    
    st.plotly_chart(fig, use_container_width=True)

# Display detailed seller breakdown
def display_seller_breakdown(seller_breakdown):
    """
    Display a comprehensive breakdown of a seller's performance
    
    This function creates a detailed seller profile section with:
    - Basic seller information (location, category, join date)
    - Performance summary (orders, revenue, AOV, ratings)
    - Key metrics (return rate, fulfillment metrics)
    - Historical trend charts and performance analysis
    
    Args:
        seller_breakdown (dict): Dictionary containing:
            - seller_info: Basic seller information
            - kpi_data: Performance metrics
            - monthly_data: Time series data for trend analysis
    
    Returns:
        None: Displays the breakdown directly in the Streamlit app
    """
    st.header(f"Detailed Analysis: {seller_breakdown['seller_info'].get('seller_name', 'Seller')}")
    
    # Display basic seller information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Seller Information")
        st.write(f"**Location:** {seller_breakdown['seller_info'].get('seller_location', 'N/A')}")
        st.write(f"**Category Specialization:** {seller_breakdown['seller_info'].get('category_specialization', 'N/A')}")
        join_date = seller_breakdown['seller_info'].get('join_date', 'N/A')
        st.write(f"**Join Date:** {join_date}")
        
        if isinstance(join_date, (datetime, pd.Timestamp)):
            days_since_joining = (datetime.now().date() - join_date.date()).days
            st.write(f"**Days Since Joining:** {days_since_joining}")
    
    with col2:
        st.subheader("Performance Summary")
        kpi_data = seller_breakdown['kpi_data']
        st.write(f"**Total Orders:** {kpi_data.get('total_orders', 0):,.0f}")
        st.write(f"**Total Revenue:** ${kpi_data.get('total_revenue', 0):,.2f}")
        st.write(f"**Average Order Value:** ${kpi_data.get('average_order_value', 0):,.2f}")
        st.write(f"**Average Rating:** {kpi_data.get('average_rating', 0):.2f}/5 ({kpi_data.get('total_review_count', 0)} reviews)")
    
    with col3:
        st.subheader("Key Metrics")
        st.write(f"**Return Rate:** {kpi_data.get('return_rate', 0):.2f}%")
        st.write(f"**Cancellation Rate:** {kpi_data.get('cancellation_rate', 0):.2f}%")
        st.write(f"**On-time Delivery Rate:** {kpi_data.get('ontime_delivery_rate', 0):.2f}%")
        st.write(f"**Negative Reviews:** {kpi_data.get('negative_review_count', 0)} ({kpi_data.get('negative_review_count', 0)/kpi_data.get('total_review_count', 1)*100:.2f}% of all reviews)")
    
    # Tabs for different detailed views
    tab1, tab2, tab3, tab4 = st.tabs(["Sales Trend", "Product Categories", "Order Status", "Ratings & Returns"])
    
    with tab1:
        # Monthly sales trend
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        trend_data = pd.DataFrame(seller_breakdown['trend_data'])
        if not trend_data.empty:
            # Sort by month
            trend_data = trend_data.sort_values('month')
            
            # Create a line chart with dual y-axes
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add revenue line
            fig.add_trace(
                go.Scatter(
                    x=trend_data['month'],
                    y=trend_data['monthly_revenue'],
                    name='Revenue',
                    line=dict(color='rgb(0, 123, 255)', width=3)
                ),
                secondary_y=False
            )
            
            # Add orders line
            fig.add_trace(
                go.Scatter(
                    x=trend_data['month'],
                    y=trend_data['total_orders'],
                    name='Orders',
                    line=dict(color='rgb(220, 53, 69)', width=3, dash='dot')
                ),
                secondary_y=True
            )
            
            # Update layout
            fig.update_layout(
                title='Monthly Sales Trend',
                xaxis=dict(title='Month'),
                legend=dict(x=0.01, y=0.99, bgcolor='rgba(255, 255, 255, 0.8)'),
                height=400
            )
            
            # Update y-axes
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            fig.update_yaxes(title_text='Revenue ($)', secondary_y=False)
            fig.update_yaxes(title_text='Number of Orders', secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No monthly trend data available for this seller.")
    
    with tab2:
        # Product category breakdown
        category_data = pd.DataFrame(seller_breakdown['category_data'])
        if not category_data.empty:
            # Create a bar chart
            fig = px.bar(
                category_data,
                y='product_category',
                x='category_revenue',
                title='Product Category Breakdown',
                color='percentage',
                color_continuous_scale='Viridis',
                orientation='h',
                height=400
            )
            
            # Add order count as text
            fig.update_traces(
                text=category_data['order_count'].apply(lambda x: f"{x:,} orders"),
                textposition='inside',
                textfont=dict(size=12, color='white')
            )
            
            # Update layout
            fig.update_layout(
                xaxis_title='Revenue ($)',
                yaxis_title='',
                yaxis=dict(autorange="reversed")  # Highest revenue at the top
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show the data table
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            st.dataframe(category_data[['product_category', 'order_count', 'percentage', 'category_revenue']])
        else:
            st.info("No product category data available for this seller.")
    
    with tab3:
        # Order status breakdown
        status_data = pd.DataFrame(seller_breakdown['status_data'])
        if not status_data.empty:
            # Create a pie chart
            fig = px.pie(
                status_data,
                values='order_count',
                names='order_status',
                title='Order Status Distribution',
                color='order_status',
                color_discrete_map={
                    'delivered': 'green',
                    'cancelled': 'red',
                    'returned': 'orange'
                },
                hole=0.4
            )
            
            # Update text information
            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=14
            )
            
            # Update layout
            fig.update_layout(
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show the data table
            st.dataframe(status_data[['order_status', 'order_count', 'percentage']])
        else:
            st.info("No order status data available for this seller.")
    
    with tab4:
        # Ratings and returns
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            rating_data = pd.DataFrame(seller_breakdown['rating_data'])
            if not rating_data.empty:
                # Create a bar chart
                fig = px.bar(
                    rating_data,
                    x='rating_score',
                    y='rating_count',
                    title='Rating Distribution',
                    color='rating_score',
                    color_continuous_scale='RdYlGn',  # Red to Yellow to Green
                    height=400
                )
                
                # Update layout
                fig.update_layout(
                    xaxis=dict(title='Rating', tickvals=[1, 2, 3, 4, 5]),
                    yaxis=dict(title='Count')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No rating data available for this seller.")
        
        with col2:
            # Return reasons
            return_data = pd.DataFrame(seller_breakdown['return_data'])
            if not return_data.empty:
                # Create a pie chart
                # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
                fig = px.pie(
                    return_data,
                    values='return_count',
                    names='return_reason',
                    title='Return Reasons',
                    height=400
                )
                
                # Update text information
                fig.update_traces(
                    textposition='inside',
                    textinfo='percent+label',
                    textfont_size=10
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No return data available for this seller.")

# Main function
def main():
    # Initialize database connection
    db = get_database_connection()
    
    # Debug mode checkbox in sidebar (moved from cached function to here)
    debug_mode = st.sidebar.checkbox("Debug Mode", False)
    # Store debug mode in session state for other parts of the app to access
    st.session_state['debug_mode'] = debug_mode
    
    # Load initial data
    initial_data = load_initial_data(_db=db)
    
    # Display debug information if requested
    if debug_mode:
        st.sidebar.write("Data structure types:")
        st.sidebar.write("Date range type:", type(initial_data['date_range']))
        st.sidebar.write("Locations type:", type(initial_data['locations']))
        st.sidebar.write("Categories type:", type(initial_data['categories']))
        st.sidebar.write("Sellers type:", type(initial_data['sellers']))
    
    # Title and description
    st.markdown('''
        <div class="title-container">
            <h1>📊 Seller Performance Analytics Dashboard</h1>
            <p>Analyze seller performance metrics and generate actionable insights for your e-commerce marketplace.</p>
        </div>
    ''', unsafe_allow_html=True)
    
    # Sidebar for filters
    st.sidebar.header("Filters")
    
    # Date range filter
    if not initial_data['date_range'].empty:
        min_date = initial_data['date_range'].iloc[0]['min_date']
        max_date = initial_data['date_range'].iloc[0]['max_date']
        
        # Default to last 3 months if data range is large enough
        default_start = max_date - timedelta(days=90) if max_date - timedelta(days=90) > min_date else min_date
        
        start_date = st.sidebar.date_input(
            "Start Date",
            value=default_start,
            min_value=min_date,
            max_value=max_date
        )
        
        end_date = st.sidebar.date_input(
            "End Date",
            value=max_date,
            min_value=min_date,
            max_value=max_date
        )
        
        # Ensure start_date <= end_date
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        if start_date > end_date:
            st.sidebar.error("Start date cannot be after end date.")
            start_date = end_date
    else:
        start_date = None
        end_date = None
    
    # Location filter
    # Fix for accessing locations data structure, works with both database connector and demo provider
    if isinstance(initial_data['locations'], pd.DataFrame) and 'seller_location' in initial_data['locations'].columns:
        # Demo data provider returns a DataFrame with a seller_location column
        location_options = ['All Locations'] + initial_data['locations']['seller_location'].tolist()
    elif isinstance(initial_data['locations'], dict) and 'seller_location' in initial_data['locations']:
        # Database connector might return a dict with a seller_location key
        location_options = ['All Locations'] + initial_data['locations']['seller_location']
    else:
        # Fallback if structure is unexpected
        location_options = ['All Locations']
        st.warning("Could not load location options. Some filters may not work correctly.")
    
    selected_location = st.sidebar.selectbox("Seller Location", location_options)
    
    # Category filter
    # Fix for accessing categories data structure, works with both database connector and demo provider
    if isinstance(initial_data['categories'], pd.DataFrame) and 'product_category' in initial_data['categories'].columns:
        # Demo data provider returns a DataFrame with a product_category column
        category_options = ['All Categories'] + initial_data['categories']['product_category'].tolist()
    elif isinstance(initial_data['categories'], dict) and 'product_category' in initial_data['categories']:
        # Database connector might return a dict with a product_category key
        category_options = ['All Categories'] + initial_data['categories']['product_category']
    else:
        # Fallback if structure is unexpected
        category_options = ['All Categories']
        st.warning("Could not load category options. Some filters may not work correctly.")
    
    selected_category = st.sidebar.selectbox("Product Category", category_options)
    
    # Seller filter
    # Fix for accessing sellers data structure, works with both database connector and demo provider
    if isinstance(initial_data['sellers'], pd.DataFrame) and 'seller_name' in initial_data['sellers'].columns:
        # Demo data provider returns a DataFrame with seller columns
        seller_options = ['All Sellers'] + initial_data['sellers']['seller_name'].tolist()
    elif isinstance(initial_data['sellers'], dict) and 'seller_name' in initial_data['sellers']:
        # Database connector might return a dict with a seller_name key
        seller_options = ['All Sellers'] + initial_data['sellers']['seller_name']
    else:
        # Fallback if structure is unexpected
        seller_options = ['All Sellers']
        st.warning("Could not load seller options. Some filters may not work correctly.")
        
    selected_seller = st.sidebar.selectbox("Seller", seller_options)
    
    # Create filters dictionary
    filters = {}
    
    if start_date:
        filters['start_date'] = start_date
    
    if end_date:
        filters['end_date'] = end_date
    
    if selected_location != 'All Locations':
        filters['location'] = selected_location
    
    if selected_category != 'All Categories':
        filters['category'] = selected_category
    
    if selected_seller != 'All Sellers':
        # Get seller_id for the selected seller, with error handling for different data structures
        try:
            if isinstance(initial_data['sellers'], pd.DataFrame):
                # For DataFrame structure
                seller_row = initial_data['sellers'][initial_data['sellers']['seller_name'] == selected_seller]
                if not seller_row.empty:
                    seller_id = seller_row['seller_id'].iloc[0]
                    filters['seller_id'] = seller_id
                else:
                    st.warning(f"Could not find seller ID for {selected_seller}")
            elif isinstance(initial_data['sellers'], dict) and 'seller_name' in initial_data['sellers']:
                # For dictionary structure
                seller_names = initial_data['sellers']['seller_name']
                seller_ids = initial_data['sellers']['seller_id']
                if selected_seller in seller_names:
                    idx = seller_names.index(selected_seller)
                    filters['seller_id'] = seller_ids[idx]
                else:
                    st.warning(f"Could not find seller ID for {selected_seller}")
        except Exception as e:
            st.error(f"Error finding seller ID: {str(e)}")
            # Continue without setting seller_id filter
    
    # Store filters in session state to detect changes
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    if 'previous_filters' not in st.session_state:
        st.session_state['previous_filters'] = {}
    
    # Check if filters have changed
    filters_changed = str(filters) != str(st.session_state['previous_filters'])
    
    # Update session state with current filters
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    st.session_state['previous_filters'] = filters.copy()
    
    # Clear cache if filters have changed to force data refresh
    if filters_changed:
        st.cache_data.clear()
        # Add a key to session state to track the filter change
        st.session_state['filter_change_count'] = st.session_state.get('filter_change_count', 0) + 1
        
    # Display session state for debugging (use session state value instead of another checkbox)
    if st.session_state.get('debug_mode', False):
        st.sidebar.write("Current filters:", filters)
        st.sidebar.write("Filters changed:", filters_changed)
        st.sidebar.write("Filter change count:", st.session_state.get('filter_change_count', 0))
    
    # Load KPI data with current filters
    # Include the filter_change_count in the function call to ensure fresh data
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    with st.spinner("Loading dashboard data..."):
        # Use the filter_change_count to force a cache miss when filters change
        filter_key = str(filters) + str(st.session_state.get('filter_change_count', 0))
        kpi_data = load_kpi_data(_db=db, filters=filters)
    
    # Display the dashboard
    if len(kpi_data) > 0:
        # KPI metrics row - pass with filters to force refresh when filters change
        display_kpi_metrics(kpi_data, filters=filters)
        
        # Main dashboard components
        st.header("Seller Performance Overview")
        
        # Visualization tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Top Sellers", "Monthly Trend", "Order Status", "Ratings vs Returns"])
        
        with tab1:
            # Top sellers by revenue
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            top_sellers = load_top_sellers(_db=db, limit=10, filters=filters)
            if len(top_sellers) > 0:
                display_top_sellers_chart(top_sellers)
            else:
                st.info("No seller data available with the current filters.")
        
        with tab2:
            # Monthly sales trend
            if selected_seller != 'All Sellers':
                # Get monthly trend for the selected seller
                monthly_trend = load_monthly_trend(_db=db, seller_id=filters.get('seller_id'), filters=filters)
            else:
                # Get top 5 sellers for the trend chart
                # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
                top_5_sellers = load_top_sellers(_db=db, limit=5, filters=filters)
                if len(top_5_sellers) > 0:
                    # Get monthly trend for top 5 sellers
                    monthly_trend = load_monthly_trend(_db=db, seller_id=None, filters=filters)
                    # Filter to only include top 5 sellers
                    monthly_trend = monthly_trend[monthly_trend['seller_id'].isin(top_5_sellers['seller_id'])]
                else:
                    monthly_trend = load_monthly_trend(_db=db, seller_id=None, filters=filters)
            
            if len(monthly_trend) > 0:
                display_monthly_trend_chart(monthly_trend)
            else:
                st.info("No monthly trend data available with the current filters.")
        
        with tab3:
            # Order status distribution
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            if selected_seller != 'All Sellers':
                # Get order status for the selected seller
                status_distribution = load_order_status(_db=db, seller_id=filters.get('seller_id'), filters=filters)
            else:
                # Get aggregated order status
                status_distribution = load_order_status(_db=db, seller_id=None, filters=filters)
            
            if len(status_distribution) > 0:
                display_order_status_chart(status_distribution)
            else:
                st.info("No order status data available with the current filters.")
        
        with tab4:
            # Ratings vs returns correlation
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            ratings_returns = load_ratings_returns(_db=db, filters=filters)
            if len(ratings_returns) > 0:
                display_ratings_returns_chart(ratings_returns)
            else:
                st.info("No ratings vs returns data available with the current filters.")
        
        # Seller drill-down
        st.header("Seller Drill-Down Analysis")
        
        if selected_seller != 'All Sellers':
            # Display comprehensive breakdown for the selected seller
            seller_breakdown = load_seller_breakdown(_db=db, seller_id=filters.get('seller_id'), start_date=start_date, end_date=end_date)
            display_seller_breakdown(seller_breakdown)
        else:
            # Select a seller for drill-down
            st.info("Select a specific seller from the sidebar to view detailed analysis.")
        
        # Export functionality
        st.header("Export Data")
        
        # Export options
        export_type = st.radio(
            "Select data to export:",
            ["Filtered Dataset", "KPI Summary", "Top Sellers"]
        )
        
        if export_type == "Filtered Dataset":
            # Export the full filtered dataset
            # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            export_data = load_export_data(_db=db, filters=filters)
            if len(export_data) > 0:
                st.write(f"Preview of data to export ({len(export_data)} rows):")
                st.dataframe(export_data.head(10))
                
                # Download button
                st.markdown(
                    get_download_link(export_data, "seller_analytics_data.csv", "Download Full Dataset as CSV"),
                    unsafe_allow_html=True
                )
            else:
                st.info("No data available to export with the current filters.")
        
        elif export_type == "KPI Summary":
            # Export the KPI summary
            if len(kpi_data) > 0:
                st.write(f"Preview of KPI summary ({len(kpi_data)} sellers):")
                st.dataframe(kpi_data.head(10))
                
                # Download button
                st.markdown(
                    get_download_link(kpi_data, "seller_kpi_summary.csv", "Download KPI Summary as CSV"),
                    unsafe_allow_html=True
                )
            else:
                st.info("No KPI data available to export with the current filters.")
        
        elif export_type == "Top Sellers":
            # Export the top sellers data
            top_sellers_export = load_top_sellers(_db=db, limit=50, filters=filters)
            if len(top_sellers_export) > 0:
                st.write(f"Preview of top sellers ({len(top_sellers_export)} sellers):")
                st.dataframe(top_sellers_export.head(10))
                
                # Download button
                st.markdown(
                    get_download_link(top_sellers_export, "top_sellers.csv", "Download Top Sellers as CSV"),
                    unsafe_allow_html=True
                )
            else:
                st.info("No top seller data available to export with the current filters.")
    
    else:
        st.warning("No data available with the current filters. Please adjust your selection.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info(
        "This dashboard provides analytics for seller performance in an e-commerce marketplace. "
        "Use the filters to explore different segments of the data and gain actionable insights."
    )
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    st.sidebar.markdown(f"Data range: {min_date if 'min_date' in locals() else 'N/A'} to {max_date if 'max_date' in locals() else 'N/A'}")

if __name__ == "__main__":
    main()
