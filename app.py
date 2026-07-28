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

# --- 2. CUSTOM CSS: LIQUID GLASS + CYBERPUNK THEME ---
st.markdown("""
    <style>
    /* Dark Cyberpunk Background */
    .stApp {
        background-color: #050508;
        color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* IdeaPulse Style Typography */
    h1 {
        font-weight: 900;
        font-size: 3rem;
        letter-spacing: -1px;
    }
    .neon-text {
        color: #00e5ff; /* Cyan blue from the image */
    }
    .sub-text {
        color: #8892b0;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* LIQUID GLASS UI CARDS (From Image 2) */
    .glass-card {
        background: rgba(255, 255, 255, 0.03); /* Extremely transparent white */
        backdrop-filter: blur(16px); /* The magic frosted glass blur */
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle glowing border */
        border-radius: 20px; /* Smooth rounded corners */
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); /* Depth shadow */
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px); /* Hover float effect */
        border: 1px solid rgba(0, 229, 255, 0.4); /* Neon border on hover */
    }

    /* Tags */
    .tag-live {
        background: rgba(0, 229, 255, 0.2);
        color: #00e5ff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid rgba(0, 229, 255, 0.3);
    }
    .tag-alert {
        background: rgba(255, 51, 51, 0.2);
        color: #ff3333;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid rgba(255, 51, 51, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. HEADER (IdeaPulse Clone) ---
st.markdown("<h1>The World, <span class='neon-text'>Live.</span></h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Where AI & tech-policy stories are breaking. Tap a city.</div>", unsafe_allow_html=True)

# --- 4. THE 3D GLOBE (PyDeck) ---
# Global nodes coordinates (Moscow, Beijing, Washington, New Delhi, Silicon Valley)
data = pd.DataFrame([
    {"city": "New Delhi", "lat": 28.6139, "lon": 77.2090, "color": [0, 229, 255]}, 
    {"city": "Washington", "lat": 38.9072, "lon": -77.0369, "color": [255, 51, 51]},
    {"city": "Moscow", "lat": 55.7558, "lon": 37.6173, "color": [255, 51, 51]},
    {"city": "Beijing", "lat": 39.9042, "lon": 116.4074, "color": [0, 229, 255]}
])

# Rendering the 3D Map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/dark-v11', # Dark map
    initial_view_state=pdk.ViewState(
        latitude=20.0,
        longitude=40.0,
        zoom=1.5,
        pitch=45, # Tilted 3D view
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=data,
            get_position='[lon, lat]',
            get_color='color',
            get_radius=500000, # Signal radius
            pickable=True,
            filled=True,
            opacity=0.8
        ),
    ],
))

st.markdown("<br>", unsafe_allow_html=True)

# --- 5. LIQUID GLASS DATA FEED ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">LIVE NODE</span> <span class="tag-alert">HOT SIGNAL</span><br><br>
        <h3 style="margin-top: 5px; margin-bottom: 10px;">Global Semiconductor Policy Shift</h3>
        <p style="color: #cccccc; font-size: 14px;">Autonomous scan detected new export restrictions from US to Asian markets. Expected disruption in supply chain within 72 hours.</p>
        <b class="neon-text">APEX Verification: True</b>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <span class="tag-live">AI FORENSIC</span><br><br>
        <h3 style="margin-top: 5px; margin-bottom: 10px;">Crude Oil vs. Pump Price Gap</h3>
        <p style="color: #cccccc; font-size: 14px;">Brent crude down by 14%, yet domestic retail fuel remains unchanged. Fact-checking the fiscal deficit narrative pushed by national media.</p>
        <b class="neon-text">APEX Verification: Analysing...</b>
    </div>
    """, unsafe_allow_html=True)
