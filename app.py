import streamlit as st
import pandas as pd
import pydeck as pdk

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="APEX AI: The World, Live",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CUSTOM CSS: LIQUID GLASS + GRADIENT BACKGROUND ---
st.markdown("""
    <style>
    /* Gradient Background to make the Glass Blur visible */
    .stApp {
        background: radial-gradient(circle at top right, #112a46 0%, #050508 60%);
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Typography */
    h1 { font-weight: 900; font-size: 3rem; letter-spacing: -1px; }
    .neon-text { color: #00e5ff; text-shadow: 0 0 10px rgba(0, 229, 255, 0.5); }
    .sub-text { color: #8892b0; font-size: 1.1rem; margin-bottom: 20px; }

    /* TRUE LIQUID GLASS CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.05); /* Slightly visible white base */
        backdrop-filter: blur(25px); /* Heavy frosted glass blur */
        -webkit-backdrop-filter: blur(25px);
        border-top: 1px solid rgba(255, 255, 255, 0.3); /* Top light reflection */
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(0, 0, 0, 0.4);
        border-bottom: 1px solid rgba(0, 0, 0, 0.4);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); /* 3D Depth */
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border-top: 1px solid rgba(0, 229, 255, 0.6); /* Neon glow on hover */
        box-shadow: 0 15px 35px rgba(0, 229, 255, 0.15);
    }

    /* Tags */
    .tag-live { background: rgba(0, 229, 255, 0.15); color: #00e5ff; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid rgba(0, 229, 255, 0.3); }
    .tag-alert { background: rgba(255, 51, 51, 0.15); color: #ff3333; padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid rgba(255, 51, 51, 0.3); }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<h1>The World, <span class='neon-text'>Live.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Where AI & tech-policy stories are breaking. Tap a city.</div>", unsafe_allow_html=True)

# --- 4. THE 3D GLOBE (FIXED: Using Carto instead of Mapbox) ---
data = pd.DataFrame([
    {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090, "color": [0, 229, 255]}, 
    {"city": "Washington", "lat": 38.9072, "lon": -77.0369, "color": [255, 51, 51]},
    {"city": "Moscow", "lat": 55.7558, "lon": 37.6173, "color": [255, 51, 51]},
    {"city": "Beijing", "lat": 39.9042, "lon": 116.4074, "color": [0, 229, 255]}
])

st.pydeck_chart(pdk.Deck(
    map_provider="carto",       # <--- THIS FIXES THE MISSING MAP
    map_style='dark_matter',    # <--- BEAUTIFUL DARK MAP WITHOUT API KEY
    initial_view_state=pdk.ViewState(
        latitude=20.0, longitude=40.0, zoom=1.5, pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer', data=data, get_position='[lon, lat]',
            get_color='color', get_radius=600000, pickable=True, filled=True, opacity=0.9
        ),
    ],
))

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. TRUE LIQUID GLASS DATA FEED ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">LIVE NODE</span> <span class="tag-alert">HOT SIGNAL</span><br><br>
        <h3 style="margin-top: 10px; margin-bottom: 10px; color: #ffffff;">Global Semiconductor Policy Shift</h3>
        <p style="color: #a0aec0; font-size: 14px; line-height: 1.5;">Autonomous scan detected new export restrictions from US to Asian markets. Expected disruption in supply chain within 72 hours.</p>
        <b class="neon-text" style="font-size: 14px;">APEX Verification: True</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">AI FORENSIC</span><br><br>
        <h3 style="margin-top: 10px; margin-bottom: 10px; color: #ffffff;">Crude Oil vs. Pump Price Gap</h3>
        <p style="color: #a0aec0; font-size: 14px; line-height: 1.5;">Brent crude down by 14%, yet domestic retail fuel remains unchanged. Fact-checking the fiscal deficit narrative pushed by national media.</p>
        <b class="neon-text" style="font-size: 14px;">APEX Verification: Analysing...</b>
    </div>
    """, unsafe_allow_html=True)
