import streamlit as st
import random
import time

# --- INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'phase': 'BOOT',
        'day': 1,
        'budget': 200000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'reputation': 100,
        'inventory': set(),
        'logs': ["> INIT: CORE v4.0 Online.", "> STATUS: Operation Silver-Data bereit."],
        'current_incident': None,
        'score': 0
    }

def add_log(msg, level="info"):
    colors = {"info": "#58a6ff", "warn": "#d29922", "error": "#f85149", "success": "#3fb950"}
    st.session_state.game['logs'].insert(0, f"<span style='color:{colors[level]}'>[T-{st.session_state.game['day']}] {msg}</span>")

# --- UI THEME ---
st.set_page_config(page_title="CORE: Silver-Data Chronicles", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; }
    .terminal { background: #010409; border: 1px solid #30363d; padding: 20px; border-radius: 5px; height: 400px; overflow-y: auto; }
    .incident-card { background: #161b22; border: 2px solid #f85149; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .stat-box { background: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME PHASES ---

# 1. BOOT: SCHUTZBEDARF (BSI MAXIMUMSPRINZIP)
if st.session_state.game['phase'] == 'BOOT':
    st.title("🕵️ SCHRITT 1: STRATEGISCHE EINSTUFUNG")
    st.info("System: Silver-Data ERP (Schmuckhandel). Analysieren Sie den Schutzbedarf für die Zertifizierung.")
    
    c, i, a = st.columns(3)
    c_sel = c.select_slider("Vertraulichkeit (Finanzdaten)", ["Normal", "Hoch", "Sehr Hoch"])
    i_sel = i.select_slider("Integrität (Warenwerte/Gold)", ["Normal", "Hoch", "Sehr Hoch"])
    a_sel = a.select_slider("Verfügbarkeit (Webshop)", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("ANALYSESCHLÜSSEL EINLOGGEN"):
        # Das Maximumsprinzip (Seite 24 PDF)
        if c_sel == "Sehr Hoch" and i_sel == "Sehr Hoch":
            st.session_state.game['budget'] += 50000
            add_log("Maximumsprinzip korrekt: Sehr hoher Schutzbedarf erkannt. Budget erhöht.", "success")
        else:
            st.session_state.game['budget'] -= 30000
            add_log("Fehlanalyse! Unterfinanzierung durch falsche Risikoeinschätzung.", "error")
        st.session_state.game['phase'] = 'STATION'
        st.rerun()

# 2. STATION: DAS HAUPTSPIEL
elif st.session_state.game['phase'] == 'STATION':
    # Top Stats Dashboard
    cols = st.columns(5)
    cols[0].markdown(f"<div class='stat-box'>💰 BUDGET<br>{st.session_state.game['budget']:,}€</div>", unsafe_allow_html=True)
    cols[1].markdown(f"<div class='stat-box'>🔒 C<br>{st.session_state.game['cia']['C']}%</div>", unsafe_allow_html=True)
    cols[2].markdown(f"<div class='stat-box'>🛠️ I<br>{st.session_state.game['cia']['I']}%</div>", unsafe_allow_html=True)
    cols[3].markdown(f"<div class='stat-box'>⚡ A<br>{st.session_state.game['cia']['A']}%</div>", unsafe_allow_html=True)
    cols[4].markdown(f"<div class='stat-box'>📈 REP<br>{st.session_state.game['reputation']}%</div>", unsafe_allow_html=True)

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        # Falls ein Incident aktiv ist, muss er gelöst werden
        if st.session_state.game['current_incident']:
            inc = st.session_state.game['current_incident']
            st.markdown(f"<div class='incident-card'><h3>🚨 INCIDENT: {inc['title']}</h3><p>{inc['dossier']}</p></div>", unsafe_allow_html=True)
            
            st.write("**Wählen Sie Ihre Reaktion (PDCA - Act):**")
            opts = st.columns(2)
            for idx, opt in enumerate(inc['options']):
                if opts[idx % 2].button(opt['label']):
                    if opt['correct']:
                        st.session_state.game['score'] += 100
                        st.session_state.game['reputation'] = min(100, st.session_state.game['reputation'] + 10)
                        add_log(f"ERFOLG: {opt['feedback']}", "success")
                    else:
                        st.session_state.game['cia'][inc['target']] -= inc['damage']
                        st.session_state.game['budget'] -= 5000
                        add_log(f"FEHLER: {opt['feedback']}", "error")
                    st.session_state.game['current_incident'] = None
                    st.rerun()
        else:
            st.subheader("🛠️ IT-GRUNDSCHUTZ (PLAN/DO)")
            st.write("Investieren Sie in TOMs (Technisch-Organisatorische Maßnahmen).")
            
            toms = {
                "G 0.19: Awareness-Training": {"cost": 15000, "cia": "C", "desc": "Schutz vor Phishing (Barclays-Szenario)."},
                "G 0.18: Offline Backups": {"cost": 30000, "cia": "A", "desc": "Wiederherstellung nach Ransomware."},
                "IDS/IPS Analyse-Tools": {"cost": 25000, "cia": "I", "desc": "Erkennt Manipulationen an Preislisten."},
                "DSGVO Audit (Art. 83)": {"cost": 20000, "cia": "C", "desc": "Minimiert das Risiko horrender Bußgelder."}
            }

            t_cols = st.columns(2)
            for i, (name, val) in enumerate(toms.items()):
                with t_cols[i % 2]:
                    if name in st.session_state.game['inventory']:
                        st.button(f"✅ {name}", disabled=True)
                    else:
                        if st.button(f"Installiere {name} ({val['cost']}€)"):
                            if st.session_state.game['budget'] >= val['cost']:
                                st.session_state.game['budget'] -= val['cost']
                                st.session_state.game['inventory'].add(name)
                                st.session_state.game['cia'][val['cia']] = min(100, st.session_state.game['cia'][val['cia']] + 15)
                                add_log(f"TOM AKTIVIERT: {name}", "info")
                                st.rerun()

    with right:
        st.subheader("📟 TERMINAL LOG")
        log_html = "".join(st.session_state.game['logs'])
        st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)
        
        if not st.session_state.game['current_incident']:
            if st.button("⏭️ NÄCHSTE SCHICHT (TAG BEENDEN)"):
                st.session_state.game['day'] += 1
                st.session_state.game['budget'] += 10000 # Daily E-Commerce Profit
                
                # Incident Generator (Basierend auf PDFs)
                if random.random() < 0.7:
                    incidents = [
                        {
                            "title": "Operation Silver-Data: Datenfragment",
                            "dossier": "LOG-FRAGMENT: <i>'UPDATE silver_prices SET price = 0 WHERE item_id = *'</i>. Herkunft: IP 192.168.45.1. Was tun?",
                            "target": "I", "damage": 40,
                            "options": [
                                {"label": "DB-Nutzerrechte einschränken", "correct": True, "feedback": "Manipulation gestoppt!"},
                                {"label": "Webshop offline nehmen", "correct": False, "feedback": "Verfügbarkeit leidet massiv."}
                            ]
                        },
                        {
                            "title": "Barclays Phishing-Welle",
                            "dossier": "Mitarbeiter berichten von einer Mail: 'Bestätigen Sie Ihren Token'. Einige haben bereits geklickt.",
                            "target": "C", "damage": 35,
                            "options": [
                                {"label": "E-Mail-Server filtern & Token sperren", "correct": True, "feedback": "Datenabfluss verhindert."},
                                {"label": "Passwörter nächste Woche ändern", "correct": False, "feedback": "Zu spät! Daten wurden bereits exfiltriert."}
                            ]
                        }
                    ]
                    st.session_state.game['current_incident'] = random.choice(incidents)
                
                # DSGVO Bußgeld-Check (Art. 83)
                if st.session_state.game['cia']['C'] < 50:
                    fine = st.session_state.game['budget'] * 0.05
                    st.session_state.game['budget'] -= fine
                    add_log(f"DSGVO-STRAFE: {fine:,.0f}€ wegen mangelnder Vertraulichkeit.", "error")

                if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
                    st.session_state.game['phase'] = 'GAMEOVER'
                st.rerun()

# 3. GAME OVER
elif st.session_state.game['phase'] == 'GAMEOVER':
    st.error("💀 UNTERNEHMEN KOLLABIERT")
    st.title("FINEL GAME REPORT")
    st.write(f"Du hast {st.session_state.game['day']} Tage überlebt. Dein Score: {st.session_state.game['score']}")
    
    st.markdown("""
    **Wichtige Erkenntnisse für die Prüfung:**
    * **Integrität:** Ohne korrekte Preise bricht der Handel zusammen.
    * **PDCA:** Sicherheit ist kein Zustand, sondern ein Zyklus.
    * **Restrisiko:** Es bleibt immer etwas übrig – man muss es managen.
    """)
    if st.button("NEUSTART"):
        del st.session_state['game']
        st.rerun()
