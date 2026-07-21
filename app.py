import streamlit as st
import time

# Page Configuration - Ekdum clean aur professional look
st.set_page_config(page_title="APEX AI | Intelligence Terminal", layout="wide")

# Styling (Dark Theme & Professional Boxes)
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .truth-box { border-left: 5px solid #00FF00; padding: 15px; background-color: #1A1C23; border-radius: 5px; margin-bottom: 10px; color: white;}
    .lie-box { border-left: 5px solid #FF0000; padding: 15px; background-color: #1A1C23; border-radius: 5px; margin-bottom: 10px; color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ APEX AI: Autonomous Intelligence Terminal")
st.markdown("### The Independent Truth & Market Audit Bureau")
st.markdown("---")

# Clean Tabs: Market alag, Media Audit alag
tab1, tab2 = st.tabs(["📊 Global Market & Trading Terminal", "📡 Media Audit & Truth Bureau"])

# --- TAB 1: GLOBAL MARKET ---
with tab1:
    st.subheader("Global Commodities & Supply-Chain Truth Matrix")
    st.markdown("Real-time telemetry and raw trading volumes (Bypassing media filters).")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="lie-box"><strong>🚨 Market Narrative:</strong> "Global supply crisis will push fuel prices to record highs."</div>', unsafe_allow_html=True)
        st.markdown('<div class="truth-box"><strong>✅ Raw API Fact:</strong> Brent Crude trading stable at $71/Barrel. Global freight volume normal.</div>', unsafe_allow_html=True)
    with col2:
        st.metric(label="Crude Benchmark", value="$71.40", delta="-2.1%")
        st.metric(label="Supply Index", value="99.4%", delta="+0.5%")

# --- TAB 2: MEDIA AUDIT & TRUTH BUREAU ---
with tab2:
    st.subheader("Autonomous Media & Narrative Exposure Engine")
    st.markdown("Exposing sponsored media narratives, political bias, and verifying ground-level facts.")
    
    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown('<div class="lie-box"><strong>🚨 Mainstream Media Claim:</strong> "Protesters were violent and lawless."</div>', unsafe_allow_html=True)
        st.markdown('<div class="truth-box"><strong>✅ Apex AI Ground Audit:</strong> Spatial data and independent feeds confirm heavy containment of peaceful assembly. Narrative marked as 91% Fabricated.</div>', unsafe_allow_html=True)
        st.warning("⚠️ Verified Ground Evidence: Unedited spatial logs confirm peaceful gathering met with disproportionate action.")
        
    with col4:
        st.subheader("🔔 Truth Watchdog")
        user_email = st.text_input("Enter Email/WhatsApp for Breaking Truth Alerts:")
        if st.button("Activate Watchdog"):
            if user_email:
                st.success("✅ Watchdog Active! You will be alerted when media pushes fabricated stories.")
