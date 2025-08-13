import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DemoDataProvider:
    """
    Provides demo data for the Seller Performance Dashboard when no database is available.
    This allows the dashboard to work in environments like Streamlit Cloud without database setup.
    """
    
    def __init__(self):
        """Initialize the demo data provider"""
        self.sellers = self._generate_sellers()
        self.orders = self._generate_orders()
        self.ratings = self._generate_ratings()
        self.returns = self._generate_returns()
    
    def _generate_sellers(self, count=50):
        """Generate sample seller data"""
        locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", 
                    "San Antonio", "San Diego", "Dallas", "San Jose"]
        categories = ["Electronics", "Fashion", "Home & Kitchen", "Books", "Toys", "Beauty", 
                     "Sports", "Automotive", "Grocery", "Health"]
        
        seller_ids = list(range(1, count + 1))
        seller_names = [f"Seller {i}" for i in range(1, count + 1)]
        join_dates = [datetime.now() - timedelta(days=np.random.randint(30, 1000)) for _ in range(count)]
        
        sellers = pd.DataFrame({
            'seller_id': seller_ids,
            'seller_name': seller_names,
            'seller_location': np.random.choice(locations, count),
            'category_specialization': np.random.choice(categories, count),
            'join_date': join_dates
        })
        
        return sellers
    
    def _generate_orders(self, min_orders=1000):
        """Generate sample order data"""
        # Use more realistic count of orders
        order_count = max(min_orders, len(self.sellers) * 50)
        
        statuses = ["delivered", "cancelled", "returned"]
        status_probabilities = [0.85, 0.08, 0.07]  # 85% delivered, 8% cancelled, 7% returned
        
        seller_ids = np.random.choice(self.sellers['seller_id'], size=order_count)
        product_categories = []
        
        # Assign product categories based on seller specialization
        for seller_id in seller_ids:
            seller_category = self.sellers[self.sellers['seller_id'] == seller_id]['category_specialization'].values[0]
            # 80% chance the order is from seller's specialized category, 20% from other categories
            if np.random.random() < 0.8:
                product_categories.append(seller_category)
            else:
                other_categories = [cat for cat in self.sellers['category_specialization'].unique() if cat != seller_category]
                product_categories.append(np.random.choice(other_categories))
        
        # Generate order dates with more recent dates having more orders (to show growth trend)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Create a skewed distribution towards more recent dates
        days_ago = np.random.exponential(scale=100, size=order_count).astype(int)
        days_ago = np.clip(days_ago, 0, 365)  # Cap at 365 days
        order_dates = [end_date - timedelta(days=int(days)) for days in days_ago]
        
        # Generate order values with a realistic distribution
        # Log-normal distribution gives a realistic right-skewed distribution for order values
        order_values = np.random.lognormal(mean=3.5, sigma=0.7, size=order_count)
        order_values = np.clip(order_values, 5, 500)  # Cap between $5 and $500
        
        # Generate the orders dataframe
        orders = pd.DataFrame({
            'order_id': range(1, order_count + 1),
            'seller_id': seller_ids,
            'order_date': order_dates,
            'product_category': product_categories,
            'order_value': order_values,
            'order_status': np.random.choice(statuses, size=order_count, p=status_probabilities)
        })
        
        return orders
    
    def _generate_ratings(self):
        """Generate sample rating data"""
        # Not all orders get ratings, approximately 40% do
        delivered_orders = self.orders[self.orders['order_status'] == 'delivered']
        rating_count = int(len(delivered_orders) * 0.4)
        
        # Sample orders that have ratings
        rated_orders = delivered_orders.sample(n=rating_count)
        
        # Generate ratings with a positivity bias (as is common in real rating systems)
        # 1: 2%, 2: 3%, 3: 10%, 4: 30%, 5: 55%
        rating_distribution = [1, 2, 3, 4, 5]
        rating_probabilities = [0.02, 0.03, 0.10, 0.30, 0.55]
        
        ratings = pd.DataFrame({
            'rating_id': range(1, rating_count + 1),
            'order_id': rated_orders['order_id'].values,
            'seller_id': rated_orders['seller_id'].values,
            'rating_score': np.random.choice(rating_distribution, size=rating_count, p=rating_probabilities),
            'rating_date': [order_date + timedelta(days=np.random.randint(1, 14)) for order_date in rated_orders['order_date']]
        })
        
        return ratings
    
    def _generate_returns(self):
        """Generate sample return data"""
        # Get orders marked as returned
        returned_orders = self.orders[self.orders['order_status'] == 'returned']
        
        return_reasons = [
            "Damaged during shipping", 
            "Not as described", 
            "Wrong item received", 
            "Changed mind", 
            "Defective product",
            "Better price elsewhere",
            "Late delivery",
            "Missing parts"
        ]
        
        returns = pd.DataFrame({
            'return_id': range(1, len(returned_orders) + 1),
            'order_id': returned_orders['order_id'].values,
            'seller_id': returned_orders['seller_id'].values,
            'return_date': [order_date + timedelta(days=np.random.randint(2, 10)) for order_date in returned_orders['order_date']],
            'return_reason': np.random.choice(return_reasons, size=len(returned_orders))
        })
        
        return returns
    
    def get_date_range(self):
        """Get the min and max dates from the orders data"""
        min_date = self.orders['order_date'].min()
        max_date = self.orders['order_date'].max()
        return pd.DataFrame([{'min_date': min_date, 'max_date': max_date}])
    
    def get_locations(self):
        """Get all unique seller locations"""
        return pd.DataFrame({'seller_location': self.sellers['seller_location'].unique()})
    
    def get_categories(self):
        """Get all unique product categories"""
        return pd.DataFrame({'product_category': self.orders['product_category'].unique()})
    
    def get_all_sellers(self):
        """Get all seller names and IDs"""
        return self.sellers[['seller_id', 'seller_name']]
    
    def get_seller_kpi_dashboard(self, filters=None):
        """Get KPI data for sellers with optional filters applied"""
        orders_df = self._apply_filters(self.orders, filters)
        
        # Group by seller and calculate KPIs
        kpi_data = orders_df.groupby('seller_id').agg(
            total_orders=('order_id', 'count'),
            total_revenue=('order_value', 'sum')
        ).reset_index()
        
        # Add average order value
        kpi_data['average_order_value'] = kpi_data['total_revenue'] / kpi_data['total_orders']
        
        # Calculate average rating
        ratings_df = self._apply_filters(self.ratings, filters)
        avg_ratings = ratings_df.groupby('seller_id').agg(
            average_rating=('rating_score', 'mean'),
            total_review_count=('rating_id', 'count')
        ).reset_index()
        
        # Merge the data
        kpi_data = pd.merge(kpi_data, avg_ratings, on='seller_id', how='left')
        
        # Calculate return rate
        delivered = orders_df[orders_df['order_status'] == 'delivered'].groupby('seller_id').size()
        returned = orders_df[orders_df['order_status'] == 'returned'].groupby('seller_id').size()
        
        # Create a dataframe with return rates
        return_rates = pd.DataFrame({
            'seller_id': delivered.index,
            'delivered_count': delivered.values,
            'returned_count': returned.reindex(delivered.index).fillna(0).values
        })
        return_rates['return_rate'] = (return_rates['returned_count'] / return_rates['delivered_count']) * 100
        
        # Merge the return data
        kpi_data = pd.merge(kpi_data, return_rates[['seller_id', 'return_rate']], on='seller_id', how='left')
        
        # Add seller names
        kpi_data = pd.merge(kpi_data, self.sellers[['seller_id', 'seller_name', 'seller_location', 'category_specialization']], 
                           on='seller_id', how='left')
        
        # Fill NaN values
        kpi_data = kpi_data.fillna({
            'average_rating': 0,
            'total_review_count': 0,
            'return_rate': 0
        })
        
        return kpi_data
    
    def get_top_sellers_by_revenue(self, limit=10, filters=None):
        """Get top sellers by revenue with optional filters applied"""
        kpi_data = self.get_seller_kpi_dashboard(filters)
        top_sellers = kpi_data.sort_values('total_revenue', ascending=False).head(limit)
        return top_sellers
    
    def get_monthly_sales_trend(self, seller_id=None, filters=None):
        """Get monthly sales trend with optional filters applied"""
        orders_df = self._apply_filters(self.orders, filters)
        
        # Filter by seller_id if provided
        if seller_id:
            orders_df = orders_df[orders_df['seller_id'] == seller_id]
        
        # Add month column
        orders_df['month'] = orders_df['order_date'].dt.strftime('%Y-%m')
        
        # Group by month and calculate metrics
        monthly_trend = orders_df.groupby('month').agg(
            total_orders=('order_id', 'count'),
            monthly_revenue=('order_value', 'sum')
        ).reset_index()
        
        # Sort by month
        monthly_trend = monthly_trend.sort_values('month')
        
        return monthly_trend
    
    def get_order_status_distribution(self, seller_id=None, filters=None):
        """Get order status distribution with optional filters applied"""
        orders_df = self._apply_filters(self.orders, filters)
        
        # Filter by seller_id if provided
        if seller_id:
            orders_df = orders_df[orders_df['seller_id'] == seller_id]
        
        # Group by order status
        status_distribution = orders_df.groupby('order_status').agg(
            order_count=('order_id', 'count')
        ).reset_index()
        
        return status_distribution
    
    def get_ratings_returns_correlation(self, filters=None):
        """Get correlation data between ratings and return rates"""
        kpi_data = self.get_seller_kpi_dashboard(filters)
        
        # Select relevant columns
        correlation_data = kpi_data[['seller_id', 'seller_name', 'average_rating', 'return_rate', 'total_orders', 'total_revenue']]
        
        return correlation_data
    
    def get_full_seller_breakdown(self, seller_id, start_date=None, end_date=None):
        """Get comprehensive breakdown data for a specific seller"""
        filters = {}
        if start_date:
            filters['start_date'] = start_date
        if end_date:
            filters['end_date'] = end_date
        
        # Filter all datasets by seller_id
        seller_info = self.sellers[self.sellers['seller_id'] == seller_id].iloc[0].to_dict()
        kpi_data = self.get_seller_kpi_dashboard(filters)
        kpi_data = kpi_data[kpi_data['seller_id'] == seller_id].iloc[0].to_dict() if len(kpi_data[kpi_data['seller_id'] == seller_id]) > 0 else {}
        
        # Get monthly trend
        trend_data = self.get_monthly_sales_trend(seller_id, filters).to_dict('records')
        
        # Get order status distribution
        status_data = self.get_order_status_distribution(seller_id, filters).to_dict('records')
        
        # Get category breakdown
        orders_df = self._apply_filters(self.orders, filters)
        orders_df = orders_df[orders_df['seller_id'] == seller_id]
        
        category_data = orders_df.groupby('product_category').agg(
            order_count=('order_id', 'count'),
            category_revenue=('order_value', 'sum')
        ).reset_index()
        
        if not category_data.empty:
            total_revenue = category_data['category_revenue'].sum()
            category_data['percentage'] = (category_data['category_revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            category_data = category_data.sort_values('category_revenue', ascending=False).to_dict('records')
        else:
            category_data = []
        
        # Get rating distribution
        ratings_df = self._apply_filters(self.ratings, filters)
        ratings_df = ratings_df[ratings_df['seller_id'] == seller_id]
        
        rating_data = ratings_df.groupby('rating_score').agg(
            rating_count=('rating_id', 'count')
        ).reset_index()
        
        # Ensure all ratings (1-5) are present
        all_ratings = pd.DataFrame({'rating_score': range(1, 6)})
        rating_data = pd.merge(all_ratings, rating_data, on='rating_score', how='left').fillna(0)
        rating_data = rating_data.to_dict('records')
        
        # Get return reasons
        returns_df = self._apply_filters(self.returns, filters)
        returns_df = returns_df[returns_df['seller_id'] == seller_id]
        
        return_data = returns_df.groupby('return_reason').agg(
            return_count=('return_id', 'count')
        ).reset_index()
        
        return_data = return_data.to_dict('records') if not return_data.empty else []
        
        # Calculate additional metrics
        cancelled_orders = orders_df[orders_df['order_status'] == 'cancelled'].shape[0]
        total_orders = orders_df.shape[0]
        cancellation_rate = (cancelled_orders / total_orders * 100) if total_orders > 0 else 0
        
        # Add ontime delivery rate (randomly generated for demo)
        ontime_delivery_rate = np.random.uniform(85, 99)
        
        # Add negative review count
        negative_reviews = ratings_df[ratings_df['rating_score'] <= 2].shape[0]
        
        # Update KPI data with additional metrics
        kpi_data.update({
            'cancellation_rate': cancellation_rate,
            'ontime_delivery_rate': ontime_delivery_rate,
            'negative_review_count': negative_reviews
        })
        
        # Compile all data
        seller_breakdown = {
            'seller_info': seller_info,
            'kpi_data': kpi_data,
            'trend_data': trend_data,
            'status_data': status_data,
            'category_data': category_data,
            'rating_data': rating_data,
            'return_data': return_data
        }
        
        return seller_breakdown
    
    def get_filtered_data_for_export(self, filters=None):
        """Get filtered data for export"""
        orders_df = self._apply_filters(self.orders, filters)
        sellers_df = self.sellers
        
        # Merge data for export
        export_data = pd.merge(
            orders_df,
            sellers_df[['seller_id', 'seller_name', 'seller_location', 'category_specialization']],
            on='seller_id',
            how='left'
        )
        
        return export_data
    
    def _apply_filters(self, df, filters=None):
        """Apply filters to a dataframe"""
        if filters is None:
            return df.copy()
        
        filtered_df = df.copy()
        
        # Apply date filter if present
        if 'start_date' in filters and hasattr(filtered_df, 'order_date'):
            filtered_df = filtered_df[filtered_df['order_date'] >= filters['start_date']]
            
        if 'end_date' in filters and hasattr(filtered_df, 'order_date'):
            filtered_df = filtered_df[filtered_df['order_date'] <= filters['end_date']]
            
        # Apply location filter if present
        if 'seller_location' in filters and filters['seller_location'] != 'All Locations':
            # Get seller IDs from the location
            seller_ids = self.sellers[self.sellers['seller_location'] == filters['seller_location']]['seller_id'].tolist()
            filtered_df = filtered_df[filtered_df['seller_id'].isin(seller_ids)]
            
        # Apply category filter if present
        if 'product_category' in filters and filters['product_category'] != 'All Categories':
            if 'product_category' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['product_category'] == filters['product_category']]
                
        # Apply seller filter if present
        if 'seller_id' in filters and filters['seller_id'] != 'All Sellers':
            filtered_df = filtered_df[filtered_df['seller_id'] == filters['seller_id']]
            
        return filtered_df
