import streamlit as st
import random

# --- INITIALISIERUNG DES KOMPLEXEN STATES ---
if 'sim' not in st.session_state:
    st.session_state.sim = {
        'day': 1,
        'ap': 3,  # Aktionspunkte pro Tag
        'budget': 500000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'rep': 100,
        'infrastructure': [],
        'active_incident': None,
        'logs': ["> System-Boot abgeschlossen. CISO-Login erfolgreich."],
        'is_game_over': False,
        'events_resolved': 0
    }

def add_log(msg, type="info"):
    icon = "ℹ️" if type == "info" else "⚠️" if type == "warn" else "🚨"
    st.session_state.sim['logs'].insert(0, f"{icon} [TAG {st.session_state.sim['day']}] {msg}")

# --- FACHWISSEN-POOL (PDF REFERENZEN) ---
DOCS = {
    "BSI": "Systematik: 10 Schichten, 47 elementare Gefährdungen (Dok. 16).",
    "GOBD": "Integrität der Buchführung ist Pflicht (Dok. 13).",
    "DSGVO": "Art. 83: Bis zu 4% Jahresumsatz Strafe (Dok. 15).",
    "AI_ACT": "Social Scoring ist 'Unannehmbar' = Verboten (Dok. 15).",
    "MAX_PRINZIP": "Höchster Schutzbedarf einer Komponente gilt für alles (Dok. 12)."
}

# --- UI SETTINGS ---
st.set_page_config(page_title="CISO Sandbox 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; }
    .stat-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; border-top: 4px solid #58a6ff; }
    .log-terminal { background: #010409; border: 1px solid #238636; color: #39ff14; padding: 15px; height: 300px; overflow-y: auto; font-size: 0.85em; }
    .action-btn { margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME OVER CHECK ---
if st.session_state.sim['cia']['C'] <= 0 or st.session_state.sim['budget'] <= 0:
    st.error("🚨 UNTERNEHMENSKOLLAPS: Du wurdest gefeuert oder die Firma ist insolvent.")
    if st.button("Simulation Neustarten"):
        del st.session_state['sim']
        st.rerun()
    st.stop()

# --- DASHBOARD ---
st.title("🛡️ CISO Strategy Command: Silver-Data GmbH")
c1, c2, c3, c4, c5 = st.columns(5)
c1.markdown(f"<div class='stat-card'>💰 BUDGET<br><b>{st.session_state.sim['budget']:,}€</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'>⚡ AKTIONSPUNKTE<br><b>{st.session_state.sim['ap']} / 3</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'>🗓️ TAG<br><b>{st.session_state.sim['day']}</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-card'>📈 REPUTATION<br><b>{st.session_state.sim['rep']}%</b></div>", unsafe_allow_html=True)
c5.markdown(f"<div class='stat-card'>🔒 CIA<br>{st.session_state.sim['cia']['C']}|{st.session_state.sim['cia']['I']}|{st.session_state.sim['cia']['A']}</div>", unsafe_allow_html=True)

st.divider()

col_act, col_log = st.columns([2, 1])

# --- SPIELMECHANIK ---
with col_act:
    tab1, tab2, tab3 = st.tabs(["🏗️ Strategie (Plan/Do)", "🔎 Analyse (Check)", "⚖️ Compliance & Recht"])
    
    # AKTIONEN: STRATEGIE
    with tab1:
        st.write("### BSI-Grundschutz Bausteine implementieren")
        investments = {
            "BSI-Schicht 1-3: Infrastruktur absichern": (60000, "A", 20, "Brandschutz & Zutritt (Dok. 16)"),
            "ISMS.1: Management-Prozesse (PDCA)": (80000, "I", 25, "Sichert GoBD-Konformität (Dok. 13)"),
            "ORP.1: Awareness & Mitwirkung": (30000, "C", 15, "Schutz gegen Phishing (Dok. 16)")
        }
        for name, (cost, stat, boost, desc) in investments.items():
            if st.button(f"{name} ({cost}€) - 1 AP", help=desc):
                if st.session_state.sim['ap'] > 0 and st.session_state.sim['budget'] >= cost:
                    st.session_state.sim['ap'] -= 1
                    st.session_state.sim['budget'] -= cost
                    st.session_state.sim['cia'][stat] = min(100, st.session_state.sim['cia'][stat] + boost)
                    add_log(f"Investition getätigt: {name}")
                    st.rerun()
                else: st.warning("Nicht genug AP oder Budget!")

    # AKTIONEN: ANALYSE
    with tab2:
        st.write("### Sicherheits-Monitoring")
        if st.button("Logs auf Anomalien scannen - 1 AP"):
            if st.session_state.sim['ap'] > 0:
                st.session_state.sim['ap'] -= 1
                # Zufälliger Incident basierend auf PDFs
                inc_type = random.choice(["SQL", "PHISH", "NONE"])
                if inc_type == "SQL":
                    st.session_state.sim['active_incident'] = "SQL_INJECTION"
                    add_log("KRITISCH: SQL-Injection in Preislisten-DB gefunden!", "error")
                elif inc_type == "PHISH":
                    st.session_state.sim['active_incident'] = "PHISHING"
                    add_log("WARNUNG: Barclays-Phishing Mails detektiert.", "warn")
                else:
                    add_log("Keine akuten Bedrohungen gefunden.")
                st.rerun()
        
        # Incident lösen
        if st.session_state.sim['active_incident']:
            st.error(f"AKTIVER INCIDENT: {st.session_state.sim['active_incident']}")
            if st.button("Incident mit Notfallplan lösen - 1 AP"):
                st.session_state.sim['ap'] -= 1
                st.session_state.sim['active_incident'] = None
                st.session_state.sim['events_resolved'] += 1
                add_log("Incident erfolgreich isoliert.")
                st.rerun()

    # AKTIONEN: COMPLIANCE
    with tab3:
        st.write("### Rechtliche Prüfungen")
        if st.button("EU AI Act Check: Social Scoring Projekt - 1 AP"):
            if st.session_state.sim['ap'] > 0:
                st.session_state.sim['ap'] -= 1
                ans = st.selectbox("Welche Risikoklasse hat Social Scoring?", ["Hoch", "Unannehmbar", "Minimal"], key="ai_q")
                if st.button("Prüfung bestätigen"):
                    if ans == "Unannehmbar":
                        st.success("Korrekt! Projekt gestoppt. Bußgeld verhindert.")
                        add_log("KI-Projekt nach AI Act gestoppt.")
                    else:
                        st.session_state.sim['budget'] -= 200000
                        add_log("DSGVO/AI-Act Bußgeld: 200.000€ Strafe!", "error")
                    st.rerun()

# --- SIDEBAR: LOGS & WISSEN ---
with col_log:
    st.subheader("📟 System-Terminal")
    log_text = "\n".join(st.session_state.sim['logs'])
    st.markdown(f"<div class='log-terminal'>{log_text}</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("📚 Aktives Wissen")
    st.info(f"**BSI-Fakt:** {DOCS['BSI']}")
    st.info(f"**Recht:** {DOCS['DSGVO']}")
    
    if st.button("🌞 NÄCHSTEN TAG STARTEN"):
        st.session_state.sim['day'] += 1
        st.session_state.sim['ap'] = 3
        # Täglicher Werte-Verfall (Entropie)
        st.session_state.sim['cia']['C'] -= random.randint(2, 8)
        st.session_state.sim['cia']['I'] -= random.randint(2, 8)
        add_log("Neuer Tag. System-Entropie hat Schutzziele leicht geschwächt.")
        st.rerun()

# --- GRAFIKEN ---
