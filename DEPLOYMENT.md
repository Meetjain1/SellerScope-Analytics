# Deployment Guide for Seller Performance Analytics Dashboard

## Streamlit Community Cloud Deployment

This guide will help you deploy your Seller Performance Analytics Dashboard to Streamlit Community Cloud for free.

### Prerequisites

1. **GitHub Account**: You need a GitHub account to deploy on Streamlit Community Cloud
2. **Repository Setup**: Your code should be in a public GitHub repository

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Seller Analytics Dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git push -u origin main
   ```

2. **Ensure all files are included**:
   - `streamlit_app.py` (main entry point)
   - `requirements.txt` (dependencies)
   - `dashboard/app.py` (main application)
   - `demo_data.py` (demo data for cloud deployment)
   - `.streamlit/config.toml` (app configuration)

### Step 2: Deploy to Streamlit Community Cloud

1. **Go to Streamlit Community Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create a new app**:
   - Click "New app"
   - Select your GitHub repository
   - Set the branch to `main`
   - Set the main file path to `streamlit_app.py`
   - Give your app a name (e.g., "seller-analytics-dashboard")

3. **Deploy**:
   - Click "Deploy!"
   - Streamlit will build and deploy your app
   - You'll get a public URL once deployment is complete

### Step 3: Configure Database (Optional)

The app will run in demo mode by default with sample data. If you want to connect to a real database:

1. **Set up a cloud database** (recommended providers):
   - **Neon** (PostgreSQL): [neon.tech](https://neon.tech) - Free tier available
   - **Supabase** (PostgreSQL): [supabase.com](https://supabase.com) - Free tier available
   - **AWS RDS** (PostgreSQL): [aws.amazon.com/rds](https://aws.amazon.com/rds)

2. **Configure Streamlit Secrets**:
   - In your Streamlit Community Cloud dashboard, go to your app
   - Click "Settings" → "Secrets"
   - Add your database configuration:
   ```toml
   [database]
   dbname = "your_database_name"
   user = "your_database_user"
   password = "your_database_password"
   host = "your_database_host"
   port = 5432
   ```

3. **Set up your database schema**:
   - Use the SQL files in the `sql/` directory to create tables
   - Import your data or use the data generation scripts

### Step 4: Customize Your Deployment

1. **Custom Domain** (Optional):
   - Streamlit Community Cloud provides a default URL
   - You can use your own domain by configuring DNS settings

2. **App Configuration**:
   - Modify `.streamlit/config.toml` for custom themes and settings
   - Update the app title and icon in `dashboard/app.py`

### Deployment Features

✅ **Demo Mode**: Works out-of-the-box with sample data  
✅ **Database Ready**: Easy database integration via secrets  
✅ **Responsive Design**: Works on desktop and mobile  
✅ **Interactive Visualizations**: Full Plotly functionality  
✅ **Data Export**: CSV download capabilities  
✅ **Filtering**: Date range, location, category, and seller filters  

### Troubleshooting

**Common Issues:**

1. **Import Errors**:
   - Ensure all dependencies are in `requirements.txt`
   - Check that file paths are correct

2. **Database Connection Issues**:
   - Verify secrets configuration
   - Check database host accessibility
   - The app will fall back to demo mode if database fails

3. **Performance Issues**:
   - Streamlit Community Cloud has resource limits
   - Use caching effectively (already implemented)
   - Consider upgrading to Streamlit Cloud Pro for better performance

### Maintenance

- **Updates**: Push changes to GitHub and Streamlit will auto-deploy
- **Monitoring**: Use Streamlit Community Cloud dashboard for logs
- **Scaling**: Consider Streamlit Cloud Pro for production use

### Alternative Deployment Options

If you need more control or resources, consider:

1. **Heroku**: Good for custom configurations
2. **Railway**: Easy deployment with database support
3. **DigitalOcean App Platform**: Simple container deployment
4. **AWS/GCP/Azure**: Full cloud platforms with more resources

### Getting Your Public URL

Once deployed, you'll get a URL like:
`https://your-app-name.streamlit.app`

Share this URL with users to access your dashboard!

### Support

For deployment issues:
- Check Streamlit Community Cloud documentation
- Visit Streamlit Community Forums
- Review the logs in your Streamlit dashboard
