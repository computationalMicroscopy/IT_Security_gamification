import streamlit as st
import random
import time

# --- KONFIGURATION ---
st.set_page_config(page_title="Cyber-Storm: Silver-Data", layout="wide", page_icon="🕵️")

# --- CUSTOM CSS (Hacker Terminal) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #58a6ff; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { border: 1px solid #238636; background-color: #21262d; color: #3fb950; font-weight: bold; height: 3em; }
    .stButton>button:hover { background-color: #238636; color: white; }
    .log-box { background-color: #010409; border: 1px solid #30363d; padding: 15px; border-radius: 5px; height: 400px; overflow-y: auto; color: #d1d5da; font-size: 0.9em; }
    .stat-card { background-color: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 8px; text-align: center; }
    .critical { color: #f85149; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISIERUNG (Zustandsverwaltung) ---
if 'state' not in st.session_state:
    st.session_state.state = {
        'phase': 'setup',
        'day': 1,
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'inventory': [],
        'logs': ["> SYSTEM INITIALIZED: Operation Silver-Data gestartet."],
        'max_prinzip_score': 0,
        'incidents_solved': 0,
        'reputation': 100
    }

def add_log(msg, level="info"):
    prefix = "✅" if level == "success" else "🚨" if level == "danger" else "ℹ️"
    st.session_state.state['logs'].insert(0, f"{prefix} Tag {st.session_state.state['day']}: {msg}")

# --- SPIEL-PHASEN ---

# PHASE 1: SCHUTZBEDARFSANALYSE (BSI-STANDARD)
if st.session_state.state['phase'] == 'setup':
    st.title("🛡️ Schritt 1: Schutzbedarfsfeststellung (BSI IT-Grundschutz)")
    st.markdown("""
    Willkommen, CISO. Bevor wir die Verteidigung hochfahren, müssen wir das System **'Silver-Data ERP'** bewerten.
    Hier lagern Kundendaten (IBANs, Adressen) und die zentralen Gold-Preislisten.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1: c_lvl = st.select_slider("Vertraulichkeit (Confidentiality)", ["Normal", "Hoch", "Sehr Hoch"])
    with col2: i_lvl = st.select_slider("Integrität (Integrity)", ["Normal", "Hoch", "Sehr Hoch"])
    with col3: a_lvl = st.select_slider("Verfügbarkeit (Availability)", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("Analyse finalisieren"):
        # Das Maximum-Prinzip aus dem PDF (Seite 24/26)
        if c_lvl == "Sehr Hoch" and i_lvl == "Sehr Hoch":
            st.session_state.state['max_prinzip_score'] = 100
            st.session_state.state['budget'] += 20000
            add_log("Analyse korrekt (Maximumsprinzip). Zusatzbudget bewilligt.", "success")
        else:
            st.session_state.state['budget'] -= 20000
            add_log("Fehlanalyse! Budgetkürzung durch die Revision.", "danger")
        
        st.session_state.state['phase'] = 'main'
        st.rerun()

# PHASE 2: DAS OPERATIVE SPIEL (Der PDCA-Zyklus)
elif st.session_state.state['phase'] == 'main':
    # --- DASHBOARD ---
    st.title(f"🕵️ Operation Silver-Data | Tag {st.session_state.state['day']}")
    
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.markdown(f"<div class='stat-card'>💰 BUDGET<br><b>{st.session_state.state['budget']:,} €</b></div>", unsafe_allow_html=True)
    d2.markdown(f"<div class='stat-card'>🔒 C<br><b>{st.session_state.state['cia']['C']}%</b></div>", unsafe_allow_html=True)
    d3.markdown(f"<div class='stat-card'>🛠️ I<br><b>{st.session_state.state['cia']['I']}%</b></div>", unsafe_allow_html=True)
    d4.markdown(f"<div class='stat-card'>⚡ A<br><b>{st.session_state.state['cia']['A']}%</b></div>", unsafe_allow_html=True)
    d5.markdown(f"<div class='stat-card'>📈 REP<br><b>{st.session_state.state['state']['reputation']}%</b></div>", unsafe_allow_html=True)
    
    st.divider()
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # PDCA: PLAN & DO (TOMs kaufen)
        st.subheader("🛠️ Technisch-Organisatorische Maßnahmen (TOMs)")
        
        toms = {
            "G 0.15: Abhörsichere Räume": {"cost": 35000, "cia": "C", "type": "T"},
            "G 0.18: Backup-System (3-2-1)": {"cost": 25000, "cia": "A", "type": "T"},
            "G 0.19: Awareness-Schulung": {"cost": 15000, "cia": "C", "type": "O"},
            "G 0.22: Redundante Firewall": {"cost": 40000, "cia": "A", "type": "T"},
            "G 0.28: Digitale Signaturen": {"cost": 20000, "cia": "I", "type": "T"},
            "G 0.45: DSGVO Compliance Audit": {"cost": 30000, "cia": "C", "type": "O"}
        }
        
        c_tom1, c_tom2 = st.columns(2)
        for i, (name, val) in enumerate(toms.items()):
            current_col = c_tom1 if i % 2 == 0 else c_tom2
            if name in st.session_state.state['inventory']:
                current_col.button(f"✅ {name}", key=name, disabled=True)
            else:
                if current_col.button(f"Investiere {val['cost']}€\n({name})", key=name):
                    if st.session_state.state['budget'] >= val['cost']:
                        st.session_state.state['budget'] -= val['cost']
                        st.session_state.state['inventory'].append(name)
                        st.session_state.state['cia'][val['cia']] = min(100, st.session_state.state['cia'][val['cia']] + 20)
                        add_log(f"TOM implementiert: {name}", "success")
                        st.rerun()
                    else:
                        st.error("Budget reicht nicht aus!")

    with col_right:
        st.subheader("📟 Incident Log (Check)")
        log_html = "".join([f"<div>{l}</div>" for l in st.session_state.state['logs']])
        st.markdown(f"<div class='log-box'>{log_html}</div>", unsafe_allow_html=True)
        
        # PDCA: ACT (Tag beenden & Simulation)
        if st.button("⏭️ Nächster Tag (Check & Act)"):
            st.session_state.state['day'] += 1
            st.session_state.state['budget'] += 8000 # Täglicher Cashflow
            
            # --- ZUFALLS-EVENTS (BASIEREND AUF PDF-INHALTEN) ---
            event = random.random()
            
            # 1. Phishing (Barclays-Szenario aus PDF)
            if event < 0.25:
                add_log("Angriff: Barclays-Phishing-Mail im Umlauf!", "danger")
                if "G 0.19: Awareness-Schulung" not in st.session_state.state['inventory']:
                    st.session_state.state['cia']['C'] -= 30
                    add_log("Mitarbeiter hat Token-Daten eingegeben. Massiver Datenabfluss!", "danger")
                else:
                    st.session_state.state['reputation'] += 5
                    add_log("Mitarbeiter hat die Mail gemeldet. Angriff gestoppt.", "success")
            
            # 2. Ransomware (Verfügbarkeit)
            elif event < 0.45:
                add_log("Angriff: Ransomware verschlüsselt ERP!", "danger")
                if "G 0.18: Backup-System (3-2-1)" not in st.session_state.state['inventory']:
                    st.session_state.state['cia']['A'] -= 45
                    st.session_state.state['budget'] -= 10000
                    add_log("Kein Backup gefunden. Lösegeldverhandlungen laufen...", "danger")
                else:
                    st.session_state.state['cia']['A'] = min(100, st.session_state.state['cia']['A'] + 10)
                    add_log("Recovery erfolgreich durch Backup-Konzept.", "success")
            
            # 3. Manipulation (Silberschmuck-Preise)
            elif event < 0.60:
                add_log("Angriff: Integrität der Preislisten kompromittiert!", "danger")
                if "G 0.28: Digitale Signaturen" not in st.session_state.state['inventory']:
                    st.session_state.state['cia']['I'] -= 35
                    add_log("Preise im Shop wurden auf 0.00€ gesetzt. Hoher Verlust!", "danger")
                else:
                    add_log("Signaturen-Prüfung hat Manipulation erkannt und gestoppt.", "success")

            # 4. DSGVO-Keule (Rechtliches)
            elif event < 0.75:
                add_log("Audit: Landesdatenschutzbeauftragter prüft...", "info")
                if st.session_state.state['cia']['C'] < 80 and "G 0.45: DSGVO Compliance Audit" not in st.session_state.state['inventory']:
                    fine = st.session_state.state['budget'] * 0.04
                    st.session_state.state['budget'] -= fine
                    add_log(f"DSGVO-Bußgeld (Art. 83): {fine:,.0f}€ fällig!", "danger")
                else:
                    add_log("Compliance-Prüfung bestanden.", "success")

            # --- WIN/LOSE CONDITIONS ---
            if any(v <= 0 for v in st.session_state.state['cia'].values()) or st.session_state.state['budget'] <= 0:
                st.session_state.state['phase'] = 'game_over'
            
            st.rerun()

# PHASE 3: GAME OVER
elif st.session_state.state['phase'] == 'game_over':
    st.error("💀 SYSTEM-KOLLAPS")
    st.title("Insolvenz & Zertifikatsentzug")
    st.write(f"Du hast das Unternehmen {st.session_state.state['day']} Tage lang geschützt.")
    
    st.subheader("Analyse der Niederlage:")
    if st.session_state.state['budget'] <= 0:
        st.write("- Finanzieller Ruin: Deine Sicherheitsmaßnahmen waren teurer als dein Ertrag oder Bußgelder haben dich ruiniert.")
    else:
        st.write("- Sicherheits-Versagen: Eines der Schutzziele (CIA) ist auf 0% gefallen. Die Operation Silver-Data ist gescheitert.")
    
    st.markdown("""
    **Was du für die Prüfung mitnehmen musst:**
    - **Integrität** ist bei Preislisten lebenswichtig.
    - **Vertraulichkeit** schützt vor DSGVO-Bußgeldern.
    - **Verfügbarkeit** sichert den Geschäftsbetrieb.
    - **Restrisiko** ist niemals Null.
    """)
    
    if st.button("Neue Instanz laden"):
        del st.session_state['state']
        st.rerun()
