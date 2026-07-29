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
        {"role": "assistant", "content": "⚡ APEX ORACLE ONLINE. \n\nI am the forensic decode agent. Paste any live data from the right feed, and I will decode the strategy for you."}
    ]

# --- 2. LANGUAGE CONFIGURATION ---
LANG_CONFIG = {
    "English": {
        "hl": "en-US", "gl": "US",
        "q_eco": "Global Economy OR Stock Market Shift",
        "q_tech": "Artificial Intelligence Innovation OR Tech Breakthrough",
        "q_edu": "Future Jobs OR Skills Demand OR Hiring Trends",
        "ui_title": "📡 LIVE TRUTH TERMINAL (RAW DATA)",
        "ui_eco": "ECONOMIC & MARKET AGENT",
        "ui_tech": "SCIENCE & TECH AGENT",
        "ui_edu": "EDUCATION AGENT"
    },
    "Hindi (हिंदी)": {
        "hl": "hi", "gl": "IN",
        "q_eco": "वैश्विक अर्थव्यवस्था OR शेयर बाजार",
        "q_tech": "आर्टिफिशियल इंटेलिजेंस तकनीक नवप्रवर्तन",
        "q_edu": "भविष्य की नौकरियां OR कौशल विकास",
        "ui_title": "📡 लाइव ट्रुथ टर्मिनल (कच्चा डेटा)",
        "ui_eco": "आर्थिक और बाजार एजेंट",
        "ui_tech": "विज्ञान और तकनीकी एजेंट",
        "ui_edu": "शिक्षा और कौशल एजेंट"
    }
}

# --- 3. ADVANCED TERMINAL CSS (Added Link & Expander Styling) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, rgba(2, 6, 23, 0.75) 0%, rgba(2, 6, 23, 0.4) 100%), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop') no-repeat center center fixed; background-size: cover; font-family: 'Inter', sans-serif; }
    header { background-color: transparent !important; }
    .stAppDeployButton, [data-testid="stToolbar"] { display: none !important; }
    
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
    .status-text { font-family: 'Courier New', monospace; font-size: 0.85rem; font-weight: bold; margin-top:10px;}
    
    /* 🚨 NEW LINK AND ARCHIVE STYLING 🚨 */
    a.headline-link { color: #e2e8f0; text-decoration: none; transition: 0.2s;}
    a.headline-link:hover { color: #00e5ff; text-decoration: underline;}
    ul.fact-list { margin-top: 5px; margin-bottom: 10px; padding-left: 20px; color: #e2e8f0; font-size: 0.85rem;}
    ul.fact-list li { margin-bottom: 8px; }
    
    details.archive-details { margin-top: 15px; }
    summary.archive-summary { color: #94a3b8; font-size: 0.8rem; cursor: pointer; font-weight: bold; font-family: 'Courier New', monospace; outline: none; transition: 0.3s; list-style: none;}
    summary.archive-summary::-webkit-details-marker { display: none; }
    summary.archive-summary:hover { color: #ffffff; text-shadow: 0 0 8px rgba(255,255,255,0.8); }
    ul.archive-list { max-height: 180px; overflow-y: auto; margin-top: 10px; padding-right: 10px; border-top: 1px dashed rgba(255,255,255,0.2); padding-top:10px;}
    
    /* Custom Scrollbar for Archive */
    ul.archive-list::-webkit-scrollbar { width: 5px; }
    ul.archive-list::-webkit-scrollbar-thumb { background: #00e5ff; border-radius: 4px; }
    ul.archive-list::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
    </style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (LANGUAGE & ORACLE) ---
with st.sidebar:
    st.markdown("<div class='sidebar-title'>⚙️ SYSTEM CONTROL</div>", unsafe_allow_html=True)
    selected_lang = st.selectbox("🌐 Select Output Language", list(LANG_CONFIG.keys()))
    cfg = LANG_CONFIG[selected_lang]
    
    st.markdown("<hr style='border-color: rgba(0,229,255,0.2);'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>💬 APEX ORACLE</div>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if prompt := st.chat_input("Ask Oracle to decode data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = f"**DATA LOGGED.** \n\nQuery: '{prompt}'. \n\n*Forensic Output:* The requested data point highlights a macro-shift. **Actionable Directive:** Analyze this shift to position your capital or skills ahead of the curve."
            typed_text = ""
            for char in full_response:
                typed_text += char
                message_placeholder.markdown(typed_text + "▌")
                time.sleep(0.01)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- 5. THE LIVE DATA PIPELINE (Now fetching TOP 12 items + Links) 🚀 ---
@st.cache_data(ttl=600)
def fetch_live_telemetry(query, hl, gl):
    try:
        safe_query = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={safe_query}&hl={hl}&gl={gl}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        facts = []
        for item in root.findall('.//item')[:12]: # Fetching top 12 now!
            title = item.find('title').text
            link = item.find('link').text
            clean_title = title.rsplit(' - ', 1)[0] if ' - ' in title else title
            facts.append({"title": clean_title, "link": link})
        return facts
    except Exception as e:
        return [{"title": "Node scan failed.", "link": "#"}, {"title": "Re-routing connection...", "link": "#"}]

eco_facts = fetch_live_telemetry(cfg["q_eco"], cfg["hl"], cfg["gl"])
tech_facts = fetch_live_telemetry(cfg["q_tech"], cfg["hl"], cfg["gl"])
edu_facts = fetch_live_telemetry(cfg["q_edu"], cfg["hl"], cfg["gl"])

# Helper function to generate Clickable HTML Cards
def create_card_html(facts, agent_name, tag_class, border_color, directive):
    if not facts: return ""
    
    # Top 2 headlines
    top_html = "".join([f"<li><a href='{f['link']}' target='_blank' class='headline-link'>{f['title']}</a></li>" for f in facts[:2]])
    
    # Remaining 10 headlines for the dropdown archive
    archive_html = "".join([f"<li><a href='{f['link']}' target='_blank' class='headline-link'>{f['title']}</a></li>" for f in facts[2:]])
    
    archive_section = f"""
        <details class="archive-details">
            <summary class="archive-summary">[+] DECRYPT FULL ARCHIVE ({len(facts[2:])} MORE)</summary>
            <ul class="fact-list archive-list">
                {archive_html}
            </ul>
        </details>
    """ if archive_html else ""

    return f"""
    <div class="feed-card" style="border-top: 1px solid {border_color};">
        <span class="tag {tag_class}">{agent_name}</span>
        <div class="card-title">Live Telemetry Feed</div>
        <div class="card-desc">
            <ul class="fact-list">
                {top_html}
            </ul>
            {archive_section}
        </div>
        <div class="status-text" style="color:{border_color};">>> DIRECTIVE: {directive}</div>
    </div>
    """

# --- 6. MAIN DASHBOARD ---
st.markdown("<h1>APEX <span class='neon-text'>NEXUS-1</span></h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown("<div class='metric-box'><div class='metric-title'>Live Nodes Active</div><div class='metric-value'>5,124</div></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-box'><div class='metric-title'>System Mode</div><div class='metric-value'>LIVE SYNC</div></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-box'><div class='metric-title'>Bias Filter</div><div style='color:#00ff9d;' class='metric-value'>100% PURE</div></div>", unsafe_allow_html=True)
with m4: st.markdown(f"<div class='metric-box'><div class='metric-title'>Language</div><div class='metric-value'>{selected_lang[:2].upper()}</div></div>", unsafe_allow_html=True)

# --- 7. SPLIT LAYOUT (Globe + Live Feed) ---
col_globe, col_feed = st.columns([1.5, 1])

with col_globe:
    df = pd.DataFrame([
        {"name": "INDIA", "lat": 28.6139, "lon": 77.2090, "color": "#00e5ff", "size": 12}, 
        {"name": "USA", "lat": 38.9072, "lon": -77.0369, "color": "#ff3333", "size": 12},
        {"name": "UK", "lat": 51.5072, "lon": -0.1276, "color": "#ffc400", "size": 12},
        {"name": "CHINA", "lat": 39.9042, "lon": 116.4074, "color": "#00ff9d", "size": 12}
    ])
    fig = go.Figure(data=go.Scattergeo(
        lon = df['lon'], lat = df['lat'], text = df['name'], mode = 'markers+text',
        textposition="top center", textfont=dict(family="Arial Black", size=12, color="white"),
        marker = dict(size = df['size'], color = df['color'], line_color='white', line_width=1, opacity=1)
    ))
    fig.update_layout(
        geo = dict(
            projection_type = 'orthographic', showland = True, landcolor = "#1e293b",     
            showocean = True, oceancolor = "#064273", showcountries=True, countrycolor="rgba(255,255,255,0.2)",
            bgcolor="rgba(0,0,0,0)"
        ), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0), height=600 
    )
    st.plotly_chart(fig, use_container_width=True)

with col_feed:
    st.markdown(f"<h4 style='color: #8892b0; font-size:1rem; margin-bottom: 15px; letter-spacing: 1px;'>{cfg['ui_title']}</h4>", unsafe_allow_html=True)
    
    # Injecting the dynamic HTML cards for all 3 agents
    st.markdown(create_card_html(eco_facts, cfg['ui_eco'], "tag-eco", "#00ff9d", "EVALUATE CAPITAL MOVEMENT."), unsafe_allow_html=True)
    st.markdown(create_card_html(tech_facts, cfg['ui_tech'], "tag-tech", "#00e5ff", "IDENTIFY TOOLS TO UPGRADE ARSENAL."), unsafe_allow_html=True)
    st.markdown(create_card_html(edu_facts, cfg['ui_edu'], "tag-edu", "#ffc400", "ALIGN LEARNING WITH DEMAND."), unsafe_allow_html=True)
