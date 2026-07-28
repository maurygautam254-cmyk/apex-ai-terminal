import streamlit as st
import pandas as pd
import pydeck as pdk

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="APEX AI: The World, Live", page_icon="🌍", layout="wide")

# --- 2. ADVANCED CSS: GLOWING BACKGROUND & REAL GLASS UI ---
st.markdown("""
    <style>
    /* Glowing Cyberpunk Background */
    .stApp {
        background-color: #050508;
        /* Creating glowing neon orbs in the background to make the glass pop */
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(0, 229, 255, 0.15), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(255, 51, 51, 0.12), transparent 25%);
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* IdeaPulse Style Typography */
    h1 { font-weight: 900; font-size: 3.5rem; letter-spacing: -1px; margin-bottom: 0;}
    .neon-text { color: #00e5ff; text-shadow: 0 0 10px rgba(0, 229, 255, 0.5); }
    .sub-text { color: #8892b0; font-size: 1.1rem; margin-bottom: 25px; }

    /* REAL LIQUID GLASS UI CARDS */
    .glass-card {
        background: rgba(20, 20, 30, 0.4); /* Slightly lighter base for contrast */
        backdrop-filter: blur(20px); /* Heavy blur */
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 229, 255, 0.3); /* Cyan glowing border */
        border-top: 1px solid rgba(255, 255, 255, 0.2); /* Light reflection on top edge */
        border-left: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px; 
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5); /* Deep shadow */
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(0, 229, 255, 0.6);
        box-shadow: 0 12px 40px 0 rgba(0, 229, 255, 0.2);
    }

    /* Tags */
    .tag-live { background: rgba(0, 229, 255, 0.15); color: #00e5ff; padding: 5px 14px; border-radius: 20px; font-size: 11px; font-weight: 800; border: 1px solid rgba(0, 229, 255, 0.4); letter-spacing: 1px;}
    .tag-alert { background: rgba(255, 51, 51, 0.15); color: #ff3333; padding: 5px 14px; border-radius: 20px; font-size: 11px; font-weight: 800; border: 1px solid rgba(255, 51, 51, 0.4); letter-spacing: 1px; margin-left: 10px;}
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<h1>The World, <span class='neon-text'>Live.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Where AI & tech-policy stories are breaking. Tap a city.</div>", unsafe_allow_html=True)

# --- 4. THE 3D GLOBE (FIXED MAP STYLE) ---
data = pd.DataFrame([
    {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090, "color": [0, 229, 255]}, 
    {"city": "Washington", "lat": 38.9072, "lon": -77.0369, "color": [255, 51, 51]},
    {"city": "Moscow", "lat": 55.7558, "lon": 37.6173, "color": [255, 51, 51]},
    {"city": "Beijing", "lat": 39.9042, "lon": 116.4074, "color": [0, 229, 255]}
])

# Using 'dark' which defaults to CartoDB (Free, no API key needed)
st.pydeck_chart(pdk.Deck(
    map_style='dark', 
    initial_view_state=pdk.ViewState(
        latitude=20.0,
        longitude=40.0,
        zoom=1.5,
        pitch=50, 
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=data,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=600000, 
            pickable=True,
            filled=True,
            opacity=0.9
        ),
    ],
))

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. LIQUID GLASS DATA FEED ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">LIVE NODE</span><span class="tag-alert">HOT SIGNAL</span><br><br>
        <h3 style="margin-top: 5px; margin-bottom: 10px;">Global Semiconductor Policy Shift</h3>
        <p style="color: #cccccc; font-size: 15px; line-height: 1.5;">Autonomous scan detected new export restrictions from US to Asian markets. Expected disruption in supply chain within 72 hours.</p>
        <b class="neon-text">⚡ APEX Verification: True</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">AI FORENSIC</span><br><br>
        <h3 style="margin-top: 5px; margin-bottom: 10px;">Crude Oil vs. Pump Price Gap</h3>
        <p style="color: #cccccc; font-size: 15px; line-height: 1.5;">Brent crude down by 14%, yet domestic retail fuel remains unchanged. Fact-checking the fiscal deficit narrative pushed by national media.</p>
        <b class="neon-text">⚡ APEX Verification: Analysing...</b>
    </div>
    """, unsafe_allow_html=True)
