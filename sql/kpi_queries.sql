-- SQL Queries for KPI Calculations

-- 1. Total Orders per seller
CREATE OR REPLACE VIEW seller_total_orders AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(o.order_id) AS total_orders
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    total_orders DESC;

-- 2. Total Sales Revenue per seller
-- # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.

CREATE OR REPLACE VIEW seller_total_revenue AS
SELECT 
    s.seller_id,
    s.seller_name,
    COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS total_revenue
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    total_revenue DESC;

-- 3. Average Order Value (AOV) per seller
CREATE OR REPLACE VIEW seller_aov AS
SELECT 
    s.seller_id,
    s.seller_name,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN ROUND(SUM(o.order_value) / COUNT(o.order_id), 2)
        ELSE 0 
    END AS average_order_value
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    average_order_value DESC;

-- 4. On-time Delivery Rate (assuming on-time is within 7 days of shipping)
CREATE OR REPLACE VIEW seller_ontime_delivery_rate AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(o.order_id) AS total_delivered,
    COUNT(CASE WHEN o.delivered_date IS NOT NULL AND o.shipped_date IS NOT NULL 
               AND (o.delivered_date - o.shipped_date) <= 7 
               THEN o.order_id END) AS ontime_delivered,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.delivered_date IS NOT NULL AND o.shipped_date IS NOT NULL 
                             AND (o.delivered_date - o.shipped_date) <= 7 
                             THEN o.order_id END)::NUMERIC / COUNT(o.order_id) * 100, 2)
        ELSE 0 
    END AS ontime_delivery_rate
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id AND o.order_status = 'delivered'
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    ontime_delivery_rate DESC;

-- 5. Order Cancellation Rate
CREATE OR REPLACE VIEW seller_cancellation_rate AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(o.order_id) AS total_orders,
    COUNT(CASE WHEN o.order_status = 'cancelled' THEN o.order_id END) AS cancelled_orders,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'cancelled' THEN o.order_id END)::NUMERIC / COUNT(o.order_id) * 100, 2)
        ELSE 0 
    END AS cancellation_rate
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    cancellation_rate ASC;

-- 6. Return Rate
-- # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
CREATE OR REPLACE VIEW seller_return_rate AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(CASE WHEN o.order_status = 'delivered' THEN o.order_id END) AS delivered_orders,
    COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END) AS returned_orders,
    CASE 
        WHEN COUNT(CASE WHEN o.order_status = 'delivered' THEN o.order_id END) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)::NUMERIC / 
                  (COUNT(CASE WHEN o.order_status = 'delivered' THEN o.order_id END) + 
                   COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)) * 100, 2)
        ELSE 0 
    END AS return_rate
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    return_rate ASC;

-- 7. Average Seller Rating
CREATE OR REPLACE VIEW seller_avg_rating AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(r.rating_id) AS total_ratings,
    CASE 
        WHEN COUNT(r.rating_id) > 0 THEN ROUND(AVG(r.rating_score), 2)
        ELSE 0 
    END AS average_rating
FROM 
    sellers s
LEFT JOIN 
    ratings r ON s.seller_id = r.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    average_rating DESC;

-- 8. Negative Review Count (ratings <= 2)
-- # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.

CREATE OR REPLACE VIEW seller_negative_reviews AS
SELECT 
    s.seller_id,
    s.seller_name,
    COUNT(CASE WHEN r.rating_score <= 2 THEN r.rating_id END) AS negative_review_count,
    COUNT(r.rating_id) AS total_review_count,
    CASE 
        WHEN COUNT(r.rating_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN r.rating_score <= 2 THEN r.rating_id END)::NUMERIC / COUNT(r.rating_id) * 100, 2)
        ELSE 0 
    END AS negative_review_percentage
FROM 
    sellers s
LEFT JOIN 
    ratings r ON s.seller_id = r.seller_id
GROUP BY 
    s.seller_id, s.seller_name
ORDER BY 
    negative_review_count DESC;

-- 9. Top Performing Sellers (based on revenue and rating)
CREATE OR REPLACE VIEW top_performing_sellers AS
SELECT 
    s.seller_id,
    s.seller_name,
    s.seller_location,
    s.category_specialization,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS total_revenue,
    CASE 
        WHEN COUNT(r.rating_id) > 0 THEN ROUND(AVG(r.rating_score), 2)
        ELSE 0 
    END AS average_rating,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)::NUMERIC / 
                  NULLIF((COUNT(CASE WHEN o.order_status = 'delivered' THEN o.order_id END) + 
                   COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)), 0) * 100, 2)
        ELSE 0 
    END AS return_rate
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
LEFT JOIN 
    ratings r ON s.seller_id = r.seller_id
GROUP BY 
    s.seller_id, s.seller_name, s.seller_location, s.category_specialization
HAVING 
    COUNT(o.order_id) >= 10 -- Minimum 10 orders to be considered
ORDER BY 
    total_revenue DESC, 
    average_rating DESC,
    return_rate ASC
LIMIT 20;

-- # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
-- 10. Underperforming Sellers (based on high cancellation or return rates)
CREATE OR REPLACE VIEW underperforming_sellers AS
SELECT 
    s.seller_id,
    s.seller_name,
    s.seller_location,
    s.category_specialization,
    COUNT(o.order_id) AS total_orders,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'cancelled' THEN o.order_id END)::NUMERIC / COUNT(o.order_id) * 100, 2)
        ELSE 0 
    END AS cancellation_rate,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)::NUMERIC / 
                  NULLIF((COUNT(CASE WHEN o.order_status = 'delivered' THEN o.order_id END) + 
                   COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)), 0) * 100, 2)
        ELSE 0 
    END AS return_rate,
    CASE 
        WHEN COUNT(r.rating_id) > 0 THEN ROUND(AVG(r.rating_score), 2)
        ELSE 0 
    END AS average_rating,
    COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS total_revenue
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
LEFT JOIN 
    ratings r ON s.seller_id = r.seller_id
GROUP BY 
    s.seller_id, s.seller_name, s.seller_location, s.category_specialization
HAVING 
    COUNT(o.order_id) >= 10 -- Minimum 10 orders to be considered
ORDER BY 
    return_rate DESC, 
    cancellation_rate DESC,
    average_rating ASC
LIMIT 20;

-- # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
-- Monthly sales trend
CREATE OR REPLACE VIEW monthly_sales_trend AS
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
GROUP BY 
    s.seller_id, s.seller_name, TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY 
    s.seller_name, month;

-- Order status distribution
CREATE OR REPLACE VIEW order_status_distribution AS
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
GROUP BY 
    s.seller_id, s.seller_name, o.order_status
ORDER BY 
    s.seller_name, o.order_status;

-- Product category distribution per seller
CREATE OR REPLACE VIEW seller_category_distribution AS
SELECT 
    s.seller_id,
    s.seller_name,
    o.product_category,
    COUNT(o.order_id) AS order_count,
    ROUND(COUNT(o.order_id)::NUMERIC / NULLIF(SUM(COUNT(o.order_id)) OVER (PARTITION BY s.seller_id), 0) * 100, 2) AS percentage,
    COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS category_revenue
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
GROUP BY 
    s.seller_id, s.seller_name, o.product_category
ORDER BY 
    s.seller_name, order_count DESC;

-- Comprehensive KPI dashboard view
-- # © 2025 Meet Jain | Project created by Meet Jain. Unauthorized copying or reproduction is prohibited.
CREATE OR REPLACE VIEW seller_kpi_dashboard AS
SELECT 
    s.seller_id,
    s.seller_name,
    s.seller_location,
    s.category_specialization,
    s.join_date,
    (CURRENT_DATE - s.join_date) AS days_since_joining,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(CASE WHEN o.order_status != 'cancelled' AND o.order_status != 'returned' THEN o.order_value ELSE 0 END), 0) AS total_revenue,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN ROUND(SUM(o.order_value) / COUNT(o.order_id), 2)
        ELSE 0 
    END AS average_order_value,
    CASE 
        WHEN COUNT(CASE WHEN o.order_status = 'delivered' OR o.order_status = 'returned' THEN o.order_id END) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.delivered_date IS NOT NULL AND o.shipped_date IS NOT NULL 
                             AND (o.delivered_date - o.shipped_date) <= 7 
                             THEN o.order_id END)::NUMERIC / 
                  COUNT(CASE WHEN o.order_status = 'delivered' OR o.order_status = 'returned' THEN o.order_id END) * 100, 2)
        ELSE 0 
    END AS ontime_delivery_rate,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'cancelled' THEN o.order_id END)::NUMERIC / COUNT(o.order_id) * 100, 2)
        ELSE 0 
    END AS cancellation_rate,
    CASE 
        WHEN COUNT(o.order_id) > 0 THEN 
            ROUND(COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)::NUMERIC / 
                  NULLIF((COUNT(CASE WHEN o.order_status = 'delivered' THEN o.order_id END) + 
                   COUNT(CASE WHEN o.order_status = 'returned' THEN o.order_id END)), 0) * 100, 2)
        ELSE 0 
    END AS return_rate,
    CASE 
        WHEN COUNT(r.rating_id) > 0 THEN ROUND(AVG(r.rating_score), 2)
        ELSE 0 
    END AS average_rating,
    COUNT(CASE WHEN r.rating_score <= 2 THEN r.rating_id END) AS negative_review_count,
    COUNT(r.rating_id) AS total_review_count
FROM 
    sellers s
LEFT JOIN 
    orders o ON s.seller_id = o.seller_id
LEFT JOIN 
    ratings r ON s.seller_id = r.seller_id
GROUP BY 
    s.seller_id, s.seller_name, s.seller_location, s.category_specialization, s.join_date
ORDER BY 
    total_revenue DESC;
