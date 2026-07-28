import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="APEX AI: The World, Live", page_icon="🌍", layout="wide")

# --- 2. HACKER/CYBERPUNK CSS ---
st.markdown("""
    <style>
    /* Force completely dark background */
    .stApp {
        background: #020617; /* Very deep dark blue/black */
        color: #ffffff;
    }
    
    /* Typography */
    h1 { font-weight: 900; font-size: 3.5rem; letter-spacing: -1px; margin-bottom: 0;}
    .neon-text { color: #00e5ff; text-shadow: 0 0 15px rgba(0, 229, 255, 0.6); }
    .sub-text { color: #8892b0; font-size: 1.1rem; margin-bottom: 10px; }

    /* REAL LIQUID GLASS UI CARDS */
    .glass-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 229, 255, 0.3);
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        border-left: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px; 
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    }
    
    /* Tags */
    .tag-live { background: rgba(0, 229, 255, 0.15); color: #00e5ff; padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: 900; border: 1px solid #00e5ff; letter-spacing: 1px;}
    .tag-alert { background: rgba(255, 51, 51, 0.15); color: #ff3333; padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: 900; border: 1px solid #ff3333; letter-spacing: 1px; margin-left: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<h1>The World, <span class='neon-text'>Live.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Where AI & tech-policy stories are breaking. Spin the globe.</div>", unsafe_allow_html=True)

# --- 4. THE HOLOGRAPHIC 3D GLOBE (PLOTLY) ---
df = pd.DataFrame([
    {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090, "color": "#00e5ff", "size": 12}, 
    {"city": "Washington", "lat": 38.9072, "lon": -77.0369, "color": "#ff3333", "size": 14},
    {"city": "Moscow", "lat": 55.7558, "lon": 37.6173, "color": "#ff3333", "size": 14},
    {"city": "Beijing", "lat": 39.9042, "lon": 116.4074, "color": "#00e5ff", "size": 12}
])

fig = go.Figure(data=go.Scattergeo(
    lon = df['lon'], lat = df['lat'], text = df['city'],
    mode = 'markers',
    marker = dict(size = df['size'], color = df['color'], line_color='white', line_width=2, opacity=1)
))

# MAGIC HAPPENS HERE: Making it look like a Cyberpunk Hologram
fig.update_layout(
    geo = dict(
        projection_type = 'orthographic',
        showland = True, 
        landcolor = "#0a192f",          # Deep Tech Blue
        showocean = True, 
        oceancolor = "rgba(0,0,0,0)",   # Transparent ocean
        showcountries=True, 
        countrycolor="#00e5ff",         # Cyan borders
        countrywidth=1,
        showcoastlines=True,
        coastlinecolor="#00e5ff",       # Cyan coastlines
        coastlinewidth=1,
        lonaxis = dict(showgrid=True, gridcolor='rgba(0, 229, 255, 0.15)', gridwidth=0.5), # Hologram grid
        lataxis = dict(showgrid=True, gridcolor='rgba(0, 229, 255, 0.15)', gridwidth=0.5),
        bgcolor="rgba(0,0,0,0)"
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=0, b=0),
    height=480
)

st.plotly_chart(fig, use_container_width=True)

# --- 5. LIQUID GLASS DATA FEED ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">LIVE NODE</span><span class="tag-alert">HOT SIGNAL</span><br><br>
        <h3 style="margin-top: 5px; margin-bottom: 10px;">Global Semiconductor Policy Shift</h3>
        <p style="color: #cccccc; font-size: 15px;">Autonomous scan detected new export restrictions from US to Asian markets. Expected disruption in supply chain within 72 hours.</p>
        <b class="neon-text">⚡ APEX Verification: True</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">AI FORENSIC</span><br><br>
        <h3 style="margin-top: 5px; margin-bottom: 10px;">Crude Oil vs. Pump Price Gap</h3>
        <p style="color: #cccccc; font-size: 15px;">Brent crude down by 14%, yet domestic retail fuel remains unchanged. Fact-checking the fiscal deficit narrative.</p>
        <b class="neon-text">⚡ APEX Verification: Analysing...</b>
    </div>
    """, unsafe_allow_html=True)
