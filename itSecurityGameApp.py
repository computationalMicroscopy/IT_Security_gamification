import streamlit as st
import random

# --- 1. INITIALISIERUNG (Fix für den KeyError) ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'day': 1,
        'ap': 3,
        'budget': 500000,
        'cia': {'C': 70, 'I': 70, 'A': 70},
        'rep': 80,
        'logs': ["> System Initialized. Welcome, CISO."],
        'incident': None,
        'unlocked_intel': [],
        'game_over': False
    }

def add_log(msg):
    st.session_state.game['logs'].insert(0, f"> [Tag {st.session_state.game['day']}] {msg}")

# --- 2. INTEL-DATENBANK (Glossar aus deinen Dokumenten) ---
INTEL_DB = {
    "BSI-Systematik": "Besteht aus 10 Schichten (Infrastruktur bis Anwendungen) und 47 elementaren Gefährdungen.",
    "Maximumprinzip": "Das Schutzziel eines Systems entspricht dem höchsten Schutzbedarf seiner Komponenten (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Buchführung. Erfordert die Unveränderbarkeit (Integrität) von Belegen.",
    "DSGVO Art. 83": "Bußgelder bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes bei schweren Verstößen.",
    "EU AI Act": "KI-Klassifizierung: Unannehmbar (verboten), Hoch (reguliert), Transparenz (offenlegungspflichtig).",
    "Authentizität": "Sicherstellung der Echtheit eines Objekts. Teilziel der Integrität nach BSI-Definition.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Kontinuierlicher Prozess zur Verbesserung der Informationssicherheit."
}

# --- 3. UI DESIGN (Cyberpunk Style) ---
st.set_page_config(page_title="CISO Command 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #00ff41; font-family: 'Courier New', monospace; }
    .status-card { background: #161b22; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; text-align: center; color: white; }
    .terminal { background: #000; border: 1px solid #00ff41; color: #00ff41; padding: 15px; height: 250px; overflow-y: auto; font-size: 0.85em; }
    .stButton>button { border: 1px solid #00ff41; background: #0b0e14; color: #00ff41; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 10px #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SEITENLEISTE (Szenario & Glossar) ---
with st.sidebar:
    st.title("🛡️ MISSION: SILVER-DATA")
    st.info("""**Szenario:** Die Silver-Data GmbH handelt mit Edelmetallen. 
    Du hast 10 Tage Zeit, die IT-Sicherheit auf BSI-Standard zu heben, bevor das Bundesamt zur Prüfung kommt. 
    Verlierst du das Budget oder sinkt die Sicherheit (CIA) auf 0, ist die Firma am Ende.""")
    
    st.divider()
    st.subheader("📖 Intel-Datenbank")
    search = st.text_input("Begriff suchen...", help="Nutze die Begriffe aus deinen Unterlagen!")
    for key, val in INTEL_DB.items():
        if not search or search.lower() in key.lower():
            st.markdown(f"**{key}:**\n{val}")

# --- 5. DASHBOARD ---
if st.session_state.game['game_over']:
    st.error("🚨 GAME OVER - SYSTEM CRITICAL ERROR")
    if st.button("Simulation Neustarten"):
        del st.session_state['game']
        st.rerun()
    st.stop()

st.title("🖥️ CISO Command Center")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='status-card'>💰 BUDGET<br>{st.session_state.game['budget']:,} €</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='status-card'>⚡ AKTIONEN<br>{st.session_state.game['ap']} AP</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='status-card'>🛡️ REPUTATION<br>{st.session_state.game['rep']}%</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='status-card'>🗓️ TAG<br>{st.session_state.game['day']} / 10</div>", unsafe_allow_html=True)

st.divider()

# PROGRESS BARS FÜR CIA

cols = st.columns(3)
for i, (k, v) in enumerate(st.session_state.game['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 6. AKTIONEN ---
col_act, col_log = st.columns([2, 1])

with col_act:
    st.subheader("⚡ Verfügbare Operationen")
    t1, t2, t3 = st.tabs(["🏗️ Prävention (Plan/Do)", "🔎 Analyse (Check)", "⚖️ Compliance (Act)"])
    
    with t1:
        st.write("Investiere in die BSI-Schichten.")
        if st.button("Mitarbeiter-Schulung: Barclays-Phishing (40k € | 1 AP)"):
            if st.session_state.game['ap'] >= 1 and st.session_state.game['budget'] >= 40000:
                st.session_state.game['ap'] -= 1
                st.session_state.game['budget'] -= 40000
                st.session_state.game['cia']['C'] += 15
                add_log("Awareness-Training durchgeführt (Dok. 16).")
                st.rerun()
        
        if st.button("BSI-Infrastruktur Level 1-5 (120k € | 2 AP)"):
            if st.session_state.game['ap'] >= 2 and st.session_state.game['budget'] >= 120000:
                st.session_state.game['ap'] -= 2
                st.session_state.game['budget'] -= 120000
                st.session_state.game['cia']['A'] += 20
                st.session_state.game['cia']['I'] += 10
                add_log("Physische Sicherheit & Netze verstärkt.")
                st.rerun()

    with t2:
        st.write("Überprüfe die Integrität deiner Daten.")
        if st.button("Datenbank-Audit: GoBD Check (1 AP)"):
            if st.session_state.game['ap'] >= 1:
                st.session_state.game['ap'] -= 1
                if random.random() > 0.5:
                    st.session_state.game['incident'] = "SQL_INJECTION"
                    add_log("Anomalie gefunden: Unberechtigte Preisänderungen detektiert!")
                else:
                    add_log("GoBD-Audit ohne Befund abgeschlossen.")
                st.rerun()

    with t3:
        st.write("Rechtliche Absicherung.")
        if st.button("EU AI Act: KI-Projektprüfung (1 AP)"):
            if st.session_state.game['ap'] >= 1:
                st.session_state.game['ap'] -= 1
                st.info("Marketing will 'Social Scoring' einführen. In welche KI-Risikoklasse fällt das?")
                if st.button("A: Unannehmbar (Verboten)"):
                    st.success("Korrekt! Projekt gestoppt.")
                    st.session_state.game['rep'] += 10
                if st.button("B: Hohes Risiko"):
                    st.error("Falsch! Bußgeld droht (4% Budget).")
                    st.session_state.game['budget'] *= 0.96
                st.rerun()

    if st.session_state.game['incident'] == "SQL_INJECTION":
        st.error("🚨 INCIDENT: SQL-Injection manipuliert Preislisten!")
        if st.button("Gegenmaßnahme: Input-Validierung (1 AP)"):
            st.session_state.game['ap'] -= 1
            st.session_state.game['incident'] = None
            st.session_state.game['cia']['I'] = 100
            add_log("Integrität wiederhergestellt.")
            st.rerun()

with col_log:
    st.subheader("📟 System-Logs")
    log_html = "".join([f"<div>{l}</div>" for l in st.session_state.game['logs']])
    st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("⏭️ TAG BEENDEN"):
        st.session_state.game['day'] += 1
        st.session_state.game['ap'] = 3
        # Täglicher Werte-Verfall (Entropie)
        for k in st.session_state.game['cia']:
            st.session_state.game['cia'][k] -= random.randint(3, 10)
        add_log("Neuer Arbeitstag. System-Entropie steigt.")
        if st.session_state.game['day'] > 10:
            st.balloons()
            st.success("ZERTIFIKAT ERHALTEN!")
        st.rerun()

# --- 7. GAME OVER LOGIC ---
if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
    st.session_state.game['game_over'] = True
