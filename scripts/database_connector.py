#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
database_connector.py - Database connection and analysis functions for Seller Analytics Dashboard
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseConnector:
    """Class to handle database connections and queries for the Seller Analytics Dashboard"""
    
    def __init__(self, db_params=None):
        """Initialize the database connector with connection parameters"""
        self.db_params = db_params or {
            'dbname': os.environ.get('DB_NAME', 'seller_analytics'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', 'postgres'),
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': int(os.environ.get('DB_PORT', '5432'))
        }
        self.engine = None
        
        # Check if we have a DATABASE_URL environment variable (used by many cloud platforms)
        database_url = os.environ.get('DATABASE_URL')
        if database_url and database_url.startswith('postgres://'):
            # Convert postgres:// to postgresql:// for SQLAlchemy
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            self.connection_string = database_url
        else:
            # Create connection string from parameters
            self.connection_string = f"postgresql://{self.db_params['user']}:{self.db_params['password']}@{self.db_params['host']}:{self.db_params['port']}/{self.db_params['dbname']}"
    
    def connect(self):
        """Establish a connection to the database"""
        try:
            self.engine = create_engine(self.connection_string)
            # Test the connection by executing a simple query
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Error connecting to database: {str(e)}")
            return False
    
    def execute_query(self, query, params=None):
        """Execute a SQL query and return the result as a DataFrame"""
        try:
            return pd.read_sql_query(text(query), self.engine, params=params)
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            logger.error(f"Query: {query}")
            return pd.DataFrame()
    
    def get_all_sellers(self):
        """Get a list of all sellers"""
        query = "SELECT seller_id, seller_name FROM sellers ORDER BY seller_name"
        return self.execute_query(query)
    
    def get_seller_details(self, seller_id=None):
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        """Get detailed information about a seller or all sellers"""
        if seller_id:
            query = """
            SELECT * FROM sellers 
            WHERE seller_id = :seller_id
            """
            return self.execute_query(query, params={"seller_id": seller_id})
        else:
            query = "SELECT * FROM sellers"
            return self.execute_query(query)
    
    def get_date_range(self):
        """Get the min and max order dates in the database"""
        query = """
        SELECT 
            MIN(order_date) as min_date, 
            MAX(order_date) as max_date 
        FROM orders
        """
        return self.execute_query(query)
    
    def get_locations(self):
        """Get a list of all seller locations"""
        query = """
        SELECT DISTINCT seller_location 
        FROM sellers 
        ORDER BY seller_location
        """
        return self.execute_query(query)
    
    def get_categories(self):
        """Get a list of all product categories"""
        query = """
        SELECT DISTINCT product_category 
        FROM orders 
        ORDER BY product_category
        """
        return self.execute_query(query)
    
    def get_seller_kpi_dashboard(self, filters=None):
        """Get the KPI dashboard view with optional filters"""
        # Use a more advanced query to calculate KPIs based on filters
        # This ensures KPI metrics reflect the selected date range, category, etc.
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        query = """
        WITH filtered_orders AS (
            SELECT 
                o.order_id,
                o.seller_id,
                o.order_value,
                o.order_status,
                o.order_date,
                r.rating_score,
                r.rating_id
            FROM 
                orders o
            LEFT JOIN 
                ratings r ON o.order_id = r.order_id
            WHERE 1=1
        """
        
        where_clauses_orders = []
        params = {}
        
        # Apply filters to the orders directly
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        if filters:
            if 'start_date' in filters and filters['start_date']:
                where_clauses_orders.append("o.order_date >= :start_date")
                params['start_date'] = filters['start_date']
            
            if 'end_date' in filters and filters['end_date']:
                where_clauses_orders.append("o.order_date <= :end_date")
                params['end_date'] = filters['end_date']
            
            if 'category' in filters and filters['category']:
                where_clauses_orders.append("o.product_category = :category")
                params['category'] = filters['category']
        
        if where_clauses_orders:
            query += " AND " + " AND ".join(where_clauses_orders)
            
        query += """
        )
        SELECT
            s.seller_id,
            s.seller_name,
            s.seller_location,
            s.join_date,
            COUNT(fo.order_id) AS total_orders,
            COALESCE(SUM(CASE WHEN fo.order_status NOT IN ('cancelled', 'returned') THEN fo.order_value ELSE 0 END), 0) AS total_revenue,
            COALESCE(
                SUM(CASE WHEN fo.order_status NOT IN ('cancelled', 'returned') THEN fo.order_value ELSE 0 END) / 
                NULLIF(COUNT(CASE WHEN fo.order_status NOT IN ('cancelled', 'returned') THEN 1 ELSE NULL END), 0),
                0
            ) AS average_order_value,
            COALESCE(AVG(fo.rating_score), 0) AS average_rating,
            COUNT(fo.rating_id) AS total_review_count,
            COALESCE(
                COUNT(CASE WHEN fo.order_status = 'returned' THEN 1 ELSE NULL END) * 100.0 / 
                NULLIF(COUNT(fo.order_id), 0),
                0
            ) AS return_rate
        FROM
            sellers s
        LEFT JOIN
            filtered_orders fo ON s.seller_id = fo.seller_id
        """
        
        where_clauses = []
        
        # Apply seller and location filters to the final result
        if filters:
            if 'seller_id' in filters and filters['seller_id']:
                where_clauses.append("s.seller_id = :seller_id")
                params['seller_id'] = filters['seller_id']
            
            if 'location' in filters and filters['location']:
                where_clauses.append("s.seller_location = :location")
                params['location'] = filters['location']
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
        GROUP BY
            s.seller_id,
            s.seller_name,
            s.seller_location,
            s.join_date
        ORDER BY 
            total_revenue DESC
        """
        
        return self.execute_query(query, params=params)
    
    def get_top_sellers_by_revenue(self, limit=10, filters=None):
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        """Get the top sellers by revenue"""
        query = """
        SELECT 
            s.seller_id,
            s.seller_name,
            COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS total_revenue,
            COUNT(o.order_id) AS total_orders
        FROM 
            sellers s
        LEFT JOIN 
            orders o ON s.seller_id = o.seller_id
        """
        
        where_clauses = []
        params = {'limit': limit}
        
        if filters:
            if 'location' in filters and filters['location']:
                where_clauses.append("s.seller_location = :location")
                params['location'] = filters['location']
            
            if 'start_date' in filters and filters['start_date']:
                where_clauses.append("o.order_date >= :start_date")
                params['start_date'] = filters['start_date']
            
            if 'end_date' in filters and filters['end_date']:
                where_clauses.append("o.order_date <= :end_date")
                params['end_date'] = filters['end_date']
            
            if 'category' in filters and filters['category']:
                where_clauses.append("o.product_category = :category")
                params['category'] = filters['category']
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
        GROUP BY 
            s.seller_id, s.seller_name
        ORDER BY 
            total_revenue DESC
        LIMIT :limit
        """
        
        return self.execute_query(query, params=params)
    
    def get_monthly_sales_trend(self, seller_id=None, filters=None):
        """Get the monthly sales trend for a seller or all sellers"""
        query = """
        SELECT 
            s.seller_id,
            s.seller_name,
            TO_CHAR(o.order_date, 'YYYY-MM') AS month,
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS monthly_revenue
        FROM 
            sellers s
        LEFT JOIN 
            orders o ON s.seller_id = o.seller_id
        """
        
        where_clauses = []
        params = {}
        
        if seller_id:
            where_clauses.append("s.seller_id = :seller_id")
            params['seller_id'] = seller_id
        
        if filters:
            if 'location' in filters and filters['location']:
                where_clauses.append("s.seller_location = :location")
                params['location'] = filters['location']
            
            if 'start_date' in filters and filters['start_date']:
                where_clauses.append("o.order_date >= :start_date")
                params['start_date'] = filters['start_date']
            
            if 'end_date' in filters and filters['end_date']:
                where_clauses.append("o.order_date <= :end_date")
                params['end_date'] = filters['end_date']
            
            if 'category' in filters and filters['category']:
                where_clauses.append("o.product_category = :category")
                params['category'] = filters['category']
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
        GROUP BY 
            s.seller_id, s.seller_name, TO_CHAR(o.order_date, 'YYYY-MM')
        ORDER BY 
            s.seller_name, month
        """
        
        return self.execute_query(query, params=params)
    # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    
    def get_order_status_distribution(self, seller_id=None, filters=None):
        """Get the order status distribution for a seller or all sellers"""
        query = """
        SELECT 
            s.seller_id,
            s.seller_name,
            o.order_status,
            COUNT(o.order_id) AS order_count,
            ROUND(COUNT(o.order_id)::NUMERIC / NULLIF(SUM(COUNT(o.order_id)) OVER (PARTITION BY s.seller_id), 0) * 100, 2) AS percentage
        FROM 
            sellers s
        LEFT JOIN 
            orders o ON s.seller_id = o.seller_id
        """
        
        where_clauses = []
        params = {}
        
        if seller_id:
            where_clauses.append("s.seller_id = :seller_id")
            params['seller_id'] = seller_id
        
        if filters:
            if 'location' in filters and filters['location']:
                where_clauses.append("s.seller_location = :location")
                params['location'] = filters['location']
            
            if 'start_date' in filters and filters['start_date']:
                where_clauses.append("o.order_date >= :start_date")
                params['start_date'] = filters['start_date']
            
            if 'end_date' in filters and filters['end_date']:
                where_clauses.append("o.order_date <= :end_date")
                params['end_date'] = filters['end_date']
            
            if 'category' in filters and filters['category']:
                where_clauses.append("o.product_category = :category")
                params['category'] = filters['category']
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
        GROUP BY 
            s.seller_id, s.seller_name, o.order_status
        ORDER BY 
            s.seller_name, o.order_status
        """
        
        return self.execute_query(query, params=params)
    
    def get_ratings_returns_correlation(self, filters=None):
        """Get data to analyze correlation between ratings and returns"""
        query = """
        SELECT 
            s.seller_id,
            s.seller_name,
            COUNT(DISTINCT r.rating_id) AS total_ratings,
            CASE 
                WHEN COUNT(DISTINCT r.rating_id) > 0 THEN ROUND(AVG(r.rating_score), 2)
                ELSE 0 
            END AS average_rating,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT rt.return_id) AS total_returns,
            CASE 
                WHEN COUNT(DISTINCT o.order_id) > 0 THEN 
                    ROUND(COUNT(DISTINCT rt.return_id)::NUMERIC / COUNT(DISTINCT o.order_id) * 100, 2)
                ELSE 0 
            END AS return_rate
        FROM 
            sellers s
        LEFT JOIN 
            orders o ON s.seller_id = o.seller_id
        LEFT JOIN 
            ratings r ON s.seller_id = r.seller_id
        LEFT JOIN 
            returns rt ON s.seller_id = rt.seller_id
        """
        
        where_clauses = []
        params = {}
        
        if filters:
            if 'location' in filters and filters['location']:
                where_clauses.append("s.seller_location = :location")
                params['location'] = filters['location']
            
            if 'start_date' in filters and filters['start_date']:
                where_clauses.append("o.order_date >= :start_date")
                params['start_date'] = filters['start_date']
            
            if 'end_date' in filters and filters['end_date']:
                where_clauses.append("o.order_date <= :end_date")
                params['end_date'] = filters['end_date']
                # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
            
            if 'category' in filters and filters['category']:
                where_clauses.append("o.product_category = :category")
                params['category'] = filters['category']
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
        GROUP BY 
            s.seller_id, s.seller_name
        HAVING 
            COUNT(DISTINCT o.order_id) > 5
        ORDER BY 
            s.seller_name
        """
        
        return self.execute_query(query, params=params)
    
    def get_full_seller_breakdown(self, seller_id, start_date=None, end_date=None):
        """Get a comprehensive breakdown of a seller's performance for drill-down analysis"""
        # Basic seller information
        seller_info = self.get_seller_details(seller_id).iloc[0].to_dict() if not self.get_seller_details(seller_id).empty else {}
        
        params = {'seller_id': seller_id}
        date_filter = ""
        
        if start_date:
            date_filter += " AND o.order_date >= :start_date"
            params['start_date'] = start_date
        
        if end_date:
            date_filter += " AND o.order_date <= :end_date"
            params['end_date'] = end_date
        
        # Overall KPIs
        kpi_query = f"""
        SELECT * FROM seller_kpi_dashboard
        WHERE seller_id = :seller_id
        """
        kpi_data = self.execute_query(kpi_query, params=params)
        
        # Monthly sales trend
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        trend_query = f"""
        SELECT 
            TO_CHAR(o.order_date, 'YYYY-MM') AS month,
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS monthly_revenue
        FROM 
            orders o
        WHERE 
            o.seller_id = :seller_id
            {date_filter}
        GROUP BY 
            TO_CHAR(o.order_date, 'YYYY-MM')
        ORDER BY 
            month
        """
        trend_data = self.execute_query(trend_query, params=params)
        
        # Order status distribution
        status_query = f"""
        SELECT 
            o.order_status,
            COUNT(o.order_id) AS order_count,
            ROUND(COUNT(o.order_id)::NUMERIC / NULLIF(SUM(COUNT(o.order_id)) OVER (), 0) * 100, 2) AS percentage
        FROM 
            orders o
        WHERE 
            o.seller_id = :seller_id
            {date_filter}
        GROUP BY 
            o.order_status
        ORDER BY 
            o.order_status
        """
        status_data = self.execute_query(status_query, params=params)
        
        # Product category distribution
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        category_query = f"""
        SELECT 
            o.product_category,
            COUNT(o.order_id) AS order_count,
            ROUND(COUNT(o.order_id)::NUMERIC / NULLIF(SUM(COUNT(o.order_id)) OVER (), 0) * 100, 2) AS percentage,
            COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS category_revenue
        FROM 
            orders o
        WHERE 
            o.seller_id = :seller_id
            {date_filter}
        GROUP BY 
            o.product_category
        ORDER BY 
            order_count DESC
        """
        category_data = self.execute_query(category_query, params=params)
        
        # Rating distribution
        rating_query = f"""
        SELECT 
            r.rating_score,
            COUNT(r.rating_id) AS rating_count,
            ROUND(COUNT(r.rating_id)::NUMERIC / NULLIF(SUM(COUNT(r.rating_id)) OVER (), 0) * 100, 2) AS percentage
        FROM 
            ratings r
        JOIN
            orders o ON r.order_id = o.order_id
        WHERE 
            r.seller_id = :seller_id
            {date_filter}
        GROUP BY 
            r.rating_score
        ORDER BY 
            r.rating_score
        """
        rating_data = self.execute_query(rating_query, params=params)
        
        # Return reasons
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        return_query = f"""
        SELECT 
            rt.return_reason,
            COUNT(rt.return_id) AS return_count,
            ROUND(COUNT(rt.return_id)::NUMERIC / NULLIF(SUM(COUNT(rt.return_id)) OVER (), 0) * 100, 2) AS percentage
        FROM 
            returns rt
        JOIN
            orders o ON rt.order_id = o.order_id
        WHERE 
            rt.seller_id = :seller_id
            {date_filter}
        GROUP BY 
            rt.return_reason
        ORDER BY 
            return_count DESC
        """
        return_data = self.execute_query(return_query, params=params)
        
        # Combine all data
        result = {
            'seller_info': seller_info,
            'kpi_data': kpi_data.iloc[0].to_dict() if not kpi_data.empty else {},
            'trend_data': trend_data.to_dict('records'),
            'status_data': status_data.to_dict('records'),
            'category_data': category_data.to_dict('records'),
            'rating_data': rating_data.to_dict('records'),
            'return_data': return_data.to_dict('records')
        }
        
        return result
    
    def get_filtered_data_for_export(self, filters=None):
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
        """Get filtered data for export to CSV"""
        query = """
        SELECT 
            s.seller_id,
            s.seller_name,
            s.seller_location,
            s.category_specialization,
            s.join_date,
            o.order_id,
            o.order_date,
            o.shipped_date,
            o.delivered_date,
            o.order_status,
            o.product_category,
            o.order_value,
            r.rating_id,
            r.rating_score,
            r.review_text,
            rt.return_id,
            rt.return_reason,
            rt.return_date
        FROM 
            sellers s
        LEFT JOIN 
            orders o ON s.seller_id = o.seller_id
        LEFT JOIN 
            ratings r ON o.order_id = r.order_id
        LEFT JOIN 
            returns rt ON o.order_id = rt.order_id
        """
        
        where_clauses = []
        params = {}
        
        if filters:
            if 'seller_id' in filters and filters['seller_id']:
                where_clauses.append("s.seller_id = :seller_id")
                params['seller_id'] = filters['seller_id']
            
            if 'location' in filters and filters['location']:
                where_clauses.append("s.seller_location = :location")
                params['location'] = filters['location']
            
            if 'start_date' in filters and filters['start_date']:
                where_clauses.append("o.order_date >= :start_date")
                params['start_date'] = filters['start_date']
            
            if 'end_date' in filters and filters['end_date']:
                where_clauses.append("o.order_date <= :end_date")
                params['end_date'] = filters['end_date']
            
            if 'category' in filters and filters['category']:
                where_clauses.append("o.product_category = :category")
                params['category'] = filters['category']
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        
        query += """
        ORDER BY 
            s.seller_name, o.order_date DESC
        """
        
        return self.execute_query(query, params=params)
        # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
    
    def close(self):
        """Close the database connection"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")


if __name__ == "__main__":
    # Example usage
    db = DatabaseConnector()
    if db.connect():
        # Get the top 5 sellers by revenue
        top_sellers = db.get_top_sellers_by_revenue(limit=5)
        print("Top 5 Sellers by Revenue:")
        print(top_sellers)
        
        # Get the monthly sales trend for the top seller
        if not top_sellers.empty:
            top_seller_id = top_sellers.iloc[0]['seller_id']
            monthly_trend = db.get_monthly_sales_trend(seller_id=top_seller_id)
            print(f"\nMonthly Sales Trend for {top_sellers.iloc[0]['seller_name']}:")
            print(monthly_trend)
        
        db.close()
