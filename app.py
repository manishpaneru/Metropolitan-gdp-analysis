import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.stoggle import stoggle 
from streamlit_extras.colored_header import colored_header
from streamlit_extras.metric_cards import style_metric_cards
import pycountry
import altair as alt
import time
import os
from plotly.subplots import make_subplots
import math
import scipy.stats as stats

# Page configuration
st.set_page_config(
    page_title="Urban Economic Efficiency Dashboard",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom components
def colored_header(label, description=None, color_name=None):
    """Return a header with a colored background."""
    if description:
        st.markdown(f'<h2 class="header-with-bg {color_name}">{label}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p class="header-description">{description}</p>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h2 class="header-with-bg {color_name}">{label}</h2>', unsafe_allow_html=True)

# Custom CSS
st.markdown("""
<style>
    /* Power BI inspired corporate theme */
    :root {
        --primary-color: #0078D4;
        --secondary-color: #0050B3;
        --accent-color: #107C10;
        --text-color: #252525;
        --light-bg: #F6F8FA;
        --card-border: #E0E0E0;
        --card-bg: #FFFFFF;
        --header-bg: #0078D4;
        --header-text: #FFFFFF;
        --subtitle-color: #605E5C;
        --filter-bg: #EFF6FC;
        --hover-bg: #F3F2F1;
    }
    
    /* General styles */
    .stApp {
        background-color: var(--light-bg);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-color);
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    p {
        color: var(--text-color);
        line-height: 1.6;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Navigation bar */
    .navbar {
        background-color: var(--primary-color);
        padding: 0.75rem;
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .nav-title {
        color: white;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 0;
        flex-grow: 0;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .nav-buttons {
        display: flex;
        gap: 5px;
        flex-grow: 1;
        justify-content: center;
    }
    
    .nav-button {
        background-color: rgba(255,255,255,0.1);
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 2px;
        cursor: pointer;
        transition: background-color 0.2s;
        font-size: 0.85rem;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .nav-button:hover {
        background-color: rgba(255,255,255,0.2);
    }
    
    /* Header styles */
    .header-with-bg {
        background-color: var(--primary-color);
        color: var(--header-text) !important;
        padding: 0.75rem 1rem;
        border-radius: 3px;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    .header-description {
        font-size: 1rem;
        color: var(--subtitle-color);
        margin-bottom: 1rem;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .blue-green-70 {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
    }
    
    /* Cards and insight boxes */
    .insight-box {
        background-color: var(--card-bg);
        border-radius: 3px;
        padding: 1.25rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%;
        border-top: 3px solid var(--primary-color);
    }
    
    .insight-box h3 {
        color: var(--primary-color);
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    .insight-box h4 {
        color: var(--text-color);
        margin-top: 0.75rem;
        margin-bottom: 0.5rem;
        font-size: 1rem;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }
    
    .insight-box ul {
        padding-left: 1.25rem;
    }
    
    .insight-box li {
        margin-bottom: 0.4rem;
        color: var(--text-color);
    }
    
    .highlight {
        background-color: #E7F3E8;
        padding: 0 0.3rem;
        border-radius: 2px;
        font-weight: 500;
        color: var(--accent-color);
    }
    
    /* Metric cards */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background-color: var(--card-bg);
        border-radius: 3px;
        padding: 1.25rem;
        flex: 1;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 3px solid var(--primary-color);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: var(--subtitle-color);
        font-size: 0.9rem;
        margin: 0;
        font-weight: 400;
    }
    
    /* Section dividers */
    .section-divider {
        height: 1px;
        background: var(--card-border);
        margin: 2rem 0;
    }
    
    /* Animations */
    .fadeIn {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Footer */
    .footer {
        background-color: var(--primary-color);
        color: rgba(255,255,255,0.8);
        padding: 1.25rem;
        text-align: center;
        margin-top: 2rem;
        border-radius: 3px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .footer p {
        margin: 0.3rem 0;
        color: rgba(255,255,255,0.8);
        font-size: 0.85rem;
    }
    
    .author-info {
        margin-top: 12px;
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.2);
    }
    
    .social-links a {
        color: rgba(255,255,255,0.9);
        text-decoration: none;
        margin: 0 5px;
        transition: color 0.2s;
    }
    
    .social-links a:hover {
        color: white;
        text-decoration: underline;
    }
    
    /* Streamlit element customization */
    div.stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--light-bg);
        padding: 0.25rem;
        border-radius: 3px;
        margin-bottom: 0.5rem;
    }
    
    div.stTabs [data-baseweb="tab"] {
        border-radius: 2px;
        padding: 0.35rem 0.75rem;
        font-size: 0.85rem;
    }
    
    div.stTabs [aria-selected="true"] {
        background-color: var(--primary-color) !important;
        color: white !important;
        font-weight: 400;
    }
    
    .stButton button {
        background-color: var(--primary-color);
        color: white;
        border: none;
        padding: 0.35rem 0.75rem;
        border-radius: 2px;
        font-weight: 400;
        font-size: 0.85rem;
    }
    
    /* Title styling */
    .dashboard-header {
        display: flex;
        align-items: center;
        background-color: var(--primary-color);
        border-radius: 3px;
        padding: 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        animation: fadeIn 0.5s ease-out;
    }
    
    .title-container {
        flex-grow: 1;
    }
    
    .main-title {
        color: white;
        font-size: 1.8rem;
        margin: 0;
        padding: 0;
        line-height: 1.2;
        font-weight: 600;
        font-family: 'Segoe UI', sans-serif;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1rem;
        margin-top: 0.5rem;
        line-height: 1.5;
        font-weight: 400;
        max-width: 800px;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Main content area */
    .main-content {
        padding: 0.75rem;
        background-color: var(--light-bg);
    }
    
    /* Custom styling for Streamlit metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
        color: var(--primary-color) !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: var(--subtitle-color) !important;
        font-size: 0.9rem !important;
        font-weight: 400 !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    div[data-testid="stMetricDelta"] {
        color: var(--accent-color) !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    div[data-testid="stExpander"] {
        border-radius: 3px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid var(--card-border);
    }
    
    div[data-testid="stExpanderContent"] {
        background-color: var(--card-bg);
    }
    
    /* Filter panel styling */
    .filter-panel {
        background-color: var(--filter-bg);
        padding: 1rem;
        border-radius: 3px;
        margin-bottom: 1rem;
        border: 1px solid var(--card-border);
    }
    
    /* Chart container styling */
    .chart-container {
        background-color: var(--card-bg);
        border-radius: 3px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid var(--card-border);
    }
    
    /* About section styling */
    .about-section {
        background-color: var(--card-bg);
        border-radius: 3px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 3px solid var(--primary-color);
    }
    
    /* Outlier container styling */
    .outlier-container {
        display: flex;
        align-items: stretch;
        margin-bottom: 1.5rem;
    }
    
    .outlier-container > div {
        display: flex;
        flex-direction: column;
    }
    
    .outlier-container .stTabs {
        height: 100%;
    }
    
    .outlier-container .stTab > div:first-child {
        height: 100%;
    }
    
    /* Navigation styling */
    .navbar {
        background-color: #FFFFFF;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: sticky;
        top: 0;
        z-index: 999;
        padding: 0.5rem 1rem;
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        border-bottom: 2px solid #F0F0F0;
    }
    
    .nav-button {
        background-color: transparent;
        color: #252525;
        border: none;
        padding: 0.5rem 1rem;
        margin: 0 0.3rem;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .nav-button:hover {
        background-color: #F0F2F5;
        color: #0078D4;
    }
    
    .nav-button.active {
        color: #0078D4;
        border-bottom: 2px solid #0078D4;
        background-color: rgba(0, 120, 212, 0.1);
    }
    
    /* Page title */
    .title-container {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1rem;
    }
    
    .dashboard-title {
        color: #252525;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        color: #605E5C;
        font-size: 1rem;
        font-weight: 400;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Metrics row styling */
    .metric-container {
        background-color: white;
        border-radius: 4px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        margin-bottom: 1rem;
    }
    
    /* Section styling */
    .section-header {
        display: flex;
        align-items: center;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #E1DFDD;
    }
    
    .section-header h2 {
        color: #252525;
        font-size: 1.4rem;
        font-weight: 600;
        margin: 0;
    }
    
    .section-description {
        color: #605E5C;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        max-width: 900px;
    }
    
    .section-divider {
        height: 2px;
        background: linear-gradient(to right, rgba(0,0,0,0), #E1DFDD, rgba(0,0,0,0));
        margin: 2rem 0;
    }
    
    /* Chart container styling */
    .chart-container {
        background-color: white;
        border-radius: 4px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-top: 3px solid #0078D4;
    }
    
    /* Insight box styling */
    .insight-box {
        background-color: white;
        border-radius: 4px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        height: 100%;
        border-left: 3px solid #0078D4;
    }
    
    /* Filter panel styling */
    .filter-panel {
        background-color: white;
        border-radius: 4px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border-left: 3px solid #0078D4;
    }
    
    /* About section styling */
    .about-section {
        background-color: white;
        border-radius: 4px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }
    
    /* Streamlit element overrides */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 2.5rem;
        white-space: pre-wrap;
        background-color: #F0F2F5;
        border-radius: 4px 4px 0 0;
        padding: 0 1rem;
        font-size: 0.9rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        font-weight: 600;
        color: #0078D4 !important;
        border-top: 2px solid #0078D4 !important;
    }
    
    /* Fix the tab height issue */
    .stTabs > div[data-baseweb="tab-panel"] {
        height: 100%;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    div[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
        margin: 0;
        padding: 0;
    }
    
    /* Make metrics stand out */
    div[data-testid="stMetric"] {
        background-color: white;
        padding: 1rem;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stMetric"] > div {
        padding: 0;
    }
    
    div[data-testid="stMetric"] label {
        color: #605E5C;
        font-size: 0.85rem;
    }
    
    div[data-testid="stMetricValue"] {
        color: #0078D4 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1rem;
        color: #252525;
        background-color: white;
        border-radius: 4px;
        border: none !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    .streamlit-expanderContent {
        background-color: white;
        border-radius: 0 0 4px 4px;
        border: none !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        # Check if file exists first using relative path
        import os
        current_dir = os.getcwd()
        dataset_path = os.path.join(current_dir, "dataset.csv")
        
        if not os.path.exists(dataset_path):
            st.error(f"Dataset file not found at: {dataset_path}")
            st.error(f"Current working directory: {current_dir}")
            available_files = os.listdir(current_dir)
            st.error(f"Available files in current directory: {available_files}")
            
            # Try absolute path as fallback
            absolute_path = r"D:\visualization project\Global GDP\dataset.csv"
            if os.path.exists(absolute_path):
                st.info(f"Found dataset at absolute path: {absolute_path}")
                df = pd.read_csv(absolute_path)
            else:
                st.error(f"Dataset also not found at absolute path: {absolute_path}")
                return None
        else:
            # Try to load the file using relative path
            df = pd.read_csv(dataset_path)
        
        # Display success message
        st.success("Dataset loaded successfully!")
        
        # Clean population column - remove spaces, commas and convert to numeric
        df['Metropolitian Population'] = df['Metropolitian Population'].str.replace(',', '').str.strip()
        df['Metropolitian Population'] = pd.to_numeric(df['Metropolitian Population'], errors='coerce')
        
        # Ensure GDP column is numeric
        df['Official est. GDP(billion US$)'] = pd.to_numeric(df['Official est. GDP(billion US$)'], errors='coerce')
        
        # Calculate GDP per capita more efficiently
        df['GDP_per_capita'] = df['Official est. GDP(billion US$)'] * 1000 / (df['Metropolitian Population'] / 1_000_000)
        df['GDP_per_capita'] = df['GDP_per_capita'].round(2)
        
        # Add region information based on country
        df['Region'] = df['Country/Region'].map(get_region)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.error(f"Traceback: {traceback.format_exc()}")
        return None

def get_region(country_name):
    regions = {
        'United States': 'North America',
        'Canada': 'North America',
        'Mexico': 'North America',
        'China': 'East Asia',
        'Japan': 'East Asia',
        'South Korea': 'East Asia',
        'Taiwan': 'East Asia',
        'India': 'South Asia',
        'Pakistan': 'South Asia',
        'Bangladesh': 'South Asia',
        'United Kingdom': 'Europe',
        'Germany': 'Europe',
        'France': 'Europe',
        'Italy': 'Europe',
        'Spain': 'Europe',
        'Russia': 'Europe',
        'Brazil': 'South America',
        'Argentina': 'South America',
        'Colombia': 'South America',
        'Australia': 'Oceania',
        'New Zealand': 'Oceania',
        'South Africa': 'Africa',
        'Nigeria': 'Africa',
        'Egypt': 'Africa',
        'Saudi Arabia': 'Middle East',
        'United Arab Emirates': 'Middle East',
        'Israel': 'Middle East',
        'Singapore': 'Southeast Asia',
        'Malaysia': 'Southeast Asia',
        'Indonesia': 'Southeast Asia',
        'Thailand': 'Southeast Asia',
        'Vietnam': 'Southeast Asia',
        'Philippines': 'Southeast Asia'
    }
    
    # Return the region if found, otherwise return 'Other'
    return regions.get(country_name, 'Other')

# Load the data
df = load_data()
if df is not None:
    data_loaded = True
else:
    data_loaded = False
    st.error("Could not load the dataset. Please check that dataset.csv exists in the current directory.")
    
    # Provide a way for users to upload the dataset manually
    uploaded_file = st.file_uploader("Upload dataset.csv file", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Clean population column - remove spaces, commas and convert to numeric
            df['Metropolitian Population'] = df['Metropolitian Population'].str.replace(',', '').str.strip()
            df['Metropolitian Population'] = pd.to_numeric(df['Metropolitian Population'], errors='coerce')
            
            # Ensure GDP column is numeric
            df['Official est. GDP(billion US$)'] = pd.to_numeric(df['Official est. GDP(billion US$)'], errors='coerce')
            
            # Calculate GDP per capita more efficiently
            df['GDP_per_capita'] = df['Official est. GDP(billion US$)'] * 1000 / (df['Metropolitian Population'] / 1_000_000)
            df['GDP_per_capita'] = df['GDP_per_capita'].round(2)
            
            # Add region information based on country
            df['Region'] = df['Country/Region'].map(get_region)
            
            data_loaded = True
            st.success("Dataset uploaded successfully!")
        except Exception as e:
            st.error(f"Error processing uploaded file: {str(e)}")
            data_loaded = False

if data_loaded:
    # Navigation bar (sticky)
    with st.container():
        st.markdown('<div class="navbar">', unsafe_allow_html=True)
        cols = st.columns([1,1,1,1,1,1])
        with cols[0]:
            st.button("📊 Dashboard", key="nav_overview")
        with cols[1]:
            st.button("🌎 Global Map", key="nav_map")
        with cols[2]:
            st.button("🏆 Top Metros", key="nav_top")
        with cols[3]:
            st.button("📈 Efficiency", key="nav_size")
        with cols[4]:
            st.button("🌐 Regions", key="nav_regions")
        with cols[5]:
            st.button("⭐ Outliers", key="nav_outliers")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Business question as title with enhanced styling
    st.markdown("""
    <div class="dashboard-header">
        <div class="title-container">
            <h1 class="main-title">Metropolitan Economic Efficiency</h1>
            <p class="subtitle">How does economic productivity (GDP per capita) vary across global metropolitan areas, and what factors contribute to the most efficient urban economies?</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction section
    st.markdown('<div class="fadeIn">', unsafe_allow_html=True)
    
    # Key metrics in a more dashboard-like format
    total_metros = len(df)
    total_population = df['Metropolitian Population'].sum()
    total_gdp = df['Official est. GDP(billion US$)'].sum()
    avg_gdp_per_capita = df['GDP_per_capita'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Metropolitan Areas", f"{total_metros:,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total Population", f"{total_population/1_000_000:.1f}M")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Total GDP (USD)", f"${total_gdp:.1f}T")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Avg GDP per Capita", f"${avg_gdp_per_capita:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    style_metric_cards()
    
    # Introduction text
    st.markdown("""
    This dashboard explores economic productivity across global metropolitan areas, analyzing how 
    GDP per capita varies by region, city size, and other factors. Discover patterns that explain 
    why some urban economies are more efficient than others and what drives exceptional performance.
    """)
    
    # About the Author and Project
    with st.expander("📌 About this Dashboard"):
        st.markdown('<div class="about-section">', unsafe_allow_html=True)
        about_col1, about_col2 = st.columns([1, 3])
        
        with about_col1:
            st.markdown("""
            <div style="text-align: center; display: flex; flex-direction: column; justify-content: center; height: 100%; padding: 20px 0;">
                <h3 style="margin-bottom: 5px; color: #0078D4; font-family: 'Segoe UI', sans-serif;">Manish Paneru</h3>
                <p style="margin-top: 0; color: #605E5C; font-family: 'Segoe UI', sans-serif;">Data Analyst</p>
                <div style="margin-top: 10px;">
                    <a href="https://linkedin.com/in/manish.paneru1" target="_blank" style="color: #0078D4; text-decoration: none; font-family: 'Segoe UI', sans-serif;">LinkedIn</a> | 
                    <a href="https://github.com/manishpaneru" target="_blank" style="color: #0078D4; text-decoration: none; font-family: 'Segoe UI', sans-serif;">GitHub</a> | 
                    <a href="https://www.analystpaneru.xyz" target="_blank" style="color: #0078D4; text-decoration: none; font-family: 'Segoe UI', sans-serif;">Portfolio</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with about_col2:
            st.markdown("""
            <div style="font-family: 'Segoe UI', sans-serif;">
            <h3 style="color: #0078D4; font-size: 1.2rem; margin-bottom: 0.75rem;">About this Project</h3>
            
            <p style="color: #252525; font-size: 0.95rem; line-height: 1.5;">
            This urban economic efficiency dashboard analyzes metropolitan GDP data from various global cities 
            to identify patterns in economic productivity. The visualizations help answer critical questions:
            </p>
            
            <ul style="color: #252525; font-size: 0.95rem; line-height: 1.5; padding-left: 1.5rem;">
                <li>What makes some metropolitan areas more economically efficient than others?</li>
                <li>How do factors like size, region, and economic specialization contribute to productivity?</li>
                <li>Which cities represent outliers in economic performance, and what can we learn from them?</li>
            </ul>
            
            <h4 style="color: #0078D4; font-size: 1.1rem; margin-top: 1rem; margin-bottom: 0.5rem;">Methodology</h4>
            
            <p style="color: #252525; font-size: 0.95rem; line-height: 1.5;">The analysis combines several key metrics:</p>
            <ul style="color: #252525; font-size: 0.95rem; line-height: 1.5; padding-left: 1.5rem;">
                <li><strong>GDP per capita</strong> as the primary measure of economic efficiency</li>
                <li><strong>Metropolitan population</strong> to understand the relationship between size and productivity</li>
                <li><strong>Total GDP</strong> to measure absolute economic output</li>
                <li><strong>Regional context</strong> to identify geographic patterns</li>
            </ul>
            
            <h4 style="color: #0078D4; font-size: 1.1rem; margin-top: 1rem; margin-bottom: 0.5rem;">Data Sources</h4>
            
            <p style="color: #252525; font-size: 0.95rem; line-height: 1.5;">
            This dashboard uses curated economic data from multiple sources including international 
            economic organizations, government statistical offices, and economic research institutions.
            </p>
            
            <p style="color: #252525; font-size: 0.95rem; line-height: 1.5;">
            <strong>Dataset source:</strong> <a href="https://www.kaggle.com/datasets/khushikhushikhushi/global-cities-by-gdp" target="_blank" style="color: #0078D4; text-decoration: none;">Global Cities by GDP on Kaggle</a>
            </p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Add filter controls in a Power BI style panel
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    filter_cols = st.columns([1, 1, 1, 1])
    
    with filter_cols[0]:
        st.markdown('<p style="font-size: 0.85rem; font-family: \'Segoe UI\', sans-serif; font-weight: 600; margin-bottom: 0.3rem; color: #252525;">Region Filter</p>', unsafe_allow_html=True)
        all_regions = sorted(df['Region'].unique().tolist())
        selected_regions = st.multiselect("", all_regions, default=all_regions, key="region_filter", label_visibility="collapsed")
    
    with filter_cols[1]:
        st.markdown('<p style="font-size: 0.85rem; font-family: \'Segoe UI\', sans-serif; font-weight: 600; margin-bottom: 0.3rem; color: #252525;">GDP Range (billions)</p>', unsafe_allow_html=True)
        min_gdp, max_gdp = st.slider("", 0.0, float(df['Official est. GDP(billion US$)'].max()), (0.0, float(df['Official est. GDP(billion US$)'].max())), key="gdp_filter", label_visibility="collapsed")
    
    with filter_cols[2]:
        st.markdown('<p style="font-size: 0.85rem; font-family: \'Segoe UI\', sans-serif; font-weight: 600; margin-bottom: 0.3rem; color: #252525;">Population Size</p>', unsafe_allow_html=True)
        pop_options = ["All", "Small (<1M)", "Medium (1-5M)", "Large (5-10M)", "Mega (>10M)"]
        selected_pop = st.selectbox("", pop_options, key="pop_filter", label_visibility="collapsed")
    
    with filter_cols[3]:
        st.markdown('<p style="font-size: 0.85rem; font-family: \'Segoe UI\', sans-serif; font-weight: 600; margin-bottom: 0.3rem; color: #252525;">Sort By</p>', unsafe_allow_html=True)
        sort_options = ["GDP per Capita (High to Low)", "Total GDP (High to Low)", "Population (High to Low)"]
        selected_sort = st.selectbox("", sort_options, key="sort_filter", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a section divider
    st.markdown('<div class="section-divider"></div><div id="global-map"></div>', unsafe_allow_html=True)
    
    # Global Overview Section with World Map (Images | Text pattern)
    st.markdown('<div class="fadeIn">', unsafe_allow_html=True)
    colored_header(
        label="Global Economic Productivity Map",
        description="Metropolitan areas sized by total GDP and colored by GDP per capita",
        color_name="blue-green-70"
    )
    
    # Create world map visualization using Plotly
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Multiple visualizations in tabs
        map_tabs = st.tabs(["World Map", "3D Globe", "Bubble Chart"])
        
        with map_tabs[0]:
            # Create a copy of the dataframe and handle NaN values
            map_df = df.copy()
            # Fill NaN values in GDP with a small value for visualization purposes
            map_df['Official est. GDP(billion US$)'] = map_df['Official est. GDP(billion US$)'].fillna(1)
            # Also handle NaN values in GDP per capita
            map_df['GDP_per_capita'] = map_df['GDP_per_capita'].fillna(0)
            
            # Create the map visualization
            fig = px.scatter_geo(
                map_df,
                locations="Country/Region",
                locationmode="country names",
                color="GDP_per_capita",
                size="Official est. GDP(billion US$)",
                hover_name="Metropolitian Area/City",
                size_max=50,
                color_continuous_scale="Viridis",
                title="Metropolitan Areas by GDP and GDP per Capita",
                hover_data={
                    "Country/Region": True,
                    "Official est. GDP(billion US$)": ":.1f",
                    "Metropolitian Population": ":,.0f",
                    "GDP_per_capita": ":$,.0f"
                }
            )
            fig.update_layout(
                height=600, 
                margin=dict(l=0, r=0, t=30, b=0),
                geo=dict(
                    showland=True,
                    landcolor="rgb(217, 217, 217)",
                    coastlinecolor="white",
                    countrycolor="rgb(200, 200, 200)",
                    showocean=True,
                    oceancolor="rgb(237, 250, 255)"
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with map_tabs[1]:
            # 3D Globe visualization
            fig = px.scatter_geo(
                map_df,
                locations="Country/Region",
                locationmode="country names",
                color="GDP_per_capita",
                size="Official est. GDP(billion US$)",
                hover_name="Metropolitian Area/City",
                size_max=50,
                color_continuous_scale="Plasma",
                title="3D Globe View of Metropolitan Economies",
                hover_data={
                    "Country/Region": True,
                    "Official est. GDP(billion US$)": ":.1f",
                    "Metropolitian Population": ":,.0f",
                    "GDP_per_capita": ":$,.0f"
                },
                projection="orthographic"
            )
            fig.update_layout(
                height=600,
                margin=dict(l=0, r=0, t=30, b=0),
                geo=dict(
                    showland=True,
                    landcolor="rgb(217, 217, 217)",
                    countrycolor="rgb(200, 200, 200)",
                    showcountries=True,
                    showocean=True,
                    oceancolor="rgb(220, 240, 255)"
                )
            )
            # Add animation for rotation
            frames = []
            for i in range(0, 361, 10):
                frames.append(go.Frame(
                    layout=dict(
                        geo=dict(
                            projection_rotation_lon=i
                        )
                    )
                ))
            fig.frames = frames
            
            # Add animation buttons
            animation_buttons = [
                dict(
                    args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True}],
                    label="Play",
                    method="animate"
                ),
                dict(
                    args=[[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    label="Pause",
                    method="animate"
                )
            ]
            fig.update_layout(
                updatemenus=[dict(
                    type="buttons",
                    showactive=False,
                    buttons=animation_buttons,
                    x=0.1,
                    y=0,
                    xanchor="right",
                    yanchor="top"
                )]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with map_tabs[2]:
            # Create a bubble chart of population vs GDP with regions
            fig = px.scatter(
                map_df,
                x="Metropolitian Population",
                y="Official est. GDP(billion US$)",
                size="GDP_per_capita",
                color="Region",
                hover_name="Metropolitian Area/City",
                log_x=True,
                log_y=True,
                size_max=60,
                color_discrete_sequence=px.colors.qualitative.Bold,
                title="Metropolitan Population vs GDP (bubble size = GDP per capita)",
                hover_data={
                    "Country/Region": True,
                    "GDP_per_capita": ":$,.0f"
                }
            )
            fig.update_layout(
                height=600,
                xaxis_title="Metropolitan Population (log scale)",
                yaxis_title="GDP in billions USD (log scale)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h3>Global Economic Patterns</h3>
        <p>The visualizations reveal several striking patterns in urban economic efficiency worldwide:</p>
        <ul>
            <li>Highly developed metropolitan areas in <span class="highlight">North America</span>, <span class="highlight">Western Europe</span>, and <span class="highlight">East Asia</span> dominate in GDP per capita</li>
            <li>Many large Asian cities show impressive total GDP but moderate per-capita figures</li>
            <li>Emerging market metros often display lower economic efficiency despite large populations</li>
        </ul>
        <p>The most efficient cities frequently benefit from specialized economic activities:</p>
        <ul>
            <li>Financial services hubs</li>
            <li>Technology centers</li>
            <li>Advanced manufacturing clusters</li>
            <li>Trade and logistics nexuses</li>
        </ul>
        <p>Explore the 3D globe and bubble chart views for additional perspectives on how economic productivity varies across regions.</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Top Performers Analysis (Text | Images pattern)
    st.markdown('<div class="fadeIn">', unsafe_allow_html=True)
    colored_header(
        label="Top Economic Performers",
        description="Metropolitan areas with the highest GDP per capita",
        color_name="blue-green-70"
    )
    
    # Get top 15 metros by GDP per capita, handling NaN values
    top_gdp_per_capita = df.dropna(subset=['GDP_per_capita']).nlargest(15, 'GDP_per_capita')
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h3>Efficiency Leaders</h3>
        <p>The top performing metros share several key characteristics:</p>
        <ul>
            <li><span class="highlight">Financial centers</span> with global importance</li>
            <li>Cities with <span class="highlight">specialized economies</span> in high-value sectors</li>
            <li>Areas with <span class="highlight">strong governance</span> and infrastructure</li>
            <li>Metropolitan regions with <span class="highlight">optimal scaling</span> of resources</li>
        </ul>
        <p>Many of these cities have achieved efficiency through specialization rather than sheer size, highlighting the importance of economic focus over raw growth.</p>
        
        <h4>Success Factors:</h4>
        <ul>
            <li>Strategic economic positioning</li>
            <li>Skilled workforce development</li>
            <li>Innovation ecosystems</li>
            <li>Quality infrastructure</li>
            <li>Business-friendly environments</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create tabs for different visualizations
        top_tabs = st.tabs(["Bar Chart", "Radar Chart", "Treemap"])
        
        with top_tabs[0]:
            # Enhanced bar chart
            fig = px.bar(
                top_gdp_per_capita,
                x='GDP_per_capita',
                y='Metropolitian Area/City',
                color='Region',
                orientation='h',
                color_discrete_sequence=px.colors.qualitative.Bold,
                title="Top 15 Metropolitan Areas by GDP per Capita",
                hover_data={
                    "Country/Region": True,
                    "Official est. GDP(billion US$)": ":.1f",
                    "Metropolitian Population": ":,.0f",
                    "GDP_per_capita": ":$,.0f"
                },
                text='GDP_per_capita'
            )
            fig.update_layout(
                height=600, 
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="GDP per Capita (USD)",
                yaxis_title="",
                bargap=0.2
            )
            fig.update_traces(
                texttemplate='$%{text:,.0f}', 
                textposition='outside'
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with top_tabs[1]:
            # Radar chart comparing top 5 cities
            top_5 = top_gdp_per_capita.head(5)
            
            # Normalize metrics for radar chart
            metrics = ['GDP_per_capita', 'Official est. GDP(billion US$)', 'Metropolitian Population']
            
            # Create a copy to avoid modifying the original
            radar_df = top_5.copy()
            
            # Normalize each metric to a 0-100 scale for radar chart
            for metric in metrics:
                max_val = radar_df[metric].max()
                radar_df[f'{metric}_normalized'] = (radar_df[metric] / max_val) * 100
            
            # Create radar chart using plotly
            fig = go.Figure()
            
            for i, row in radar_df.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[
                        row['GDP_per_capita_normalized'],
                        row['Official est. GDP(billion US$)_normalized'],
                        row['Metropolitian Population_normalized']
                    ],
                    theta=['GDP per Capita', 'Total GDP', 'Population'],
                    fill='toself',
                    name=row['Metropolitian Area/City']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                height=600,
                title="Top 5 Metropolitan Areas - Key Metrics Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="font-size: 0.85rem; color: #666; margin-top: -20px;">
            <p><i>Note: Each metric is normalized to a 0-100 scale relative to the maximum value among the top 5 cities.</i></p>
            </div>
            """, unsafe_allow_html=True)
            
        with top_tabs[2]:
            # Treemap of top performers by region
            fig = px.treemap(
                top_gdp_per_capita,
                path=[px.Constant("All Regions"), 'Region', 'Metropolitian Area/City'],
                values='GDP_per_capita',
                color='GDP_per_capita',
                color_continuous_scale='Viridis',
                title="Top Performers Grouped by Region",
                hover_data={
                    "Country/Region": True,
                    "GDP_per_capita": ":$,.0f"
                }
            )
            fig.update_layout(height=600)
            fig.update_traces(textinfo="label+value")
            st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Size-Efficiency Relationship (Images | Text pattern)
    st.markdown('<div class="fadeIn">', unsafe_allow_html=True)
    colored_header(
        label="Size-Efficiency Relationship",
        description="Examining how metropolitan size relates to economic efficiency",
        color_name="blue-green-70"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create scatter plot of population vs GDP per capita, handling NaN values
        scatter_df = df.dropna(subset=['Metropolitian Population', 'GDP_per_capita', 'Official est. GDP(billion US$)'])
        
        # Create tabs for different visualizations
        scatter_tabs = st.tabs(["Interactive Scatter", "Size Distribution", "Regression Analysis"])
        
        with scatter_tabs[0]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig = px.scatter(
                scatter_df,
                x='Metropolitian Population',
                y='GDP_per_capita',
                color='Region',
                size='Official est. GDP(billion US$)',
                hover_name='Metropolitian Area/City',
                log_x=True,
                log_y=True,
                size_max=60,
                opacity=0.7,
                color_discrete_sequence=px.colors.qualitative.Bold,
                title="Population vs. GDP per Capita (log scales)",
                hover_data={
                    "Country/Region": True,
                    "Official est. GDP(billion US$)": ":.1f",
                    "Metropolitian Population": ":,.0f",
                    "GDP_per_capita": ":$,.0f"
                }
            )
            
            # Add trendline
            trendline = px.scatter(
                scatter_df,
                x='Metropolitian Population',
                y='GDP_per_capita',
                log_x=True,
                log_y=True,
                trendline="ols",
                trendline_scope="overall",
                trendline_color_override="red"
            )
            
            # Add trendline trace to main figure
            for trace in trendline.data:
                if trace.mode == 'lines':
                    trace.name = "Regression Trend"
                    trace.line.width = 3
                    fig.add_trace(trace)
            
            # Add annotation for optimal city size range
            fig.add_shape(
                type="rect",
                x0=1_000_000, 
                y0=fig.data[0].y.min(), 
                x1=5_000_000, 
                y1=fig.data[0].y.max(),
                line=dict(color="rgba(0,200,0,0.3)", width=2),
                fillcolor="rgba(0,200,0,0.1)",
                layer="below"
            )
            
            fig.add_annotation(
                x=2_500_000,
                y=fig.data[0].y.max() * 0.8,
                text="Optimal City Size Range",
                showarrow=True,
                arrowhead=1,
                arrowcolor="green",
                font=dict(color="green")
            )
            
            fig.update_layout(
                height=600,
                xaxis_title="Metropolitan Population (log scale)",
                yaxis_title="GDP per Capita USD (log scale)",
                legend_title="Region"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with scatter_tabs[1]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create population size categories
            scatter_df['Population Size Category'] = pd.cut(
                scatter_df['Metropolitian Population'], 
                bins=[0, 1_000_000, 5_000_000, 10_000_000, 50_000_000],
                labels=['Small (<1M)', 'Medium (1-5M)', 'Large (5-10M)', 'Mega (>10M)']
            )
            
            # Box plot of GDP per capita by population size category
            fig = px.box(
                scatter_df,
                x='Population Size Category',
                y='GDP_per_capita',
                color='Population Size Category',
                title="GDP per Capita Distribution by Metropolitan Size",
                points="all",
                hover_name='Metropolitian Area/City',
                hover_data={
                    "Country/Region": True,
                    "Official est. GDP(billion US$)": ":.1f",
                    "Metropolitian Population": ":,.0f",
                    "GDP_per_capita": ":$,.0f"
                }
            )
            
            fig.update_layout(
                height=600,
                xaxis_title="Metropolitan Size Category",
                yaxis_title="GDP per Capita (USD)",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with scatter_tabs[2]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Calculate city size vs efficiency metrics
            size_efficiency = pd.DataFrame()
            
            # Create population bins and calculate average GDP per capita
            pop_bins = [0, 500000, 1000000, 2000000, 5000000, 10000000, 50000000]
            pop_labels = ['<500K', '500K-1M', '1M-2M', '2M-5M', '5M-10M', '>10M']
            
            scatter_df['Pop_Bin'] = pd.cut(scatter_df['Metropolitian Population'], bins=pop_bins, labels=pop_labels)
            size_efficiency = scatter_df.groupby('Pop_Bin').agg({
                'GDP_per_capita': ['mean', 'median', 'std', 'count'],
                'Official est. GDP(billion US$)': 'mean'
            }).reset_index()
            
            # Flatten multi-level columns
            size_efficiency.columns = ['Population_Size', 'Mean_GDP_Per_Capita', 'Median_GDP_Per_Capita', 
                                     'Std_GDP_Per_Capita', 'Count', 'Mean_GDP_Billion']
            
            # Create multi-line chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=size_efficiency['Population_Size'],
                y=size_efficiency['Mean_GDP_Per_Capita'],
                mode='lines+markers',
                name='Mean GDP per Capita',
                line=dict(color='#0078D4', width=3),
                marker=dict(size=10)
            ))
            
            fig.add_trace(go.Scatter(
                x=size_efficiency['Population_Size'],
                y=size_efficiency['Median_GDP_Per_Capita'],
                mode='lines+markers',
                name='Median GDP per Capita',
                line=dict(color='#107C10', width=3, dash='dash'),
                marker=dict(size=10)
            ))
            
            # Add error bars using standard deviation
            fig.add_trace(go.Scatter(
                x=size_efficiency['Population_Size'],
                y=size_efficiency['Mean_GDP_Per_Capita'] + size_efficiency['Std_GDP_Per_Capita'],
                mode='lines',
                line=dict(width=0),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=size_efficiency['Population_Size'],
                y=size_efficiency['Mean_GDP_Per_Capita'] - size_efficiency['Std_GDP_Per_Capita'],
                mode='lines',
                line=dict(width=0),
                fill='tonexty',
                fillcolor='rgba(0, 120, 212, 0.2)',
                name='Std Deviation'
            ))
            
            # Add sample size as text
            for i, row in size_efficiency.iterrows():
                fig.add_annotation(
                    x=row['Population_Size'],
                    y=row['Mean_GDP_Per_Capita'] + row['Std_GDP_Per_Capita'] + 5000,
                    text=f"n={row['Count']}",
                    showarrow=False,
                    font=dict(size=10)
                )
            
            fig.update_layout(
                title="City Size vs. Economic Efficiency Analysis",
                xaxis_title="Metropolitan Population Size",
                yaxis_title="GDP per Capita (USD)",
                height=600,
                hovermode="x unified",
                plot_bgcolor='rgba(246,248,250,0.8)',
                paper_bgcolor='rgba(246,248,250,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display regression results in an expander
            with st.expander("View Statistical Analysis"):
                import statsmodels.formula.api as smf
                
                # Create log columns for regression
                scatter_df['log_population'] = np.log(scatter_df['Metropolitian Population'])
                scatter_df['log_gdp_per_capita'] = np.log(scatter_df['GDP_per_capita'])
                
                # Run regression
                model = smf.ols(formula='log_gdp_per_capita ~ log_population', data=scatter_df).fit()
                
                # Display results
                st.markdown(f"""
                **Regression Results: log(GDP per Capita) ~ log(Population)**
                
                R-squared: {model.rsquared:.4f}  
                p-value: {model.f_pvalue:.4f}
                
                Coefficient for log(Population): {model.params[1]:.4f} (p-value: {model.pvalues[1]:.4f})
                
                Interpretation: A 1% increase in population is associated with a {model.params[1]:.4f}% change in GDP per capita.
                """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <h3>Optimal City Size?</h3>
        <p>The relationship between metropolitan size and economic efficiency reveals important patterns:</p>
        <ul>
            <li>Medium-sized metros (1-5M) often achieve <span class="highlight">higher efficiency</span> than mega-cities</li>
            <li>Very large cities face <span class="highlight">diminishing returns</span> due to congestion and complexity costs</li>
            <li>Small metros (<1M) show wide variance - specialized ones can be highly efficient</li>
            <li>Regional factors often <span class="highlight">outweigh size considerations</span></li>
        </ul>
        
        <h4>Key Findings:</h4>
        <ul>
            <li>Optimal efficiency appears in the 1-5 million population range</li>
            <li>Specialized economic function is more important than size</li>
            <li>Governance quality and infrastructure impact efficiency</li>
            <li>Medium-sized cities balance agglomeration benefits with lower congestion costs</li>
        </ul>
        
        <p>The statistical analysis reveals that population size alone explains only a small portion of the variation in economic efficiency. Other factors like economic specialization, governance quality, and regional context play crucial roles.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Regional Comparisons (Text | Images pattern)
    st.markdown('<div class="fadeIn">', unsafe_allow_html=True)
    colored_header(
        label="Regional Economic Performance",
        description="Comparing economic indicators across global regions",
        color_name="blue-green-70"
    )
    
    # Ensure data is clean for regional aggregations
    clean_df = df.dropna(subset=['GDP_per_capita', 'Metropolitian Population', 'Official est. GDP(billion US$)', 'Region'])
    
    # Calculating regional aggregates
    regional_summary = clean_df.groupby('Region').agg({
        'Metropolitian Area/City': 'count',
        'GDP_per_capita': ['mean', 'median', 'std'],
        'Metropolitian Population': 'sum',
        'Official est. GDP(billion US$)': 'sum'
    }).reset_index()
    
    # Flatten the multi-index columns
    regional_summary.columns = [
        'Region', 'Metro_Count', 'Mean_GDP_per_capita', 'Median_GDP_per_capita', 
        'Std_GDP_per_capita', 'Total_Population', 'Total_GDP'
    ]
    
    # Calculate GDP productivity ratio (Total GDP / Total Population in millions)
    regional_summary['Regional_Productivity'] = regional_summary['Total_GDP'] / (regional_summary['Total_Population'] / 1000000)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown("""
        <div class="insight-box">
        <h3>Regional Economic Patterns</h3>
        <p>Economic productivity varies significantly across global regions, revealing important patterns:</p>
        
        <h4>Key Observations:</h4>
        <ul>
            <li><span class="highlight">North America and Oceania</span> lead in GDP per capita, highlighting their advanced economies</li>
            <li><span class="highlight">East Asia</span> shows extraordinary economic density and efficiency in its metropolitan areas</li>
            <li><span class="highlight">Western Europe</span> maintains high productivity with balanced urban development</li>
            <li><span class="highlight">Middle East</span> displays high variance due to oil-rich cities contrasting with developing areas</li>
            <li><span class="highlight">South Asia and Africa</span> have emerging metros with significant growth potential</li>
        </ul>
        
        <p>These regional differences reflect historical development patterns, governance structures, resource availability, and economic specialization strategies.</p>
        
        <p>Metros in developing regions often show faster growth rates despite lower absolute productivity values.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        region_tabs = st.tabs(["Regional Comparison", "GDP Composition", "Performance Matrix"])
        
        with region_tabs[0]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create a comprehensive regional comparison chart
            fig = go.Figure()
            
            # Add bar chart for Mean GDP per capita
            fig.add_trace(go.Bar(
                x=regional_summary['Region'],
                y=regional_summary['Mean_GDP_per_capita'],
                name='Mean GDP per Capita',
                marker_color='#0078D4',
                hovertemplate='<b>%{x}</b><br>Mean GDP per Capita: $%{y:,.0f}<br>Metro Count: %{customdata[0]}<extra></extra>',
                customdata=np.column_stack((regional_summary['Metro_Count'], regional_summary['Median_GDP_per_capita']))
            ))
            
            # Add line for Regional Productivity (economic efficiency)
            fig.add_trace(go.Scatter(
                x=regional_summary['Region'],
                y=regional_summary['Regional_Productivity'],
                mode='lines+markers',
                name='Regional Productivity',
                yaxis='y2',
                line=dict(color='#107C10', width=3),
                marker=dict(size=10, symbol='diamond'),
                hovertemplate='<b>%{x}</b><br>Regional Productivity: $%{y:,.0f}<br>Total GDP: $%{customdata[0]:,.0f} billion<extra></extra>',
                customdata=np.column_stack((regional_summary['Total_GDP'], regional_summary['Total_Population']))
            ))
            
            # Update layout with dual y-axes
            fig.update_layout(
                title='Regional Economic Performance',
                xaxis=dict(title='Region', tickangle=45),
                yaxis=dict(
                    title='Mean GDP per Capita (USD)',
                    side='left',
                    showgrid=True
                ),
                yaxis2=dict(
                    title='Regional Productivity (GDP/Population in millions)',
                    side='right',
                    overlaying='y',
                    showgrid=False
                ),
                height=600,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                hovermode='closest',
                plot_bgcolor='rgba(246,248,250,0.8)',
                paper_bgcolor='rgba(246,248,250,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with region_tabs[1]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create data for the sunburst chart
            region_metro_data = []
            
            for region in clean_df['Region'].unique():
                region_df = clean_df[clean_df['Region'] == region]
                # Get top 5 metros by GDP in each region
                top_metros = region_df.nlargest(5, 'Official est. GDP(billion US$)')
                
                # Add top metros individually
                for _, metro in top_metros.iterrows():
                    region_metro_data.append({
                        'Region': region,
                        'Metro': metro['Metropolitian Area/City'],
                        'GDP': metro['Official est. GDP(billion US$)'],
                        'Population': metro['Metropolitian Population'],
                        'GDP_per_capita': metro['GDP_per_capita']
                    })
                
                # Add "Other" category for remaining metros
                other_metros = region_df.drop(top_metros.index)
                if len(other_metros) > 0:
                    region_metro_data.append({
                        'Region': region,
                        'Metro': f'Other {region} Metros',
                        'GDP': other_metros['Official est. GDP(billion US$)'].sum(),
                        'Population': other_metros['Metropolitian Population'].sum(),
                        'GDP_per_capita': other_metros['Official est. GDP(billion US$)'].sum() * 1e9 / other_metros['Metropolitian Population'].sum()
                    })
            
            # Convert to DataFrame
            sunburst_df = pd.DataFrame(region_metro_data)
            
            # Create sunburst chart
            fig = px.sunburst(
                sunburst_df,
                path=['Region', 'Metro'],
                values='GDP',
                color='GDP_per_capita',
                color_continuous_scale='Blues',
                title='Regional GDP Composition by Metropolitan Areas',
                hover_data=['Population', 'GDP_per_capita'],
                custom_data=['Population', 'GDP_per_capita']
            )
            
            fig.update_traces(
                hovertemplate='<b>%{label}</b><br>GDP: $%{value:.1f} billion<br>Population: %{customdata[0]:,.0f}<br>GDP per Capita: $%{customdata[1]:,.0f}<extra></extra>'
            )
            
            fig.update_layout(
                height=600,
                margin=dict(t=50, l=0, r=0, b=0),
                paper_bgcolor='rgba(246,248,250,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with region_tabs[2]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create a quadrant chart comparing metrics across regions
            
            # Calculate normalized metrics
            regional_summary['Normalized_GDP_per_capita'] = (regional_summary['Mean_GDP_per_capita'] - regional_summary['Mean_GDP_per_capita'].min()) / (regional_summary['Mean_GDP_per_capita'].max() - regional_summary['Mean_GDP_per_capita'].min())
            regional_summary['Normalized_Total_GDP'] = (regional_summary['Total_GDP'] - regional_summary['Total_GDP'].min()) / (regional_summary['Total_GDP'].max() - regional_summary['Total_GDP'].min())
            regional_summary['Size'] = regional_summary['Metro_Count'] * 20 + 20  # Scale the size for visualization
            
            # Create the quadrant chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=regional_summary['Normalized_Total_GDP'],
                y=regional_summary['Normalized_GDP_per_capita'],
                mode='markers+text',
                marker=dict(
                    size=regional_summary['Size'],
                    color=regional_summary['Normalized_GDP_per_capita'],
                    colorscale='Blues',
                    line=dict(width=2, color='#0078D4'),
                    showscale=True,
                    colorbar=dict(title='Normalized GDP per Capita')
                ),
                text=regional_summary['Region'],
                textposition='top center',
                hovertemplate='<b>%{text}</b><br>GDP per Capita: $%{customdata[0]:,.0f}<br>Total GDP: $%{customdata[1]:,.0f} billion<br>Metros: %{customdata[2]}<extra></extra>',
                customdata=np.column_stack((
                    regional_summary['Mean_GDP_per_capita'],
                    regional_summary['Total_GDP'],
                    regional_summary['Metro_Count']
                ))
            ))
            
            # Add quadrant lines
            fig.add_shape(
                type='line',
                x0=0.5, y0=0, x1=0.5, y1=1,
                line=dict(color='#605E5C', width=1, dash='dash')
            )
            
            fig.add_shape(
                type='line',
                x0=0, y0=0.5, x1=1, y1=0.5,
                line=dict(color='#605E5C', width=1, dash='dash')
            )
            
            # Add quadrant labels
            fig.add_annotation(x=0.25, y=0.75, text="High Efficiency<br>Low Total GDP", showarrow=False, font=dict(size=10, color='#252525'))
            fig.add_annotation(x=0.75, y=0.75, text="High Efficiency<br>High Total GDP", showarrow=False, font=dict(size=10, color='#252525'))
            fig.add_annotation(x=0.25, y=0.25, text="Low Efficiency<br>Low Total GDP", showarrow=False, font=dict(size=10, color='#252525'))
            fig.add_annotation(x=0.75, y=0.25, text="Low Efficiency<br>High Total GDP", showarrow=False, font=dict(size=10, color='#252525'))
            
            fig.update_layout(
                title='Regional Economic Performance Matrix',
                xaxis=dict(
                    title='Normalized Total GDP (Economic Scale)',
                    showgrid=True,
                    zeroline=True,
                    range=[-0.05, 1.05]
                ),
                yaxis=dict(
                    title='Normalized GDP per Capita (Economic Efficiency)',
                    showgrid=True,
                    zeroline=True,
                    range=[-0.05, 1.05]
                ),
                height=600,
                plot_bgcolor='rgba(246,248,250,0.8)',
                paper_bgcolor='rgba(246,248,250,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Outliers Analysis (Images | Text pattern)
    st.markdown('<div class="section-header" id="outliers"><h2>📊 Outlier Analysis</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Identifying metropolitan areas that significantly deviate from expected economic patterns, highlighting overperformers and underperformers relative to their size and region.</div>', unsafe_allow_html=True)
    
    # Detect Outliers
    # Drop NaN values to ensure accurate outlier detection
    clean_df = df.dropna(subset=['GDP_per_capita', 'Metropolitian Population', 'Official est. GDP(billion US$)'])
    
    # Calculate Z-scores
    z_scores = stats.zscore(clean_df[['GDP_per_capita']])
    clean_df['z_score'] = z_scores
    
    # Identify outliers
    outliers_high = clean_df[clean_df['z_score'] > 2].sort_values('z_score', ascending=False)
    outliers_low = clean_df[clean_df['z_score'] < -2].sort_values('z_score')
    
    st.markdown('<div class="outlier-container">', unsafe_allow_html=True)
    outlier_col1, outlier_col2 = st.columns([3, 2])
    
    with outlier_col1:
        outlier_tabs = st.tabs(["Outlier Distribution", "Z-Score Analysis", "Performance Quadrants"])
        
        with outlier_tabs[0]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create a scatter plot with z-scores
            fig = px.scatter(
                clean_df, 
                x='Metropolitian Population', 
                y='GDP_per_capita',
                size='Official est. GDP(billion US$)',
                color='z_score',
                color_continuous_scale='RdBu_r',
                range_color=[-3, 3],
                hover_name='Metropolitian Area/City',
                hover_data={
                    'Metropolitian Population': ':,',
                    'GDP_per_capita': ':,',
                    'Official est. GDP(billion US$)': ':.1f',
                    'z_score': ':.2f',
                    'Region': True
                },
                labels={
                    'Metropolitian Population': 'Metropolitan Population',
                    'GDP_per_capita': 'GDP per Capita (US$)',
                    'Official est. GDP(billion US$)': 'GDP (billion US$)',
                    'z_score': 'Z-Score'
                }
            )
            
            # Update layout
            fig.update_layout(
                title='Economic Outliers by Z-Score',
                height=500,
                plot_bgcolor='rgba(240, 242, 246, 0.8)',
                paper_bgcolor='rgba(240, 242, 246, 0.0)',
                font=dict(family="Segoe UI, sans-serif", color="#252525"),
                margin=dict(l=20, r=20, t=50, b=20),
                coloraxis_colorbar=dict(
                    title="Z-Score",
                    tickvals=[-3, -2, 0, 2, 3],
                    ticktext=["Strong Underperformer", "Underperformer", "Average", "Overperformer", "Strong Overperformer"]
                ),
                xaxis=dict(
                    type='log',
                    title_font=dict(size=14, color="#252525"),
                    tickfont=dict(size=12, color="#252525"),
                    gridcolor='rgba(220, 220, 220, 0.8)',
                    zerolinecolor='rgba(220, 220, 220, 0.8)'
                ),
                yaxis=dict(
                    type='log',
                    title_font=dict(size=14, color="#252525"),
                    tickfont=dict(size=12, color="#252525"),
                    gridcolor='rgba(220, 220, 220, 0.8)',
                    zerolinecolor='rgba(220, 220, 220, 0.8)'
                )
            )
            
            # Add outlier zones
            fig.add_shape(
                type="rect",
                x0=clean_df['Metropolitian Population'].min() * 0.8,
                y0=clean_df['GDP_per_capita'].quantile(0.75) * 1.5,
                x1=clean_df['Metropolitian Population'].max() * 1.2,
                y1=clean_df['GDP_per_capita'].max() * 1.2,
                line=dict(color="#0078D4", width=1, dash="dot"),
                fillcolor="rgba(0, 120, 212, 0.1)",
            )
            
            fig.add_shape(
                type="rect",
                x0=clean_df['Metropolitian Population'].min() * 0.8,
                y0=clean_df['GDP_per_capita'].min() * 0.8,
                x1=clean_df['Metropolitian Population'].max() * 1.2,
                y1=clean_df['GDP_per_capita'].quantile(0.25) * 0.5,
                line=dict(color="#D83B01", width=1, dash="dot"),
                fillcolor="rgba(216, 59, 1, 0.1)",
            )
            
            # Add annotations for outlier zones
            fig.add_annotation(
                x=clean_df['Metropolitian Population'].median(),
                y=clean_df['GDP_per_capita'].max() * 0.95,
                text="High Performers",
                showarrow=False,
                font=dict(size=14, color="#0078D4", family="Segoe UI, sans-serif"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="#0078D4",
                borderwidth=1,
                borderpad=4
            )
            
            fig.add_annotation(
                x=clean_df['Metropolitian Population'].median(),
                y=clean_df['GDP_per_capita'].min() * 1.05,
                text="Low Performers",
                showarrow=False,
                font=dict(size=14, color="#D83B01", family="Segoe UI, sans-serif"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="#D83B01",
                borderwidth=1,
                borderpad=4
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with outlier_tabs[1]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create a bar chart showing z-scores for outliers
            combined_outliers = pd.concat([outliers_high, outliers_low])
            
            fig = px.bar(
                combined_outliers.sort_values('z_score'), 
                y='Metropolitian Area/City',
                x='z_score',
                color='z_score',
                color_continuous_scale='RdBu_r',
                range_color=[-3, 3],
                text='GDP_per_capita',
                hover_data={
                    'GDP_per_capita': ':,',
                    'Metropolitian Population': ':,',
                    'Official est. GDP(billion US$)': ':.1f'
                },
                labels={
                    'Metropolitian Area/City': 'Metropolitan Area',
                    'z_score': 'Z-Score (GDP per Capita)',
                    'GDP_per_capita': 'GDP per Capita (US$)'
                }
            )
            
            # Update layout
            fig.update_layout(
                title='Z-Score Analysis of Outliers',
                plot_bgcolor='rgba(240, 242, 246, 0.8)',
                paper_bgcolor='rgba(240, 242, 246, 0.0)',
                height=600,
                margin=dict(l=20, r=20, t=50, b=20),
                font=dict(family="Segoe UI, sans-serif", color="#252525"),
                xaxis=dict(
                    title_font=dict(size=14, color="#252525"),
                    tickfont=dict(size=12, color="#252525"),
                    gridcolor='rgba(220, 220, 220, 0.8)',
                    zerolinecolor='#605E5C'
                ),
                yaxis=dict(
                    title=None,
                    tickfont=dict(size=12, color="#252525")
                )
            )
            
            # Format text
            fig.update_traces(
                texttemplate='$%{text:,.0f}',
                textposition='outside'
            )
            
            # Add a vertical line at z=0
            fig.add_shape(
                type="line",
                x0=0, y0=-0.5,
                x1=0, y1=len(combined_outliers) - 0.5,
                line=dict(color="#605E5C", width=1.5, dash="solid")
            )
            
            # Add z-score interpretation bands
            fig.add_shape(
                type="rect",
                x0=2, y0=-0.5,
                x1=5, y1=len(combined_outliers) - 0.5,
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(0, 120, 212, 0.1)",
                layer="below"
            )
            
            fig.add_shape(
                type="rect",
                x0=-5, y0=-0.5,
                x1=-2, y1=len(combined_outliers) - 0.5,
                line=dict(color="rgba(0,0,0,0)"),
                fillcolor="rgba(216, 59, 1, 0.1)",
                layer="below"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with outlier_tabs[2]:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Create a quadrant chart for outliers
            # Normalize GDP per capita and population for plotting
            clean_df['gdp_per_capita_norm'] = (clean_df['GDP_per_capita'] - clean_df['GDP_per_capita'].min()) / (clean_df['GDP_per_capita'].max() - clean_df['GDP_per_capita'].min())
            clean_df['pop_norm'] = (clean_df['Metropolitian Population'] - clean_df['Metropolitian Population'].min()) / (clean_df['Metropolitian Population'].max() - clean_df['Metropolitian Population'].min())
            
            # Identify quadrant for each city
            clean_df['quadrant'] = 'Average'
            clean_df.loc[(clean_df['gdp_per_capita_norm'] > 0.5) & (clean_df['pop_norm'] > 0.5), 'quadrant'] = 'Large & Efficient'
            clean_df.loc[(clean_df['gdp_per_capita_norm'] > 0.5) & (clean_df['pop_norm'] < 0.5), 'quadrant'] = 'Small & Efficient'
            clean_df.loc[(clean_df['gdp_per_capita_norm'] < 0.5) & (clean_df['pop_norm'] > 0.5), 'quadrant'] = 'Large & Less Efficient'
            clean_df.loc[(clean_df['gdp_per_capita_norm'] < 0.5) & (clean_df['pop_norm'] < 0.5), 'quadrant'] = 'Small & Less Efficient'
            
            # Filter outliers for chart
            quadrant_df = pd.concat([
                outliers_high,
                outliers_low,
                clean_df[(clean_df['z_score'] <= 2) & (clean_df['z_score'] >= -2)].sample(min(20, len(clean_df)))
            ])
            
            # Apply the same normalization to the filtered dataframe
            quadrant_df['gdp_per_capita_norm'] = (quadrant_df['GDP_per_capita'] - clean_df['GDP_per_capita'].min()) / (clean_df['GDP_per_capita'].max() - clean_df['GDP_per_capita'].min())
            quadrant_df['pop_norm'] = (quadrant_df['Metropolitian Population'] - clean_df['Metropolitian Population'].min()) / (clean_df['Metropolitian Population'].max() - clean_df['Metropolitian Population'].min())
            
            # Set quadrant
            quadrant_df['quadrant'] = 'Average'
            quadrant_df.loc[(quadrant_df['gdp_per_capita_norm'] > 0.5) & (quadrant_df['pop_norm'] > 0.5), 'quadrant'] = 'Large & Efficient'
            quadrant_df.loc[(quadrant_df['gdp_per_capita_norm'] > 0.5) & (quadrant_df['pop_norm'] < 0.5), 'quadrant'] = 'Small & Efficient'
            quadrant_df.loc[(quadrant_df['gdp_per_capita_norm'] < 0.5) & (quadrant_df['pop_norm'] > 0.5), 'quadrant'] = 'Large & Less Efficient'
            quadrant_df.loc[(quadrant_df['gdp_per_capita_norm'] < 0.5) & (quadrant_df['pop_norm'] < 0.5), 'quadrant'] = 'Small & Less Efficient'
            
            # Create scatter plot
            fig = px.scatter(
                quadrant_df,
                x='pop_norm',
                y='gdp_per_capita_norm',
                color='z_score',
                size='Official est. GDP(billion US$)',
                hover_name='Metropolitian Area/City',
                color_continuous_scale='RdBu_r',
                range_color=[-3, 3],
                hover_data={
                    'gdp_per_capita_norm': False,
                    'pop_norm': False,
                    'GDP_per_capita': ':,',
                    'Metropolitian Population': ':,',
                    'quadrant': True,
                    'z_score': ':.2f'
                },
                labels={
                    'pop_norm': 'Population Size (normalized)',
                    'gdp_per_capita_norm': 'GDP per Capita (normalized)',
                    'z_score': 'Z-Score'
                }
            )
            
            # Update layout
            fig.update_layout(
                title='Performance Quadrants Analysis',
                height=600,
                plot_bgcolor='rgba(240, 242, 246, 0.8)',
                paper_bgcolor='rgba(240, 242, 246, 0.0)',
                font=dict(family="Segoe UI, sans-serif", color="#252525"),
                margin=dict(l=20, r=20, t=50, b=20),
                coloraxis_colorbar=dict(
                    title="Z-Score",
                    tickvals=[-3, -2, 0, 2, 3],
                    ticktext=["Strong Underperformer", "Underperformer", "Average", "Overperformer", "Strong Overperformer"]
                )
            )
            
            # Add quadrant lines
            fig.add_shape(
                type="line",
                x0=0.5, y0=0,
                x1=0.5, y1=1,
                line=dict(color="#605E5C", width=1, dash="dash")
            )
            
            fig.add_shape(
                type="line",
                x0=0, y0=0.5,
                x1=1, y1=0.5,
                line=dict(color="#605E5C", width=1, dash="dash")
            )
            
            # Add quadrant annotations
            fig.add_annotation(
                x=0.25, y=0.75,
                text="Small & Efficient",
                showarrow=False,
                font=dict(size=12, color="#0078D4", family="Segoe UI, sans-serif"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="#0078D4",
                borderwidth=1,
                borderpad=2
            )
            
            fig.add_annotation(
                x=0.75, y=0.75,
                text="Large & Efficient",
                showarrow=False,
                font=dict(size=12, color="#0078D4", family="Segoe UI, sans-serif"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="#0078D4",
                borderwidth=1,
                borderpad=2
            )
            
            fig.add_annotation(
                x=0.25, y=0.25,
                text="Small & Less Efficient",
                showarrow=False,
                font=dict(size=12, color="#D83B01", family="Segoe UI, sans-serif"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="#D83B01",
                borderwidth=1,
                borderpad=2
            )
            
            fig.add_annotation(
                x=0.75, y=0.25,
                text="Large & Less Efficient",
                showarrow=False,
                font=dict(size=12, color="#D83B01", family="Segoe UI, sans-serif"),
                bgcolor="rgba(255, 255, 255, 0.7)",
                bordercolor="#D83B01",
                borderwidth=1,
                borderpad=2
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with outlier_col2:
        st.markdown('<div class="insight-box" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">', unsafe_allow_html=True)
        
        st.markdown('<h3 style="color: #0078D4; font-family: \'Segoe UI\', sans-serif; font-size: 1.3rem; margin-bottom: 1rem;">Outlier Insights</h3>', unsafe_allow_html=True)
        
        st.markdown('<h4 style="color: #252525; font-family: \'Segoe UI\', sans-serif; font-size: 1.1rem; margin-bottom: 0.5rem;">Economic Overperformers</h4>', unsafe_allow_html=True)
        
        st.markdown('<p style="margin-bottom: 1rem; line-height: 1.5; color: #252525; font-family: \'Segoe UI\', sans-serif;">Metropolitan areas with exceptionally high GDP per capita (z-score > 2) demonstrate unique characteristics that drive economic efficiency:</p>', unsafe_allow_html=True)
        
        st.markdown('''
        <ul style="margin-bottom: 1.5rem; padding-left: 1.5rem; color: #252525; font-family: 'Segoe UI', sans-serif;">
            <li><strong>Specialized economies</strong> focused on high-value industries like finance, technology, or energy</li>
            <li><strong>Optimal scale</strong> balancing population size with economic output</li>
            <li><strong>Strategic location</strong> advantage for trade and business</li>
            <li><strong>Governance structures</strong> that facilitate business efficiency</li>
        </ul>
        ''', unsafe_allow_html=True)
        
        st.markdown('<h4 style="color: #252525; font-family: \'Segoe UI\', sans-serif; font-size: 1.1rem; margin-bottom: 0.5rem;">Economic Underperformers</h4>', unsafe_allow_html=True)
        
        st.markdown('<p style="margin-bottom: 1rem; line-height: 1.5; color: #252525; font-family: \'Segoe UI\', sans-serif;">Metropolitan areas with significantly lower GDP per capita (z-score < -2) typically face various challenges:</p>', unsafe_allow_html=True)
        
        st.markdown('''
        <ul style="margin-bottom: 1.5rem; padding-left: 1.5rem; color: #252525; font-family: 'Segoe UI', sans-serif;">
            <li><strong>Economic transition challenges</strong> from manufacturing to service economies</li>
            <li><strong>Infrastructure limitations</strong> constraining productivity</li>
            <li><strong>Regional economic disparities</strong> affecting development</li>
            <li><strong>Rapid population growth</strong> outpacing economic development</li>
        </ul>
        ''', unsafe_allow_html=True)
        
        st.markdown('<h4 style="color: #252525; font-family: \'Segoe UI\', sans-serif; font-size: 1.1rem; margin-bottom: 0.5rem;">Key Takeaways</h4>', unsafe_allow_html=True)
        
        st.markdown('<p style="line-height: 1.5; color: #252525; font-family: \'Segoe UI\', sans-serif;">The analysis reveals that population size alone does not determine economic efficiency. The most efficient metropolitan economies combine strategic specialization, optimal scale, strong governance, and advantageous positioning within global economic networks.</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add a section divider
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Add a footer section
    st.markdown("""
    <div class="footer">
        <p>Urban Economic Efficiency Dashboard | Data analysis of metropolitan economic indicators</p>
        <p>Data sources: Various economic databases and reports | Last updated: 2023</p>
        <div class="author-info">
            <p><strong>Created by Manish Paneru</strong> | Data Analyst</p>
            <div class="social-links">
                <a href="https://linkedin.com/in/manish.paneru1" target="_blank"><i class="fab fa-linkedin"></i> LinkedIn</a> |
                <a href="https://github.com/manishpaneru" target="_blank"><i class="fab fa-github"></i> GitHub</a> |
                <a href="https://www.analystpaneru.xyz" target="_blank"><i class="fa fa-globe"></i> Portfolio</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add Font Awesome for social icons
    st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        .author-info {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
        .social-links {
            margin-top: 5px;
        }
        .social-links a {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            margin: 0 5px;
            transition: color 0.3s;
        }
        .social-links a:hover {
            color: white;
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.error("Could not load the dataset. Please check that dataset.csv exists in the current directory.") 