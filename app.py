import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. PAGE CONFIGURATION (ORACLE AUTO-OPEN) ---
# FIX: initial_sidebar_state ko "expanded" kar diya hai!
st.set_page_config(page_title="APEX AI: NEXUS-1", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

# Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "⚡ APEX ORACLE ONLINE. \n\nI am the forensic decode agent. Paste any headline or data from the right feed, and I will decode the real strategy for you."}
    ]

# --- 2. TERMINAL CSS (Cleaned up for perfect rendering) ---
st.markdown("""
    <style>
    /* CINEMATIC BACKGROUND */
    .stApp {
        background: linear-gradient(to bottom, rgba(2, 6, 23, 0.75) 0%, rgba(2, 6, 23, 0.4) 100%), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    
    /* 🚨 STREAMLIT HEADER CLEANUP (No more hiding bugs) 🚨 */
    header { background-color: transparent !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    
    /* SIDEBAR CUSTOMIZATION (Hacker/Dark Vibe) */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 15, 30, 0.95) !important;
        border-right: 1px solid rgba(0, 229, 255, 0.3);
    }
    .sidebar-title { color: #00e5ff; font-weight: 900; font-size: 1.5rem; letter-spacing: 1px; margin-bottom: 20px; text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);}
    
    /* TYPOGRAPHY & BRANDING */
    h1 { font-weight: 900; font-size: 2.8rem; letter-spacing: -1px; margin-bottom: 0; color: #ffffff; margin-top: -30px;}
    .neon-text { color: #00e5ff; text-shadow: 0 0 10px rgba(0, 0, 0, 0.8); }
    
    /* TOP KPI METRIC BOXES */
    .metric-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .metric-title { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; font-weight: 700;}
    .metric-value { font-size: 1.6rem; color: #00e5ff; font-weight: 900; text-shadow: 0 0 10px rgba(0, 229, 255, 0.3);}

    /* THE DARK SMOKED GLASS FEED CARDS */
    .feed-card {
        background: rgba(10, 15, 30, 0.75); 
        backdrop-filter: blur(20px); 
        -webkit-backdrop-filter: blur(20px);
        border-left: 4px solid #00e5ff; 
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px; 
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s ease;
    }
    .feed-card:hover { transform: translateX(-5px); border-left: 4px solid #ffffff; }
    
    /* TAGS & TEXT STYLING */
    .tag-eco { background: rgba(0, 255, 157, 0.15); color: #00ff9d; padding: 4px 10px; border-radius: 5px; font-size: 10px; font-weight: 800; border: 1px solid rgba(0, 255, 157, 0.4); letter-spacing: 1px;}
    .tag-tech { background: rgba(0, 229, 255, 0.15); color: #00e5ff; padding: 4px 10px; border-radius: 5px; font-size: 10px; font-weight: 800; border: 1px solid rgba(0, 229, 255, 0.4); letter-spacing: 1px;}
    .tag-edu { background: rgba(255, 196, 0, 0.15); color: #ffc400; padding: 4px 10px; border-radius: 5px; font-size: 10px; font-weight: 800; border: 1px solid rgba(255, 196, 0, 0.4); letter-spacing: 1px;}
    .card-title { font-size: 1.1rem; font-weight: 700; margin-top: 12px; margin-bottom: 8px; color: #ffffff; line-height: 1.3;}
    .card-desc { color: #cbd5e1; font-size: 0.85rem; line-height: 1.5; margin-bottom: 12px;}
    .status-text { font-family: 'Courier New', monospace; font-size: 0.85rem; font-weight: bold;}
    ul.fact-list { margin-top: 5px; margin-bottom: 10px; padding-left: 20px; color: #e2e8f0; font-size: 0.85rem;}
    ul.fact-list li { margin-bottom: 4px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. THE APEX ORACLE CHATBOT (SIDEBAR) ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>💬 APEX ORACLE</div>", unsafe_allow_html=True)
    
    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Chat Input Logic
    if prompt := st.chat_input("Ask Oracle to decode a headline..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = f"**FORENSIC ANALYSIS INITIATED:** \n\nQuery: '{prompt}'. \n\n*Decoding logic...* Based on current global telemetry, this indicates a major realignment. **Actionable move:** Focus on upskilling in this specific domain to capture the trend."
            
            # Hacker Typewriter effect
            typed_text = ""
            for char in full_response:
                typed_text += char
                message_placeholder.markdown(typed_text + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 4. HEADER & KPI DASHBOARD (MAIN SCREEN) ---
st.markdown("<h1>APEX <span class='neon-text'>NEXUS-1</span></h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown("<div class='metric-box'><div class='metric-title'>Total Data Nodes</div><div class='metric-value'>3,842</div></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-box'><div class='metric-title'>Global Volatility</div><div class='metric-value'>42.1%</div></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-box'><div class='metric-title'>AI Skill Demand Shift</div><div style='color:#00ff9d;' class='metric-value'>+18%</div></div>", unsafe_allow_html=True)
with m4: st.markdown("<div class='metric-box'><div class='metric-title'>Multi-Agent Status</div><div class='metric-value'>ONLINE & RAW</div></div>", unsafe_allow_html=True)

# --- 5. THE COMMAND CENTER (SPLIT LAYOUT) ---
col_globe, col_feed = st.columns([1.5, 1])

with col_globe:
    df = pd.DataFrame([
        {"name": "INDIA", "lat": 28.6139, "lon": 77.2090, "color": "#00e5ff", "size": 12}, 
        {"name": "USA", "lat": 38.9072, "lon": -77.0369, "color": "#ff3333", "size": 12},
        {"name": "RUSSIA", "lat": 55.7558, "lon": 37.6173, "color": "#ffc400", "size": 12},
        {"name": "CHINA", "lat": 39.9042, "lon": 116.4074, "color": "#00ff9d", "size": 12}
    ])

    fig = go.Figure(data=go.Scattergeo(
        lon = df['lon'], lat = df['lat'], text = df['name'],
        mode = 'markers+text',
        textposition="top center",
        textfont=dict(family="Arial Black", size=12, color="white"),
        marker = dict(size = df['size'], color = df['color'], line_color='white', line_width=1, opacity=1)
    ))

    fig.update_layout(
        geo = dict(
            projection_type = 'orthographic',
            showland = True, landcolor = "#1e293b",     
            showocean = True, oceancolor = "#064273",    
            showcountries=True, countrycolor="rgba(255,255,255,0.2)",
            showcoastlines=True, coastlinecolor="rgba(255,255,255,0.4)",
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=600 
    )
    st.plotly_chart(fig, use_container_width=True)

with col_feed:
    st.markdown("<h4 style='color: #8892b0; font-size:1rem; margin-bottom: 15px; letter-spacing: 1px;'>📡 LIVE TRUTH TERMINAL (RAW DATA)</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feed-card" style="border-left-color: #00ff9d;">
        <span class="tag-eco">ECONOMIC & MARKET AGENT</span>
        <div class="card-title">Global IT Sector Shift: Hiring vs. Revenue</div>
        <div class="card-desc">
            Extracted Telemetry (Last 72 Hrs):
            <ul class="fact-list">
                <li>Top 5 Indian IT firms report 14% drop in traditional entry-level hiring.</li>
                <li>Simultaneous 22% increase in mid-level AI integration roles.</li>
            </ul>
        </div>
        <div class="status-text" style="color:#00ff9d;">>> DATA PATHWAY: OPPORTUNITY IN 'AI INTEGRATION' SKILLS.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feed-card" style="border-left-color: #00e5ff;">
        <span class="tag-tech">SCIENCE & TECH AGENT</span>
        <div class="card-title">Open-Source LLM Hardware Breakthrough</div>
        <div class="card-desc">
            Raw Fact Cross-Check:
            <ul class="fact-list">
                <li>New open-weight AI model successfully runs entirely locally on 16GB RAM laptops.</li>
                <li>Data privacy compliance for local businesses reaches 100%.</li>
            </ul>
        </div>
        <div class="status-text neon-text">>> DATA PATHWAY: LOCAL AI DEPLOYMENT IS HIGHLY VIABLE.</div>
    </div>
    """, unsafe_allow_html=True)
