import streamlit as st
import random
import time

# --- KONFIGURATION ---
st.set_page_config(page_title="Cyber-Defender: Silver-Data", layout="wide", page_icon="💎")

# CSS für echtes Hacker-Interface
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .stButton>button { border: 1px solid #00ff41; background-color: #000; color: #00ff41; border-radius: 0; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #00ff41; color: #000; box-shadow: 0 0 20px #00ff41; }
    .terminal-card { background: #000; border: 1px solid #00ff41; padding: 15px; border-radius: 2px; height: 350px; overflow-y: auto; }
    .status-panel { background: #111; border: 1px solid #444; padding: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE INITIALISIERUNG ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'step': 'intro',
        'day': 1,
        'budget': 120000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'inventory': [],
        'logs': ["> SYSTEM INITIALISIERT. WARTE AUF BEFEHLE."],
        'threat_meter': 0,
        'is_game_over': False
    }

def add_log(msg, type="info"):
    color = "#00ff41" if type == "info" else "#ff4b4b" if type == "error" else "#ffff00"
    st.session_state.game_state['logs'].insert(0, f"<span style='color:{color}'>[TAG {st.session_state.game_state['day']}] {msg}</span>")

# --- SPIEL-LOGIK ---

def trigger_random_attack():
    # BSI Elementare Gefährdungen & Szenario Silver-Data
    attacks = [
        {"name": "Phishing-Welle (Barclays-Imitat)", "target": "C", "damage": 35, "defense": "Security Awareness Training", "msg": "Mitarbeiter gab Zugangsdaten auf Fake-Portal ein!"},
        {"name": "Ransomware-Infiltration", "target": "A", "damage": 50, "defense": "Backup-Konzept (3-2-1 Regel)", "msg": "Verschlüsselungstrojaner legt den Webshop lahm!"},
        {"name": "SQL-Injection (Preis-Manipulation)", "target": "I", "damage": 40, "defense": "WAF & Input Validation", "msg": "Angreifer hat Schmuckpreise auf 0,00€ gesetzt!"},
        {"name": "DSGVO-Audit durch Aufsichtsbehörde", "target": "BUDGET", "damage": 20000, "defense": "Datenschutz-Folgenabschätzung", "msg": "Lücken in der Dokumentation führen zu Bußgeld!"}
    ]
    
    attack = random.choice(attacks)
    add_log(f"⚠ ALARM: {attack['name']}", "warn")
    
    if attack['defense'] in st.session_state.game_state['inventory']:
        add_log(f"🛡 ABGEWEHRT: {attack['defense']} hat den Schaden verhindert.", "info")
    else:
        if attack['target'] == "BUDGET":
            st.session_state.game_state['budget'] -= attack['damage']
        else:
            st.session_state.game_state['cia'][attack['target']] -= attack['damage']
        add_log(f"💥 SCHADEN: {attack['msg']}", "error")

# --- UI RENDERING ---

# INTRO PHASE
if st.session_state.game_state['step'] == 'intro':
    st.title("💎 OPERATION: SILVER-DATA")
    st.write("""
    **Szenario:** Du bist der neue Chief Information Security Officer (CISO) bei einem Schmuck-Händler.
    Deine Vorgänger haben die IT vernachlässigt. Die Integrität der Preislisten ist instabil.
    Deine Aufgabe: Nutze den BSI-Grundschutz, um das Unternehmen zu retten.
    """)
    if st.button("Simulation starten"):
        st.session_state.game_state['step'] = 'analysis'
        st.rerun()

# PHASE 1: SCHUTZBEDARFSANALYSE
elif st.session_state.game_state['step'] == 'analysis':
    st.header("📂 Phase 1: Schutzbedarfsanalyse (Maximumsprinzip)")
    st.write("Wähle den Schutzbedarf basierend auf dem Schadenspotenzial (Existenzbedrohung, Gesetzesverstoß).")
    
    col1, col2, col3 = st.columns(3)
    c_req = col1.select_slider("Vertraulichkeit (IBANs/Adressen)", ["Normal", "Hoch", "Sehr Hoch"])
    i_req = col2.select_slider("Integrität (Gold-Preise)", ["Normal", "Hoch", "Sehr Hoch"])
    a_req = col3.select_slider("Verfügbarkeit (Webshop)", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("Analyse einloggen"):
        # Logik aus PDF: Finanzdaten = Sehr Hoch
        if c_req == "Sehr Hoch" or i_req == "Sehr Hoch":
            st.session_state.game_state['budget'] += 30000
            add_log("Analyse korrekt. Zusätzliche Fördermittel bewilligt.")
        else:
            st.session_state.game_state['budget'] -= 10000
            add_log("Fehleinschätzung! Revision kürzt Budget.", "error")
        st.session_state.game_state['step'] = 'main'
        st.rerun()

# PHASE 2: HAUPTSPIEL (ENDLOS-MODUS)
elif st.session_state.game_state['step'] == 'main':
    # Dashboard
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Kapital", f"{st.session_state.game_state['budget']:,} €")
    c2.metric("Vertraulichkeit (C)", f"{st.session_state.game_state['cia']['C']}%")
    c3.metric("Integrität (I)", f"{st.session_state.game_state['cia']['I']}%")
    c4.metric("Verfügbarkeit (A)", f"{st.session_state.game_state['cia']['A']}%")
    
    st.divider()
    
    col_play, col_log = st.columns([2, 1])
    
    with col_play:
        st.subheader("🛡 Strategische Maßnahmen (Plan/Do)")
        toms = {
            "Security Awareness Training": {"cost": 15000, "desc": "Schult Mitarbeiter gegen Phishing (Mitwirkungspflicht)."},
            "Backup-Konzept (3-2-1 Regel)": {"cost": 25000, "desc": "Sichert Verfügbarkeit nach Ransomware-Angriff."},
            "WAF & Input Validation": {"cost": 20000, "desc": "Verhindert SQL-Injections und Preis-Manipulation."},
            "Datenschutz-Folgenabschätzung": {"cost": 10000, "desc": "Senkt DSGVO-Bußgeldrisiko massiv."},
            "BSI Baustein: Sicherer Client": {"cost": 18000, "desc": "Härtet Endgeräte gegen Malware."}
        }
        
        cols = st.columns(2)
        for i, (name, details) in enumerate(toms.items()):
            with cols[i % 2]:
                if name in st.session_state.game_state['inventory']:
                    st.button(f"✅ {name}", disabled=True)
                else:
                    if st.button(f"Kaufen: {name}\n({details['cost']}€)"):
                        if st.session_state.game_state['budget'] >= details['cost']:
                            st.session_state.game_state['budget'] -= details['cost']
                            st.session_state.game_state['inventory'].append(name)
                            add_log(f"TOM implementiert: {name}")
                            st.rerun()
                        else:
                            st.error("Budget unzureichend!")
                            
        st.divider()
        if st.button("⏭ NÄCHSTER TAG (PDCA-Zyklus fortsetzen)"):
            st.session_state.game_state['day'] += 1
            st.session_state.game_state['budget'] += 5000 # Einnahmen
            trigger_random_attack()
            
            # Check Lose Condition
            if any(v <= 0 for v in st.session_state.game_state['cia'].values()) or st.session_state.game_state['budget'] <= 0:
                st.session_state.game_state['step'] = 'game_over'
            st.rerun()

    with col_log:
        st.subheader("📟 Incident Log")
        log_html = f"<div class='terminal-card'>{'<br>'.join(st.session_state.game_state['logs'])}</div>"
        st.markdown(log_html, unsafe_allow_html=True)

# PHASE 3: GAME OVER
elif st.session_state.game_state['step'] == 'game_over':
    st.error("💀 SYSTEM-KOLLAPS")
    st.title("Insolvenz & Datenverlust")
    st.write(f"Du hast das Unternehmen {st.session_state.game_state['day']} Tage lang verteidigt.")
    st.write("Einer deiner CIA-Werte oder dein Budget ist auf Null gefallen. Die Aufsichtsbehörde hat den Shop geschlossen.")
    
    if st.button("Neue Simulation starten"):
        del st.session_state['game_state']
        st.rerun()
