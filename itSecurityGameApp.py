import streamlit as st
import random
import time

# --- INITIALISIERUNG DER ENGINE ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'phase': 'setup',
        'day': 1,
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'reputation': 100,
        'inventory': set(),
        'logs': ["> SYSTEM BOOT COMPLETE. WELCOME, CISO."],
        'threat_history': [],
        'unlocked_achievements': []
    }

def add_log(msg, level="info"):
    colors = {"info": "#58a6ff", "warn": "#d29922", "danger": "#f85149", "success": "#3fb950"}
    color = colors.get(level, "#58a6ff")
    st.session_state.game_state['logs'].insert(0, f"<span style='color:{color}'>[T-{st.session_state.game_state['day']}] {msg}</span>")

# --- UI LAYOUT ---
st.set_page_config(page_title="Cyber Defense: Operation Silver-Data", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .stat-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .log-container { background: #010409; border: 1px solid #30363d; padding: 15px; height: 450px; overflow-y: auto; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- SPIELPHASEN ---

# PHASE 1: STRATEGISCHES SETUP
if st.session_state.game_state['phase'] == 'setup':
    st.title("🕵️ Phase 1: Die Schutzbedarfsanalyse")
    st.info("Szenario: 'Operation Silver-Data'. Analysiere den E-Commerce Shop für Silberschmuck.")
    
    col1, col2, col3 = st.columns(3)
    c_val = col1.select_slider("Vertraulichkeit (Kundendaten)", ["Normal", "Hoch", "Sehr Hoch"])
    i_val = col2.select_slider("Integrität (Preislisten/Goldwert)", ["Normal", "Hoch", "Sehr Hoch"])
    a_val = col3.select_slider("Verfügbarkeit (Webshop-Uptime)", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("Analyse finalisieren"):
        # Logik basierend auf BSI Maximumsprinzip
        if c_val == "Sehr Hoch" and i_val == "Sehr Hoch":
            st.session_state.game_state['budget'] += 50000
            add_log("Maximumsprinzip korrekt angewendet. Risikobudget bewilligt.", "success")
        else:
            st.session_state.game_state['budget'] -= 20000
            add_log("Fehlanalyse! Die Revision hat das Budget gekürzt.", "danger")
        st.session_state.game_state['phase'] = 'main'
        st.rerun()

# PHASE 2: DAS OPERATIVE DASHBOARD
elif st.session_state.game_state['phase'] == 'main':
    # Dashboard Header
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(f"<div class='stat-card'>💰 BUDGET<br><h3>{st.session_state.game_state['budget']:,}€</h3></div>", unsafe_allow_html=True)
    m2.markdown(f"<div class='stat-card'>🔒 C<br><h3>{st.session_state.game_state['cia']['C']}%</h3></div>", unsafe_allow_html=True)
    m3.markdown(f"<div class='stat-card'>🛠️ I<br><h3>{st.session_state.game_state['cia']['I']}%</h3></div>", unsafe_allow_html=True)
    m4.markdown(f"<div class='stat-card'>⚡ A<br><h3>{st.session_state.game_state['cia']['A']}%</h3></div>", unsafe_allow_html=True)
    m5.markdown(f"<div class='stat-card'>📈 REP<br><h3>{st.session_state.game_state['reputation']}%</h3></div>", unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.subheader("🛠️ PDCA-Zyklus: TOM-Marktplatz")
        # Erweiterter Katalog basierend auf BSI elementaren Gefährdungen
        toms = {
            "ISO 27001 ISMS": {"cost": 50000, "cia": "ALL", "desc": "Der Goldstandard. Erhöht alle Werte permanent."},
            "Awareness Kampagne": {"cost": 12000, "cia": "C", "desc": "Schutz vor Phishing (Barclays-Szenario)."},
            "Backup Cluster (Offline)": {"cost": 25000, "cia": "A", "desc": "Sichert Verfügbarkeit gegen Ransomware."},
            "WAF (SQL-Injection Filter)": {"cost": 18000, "cia": "I", "desc": "Verhindert Manipulation der Schmuckpreise."},
            "DSGVO Rechtsberatung": {"cost": 15000, "cia": "C", "desc": "Minimiert Bußgelder nach Art. 83 DSGVO."},
            "IDS/IPS Sensoren": {"cost": 22000, "cia": "I", "desc": "Detektiert Integritätsbrüche in Echtzeit."}
        }

        cols = st.columns(2)
        for i, (name, d) in enumerate(toms.items()):
            with cols[i % 2]:
                if name in st.session_state.game_state['inventory']:
                    st.button(f"✅ {name}", disabled=True, key=f"btn_{name}")
                else:
                    if st.button(f"Investiere {d['cost']}€\n({name})", key=f"btn_{name}"):
                        if st.session_state.game_state['budget'] >= d['cost']:
                            st.session_state.game_state['budget'] -= d['cost']
                            st.session_state.game_state['inventory'].add(name)
                            if d['cia'] == "ALL":
                                for k in st.session_state.game_state['cia']: st.session_state.game_state['cia'][k] = min(100, st.session_state.game_state['cia'][k] + 15)
                            else:
                                st.session_state.game_state['cia'][d['cia']] = min(100, st.session_state.game_state['cia'][d['cia']] + 20)
                            add_log(f"TOM implementiert: {name}", "success")
                            st.rerun()
                        else:
                            st.error("Budget unzureichend!")

    with right:
        st.subheader("📟 Incident Control")
        log_html = "".join(st.session_state.game_state['logs'])
        st.markdown(f"<div class='log-container'>{log_html}</div>", unsafe_allow_html=True)
        
        if st.button("⏭️ NÄCHSTER TAG (Simuliere Bedrohungen)"):
            st.session_state.game_state['day'] += 1
            st.session_state.game_state['budget'] += 7500 # Daily Revenue
            
            # --- RANDOM THREAT ENGINE ---
            threat_roll = random.random()
            
            if threat_roll < 0.3: # Phishing (PDF Bezug)
                add_log("BEDROHUNG: Phishing-Welle 'Barclays Update' detektiert!", "warn")
                if "Awareness Kampagne" not in st.session_state.game_state['inventory']:
                    st.session_state.game_state['cia']['C'] -= 35
                    st.session_state.game_state['reputation'] -= 20
                    add_log("SCHADEN: Mitarbeiter hat Token-Daten geleakt. Vertraulichkeit sinkt!", "danger")
                else:
                    add_log("ABGEWEHRT: Mitarbeiter haben verdächtige Mails gemeldet.", "success")
            
            elif threat_roll < 0.5: # Ransomware
                add_log("BEDROHUNG: Crypto-Locker 'Silver-Lock' aktiv!", "warn")
                if "Backup Cluster (Offline)" not in st.session_state.game_state['inventory']:
                    st.session_state.game_state['cia']['A'] -= 45
                    add_log("SCHADEN: Alle Preislisten verschlüsselt! Shop offline.", "danger")
                else:
                    add_log("ABGEWEHRT: Backups wurden innerhalb von 2h eingespielt.", "success")
            
            elif threat_roll < 0.7: # Integrität
                add_log("BEDROHUNG: Manipulation der Gold-Preis-API!", "warn")
                if "WAF (SQL-Injection Filter)" not in st.session_state.game_state['inventory']:
                    st.session_state.game_state['cia']['I'] -= 30
                    add_log("SCHADEN: Schmuckstücke für 0.00€ verkauft. Finanzieller Verlust!", "danger")
                else:
                    add_log("ABGEWEHRT: Angriff wurde durch WAF blockiert.", "success")
            
            # DSGVO Prüfung (Automatischer Check)
            if st.session_state.game_state['cia']['C'] < 60:
                fine = st.session_state.game_state['budget'] * 0.04
                st.session_state.game_state['budget'] -= fine
                add_log(f"DSGVO-STRAFE: Verstoß gegen Art. 83! Bußgeld: {fine:,.0f}€.", "danger")

            # Check Win/Loss
            if any(v <= 0 for v in st.session_state.game_state['cia'].values()) or st.session_state.game_state['budget'] <= 0:
                st.session_state.game_state['phase'] = 'over'
            st.rerun()

# PHASE 3: GAME OVER
elif st.session_state.game_state['phase'] == 'over':
    st.error("💀 MISSION GESCHEITERT")
    st.title("Unternehmens-Kollaps")
    st.write(f"Du hast Silver-Data für {st.session_state.game_state['day']} Tage am Markt gehalten.")
    
    # Didaktische Zusammenfassung (Basierend auf PDFs)
    st.info("""
    **Was du lernen solltest:**
    - Informationssicherheit ist ein Prozess (**PDCA-Zyklus**).
    - Ohne **Integrität** sind deine Preislisten wertlos.
    - Ohne **Vertraulichkeit** ruiniert dich die DSGVO.
    - Ohne **Verfügbarkeit** verlierst du deine Kunden.
    """)
    
    if st.button("Neustart"):
        del st.session_state['game_state']
        st.rerun()
