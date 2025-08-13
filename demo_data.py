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
    """Generate demo seller data with Indian context"""
    sellers = [
        {"seller_id": 1, "seller_name": "Mumbai Electronics Hub", "seller_location": "Mumbai", "category_specialization": "Electronics"},
        {"seller_id": 2, "seller_name": "Delhi Fashion Store", "seller_location": "Delhi", "category_specialization": "Clothing"},
        {"seller_id": 3, "seller_name": "Bangalore Home Decor", "seller_location": "Bangalore", "category_specialization": "Home & Garden"},
        {"seller_id": 4, "seller_name": "Chennai Sports Corner", "seller_location": "Chennai", "category_specialization": "Sports & Outdoors"},
        {"seller_id": 5, "seller_name": "Kolkata Book Palace", "seller_location": "Kolkata", "category_specialization": "Books"},
        {"seller_id": 6, "seller_name": "Pune Beauty Bazaar", "seller_location": "Pune", "category_specialization": "Health & Beauty"},
        {"seller_id": 7, "seller_name": "Hyderabad Auto Parts", "seller_location": "Hyderabad", "category_specialization": "Automotive"},
        {"seller_id": 8, "seller_name": "Ahmedabad Pet Store", "seller_location": "Ahmedabad", "category_specialization": "Pet Supplies"},
        {"seller_id": 9, "seller_name": "Jaipur Kitchen World", "seller_location": "Jaipur", "category_specialization": "Kitchen & Dining"},
        {"seller_id": 10, "seller_name": "Lucknow Toy Junction", "seller_location": "Lucknow", "category_specialization": "Toys & Games"},
    ]
    return pd.DataFrame(sellers)

def generate_demo_kpi_data():
    """Generate demo KPI data"""
    sellers = generate_demo_sellers()
    
    kpi_data = []
    for _, seller in sellers.iterrows():
        # Generate realistic metrics based on seller type and Indian market context
        base_orders = random.randint(300, 1500)  # Adjusted for Indian market scale
        base_revenue = base_orders * random.uniform(800, 4500)  # In INR (₹20-120 per order avg)
        
        kpi_data.append({
            "seller_id": seller["seller_id"],
            "seller_name": seller["seller_name"],
            "seller_location": seller["seller_location"],
            "total_orders": base_orders,
            "total_revenue": base_revenue,
            "average_order_value": base_revenue / base_orders,
            "average_rating": round(random.uniform(3.5, 4.8), 2),
            "total_review_count": random.randint(80, 600),
            "return_rate": round(random.uniform(2, 12), 2),  # Slightly lower return rates in India
            "cancellation_rate": round(random.uniform(1, 6), 2),
            "ontime_delivery_rate": round(random.uniform(85, 98), 2),
            "negative_review_count": random.randint(3, 35)
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
            # Add seasonality and randomness - Indian market context
            base_revenue = random.uniform(25000, 150000)  # Monthly revenue in INR
            seasonal_factor = 1.3 if current_date.month in [10, 11, 12] else 1.0  # Diwali/festive season boost
            monthly_revenue = base_revenue * seasonal_factor * random.uniform(0.8, 1.3)
            
            monthly_data.append({
                "seller_id": seller["seller_id"],
                "seller_name": seller["seller_name"],
                "month": month_str,
                "monthly_revenue": monthly_revenue,
                "total_orders": int(monthly_revenue / random.uniform(800, 2500))  # Average order value in INR
            })
        
        # Move to next month
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year + 1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month + 1)
    
    return pd.DataFrame(monthly_data)

def generate_demo_order_status():
    """Generate demo order status distribution for Indian e-commerce"""
    status_data = [
        {"order_status": "delivered", "order_count": 7800},  # Slightly lower delivery rate
        {"order_status": "cancelled", "order_count": 650},   # Higher cancellation in India
        {"order_status": "returned", "order_count": 280},    # Lower return rate
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
            "total_orders": random.randint(250, 1200),
            "total_revenue": random.uniform(50000, 400000)  # Revenue in INR
        })
    
    return pd.DataFrame(correlation_data)

def get_demo_date_range():
    """Generate demo date range"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    return pd.DataFrame([{"min_date": start_date, "max_date": end_date}])

def get_demo_locations():
    """Generate demo locations with Indian cities"""
    locations = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", 
                "Pune", "Hyderabad", "Ahmedabad", "Jaipur", "Lucknow"]
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
    
    # Category data - Indian e-commerce context
    categories = ["Electronics", "Mobile Accessories", "Computer Components"]
    category_data = []
    total_revenue = seller_kpi["total_revenue"]
    
    for i, category in enumerate(categories):
        percentage = random.uniform(25, 45) if i == 0 else random.uniform(15, 35)
        category_revenue = total_revenue * (percentage / 100)
        category_data.append({
            "product_category": category,
            "category_revenue": category_revenue,
            "order_count": int(category_revenue / random.uniform(1200, 2800)),  # INR per order
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
    
    # Return data - Indian e-commerce return reasons
    return_data = [
        {"return_reason": "Product Damaged", "return_count": random.randint(8, 40)},
        {"return_reason": "Wrong Product Delivered", "return_count": random.randint(5, 25)},
        {"return_reason": "Quality Issues", "return_count": random.randint(4, 20)},
        {"return_reason": "Not as Described", "return_count": random.randint(3, 15)},
        {"return_reason": "Size/Fit Issues", "return_count": random.randint(2, 12)},
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
