# Seller Performance Analytics Dashboard

A modern, interactive analytics platform for e-commerce marketplace administrators to monitor seller performance, analyze trends, and generate actionable insights that drive business growth and improve customer satisfaction.

![Seller Analytics Dashboard](https://via.placeholder.com/800x450.png?text=Seller+Analytics+Dashboard+Preview)

## Live Demo

Check out the live demo of this dashboard at:
[https://sellerscope-analytics.streamlit.app](https://sellerscope-analytics.streamlit.app)

The live demo runs in demo mode with generated sample data (no database required).

## Live Demo

Check out the live demo of this dashboard at:
[https://sellerscope-analytics.streamlit.app](https://sellerscope-analytics.streamlit.app)

The live demo runs in demo mode with generated sample data (no database required).

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
  - [Deployment to Streamlit Cloud](#deployment-to-streamlit-cloud)
  - [Local Setup](#local-setup)
- [Using the Dashboard](#using-the-dashboard)
- [KPIs and Metrics](#kpis-and-metrics)
- [Data Analysis](#data-analysis)
- [Business Insights](#business-insights)
- [Architecture](#architecture)
- [Implementation Details](#implementation-details)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)

## Overview

The Seller Performance Analytics Dashboard is a powerful tool designed for e-commerce marketplace administrators to closely monitor seller-level performance metrics. This comprehensive solution enables data-driven decision making by visualizing key performance indicators through an intuitive and interactive interface.

With this dashboard, administrators can:
- Track seller sales trends and revenue generation
- Monitor order fulfillment and delivery performance
- Analyze customer satisfaction through ratings and reviews
- Identify problematic return patterns and their root causes
- Compare performance across different locations and product categories

The system leverages a well-structured PostgreSQL database with optimized queries, powerful Python data processing, and elegant Streamlit visualizations to deliver actionable insights that can improve marketplace operations and seller performance.

## Project Structure

The project is organized into a modular structure that separates concerns and promotes maintainability:

```
Seller Performance Analytics Dashboard/
├── dashboard/                    # Streamlit dashboard application
│   └── app.py                    # Main dashboard application with UI components
├── sql/                          # Database related SQL scripts
│   ├── schema.sql                # Database schema definition with table structures
│   └── kpi_queries.sql           # SQL views for efficient KPI calculations
├── scripts/                      # Utility scripts
│   ├── database_connector.py     # Database connection and query execution class
│   └── demo_data_provider.py     # Demo data provider for running without a database
├── config.py                     # Configuration settings with environment variable support
├── streamlit_app.py              # Entry point for Streamlit Cloud deployment
├── requirements.txt              # Python dependencies with version specifications
├── runtime.txt                   # Python runtime specification for deployment
├── setup.sh                      # Streamlit Cloud setup script
├── Procfile                      # Process file for Streamlit Cloud deployment
├── .gitignore                    # Git ignore patterns
└── README.md                     # Project documentation and user guide
```

## Tech Stack

The application leverages modern technologies to deliver a robust analytics solution:

- **Database**: 
  - PostgreSQL 13+ for reliable relational data storage
  - SQL views for optimized query performance
  - Proper indexing for fast data retrieval

- **Backend**:
  - Python 3.9+ core programming language
  - SQLAlchemy for ORM capabilities and database abstraction
  - Pandas & NumPy for efficient data manipulation and numerical operations
  - Scikit-learn for basic statistical analysis
  - NLTK for text analysis of review comments

- **Visualization**:
  - Streamlit framework for rapid dashboard development
  - Plotly for interactive, publication-quality visualizations
  - Custom CSS for enhanced user experience
  - Responsive design for various screen sizes

- **Development Tools**:
  - Virtual environment for dependency isolation
  - Git for version control
  - Faker library for generating realistic test data
  - Jupyter Notebook for exploratory data analysis

- **Deployment**:
  - Streamlit Cloud for hosting
  - Environment variables for configuration
  - Demo mode for database-less operation

## Features

- **Interactive Dashboard**:
  - Filter by date range, seller location, and product category
  - View top performers and underperformers
  - Analyze monthly sales trends
  - Explore order status distribution

- **Visualizations**:
  - Bar charts for top sellers by revenue
  - Line charts for monthly sales trends
  - Pie charts for order status distribution
  - Scatter plots for ratings vs returns correlation
  - KPI metric cards

- **Seller Drill-down**:
  - Comprehensive breakdown of individual seller performance
  - Product category analysis
  - Rating distribution
  - Return reason analysis

- **Data Export**:
  - Export filtered dataset to CSV
  - Export KPI summary to CSV
  - Export top sellers list to CSV

- **Business Insights**:
  - Actionable recommendations for marketplace improvement
  - Identification of top performer success factors
  - Analysis of underperformer challenges
  - Category-specific insights

### Dashboard Navigation

1. **Filters**: Use the sidebar to filter by date range, seller location, product category, or specific seller
2. **KPI Metrics**: View the top KPI cards at the beginning of the dashboard
3. **Visualizations**: Explore the various tabs for different visualization types
4. **Seller Drill-down**: Select a specific seller to view detailed performance analytics
5. **Data Export**: Use the export section to download data in CSV format

## Setup Instructions

### Deployment to Streamlit Cloud

The dashboard is designed to be easily deployed to Streamlit Cloud:

1. **Fork or Clone the Repository**
   - Fork this repository to your GitHub account, or clone it and push to a new repository.

2. **Connect to Streamlit Cloud**
   - Go to [Streamlit Cloud](https://streamlit.io/cloud) and sign in with your GitHub account.
   - Click "New app" and select your repository.
   - Set the main file path to either `streamlit_app.py` or `dashboard/app.py`.
   - Under "Advanced settings", add the following:
     - Set environment variable `DEMO_MODE` to `true`

3. **Deploy**
   - Click "Deploy" and wait for the build to complete.
   - The app will run in demo mode with generated sample data.

4. **Optional Database Configuration**
   - To use a real PostgreSQL database, set these environment variables:
     - `DB_HOST`: Your database host
     - `DB_NAME`: Database name
     - `DB_USER`: Database username
     - `DB_PASSWORD`: Database password
     - `DB_PORT`: Database port (default 5432)
     - `DEMO_MODE`: Set to `false`

### Local Setup

To run the dashboard locally:

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Seller\ Performance\ Analytics\ Dashboard
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Dashboard in Demo Mode**
   ```bash
   DEMO_MODE=true streamlit run dashboard/app.py
   ```

5. **Optional: Configure a Database**
   - Set up a PostgreSQL database and update the connection parameters in `dashboard/app.py` or use environment variables as mentioned in the Deployment section.
   - Use the SQL scripts in the `sql/` directory to create the necessary tables and views.
   - To run with a database:
     ```bash
     streamlit run dashboard/app.py
     ```

## KPIs and Metrics

The dashboard calculates the following key performance indicators:

1. **Total Orders** per seller
2. **Total Sales Revenue** per seller
3. **Average Order Value (AOV)** = Total Revenue / Total Orders
4. **On-time Delivery Rate** = % of orders delivered within 7 days from shipping
5. **Order Cancellation Rate** = Cancelled Orders / Total Orders
6. **Return Rate** = Returned Orders / Delivered Orders
7. **Average Seller Rating** (1-5 scale)
8. **Negative Review Count** (based on ratings ≤ 2)
9. **Top Performing Sellers** (based on revenue and rating)
10. **Underperforming Sellers** (based on high cancellation or return rates)

## Data Analysis

For a deeper understanding of the data and methodology:

1. Open the Jupyter notebook in the `analysis` directory:
```bash
jupyter notebook analysis/seller_performance_analysis.ipynb
```

2. The notebook provides detailed analysis of:
   - Top performer characteristics
   - Underperformer challenges
   - Correlation between metrics
   - Monthly sales trends
   - Category performance

## Business Insights

A comprehensive business insights report is available at `analysis/business_insights_report.md`. This report includes:

- Executive summary of marketplace performance
- Detailed analysis of top performers and underperformers
- Sales and return trends
- Actionable recommendations for improvement
- Implementation timeline and expected outcomes

## Architecture

The Seller Performance Analytics Dashboard follows a modular three-tier architecture designed for scalability, maintainability, and performance:

```
┌───────────────────────┐
│    Presentation       │
│    Layer (UI)         │
│                       │
│  ┌─────────────────┐  │
│  │  Streamlit UI   │  │
│  │  Components     │  │
│  └────────┬────────┘  │
│           │           │
│  ┌────────┴────────┐  │
│  │  Visualization  │  │
│  │  (Plotly)       │  │
│  └─────────────────┘  │
└───────────┬───────────┘
            │
┌───────────┴───────────┐
│    Business Logic     │
│    Layer              │
│                       │
│  ┌─────────────────┐  │
│  │  Data           │  │
│  │  Processing     │  │
│  └────────┬────────┘  │
│           │           │
│  ┌────────┴────────┐  │
│  │  KPI            │  │
│  │  Calculation    │  │
│  └─────────────────┘  │
└───────────┬───────────┘
            │
┌───────────┴───────────┐
│    Data Access        │
│    Layer              │
│                       │
│  ┌─────────────────┐  │
│  │  Database       │  │
│  │  Connector      │  │
│  └────────┬────────┘  │
│           │           │
│  ┌────────┴────────┐  │
│  │  PostgreSQL     │  │
│  │  Database       │  │
│  └─────────────────┘  │
└───────────────────────┘
```

### 1. Data Access Layer

- **PostgreSQL Database**: Stores all seller and order data in a normalized schema
- **Database Schema**: Comprises four main tables:
  - `Sellers`: Seller profiles with location and category specialization
  - `Orders`: Order details with timestamps and status information
  - `Ratings`: Customer ratings and reviews for sellers
  - `Returns`: Order return information with reasons
- **SQL Views**: Pre-computed aggregations for efficient KPI calculations
- **Database Connector**: Python class that handles database connections and query execution

### 2. Business Logic Layer

- **Data Processing**: Uses Pandas to clean, transform, and prepare data for visualization
- **KPI Calculation**: Computes essential metrics like:
  - Revenue metrics (total revenue, average order value)
  - Operational metrics (on-time delivery rate, return rate)
  - Customer satisfaction metrics (average rating, review sentiment)
- **Data Filtering**: Implements logic for applying user-selected filters
- **Analytics Engine**: Performs statistical analysis and trend detection

### 3. Presentation Layer

- **Streamlit UI**: Provides the interactive web interface with:
  - Filter controls (date range, location, category, seller selection)
  - KPI metric cards displaying key performance numbers
  - Tabbed interface for different visualization types
  - Export functionality for data extraction
- **Visualizations**: Plotly-powered interactive charts and graphs:
  - Bar charts for comparison metrics
  - Line charts for trend analysis over time
  - Pie/donut charts for distribution analysis
  - Scatter plots for correlation analysis
- **Responsive Design**: Adapts to different screen sizes and devices

### Data Flow

1. User interacts with filter controls in the Streamlit UI
2. Filter parameters are passed to the business logic layer
3. Business logic requests filtered data from the data access layer
4. Database connector executes optimized SQL queries
5. Data is processed and transformed in the business logic layer
6. Processed data is used to generate visualizations
7. Visualizations are displayed in the Streamlit UI

This architecture provides clear separation of concerns, making the application easier to maintain and extend. It also ensures good performance by optimizing data access through SQL views and caching frequently used data.

## Implementation Details

The dashboard implementation represents a practical example of modern data engineering and visualization techniques. Here's a detailed breakdown of how each component works:

### Database Design

The database schema was carefully designed to balance normalization principles with query performance:

1. **Normalized Tables**: The core schema uses four main tables (Sellers, Orders, Ratings, Returns) with proper foreign key relationships to maintain data integrity.

2. **SQL Views**: Complex calculations are pre-computed using SQL views, reducing the computational load on the application and providing faster access to aggregated data.

3. **Indexing Strategy**: Strategic indexes on frequently queried columns improve query performance, particularly for:
   - Seller ID for quick seller-specific lookups
   - Order dates for efficient date range filtering
   - Category and location fields for dimensional filtering

4. **Data Types**: Appropriate data types were chosen for each column to optimize storage and query performance (e.g., using `DECIMAL` for monetary values, `TIMESTAMP` for dates).

### Data Generation

The `data_generator.py` script creates synthetic but realistic e-commerce data:

1. **Seller Profiles**: Generates diverse seller profiles with:
   - Varied joining dates to show marketplace growth
   - Geographic distribution across multiple locations
   - Category specialization following realistic market segments

2. **Order Patterns**: Creates order data with:
   - Seasonal variations in sales volume
   - Day-of-week patterns (higher weekend volume)
   - Realistic order value distribution using log-normal distribution
   - Order statuses following typical e-commerce lifecycle

3. **Ratings and Reviews**: Generates rating data with:
   - Correlation between ratings and seller performance
   - Realistic review text using templates and random variations
   - Rating distribution skewed toward the high end (as in real platforms)

4. **Returns Data**: Creates return records with:
   - Common return reasons (damaged items, wrong size, etc.)
   - Higher return rates for certain product categories
   - Correlation between returns and low ratings

### Database Connector

The `database_connector.py` module provides a clean interface between the application and the database:

1. **Connection Pool**: Implements connection pooling for efficient database access

2. **Query Methods**: Provides specialized methods for:
   - KPI calculations with filtering capabilities
   - Data retrieval for different visualization needs
   - Export functionality with customizable output formats

3. **Error Handling**: Robust error management with detailed logging

4. **Performance Optimization**: Uses parameterized queries to prevent SQL injection and improve query planning

### Dashboard Application

The `app.py` file is the heart of the application, implementing the Streamlit interface:

1. **UI Components**:
   - Custom-styled metric cards for KPI display
   - Interactive filter controls in the sidebar
   - Tabbed interface for organizing visualizations
   - Export functionality with download buttons

2. **Data Caching**: Implements Streamlit's caching mechanism to prevent redundant database queries and calculations, significantly improving the user experience during interactive sessions.

3. **Responsive Design**: Custom CSS ensures the dashboard works well on different devices and screen sizes.

4. **Visualization Techniques**:
   - Color schemes chosen for clarity and accessibility
   - Interactive elements like tooltips and hover info
   - Consistent styling across different chart types
   - Appropriate chart types for different data relationships

### Performance Considerations

Several techniques were implemented to ensure good performance:

1. **Query Optimization**: SQL views and efficient joins reduce database load

2. **Data Caching**: Strategic use of Streamlit's `@st.cache_data` decorator to cache expensive operations

3. **Lazy Loading**: Visualizations are only generated when their respective tabs are selected

4. **Efficient Data Processing**: Using vectorized operations in Pandas rather than loops

5. **Pagination**: For large data exports, implementing pagination to avoid memory issues

## Future Enhancements

The Seller Performance Analytics Dashboard has a roadmap for continued improvement and expansion. These planned enhancements will add value to marketplace administrators and improve the overall analytics experience:

### Data and Analytics Enhancements

1. **Advanced Predictive Analytics**:
   - Implement machine learning models to predict seller performance trends
   - Add churn prediction to identify at-risk sellers
   - Develop revenue forecasting capabilities based on historical data

2. **Expanded KPIs and Metrics**:
   - Customer satisfaction correlation with seller performance
   - Return rate analysis and quality control metrics
   - Competitive benchmarking against marketplace averages

3. **Real-time Analytics**:
   - Move from daily to near real-time data processing
   - Implement streaming data pipeline for live updates
   - Add alerting for significant performance changes

