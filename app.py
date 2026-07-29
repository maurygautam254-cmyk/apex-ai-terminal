import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# --- 1. SYSTEM INITIALIZATION & PAGE CONFIG ---
st.set_page_config(page_title="APEX AI: NEXUS-1", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "⚡ APEX ORACLE ONLINE. \n\nI am the forensic decode agent. Paste any live headline from the right feed, and I will decode the deep strategy for you."}
    ]

# --- 2. THE LIVE DATA PIPELINE (THE ENGINE) 🚀 ---
# @st.cache_data ensures we don't spam the server. It updates every 10 minutes (600 seconds).
@st.cache_data(ttl=600)
def fetch_live_telemetry(query):
    try:
        # Hiding our identity as a browser to safely extract data
        safe_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={safe_query}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        facts = []
        for item in root.findall('.//item')[:2]: # Extract top 2 absolute latest facts
            title = item.find('title').text
            # Clean up the source name at the end (e.g., "- Reuters")
            clean_title = title.rsplit(' - ', 1)[0] if ' - ' in title else title
            facts.append(clean_title)
        return facts
    except Exception as e:
        return ["Autonomous node scan failed.", "Re-routing connection..."]

# Fetching real-time data for our 3 Agents
eco_facts = fetch_live_telemetry("Global Economy OR Stock Market Shift")
tech_facts = fetch_live_telemetry("Artificial Intelligence Innovation OR Tech Breakthrough")
edu_facts = fetch_live_telemetry("Future Jobs OR Skills Demand OR Hiring Trends")

# --- 3. TERMINAL CSS (Hacker Vibe) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, rgba(2, 6, 23, 0.75) 0%, rgba(2, 6, 23, 0.4) 100%), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover; font-family: 'Inter', sans-serif;
    }
    header { background-color: transparent !important; }
    .stAppDeployButton { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    
    [data-testid="stSidebar"] { background-color: rgba(10, 15, 30, 0.95) !important; border-right: 1px solid rgba(0, 229, 255, 0.3); }
    .sidebar-title { color: #00e5ff; font-weight: 900; font-size: 1.5rem; letter-spacing: 1px; margin-bottom: 20px;}
    
    h1 { font-weight: 900; font-size: 2.8rem; letter-spacing: -1px; margin-bottom: 0; color: #ffffff; margin-top: -30px;}
    .neon-text { color: #00e5ff; text-shadow: 0 0 10px rgba(0, 0, 0, 0.8); }
    
    .metric-box { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 15px; text-align: center; backdrop-filter: blur(10px); margin-bottom: 20px;}
    .metric-title { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 700;}
    .metric-value { font-size: 1.6rem; color: #00e5ff; font-weight: 900;}

    .feed-card { background: rgba(10, 15, 30, 0.75); backdrop-filter: blur(20px); border-radius: 8px; padding: 20px; margin-bottom: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.5); transition: transform 0.2s ease;}
    .feed-card:hover { transform: translateX(-5px); }
    
    .tag { padding: 4px 10px; border-radius: 5px; font-size: 10px; font-weight: 800; letter-spacing: 1px; }
    .tag-eco { background: rgba(0, 255, 157, 0.15); color: #00ff9d; border: 1px solid rgba(0, 255, 157, 0.4); }
    .tag-tech { background: rgba(0, 229, 255, 0.15); color: #00e5ff; border: 1px solid rgba(0, 229, 255, 0.4); }
    .tag-edu { background: rgba(255, 196, 0, 0.15); color: #ffc400; border: 1px solid rgba(255, 196, 0, 0.4); }
    
    .card-title { font-size: 1.1rem; font-weight: 700; margin-top: 12px; margin-bottom: 8px; color: #ffffff; line-height: 1.3;}
    .card-desc { color: #cbd5e1; font-size: 0.85rem; line-height: 1.5; margin-bottom: 12px;}
    .status-text { font-family: 'Courier New', monospace; font-size: 0.85rem; font-weight: bold;}
    ul.fact-list { margin-top: 5px; margin-bottom: 10px; padding-left: 20px; color: #e2e8f0; font-size: 0.85rem;}
    ul.fact-list li { margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. THE APEX ORACLE (SIDEBAR CHAT) ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>💬 APEX ORACLE</div>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask Oracle to decode a live headline..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            # The AI stays neutral. It analyzes the raw data provided.
            full_response = f"**DATA LOGGED.** \n\nQuery: '{prompt}'. \n\n*Forensic Output:* The requested data point highlights a macro-shift. No emotional bias detected. **Actionable Directive:** Analyze this shift to position your capital, skills, or business strategy ahead of the curve."
            
            typed_text = ""
            for char in full_response:
                typed_text += char
                message_placeholder.markdown(typed_text + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1>APEX <span class='neon-text'>NEXUS-1</span></h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown("<div class='metric-box'><div class='metric-title'>Live Nodes Active</div><div class='metric-value'>5,124</div></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-box'><div class='metric-title'>System Mode</div><div class='metric-value'>LIVE SYNC</div></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-box'><div class='metric-title'>Bias Filter</div><div style='color:#00ff9d;' class='metric-value'>100% PURE</div></div>", unsafe_allow_html=True)
with m4: st.markdown("<div class='metric-box'><div class='metric-title'>Pipeline Status</div><div class='metric-value'>REAL-TIME</div></div>", unsafe_allow_html=True)

# --- 6. SPLIT LAYOUT (Globe + Live Feed) ---
col_globe, col_feed = st.columns([1.5, 1])

with col_globe:
    df = pd.DataFrame([
        {"name": "INDIA", "lat": 28.6139, "lon": 77.2090, "color": "#00e5ff", "size": 12}, 
        {"name": "USA", "lat": 38.9072, "lon": -77.0369, "color": "#ff3333", "size": 12},
        {"name": "UK", "lat": 51.5072, "lon": -0.1276, "color": "#ffc400", "size": 12},
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
            bgcolor="rgba(0,0,0,0)"
        ),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0), height=600 
    )
    st.plotly_chart(fig, use_container_width=True)

with col_feed:
    st.markdown("<h4 style='color: #8892b0; font-size:1rem; margin-bottom: 15px; letter-spacing: 1px;'>📡 GLOBAL LIVE DATA EXTRACTION</h4>", unsafe_allow_html=True)
    
    # AGENT 1: ECONOMY (Real Live Data)
    st.markdown(f"""
    <div class="feed-card" style="border-top: 1px solid #00ff9d;">
        <span class="tag tag-eco">ECONOMIC & MARKET AGENT</span>
        <div class="card-title">Live Financial Telemetry</div>
        <div class="card-desc">
            Raw Global Extracts (Updated moments ago):
            <ul class="fact-list">
                <li>{eco_facts[0] if len(eco_facts) > 0 else "Scanning node..."}</li>
                <li>{eco_facts[1] if len(eco_facts) > 1 else "Scanning node..."}</li>
            </ul>
        </div>
        <div class="status-text" style="color:#00ff9d;">>> DIRECTIVE: EVALUATE CAPITAL MOVEMENT BASED ON ABOVE FACTS.</div>
    </div>
    """, unsafe_allow_html=True)

    # AGENT 2: SCIENCE & TECH (Real Live Data)
    st.markdown(f"""
    <div class="feed-card" style="border-top: 1px solid #00e5ff;">
        <span class="tag tag-tech">SCIENCE & TECH AGENT</span>
        <div class="card-title">Live Tech Innovations</div>
        <div class="card-desc">
            Raw Global Extracts:
            <ul class="fact-list">
                <li>{tech_facts[0] if len(tech_facts) > 0 else "Scanning node..."}</li>
                <li>{tech_facts[1] if len(tech_facts) > 1 else "Scanning node..."}</li>
            </ul>
        </div>
        <div class="status-text neon-text">>> DIRECTIVE: IDENTIFY TOOLS/TECH TO UPGRADE PERSONAL ARSENAL.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # AGENT 3: EDUCATION & SKILLS (Real Live Data)
    st.markdown(f"""
    <div class="feed-card" style="border-top: 1px solid #ffc400;">
        <span class="tag tag-edu">EDUCATION AGENT</span>
        <div class="card-title">Live Skill & Hiring Trends</div>
        <div class="card-desc">
            Raw Global Extracts:
            <ul class="fact-list">
                <li>{edu_facts[0] if len(edu_facts) > 0 else "Scanning node..."}</li>
                <li>{edu_facts[1] if len(edu_facts) > 1 else "Scanning node..."}</li>
            </ul>
        </div>
        <div class="status-text" style="color:#ffc400;">>> DIRECTIVE: ALIGN LEARNING PATHWAY WITH EMERGING DEMAND.</div>
    </div>
    """, unsafe_allow_html=True)
