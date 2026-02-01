import streamlit as st
import random
import time

# --- SETUP & STYLES ---
st.set_page_config(page_title="CORE: Silver-Data", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #58a6ff; font-family: 'Courier New', monospace; }
    .stButton>button { border: 1px solid #238636; background-color: #21262d; color: #238636; width: 100%; font-weight: bold; }
    .stButton>button:hover { background-color: #238636; color: white; border: 1px solid #238636; }
    .terminal-output { background-color: #010409; padding: 15px; border-radius: 5px; border: 1px solid #30363d; color: #d1d5da; font-size: 0.85em; height: 300px; overflow-y: scroll; }
    .metric-card { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'phase': 'init',
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'day': 1,
        'logs': ["> SYSTEM INITIALIZED", "> WAITING FOR SECTOR ANALYSIS..."],
        'unlocked_toms': [],
        'threats_found': 0,
        'compliance_risk': 0
    }

def add_log(msg):
    st.session_state.game['logs'].insert(0, f"> {time.strftime('%H:%M:%S')} | {msg}")

# --- GAME PHASES ---

# --- PHASE 0: INITIAL ANALYSIS (BSI MAXIMUMSPRINZIP) ---
if st.session_state.game['phase'] == 'init':
    st.title("💎 OPERATION: SILVER-DATA")
    st.info("Szenario: Ein E-Commerce-Händler für Silberschmuck. Preislisten wurden manipuliert, Kundendaten sind instabil.")
    
    st.subheader("Analyse des Schutzbedarfs (BSI Standard)")
    st.write("Wähle die Kategorien für das Hauptsystem (Shop + ERP):")
    
    col1, col2, col3 = st.columns(3)
    c = col1.selectbox("Vertraulichkeit (Kundendaten)", ["Normal", "Hoch", "Sehr Hoch"])
    i = col2.selectbox("Integrität (Preislisten)", ["Normal", "Hoch", "Sehr Hoch"])
    a = col3.selectbox("Verfügbarkeit (Webshop)", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("Analyse bestätigen"):
        # Das Maximumsprinzip anwenden
        levels = {"Normal": 1, "Hoch": 2, "Sehr Hoch": 3}
        max_level = max(levels[c], levels[i], levels[a])
        
        if max_level >= 2:
            st.session_state.game['phase'] = 'main'
            add_log(f"Schutzbedarf auf '{'HOCH' if max_level==2 else 'SEHR HOCH'}' gesetzt.")
            st.rerun()
        else:
            st.error("Warnung: Analyse zu niedrig! Bei Silberschmuck-Handel (IBANs/Goldpreise) ist der Bedarf mindestens 'Hoch'.")

# --- PHASE 1: MAIN OPERATION ---
elif st.session_state.game['phase'] == 'main':
    # Dashboard oben
    cols = st.columns(4)
    with cols[0]: st.markdown(f"<div class='metric-card'>💰 BUDGET<br><h3>{st.session_state.game['budget']:,} €</h3></div>", unsafe_allow_html=True)
    with cols[1]: st.markdown(f"<div class='metric-card'>🔒 CONFID.<br><h3>{st.session_state.game['cia']['C']}%</h3></div>", unsafe_allow_html=True)
    with cols[2]: st.markdown(f"<div class='metric-card'>🛠️ INTEGR.<br><h3>{st.session_state.game['cia']['I']}%</h3></div>", unsafe_allow_html=True)
    with cols[3]: st.markdown(f"<div class='metric-card'>⚡ AVAIL.<br><h3>{st.session_state.game['cia']['A']}%</h3></div>", unsafe_allow_html=True)

    st.divider()

    # Split Screen
    left, right = st.columns([2, 1])

    with left:
        st.subheader("🛡️ PDCA-Zyklus: Maßnahmen-Planung (Plan-Do)")
        
        # TOMs aus den PDFs (Abschnitt III)
        toms = {
            "BSI-Baustein 'Allgemeiner Client'": {"cost": 20000, "cia": "I", "desc": "Härtung der Mitarbeiter-PCs gegen Malware."},
            "DSGVO-Compliance Audit": {"cost": 15000, "cia": "C", "desc": "Senkt Bußgeld-Risiko (Art. 83)."},
            "DDoS-Protection Cluster": {"cost": 30000, "cia": "A", "desc": "Schützt die Shop-Verfügbarkeit."},
            "Intrusion Detection System (IDS)": {"cost": 25000, "cia": "I", "desc": "Erkennt Manipulationen an Preislisten sofort."},
            "Awareness Kampagne": {"cost": 10000, "cia": "C", "desc": "Mitarbeiter erkennen Phishing (Mitwirkungspflicht)."}
        }

        cols_tom = st.columns(2)
        for idx, (name, data) in enumerate(toms.items()):
            with cols_tom[idx % 2]:
                if st.button(f"{name} | {data['cost']}€"):
                    if st.session_state.game['budget'] >= data['cost'] and name not in st.session_state.game['unlocked_toms']:
                        st.session_state.game['budget'] -= data['cost']
                        st.session_state.game['unlocked_toms'].append(name)
                        st.session_state.game['cia'][data['cia']] = min(100, st.session_state.game['cia'][data['cia']] + 15)
                        add_log(f"TOM implementiert: {name}")
                        st.rerun()

    with right:
        st.subheader("📟 System-Monitor")
        log_html = f"<div class='terminal-output'>{'<br>'.join(st.session_state.game['logs'])}</div>"
        st.markdown(log_html, unsafe_allow_html=True)
        
        if st.button("➡️ TAG BEENDEN (Simulation)"):
            st.session_state.game['day'] += 1
            
            # ZUFÄLLIGE GEFÄHRDUNGEN (BSI-Grundschutz Kompendium)
            event = random.randint(1, 4)
            
            if event == 1: # PHISHING
                add_log("ALARM: Phishing-E-Mail 'Barclays Update' im Umlauf!")
                if "Awareness Kampagne" not in st.session_state.game['unlocked_toms']:
                    st.session_state.game['cia']['C'] -= 30
                    add_log("ERGEBNIS: Mitarbeiter gab Credentials preis. Datenabfluss.", "warn")
                else:
                    add_log("ERGEBNIS: Angriff durch Mitarbeiter-Meldung blockiert.")
            
            if event == 2: # MANIPULATION (Operation Silver-Data Kern)
                add_log("ALARM: Preislisten-Integrität wird angegriffen!")
                if "Intrusion Detection System (IDS)" not in st.session_state.game['unlocked_toms']:
                    st.session_state.game['cia']['I'] -= 25
                    add_log("ERGEBNIS: Preise im Shop auf 0.00€ geändert!", "warn")
                else:
                    add_log("ERGEBNIS: IDS hat Schreibzugriff blockiert.")

            if event == 3: # DSGVO CHECK
                add_log("AUDIT: Datenschutz-Aufsicht prüft Compliance...")
                if st.session_state.game['cia']['C'] < 70:
                    fine = st.session_state.game['budget'] * 0.10
                    st.session_state.game['budget'] -= fine
                    add_log(f"DSGVO-BUẞGELD: {fine:,.0f}€ fällig (Art. 83).", "warn")
                else:
                    add_log("AUDIT: Keine Beanstandungen.")

            # Win/Lose Check
            if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
                st.session_state.game['phase'] = 'game_over'
            st.rerun()

# --- PHASE 2: GAME OVER ---
elif st.session_state.game['phase'] == 'game_over':
    st.error("❌ MISSION GESCHEITERT: SYSTEM COLLAPSE")
    st.write(f"Überlebte Tage: {st.session_state.game['day']}")
    st.markdown("""
    **Debriefing:**
    - Dein Budget oder eines deiner Schutzziele ist auf 0 gefallen.
    - Gemäß BSI-Standard hast du das **Restrisiko** nicht ausreichend gemanagt.
    - Die **Operation Silver-Data** war erfolgreich – für die Hacker.
    """)
    if st.button("Neue Instanz laden"):
        del st.session_state['game']
        st.rerun()
