#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
demo_data.py - Demo data generator for Streamlit Community Cloud deployment

This module provides sample data for the dashboard when a database connection
is not available, allowing the app to run in demo mode on Streamlit Cloud.

Created by: Meet Jain
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducible demo data
np.random.seed(42)
random.seed(42)

def generate_demo_sellers():
    """Generate demo seller data"""
    sellers = [
        {"seller_id": 1, "seller_name": "TechHub Electronics", "seller_location": "New York", "category_specialization": "Electronics"},
        {"seller_id": 2, "seller_name": "Fashion Forward", "seller_location": "California", "category_specialization": "Clothing"},
        {"seller_id": 3, "seller_name": "Home Comfort Store", "seller_location": "Texas", "category_specialization": "Home & Garden"},
        {"seller_id": 4, "seller_name": "Sports Galaxy", "seller_location": "Florida", "category_specialization": "Sports & Outdoors"},
        {"seller_id": 5, "seller_name": "Book Haven", "seller_location": "Washington", "category_specialization": "Books"},
        {"seller_id": 6, "seller_name": "Beauty Boutique", "seller_location": "Illinois", "category_specialization": "Health & Beauty"},
        {"seller_id": 7, "seller_name": "Auto Parts Pro", "seller_location": "Michigan", "category_specialization": "Automotive"},
        {"seller_id": 8, "seller_name": "Pet Paradise", "seller_location": "Colorado", "category_specialization": "Pet Supplies"},
        {"seller_id": 9, "seller_name": "Kitchen Masters", "seller_location": "Oregon", "category_specialization": "Kitchen & Dining"},
        {"seller_id": 10, "seller_name": "Toy Universe", "seller_location": "Nevada", "category_specialization": "Toys & Games"},
    ]
    return pd.DataFrame(sellers)

def generate_demo_kpi_data():
    """Generate demo KPI data"""
    sellers = generate_demo_sellers()
    
    kpi_data = []
    for _, seller in sellers.iterrows():
        # Generate realistic metrics based on seller type
        base_orders = random.randint(500, 2000)
        base_revenue = base_orders * random.uniform(25, 150)
        
        kpi_data.append({
            "seller_id": seller["seller_id"],
            "seller_name": seller["seller_name"],
            "seller_location": seller["seller_location"],
            "total_orders": base_orders,
            "total_revenue": base_revenue,
            "average_order_value": base_revenue / base_orders,
            "average_rating": round(random.uniform(3.5, 4.8), 2),
            "total_review_count": random.randint(100, 800),
            "return_rate": round(random.uniform(2, 15), 2),
            "cancellation_rate": round(random.uniform(1, 8), 2),
            "ontime_delivery_rate": round(random.uniform(85, 98), 2),
            "negative_review_count": random.randint(5, 50)
        })
    
    return pd.DataFrame(kpi_data)

def generate_demo_monthly_trend():
    """Generate demo monthly trend data"""
    sellers = generate_demo_sellers()
    
    # Generate data for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    monthly_data = []
    current_date = start_date
    
    while current_date <= end_date:
        month_str = current_date.strftime("%Y-%m")
        
        for _, seller in sellers.iterrows():
            # Add seasonality and randomness
            base_revenue = random.uniform(10000, 50000)
            seasonal_factor = 1.2 if current_date.month in [11, 12, 1] else 1.0  # Holiday season boost
            monthly_revenue = base_revenue * seasonal_factor * random.uniform(0.8, 1.3)
            
            monthly_data.append({
                "seller_id": seller["seller_id"],
                "seller_name": seller["seller_name"],
                "month": month_str,
                "monthly_revenue": monthly_revenue,
                "total_orders": int(monthly_revenue / random.uniform(30, 80))
            })
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    return pd.DataFrame(monthly_data)

def generate_demo_order_status():
    """Generate demo order status distribution"""
    status_data = [
        {"order_status": "delivered", "order_count": 8500},
        {"order_status": "cancelled", "order_count": 450},
        {"order_status": "returned", "order_count": 350},
    ]
    return pd.DataFrame(status_data)

def generate_demo_ratings_returns():
    """Generate demo ratings vs returns correlation data"""
    sellers = generate_demo_sellers()
    
    correlation_data = []
    for _, seller in sellers.iterrows():
        # Create inverse correlation between ratings and returns
        rating = round(random.uniform(3.2, 4.9), 2)
        # Higher ratings should generally have lower return rates
        return_rate = max(1, round(random.uniform(2, 20) * (5.0 - rating) / 2, 2))
        
        correlation_data.append({
            "seller_name": seller["seller_name"],
            "seller_id": seller["seller_id"],
            "average_rating": rating,
            "return_rate": return_rate,
            "total_orders": random.randint(300, 1500),
            "total_revenue": random.uniform(15000, 120000)
        })
    
    return pd.DataFrame(correlation_data)

def get_demo_date_range():
    """Generate demo date range"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    return pd.DataFrame([{"min_date": start_date, "max_date": end_date}])

def get_demo_locations():
    """Generate demo locations"""
    locations = ["New York", "California", "Texas", "Florida", "Washington", 
                "Illinois", "Michigan", "Colorado", "Oregon", "Nevada"]
    return pd.DataFrame({"seller_location": locations})

def get_demo_categories():
    """Generate demo categories"""
    categories = ["Electronics", "Clothing", "Home & Garden", "Sports & Outdoors", 
                 "Books", "Health & Beauty", "Automotive", "Pet Supplies", 
                 "Kitchen & Dining", "Toys & Games"]
    return pd.DataFrame({"product_category": categories})

def generate_demo_seller_breakdown(seller_id):
    """Generate detailed demo breakdown for a specific seller"""
    sellers = generate_demo_sellers()
    seller_info = sellers[sellers["seller_id"] == seller_id].iloc[0].to_dict()
    
    # Add join date
    seller_info["join_date"] = datetime.now() - timedelta(days=random.randint(180, 1000))
    
    # KPI data
    kpi_data = generate_demo_kpi_data()
    seller_kpi = kpi_data[kpi_data["seller_id"] == seller_id].iloc[0].to_dict()
    
    # Trend data
    trend_data = generate_demo_monthly_trend()
    seller_trend = trend_data[trend_data["seller_id"] == seller_id].to_dict('records')
    
    # Category data
    categories = ["Electronics", "Accessories", "Components"]
    category_data = []
    total_revenue = seller_kpi["total_revenue"]
    
    for i, category in enumerate(categories):
        percentage = random.uniform(20, 40) if i == 0 else random.uniform(10, 30)
        category_revenue = total_revenue * (percentage / 100)
        category_data.append({
            "product_category": category,
            "category_revenue": category_revenue,
            "order_count": int(category_revenue / random.uniform(40, 80)),
            "percentage": percentage
        })
    
    # Status data
    status_data = [
        {"order_status": "delivered", "order_count": int(seller_kpi["total_orders"] * 0.85), "percentage": 85},
        {"order_status": "cancelled", "order_count": int(seller_kpi["total_orders"] * 0.08), "percentage": 8},
        {"order_status": "returned", "order_count": int(seller_kpi["total_orders"] * 0.07), "percentage": 7},
    ]
    
    # Rating data
    rating_data = [
        {"rating_score": 5, "rating_count": int(seller_kpi["total_review_count"] * 0.6)},
        {"rating_score": 4, "rating_count": int(seller_kpi["total_review_count"] * 0.25)},
        {"rating_score": 3, "rating_count": int(seller_kpi["total_review_count"] * 0.1)},
        {"rating_score": 2, "rating_count": int(seller_kpi["total_review_count"] * 0.03)},
        {"rating_score": 1, "rating_count": int(seller_kpi["total_review_count"] * 0.02)},
    ]
    
    # Return data
    return_data = [
        {"return_reason": "Damaged Item", "return_count": random.randint(10, 50)},
        {"return_reason": "Wrong Size", "return_count": random.randint(5, 30)},
        {"return_reason": "Not as Described", "return_count": random.randint(3, 20)},
        {"return_reason": "Changed Mind", "return_count": random.randint(2, 15)},
    ]
    
    return {
        "seller_info": seller_info,
        "kpi_data": seller_kpi,
        "trend_data": seller_trend,
        "category_data": category_data,
        "status_data": status_data,
        "rating_data": rating_data,
        "return_data": return_data
    }
