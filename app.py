import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="APEX AI: The World, Live", page_icon="🌍", layout="wide")

# --- 2. EXACT LIQUID GLASS CSS (COLORFUL ABSTRACT BACKGROUND) ---
st.markdown("""
    <style>
    /* 1. THE COLORFUL ABSTRACT BACKGROUND */
    .stApp {
        /* Wahi purana colorful tech background jo tujhe pasand aaya tha + Halka dark tint text readability ke liye */
        background: linear-gradient(to bottom, rgba(5, 10, 20, 0.4) 0%, rgba(5, 10, 20, 0.1) 100%), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    
    header {visibility: hidden;}
    
    /* 2. TYPOGRAPHY (Shadows for readability) */
    h1 { font-weight: 900; font-size: 4rem; letter-spacing: -2px; margin-bottom: 0; color: #ffffff; text-shadow: 0px 4px 15px rgba(0,0,0,0.8);}
    .neon-text { color: #00e5ff; text-shadow: 0 0 10px rgba(0, 0, 0, 0.8); }
    .sub-text { color: #f8fafc; font-size: 1.2rem; margin-bottom: 30px; font-weight: 500; text-shadow: 0px 2px 10px rgba(0,0,0,0.8);}

    /* 3. PURE LIQUID GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05); /* Very light white tint for frosted glass */
        backdrop-filter: blur(25px); /* Heavy blur */
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.3); /* Glowing edge */
        border-radius: 24px; 
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3), inset 0 0 20px rgba(255, 255, 255, 0.05); 
        transition: transform 0.3s ease;
        color: #ffffff;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 255, 255, 0.6);
    }

    /* Tags */
    .tag-live { background: rgba(0, 0, 0, 0.5); color: #00e5ff; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; border: 1px solid rgba(255,255,255,0.3); letter-spacing: 1px;}
    .tag-alert { background: rgba(0, 0, 0, 0.5); color: #ff3333; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 800; border: 1px solid rgba(255,255,255,0.3); letter-spacing: 1px; margin-left: 10px;}
    
    .card-title { font-size: 1.4rem; font-weight: 700; margin-top: 15px; margin-bottom: 10px; color: #ffffff; text-shadow: 0px 2px 5px rgba(0,0,0,0.8);}
    .card-desc { color: #f1f5f9; font-size: 0.95rem; line-height: 1.6; margin-bottom: 20px; text-shadow: 0px 1px 3px rgba(0,0,0,0.8);}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<h1>The World, <span class='neon-text'>Live.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Where AI & tech-policy stories are breaking. Spin the globe.</div>", unsafe_allow_html=True)

# --- 4. THE SOLID GLOBE WITH WATER & COUNTRY NAMES ---
df = pd.DataFrame([
    {"name": "INDIA", "lat": 28.6139, "lon": 77.2090, "color": "#00e5ff", "size": 14}, 
    {"name": "USA", "lat": 38.9072, "lon": -77.0369, "color": "#ff3333", "size": 14},
    {"name": "RUSSIA", "lat": 55.7558, "lon": 37.6173, "color": "#ff3333", "size": 14},
    {"name": "CHINA", "lat": 39.9042, "lon": 116.4074, "color": "#00e5ff", "size": 14}
])

fig = go.Figure(data=go.Scattergeo(
    lon = df['lon'], lat = df['lat'], text = df['name'],
    mode = 'markers+text',
    textposition="top center",
    textfont=dict(family="Arial Black", size=14, color="white"),
    marker = dict(size = df['size'], color = df['color'], line_color='white', line_width=2, opacity=1)
))

# MAGICAL GLOBE SETTINGS
fig.update_layout(
    geo = dict(
        projection_type = 'orthographic',
        showland = True, 
        landcolor = "#1e293b", # Solid dark land (Zameen)
        showocean = True, 
        oceancolor = "#064273", # DEEP OCEAN BLUE WATER (Pani) 🌊
        showcountries=True, countrycolor="rgba(255,255,255,0.4)",
        showcoastlines=True, coastlinecolor="rgba(255,255,255,0.7)",
        bgcolor="rgba(0,0,0,0)"
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=0, b=0),
    height=480
)

st.plotly_chart(fig, use_container_width=True)

# --- 5. THE PURE LIQUID GLASS CARDS ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">LIVE NODE</span><span class="tag-alert">HOT SIGNAL</span>
        <div class="card-title">Global Semiconductor Policy Shift</div>
        <div class="card-desc">Autonomous scan detected new export restrictions from US to Asian markets. Expected disruption in supply chain within 72 hours.</div>
        <b class="neon-text">⚡ APEX Verification: True</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">AI FORENSIC</span>
        <div class="card-title">Crude Oil vs. Pump Price Gap</div>
        <div class="card-desc">Brent crude down by 14%, yet domestic retail fuel remains unchanged. Cross-checking the fiscal deficit narrative pushed by national media.</div>
        <b class="neon-text">⚡ APEX Status: Analysing...</b>
    </div>
    """, unsafe_allow_html=True)
