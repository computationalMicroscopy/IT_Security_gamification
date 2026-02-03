import streamlit as st
import random
import time

# --- INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'phase': 'INTRO',  # Startet mit der Story-Erklärung
        'day': 1,
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'reputation': 100,
        'inventory': set(),
        'logs': ["> SYSTEM INITIALIZED..."],
        'current_incident': None
    }

def add_log(msg, level="info"):
    colors = {"info": "#58a6ff", "warn": "#d29922", "error": "#f85149", "success": "#3fb950"}
    st.session_state.game['logs'].insert(0, f"<span style='color:{colors[level]}'>[T-{st.session_state.game['day']}] {msg}</span>")

# --- UI THEME ---
st.set_page_config(page_title="Cyber-Storm: Silver-Data", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; }
    .terminal { background: #010409; border: 1px solid #30363d; padding: 20px; border-radius: 5px; height: 350px; overflow-y: auto; }
    .briefing-card { background: #161b22; border-left: 5px solid #58a6ff; padding: 25px; border-radius: 5px; margin-bottom: 20px; }
    .stat-box { background: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 5px; text-align: center; }
    .highlight { color: #58a6ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME PHASES ---

# PHASE 1: DAS BRIEFING (SZENARIO & ZIEL)
if st.session_state.game['phase'] == 'INTRO':
    st.title("📟 EINGEHENDE NACHRICHT: OPERATION SILVER-DATA")
    
    st.markdown(f"""
    <div class="briefing-card">
    <h3>📂 SZENARIO: Krisenherd Silver-Data GmbH</h3>
    <p>Willkommen, CISO. Sie wurden als IT-Sicherheitsverantwortlicher für die <b>Silver-Data GmbH</b> eingesetzt – ein mittelständischer E-Commerce-Händler für Silberschmuck.</p>
    <p><b>Die Lage:</b> Am Montagmorgen wurde ein massiver Vorfall gemeldet. Die <span class="highlight">Integrität</span> der Preislisten ist nicht mehr gewährleistet (Goldpreise wurden manipuliert). Zudem gibt es Hinweise auf exfiltrierte Kundendaten (IBANs, Adressen).</p>
    <p><b>Ihr Ziel:</b> Retten Sie das Unternehmen! Sie müssen die drei Schutzziele der <b>CIA-Triade</b> stabilisieren und gleichzeitig die Wirtschaftlichkeit wahren.</p>
    <ul>
        <li><b>Confidentiality (C):</b> Schützen Sie Kundendaten vor Leaks (Vermeidung von DSGVO-Bußgeldern).</li>
        <li><b>Integrity (I):</b> Sichern Sie Preislisten und Warenbestände gegen Manipulation.</li>
        <li><b>Availability (A):</b> Halten Sie den Shop online. Jeder Ausfall kostet 10.000€/Stunde.</li>
    </ul>
    <p><b>Die Mechanik:</b> Sie agieren im <b>PDCA-Zyklus</b> (Plan-Do-Check-Act). Investieren Sie klug in TOMs und reagieren Sie auf Incidents!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("BRIEFING GELESEN - ZUR SCHUTZBEDARFSANALYSE"):
        st.session_state.game['phase'] = 'ANALYSIS'
        st.rerun()

# PHASE 2: SCHUTZBEDARFSANALYSE (BSI MAXIMUMSPRINZIP)
elif st.session_state.game['phase'] == 'ANALYSIS':
    st.title("🕵️ SCHRITT 1: SCHUTZBEDARFSFESTSTELLUNG")
    st.write("""
    Bevor wir Maßnahmen einleiten, müssen wir das System einstufen. 
    Wenden Sie das **Maximumsprinzip** an: Der Schutzbedarf des Gesamtsystems richtet sich nach dem 
    kritischsten Datenbestand (Kundendaten, Finanzdaten, Gold-Preise).
    """)
    
    c1, c2, c3 = st.columns(3)
    c_sel = c1.select_slider("Vertraulichkeit", ["Normal", "Hoch", "Sehr Hoch"])
    i_sel = c2.select_slider("Integrität", ["Normal", "Hoch", "Sehr Hoch"])
    a_sel = c3.select_slider("Verfügbarkeit", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("ANALYSE EINLOGGEN"):
        # Logik aus PDF: Finanz- und Kundendaten im Schmuckhandel = Sehr Hoch
        if c_sel == "Sehr Hoch" and i_sel == "Sehr Hoch":
            st.session_state.game['budget'] += 30000
            add_log("Analyse korrekt (Maximumsprinzip). Zusätzliches Budget für Hochrisiko-Systeme bewilligt.", "success")
        else:
            st.session_state.game['budget'] -= 20000
            add_log("Fehlanalyse! Die Revision hat Ihr Budget wegen mangelhafter Risikoeinschätzung gekürzt.", "error")
        st.session_state.game['phase'] = 'DASHBOARD'
        st.rerun()

# PHASE 3: DAS OPERATIVE DASHBOARD (PDCA)
elif st.session_state.game['phase'] == 'DASHBOARD':
    # Stats Dashboard
    cols = st.columns(5)
    cols[0].markdown(f"<div class='stat-box'>💰 BUDGET<br>{st.session_state.game['budget']:,}€</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='stat-box'>🔒 C (Conf.)<br>{st.session_state.game['cia']['C']}%</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div class='stat-box'>🛠️ I (Integ.)<br>{st.session_state.game['cia']['I']}%</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div class='stat-box'>⚡ A (Avail.)<br>{st.session_state.game['cia']['A']}%</div>", unsafe_allow_html=True)
    cols[4].markdown(f"<div class='stat-box'>📈 REP<br>{st.session_state.game['reputation']}%</div>", unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        if st.session_state.game['current_incident']:
            inc = st.session_state.game['current_incident']
            st.error(f"🚨 KRITISCHER INCIDENT: {inc['title']}")
            st.info(f"**LOG-DOSSIER FRAGMENT:** {inc['dossier']}")
            
            for opt in inc['options']:
                if st.button(opt['label'], key=opt['label']):
                    if opt['correct']:
                        st.session_state.game['reputation'] = min(100, st.session_state.game['reputation'] + 5)
                        add_log(f"ERFOLG: {opt['feedback']}", "success")
                    else:
                        st.session_state.game['cia'][inc['target']] -= inc['damage']
                        add_log(f"FEHLREAKTION: {opt['feedback']}", "error")
                    st.session_state.game['current_incident'] = None
                    st.rerun()
        else:
            st.subheader("🛡️ Maßnahmen-Katalog (Plan/Do)")
            toms = {
                "G 0.19: Awareness-Schulung": {"cost": 15000, "cia": "C", "desc": "Schutz vor Phishing (Barclays-Szenario)."},
                "G 0.18: Redundante Backups": {"cost": 30000, "cia": "A", "desc": "Sichert Verfügbarkeit gegen Ransomware."},
                "Digitale Signaturen (API)": {"cost": 25000, "cia": "I", "desc": "Verhindert Preismanipulation."},
                "DSGVO Audit-Paket": {"cost": 20000, "cia": "C", "desc": "Schutz vor Bußgeldern (Art. 83 DSGVO)."}
            }
            
            t_cols = st.columns(2)
            for i, (name, val) in enumerate(toms.items()):
                with t_cols[i%2]:
                    if name in st.session_state.game['inventory']:
                        st.button(f"✅ {name}", disabled=True)
                    else:
                        if st.button(f"{name} ({val['cost']}€)"):
                            if st.session_state.game['budget'] >= val['cost']:
                                st.session_state.game['budget'] -= val['cost']
                                st.session_state.game['inventory'].add(name)
                                st.session_state.game['cia'][val['cia']] = min(100, st.session_state.game['cia'][val['cia']] + 20)
                                add_log(f"TOM AKTIVIERT: {name}", "info")
                                st.rerun()

    with right:
        st.subheader("📟 System-Logs")
        log_html = "".join(st.session_state.game['logs'])
        st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)
        
        if not st.session_state.game['current_incident']:
            if st.button("⏭️ NÄCHSTER TAG (SIMULATION)"):
                st.session_state.game['day'] += 1
                st.session_state.game['budget'] += 5000
                
                # Incident Engine
                if random.random() < 0.6:
                    st.session_state.game['current_incident'] = {
                        "title": "Unbekannte Preisänderung",
                        "dossier": "UPDATE prices SET value=0.01 WHERE type='Gold'. IP: 185.x.x.x",
                        "target": "I", "damage": 30,
                        "options": [
                            {"label": "WAF & Input Validation aktivieren", "correct": True, "feedback": "Manipulation unterbunden!"},
                            {"label": "Passwörter aller Mitarbeiter ändern", "correct": False, "feedback": "Nutzt nichts gegen SQL-Injection!"}
                        ]
                    }
                
                # Check Lose
                if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
                    st.session_state.game['phase'] = 'GAMEOVER'
                st.rerun()

elif st.session_state.game['phase'] == 'GAMEOVER':
    st.error("💀 UNTERNEHMEN INSOLVENT / ZERTIFIKAT ENTZOGEN")
    if st.button("NEUSTART"):
        del st.session_state['game']
        st.rerun()
