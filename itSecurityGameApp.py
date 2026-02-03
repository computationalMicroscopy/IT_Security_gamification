import streamlit as st
import random
import pandas as pd

# --- INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'day': 1,
        'budget': 350000,
        'rep': 100,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'unlocked_bausteine': set(),
        'solved_incidents': 0,
        'logs': ["> SYSTEM INITIALIZED. Willkommen CISO."],
        'threat_detected': None,
        'is_game_over': False
    }

def add_log(msg, type="info"):
    colors = {"info": "#58a6ff", "warn": "#f2cc60", "error": "#f85149"}
    st.session_state.game['logs'].insert(0, f"<span style='color:{colors[type]}'>[TAG {st.session_state.game['day']}] {msg}</span>")

# --- UI SETTINGS ---
st.set_page_config(page_title="CISO Sandbox: Silver-Data", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .stat-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .terminal { background: #010409; border: 1px solid #30363d; padding: 15px; height: 300px; overflow-y: auto; font-family: 'Courier New'; }
    .incident-box { background: #21262d; border-left: 5px solid #f85149; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME LOGIC ---
if st.session_state.game['is_game_over']:
    st.error("🚨 UNTERNEHMEN INSOLVENT ODER ZERTIFIKAT ENTZOGEN")
    st.write(f"Du hast {st.session_state.game['day']} Tage durchgehalten.")
    if st.button("Simulation Neustarten"):
        del st.session_state['game']
        st.rerun()
    st.stop()

# --- HEADER / DASHBOARD ---
st.title("🛡️ CISO Sandbox: Operation Silver-Data")
cols = st.columns(4)
cols[0].markdown(f"<div class='stat-card'>💰 BUDGET<br><b>{st.session_state.game['budget']:,} €</b></div>", unsafe_allow_html=True)
cols[1].markdown(f"<div class='stat-card'>🗓️ TAG<br><b>{st.session_state.game['day']}</b></div>", unsafe_allow_html=True)
cols[2].markdown(f"<div class='stat-card'>🛡️ REPUTATION<br><b>{st.session_state.game['rep']}%</b></div>", unsafe_allow_html=True)
cols[3].markdown(f"<div class='stat-card'>🔒 CIA LEVEL<br>C:{st.session_state.game['cia']['C']}% I:{st.session_state.game['cia']['I']}% A:{st.session_state.game['cia']['A']}%</div>", unsafe_allow_html=True)

st.divider()

left, mid, right = st.columns([1.5, 1.5, 1])

# --- SPALTE 1: STRATEGIE & INVESTITION (PLAN/DO) ---
with left:
    st.subheader("📋 BSI Baustein-Katalog")
    st.write("Investiere in die 10 Schichten des Grundschutzes.")
    
    bausteine = {
        "ISMS.1 (Org)": {"cost": 40000, "cia": "I", "info": "Sichert GoBD-Konformität & Integrität."},
        "ORP.1 (Mensch)": {"cost": 25000, "cia": "C", "info": "Awareness gegen Phishing (Barclays-Mail)."},
        "CON.1 (Krypt)": {"cost": 35000, "cia": "C", "info": "Verschlüsselung nach DSGVO Standard."},
        "OPS.1 (Betrieb)": {"cost": 45000, "cia": "A", "info": "Verfügbarkeit durch Backup-Konzepte."}
    }
    
    for name, data in bausteine.items():
        col1, col2 = st.columns([2, 1])
        col1.write(f"**{name}**\n*{data['info']}*")
        if name in st.session_state.game['unlocked_bausteine']:
            col2.button("Aktiviert", key=name, disabled=True)
        else:
            if col2.button(f"{data['cost']}€", key=name):
                if st.session_state.game['budget'] >= data['cost']:
                    st.session_state.game['budget'] -= data['cost']
                    st.session_state.game['unlocked_bausteine'].add(name)
                    st.session_state.game['cia'][data['cia']] = min(100, st.session_state.game['cia'][data['cia']] + 15)
                    add_log(f"Baustein {name} implementiert.", "info")
                    st.rerun()

# --- SPALTE 2: OPERATIONEN & ANALYSE (CHECK/ACT) ---
with mid:
    st.subheader("🕵️ Operations-Center")
    
    # Der tägliche Incident
    if not st.session_state.game['threat_detected']:
        if st.button("🔎 System-Audit durchführen (Check)"):
            # Generiere Bedrohung aus den Inhalten
            threats = [
                {"t": "SQL-Injection", "desc": "Ungewöhnliche DB-Queries auf Preislisten detektiert.", "cia": "I", "doc": "Dok. 12"},
                {"t": "Phishing-Welle", "desc": "Mails mit Barclays-Logo im Umlauf.", "cia": "C", "doc": "Dok. 16"},
                {"t": "AI-Risiko", "desc": "Marketing plant Social-Scoring System.", "cia": "C", "doc": "Dok. 15"}
            ]
            st.session_state.game['threat_detected'] = random.choice(threats)
            st.rerun()
    else:
        threat = st.session_state.game['threat_detected']
        st.markdown(f"""<div class='incident-box'>
            <b>🚨 ALARM: {threat['t']}</b><br>{threat['desc']}<br>Quelle: {threat['doc']}</div>""", unsafe_allow_html=True)
        
        # Abfrage Fachwissen
        if threat['t'] == "AI-Risiko":
            ans = st.radio("In welche EU AI Act Klasse fällt Social Scoring?", ["Hoch", "Unannehmbar", "Minimal"], index=None)
            if st.button("Entscheidung treffen"):
                if ans == "Unannehmbar":
                    add_log("KI-Projekt gestoppt. Bußgeld verhindert!", "info")
                    st.session_state.game['threat_detected'] = None
                    st.session_state.game['day'] += 1
                else:
                    st.session_state.game['budget'] -= 100000
                    st.session_state.game['rep'] -= 30
                    add_log("Verbotene KI genutzt! DSGVO Bußgeld (4% Umsatz) fällig.", "error")
                    st.session_state.game['threat_detected'] = None
                    st.session_state.game['day'] += 1
                st.rerun()
        
        elif threat['t'] == "SQL-Injection":
            ans = st.radio("Wie viele elementare Gefährdungen listet das BSI?", ["40", "47", "52"], index=None)
            if st.button("Reaktion einleiten"):
                if ans == "47":
                    add_log("Integrität der Preislisten gesichert.", "info")
                    st.session_state.game['threat_detected'] = None
                    st.session_state.game['day'] += 1
                else:
                    st.session_state.game['cia']['I'] -= 40
                    add_log("Falsche Analyse! Preise wurden auf 0,00€ gesetzt.", "error")
                    st.session_state.game['threat_detected'] = None
                    st.session_state.game['day'] += 1
                st.rerun()
        
        elif threat['t'] == "Phishing-Welle":
            if st.button("Awareness-Kampagne (Mitarbeiter-Mitwirkung)"):
                add_log("Mitarbeiter haben den Betrug erkannt.", "info")
                st.session_state.game['threat_detected'] = None
                st.session_state.game['day'] += 1
                st.rerun()

# --- SPALTE 3: MONITORING & LOGS ---
with right:
    st.subheader("📟 Logs")
    log_html = "".join(st.session_state.game['logs'])
    st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)
    
    st.write("---")
    # Schutzziel Visualisierung
    
    
    if st.button("⏭️ Nächster Tag (Warten)"):
        st.session_state.game['day'] += 1
        st.session_state.game['budget'] += 5000 # Täglicher Cashflow
        if st.session_state.game['threat_detected']:
            t = st.session_state.game['threat_detected']
            st.session_state.game['cia'][t['cia']] -= 25
            add_log(f"Schaden durch Ignorieren von {t['t']}!", "error")
            st.session_state.game['threat_detected'] = None
        st.rerun()

# --- GAME OVER CHECK ---
if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
    st.session_state.game['is_game_over'] = True
    st.rerun()
