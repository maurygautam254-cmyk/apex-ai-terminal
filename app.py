import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
import sqlite3 
import json
import google.generativeai as genai

# --- GEMINI API CONFIGURATION (दिमाग की चाबी) ---
# 🚨 ध्यान दें: नीचे वाले "YOUR_GEMINI_API_KEY" को हटाकर अपनी असली API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])")

# --- 1. SYSTEM INITIALIZATION ---
st.set_page_config(page_title="APEX AI", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

if "selected_news" not in st.session_state:
    st.session_state.selected_news = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "⚡ APEX ORACLE ONLINE. \n\nI operate strictly on POSITIVE ECONOMICS. Ask me to decode any macro trend."}
    ]

# --- 2. DATABASE ENGINE (मेमोरी) ---
def init_db():
    conn = sqlite3.connect('apex_core.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS global_data 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, agent_type TEXT, title TEXT, link TEXT UNIQUE, date_str TEXT, 
                 description TEXT, analysis_json TEXT, added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    try:
        c.execute("ALTER TABLE global_data ADD COLUMN description TEXT")
        c.execute("ALTER TABLE global_data ADD COLUMN analysis_json TEXT")
    except:
        pass 
    conn.commit()
    return conn
conn = init_db()

# --- 3. HARDCORE TERMINAL CSS (डिज़ाइन) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, rgba(2, 6, 23, 0.95) 0%, rgba(2, 6, 23, 0.8) 100%), url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2564&auto=format&fit=crop') no-repeat center center fixed; background-size: cover; font-family: 'Inter', sans-serif; }
    header { background-color: transparent !important; }
    .stAppDeployButton, [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stSidebar"] { background-color: rgba(10, 15, 30, 0.95) !important; border-right: 1px solid rgba(0, 229, 255, 0.3); }
    h1 { font-weight: 900; font-size: 2.8rem; letter-spacing: -1px; margin-bottom: 0; color: #ffffff; margin-top: -30px;}
    .neon-text { color: #00e5ff; text-shadow: 0 0 10px rgba(0, 0, 0, 0.8); }
    .feed-list-box { background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; height: 600px; overflow-y: auto;}
    .feed-list-box::-webkit-scrollbar { width: 4px; }
    .feed-list-box::-webkit-scrollbar-thumb { background: #00e5ff; border-radius: 4px; }
    .news-item { background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); padding: 15px; border-radius: 6px; margin-bottom: 12px; transition: 0.2s;}
    .news-item:hover { border-color: rgba(0, 229, 255, 0.4); background: rgba(0, 229, 255, 0.05);}
    .news-date { font-family: 'Courier New', monospace; font-size: 0.75rem; color: #00ff9d; font-weight: bold; margin-bottom: 5px;}
    .news-title { font-size: 0.95rem; color: #f8fafc; font-weight: 600; line-height: 1.4; margin-bottom: 10px;}
    .explainer-window { background: rgba(10, 15, 30, 0.9); backdrop-filter: blur(20px); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 8px; padding: 25px; height: 600px; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border-top: 4px solid #00e5ff;}
    .explainer-window::-webkit-scrollbar { width: 4px; }
    .explainer-window::-webkit-scrollbar-thumb { background: #00e5ff; border-radius: 4px; }
    .exp-title { font-size: 1.3rem; font-weight: 800; color: #ffffff; margin-bottom: 15px; line-height: 1.4;}
    .section-title { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; font-weight: 800; letter-spacing: 1px; margin-top: 20px; margin-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;}
    .section-content { font-size: 0.95rem; color: #cbd5e1; line-height: 1.6;}
    .action-box { background: rgba(0, 255, 157, 0.08); border: 1px solid rgba(0, 255, 157, 0.4); border-radius: 6px; padding: 15px; margin-top: 25px; }
    .action-title { font-size: 0.85rem; color: #00ff9d; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;}
    .stButton>button { background-color: rgba(0, 229, 255, 0.1); border: 1px solid #00e5ff; color: #00e5ff; font-weight: bold; border-radius: 4px; padding: 2px 15px; font-size: 0.75rem; transition: 0.3s;}
    .stButton>button:hover { background-color: #00e5ff; color: #020617; box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);}
    </style>
""", unsafe_allow_html=True)

# --- 4. DATA FETCHING PIPELINE ---
@st.cache_data(ttl=600)
def fetch_all_macro_data():
    try:
        url = "https://news.google.com/rss/search?q=Global+Economy+OR+Market+Crash+OR+Tech+Stocks&hl=en-US&gl=US"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        root = ET.fromstring(urllib.request.urlopen(req).read())
        c = conn.cursor()
        for item in root.findall('.//item')[:25]: 
            title = item.find('title').text
            link = item.find('link').text
            desc_elem = item.find('description')
            description = desc_elem.text if desc_elem is not None else ""
            try: dt = parsedate_to_datetime(item.find('pubDate').text); date_str = dt.strftime("%d %b, %H:%M")
            except: date_str = "LIVE"
            clean_title = title.rsplit(' - ', 1)[0] if ' - ' in title else title
            
            c.execute("INSERT OR IGNORE INTO global_data (agent_type, title, link, date_str, description) VALUES (?, ?, ?, ?, ?)", 
                      ("MACRO", clean_title, link, date_str, description))
        conn.commit()
    except: pass
    
    c = conn.cursor()
    c.execute("SELECT title, link, date_str, description, analysis_json FROM global_data WHERE agent_type='MACRO' ORDER BY added_on DESC LIMIT 25")
    return [{"title": r[0], "link": r[1], "date": r[2], "description": r[3], "analysis_json": r[4]} for r in c.fetchall()]

all_macro_data = fetch_all_macro_data()

def set_selected_news(news_data):
    st.session_state.selected_news = news_data

# --- 5. AI GENERATION PIPELINE ---
def generate_analysis(title, description):
    if not title and not description: return None
    prompt = f"""
    Analyze the following financial news article. Title: {title} Context: {description}
    STRICT RULES:
    1. Output ONLY a raw, valid JSON object with EXACTLY these 4 keys: "what_happened", "why_it_matters", "who_should_care", "action".
    2. Do NOT invent facts. 
    3. Keep each value to a maximum of 2-3 concise sentences.
    4. Do not include markdown formatting like ```json in the output.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        raw_output = response.text.strip()
        if raw_output.startswith('```json'): raw_output = raw_output[7:-3].strip()
        elif raw_output.startswith('```'): raw_output = raw_output[3:-3].strip()
            
        parsed_json = json.loads(raw_output)
        expected_keys = ["what_happened", "why_it_matters", "who_should_care", "action"]
        for key in expected_keys:
            if key not in parsed_json: parsed_json[key] = "Insufficient data in source"
        return parsed_json
    except: return None

# --- 6. MAIN DASHBOARD UI ---
st.markdown("<h1>APEX <span class='neon-text'>AI</span></h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #8892b0; font-size:0.9rem; margin-top: 10px; margin-bottom: -20px; text-transform: uppercase;'>🌍 Global Macro Radar</h4>", unsafe_allow_html=True)

df = pd.DataFrame([{"name": "INDIA", "lat": 28.6139, "lon": 77.2090, "color": "#00e5ff", "size": 10}, {"name": "USA", "lat": 38.9072, "lon": -77.0369, "color": "#ff3333", "size": 10}])
fig = go.Figure(data=go.Scattergeo(lon=df['lon'], lat=df['lat'], text=df['name'], mode='markers+text', textposition="top center", textfont=dict(family="Arial Black", size=10, color="white"), marker=dict(size=df['size'], color=df['color'], line_color='white', line_width=1, opacity=1)))
fig.update_layout(geo=dict(projection_type='orthographic', showland=True, landcolor="#0f172a", showocean=True, oceancolor="#020617", showcountries=True, countrycolor="rgba(255,255,255,0.1)", bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=20, b=20), height=300)
st.plotly_chart(fig, use_container_width=True)
st.markdown("<hr style='border-color: rgba(0, 229, 255, 0.2); margin-top: -20px; margin-bottom: 20px;'>", unsafe_allow_html=True)

col_feed, col_explainer = st.columns([1.2, 1.5])

# LEFT COLUMN: THE FEED LIST
with col_feed:
    st.markdown("<h4 style='color: #00e5ff; font-size:1rem; margin-bottom: 15px; letter-spacing: 1px;'>📡 LIVE TELEMETRY LOGS</h4>", unsafe_allow_html=True)
    st.markdown("<div class='feed-list-box'>", unsafe_allow_html=True)
    if not all_macro_data: st.write("Scanning nodes...")
    else:
        for idx, row in enumerate(all_macro_data):
            st.markdown(f"<div class='news-item'><div class='news-date'>[{row['date']}]</div><div class='news-title'>{row['title']}</div></div>", unsafe_allow_html=True)
            st.button("DECODE THREAT", key=f"btn_{idx}", on_click=set_selected_news, args=(row,))
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN: THE AI EXPLAINER WINDOW
with col_explainer:
    st.markdown("<h4 style='color: #00ff9d; font-size:1rem; margin-bottom: 15px; letter-spacing: 1px;'>🧠 FORENSIC DECODE (EXECUTIVE BRIEF)</h4>", unsafe_allow_html=True)
    if st.session_state.selected_news:
        news = st.session_state.selected_news
        # AI & CACHING LOGIC
        if not news.get('analysis_json'):
            with st.spinner("Decoding telemetry using Gemini AI..."):
                analysis_data = generate_analysis(news['title'], news['description'])
                if analysis_data:
                    news['analysis_json'] = json.dumps(analysis_data)
                    c = conn.cursor()
                    c.execute("UPDATE global_data SET analysis_json = ? WHERE link = ?", (news['analysis_json'], news['link']))
                    conn.commit()
                else: analysis_data = None 
        else:
            try: analysis_data = json.loads(news['analysis_json'])
            except: analysis_data = None

        if analysis_data:
            st.markdown(f"""
            <div class='explainer-window'>
                <div class='exp-title'>{news['title']}</div>
                <div class='section-title'>What Happened</div><div class='section-content'>{analysis_data['what_happened']}</div>
                <div class='section-title'>Why It Matters</div><div class='section-content'>{analysis_data['why_it_matters']}</div>
                <div class='section-title'>Who Should Care</div><div class='section-content'>{analysis_data['who_should_care']}</div>
                <div class='action-box'>
                    <div class='action-title'>>> Actionable Directive</div>
                    <div style='font-size: 0.95rem; color: #ffffff; font-weight: 500;'>
                        {analysis_data['action']} <br><br>
                        <a href='{news['link']}' target='_blank' style='color:#00e5ff; font-weight:bold; text-decoration:none;'>[🔗 VERIFY RAW SOURCE DATA]</a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='explainer-window'><div class='exp-title'>{news['title']}</div><div style='color: #ff3333; margin-top: 30px; font-weight: bold;'>Analysis unavailable — try again later</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='explainer-window' style='display: flex; align-items: center; justify-content: center; text-align: center;'><div><h3 style='color: #94a3b8; font-weight: 600;'>AWAITING SIGNAL DECODE</h3><p style='color: #64748b;'>Select a telemetry log from the left feed to generate an AI executive briefing.</p></div></div>", unsafe_allow_html=True)

with st.sidebar:
    pass
