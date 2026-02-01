import streamlit as st
import random
import time

# --- KONFIGURATION & THEME ---
st.set_page_config(page_title="CORE: GRC Simulator", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #050505; }
    .stMetric { background-color: #111; padding: 10px; border-radius: 5px; border-left: 3px solid #00d4ff; }
    .stAlert { background-color: #1a1a1a; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISIERUNG ---
if 'init' not in st.session_state:
    st.session_state.update({
        'init': True,
        'scene': 'setup',
        'budget': 100000,
        'compliance': 100,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'inventory': set(),
        'day': 1,
        'reputation': 100,
        'logs': ["System initialisiert. Warte auf Schutzbedarfsanalyse..."]
    })

def add_log(msg, type="info"):
    icon = "ℹ️" if type == "info" else "⚠️" if type == "warn" else "🚨"
    st.session_state.logs.insert(0, f"Tag {st.session_state.day} {icon}: {msg}")

# --- DASHBOARD SIDEBAR ---
with st.sidebar:
    st.title("🛡️ CISO Terminal")
    st.metric("Budget", f"{st.session_state.budget:,.0f} €")
    st.metric("Reputation", f"{st.session_state.reputation}%")
    st.divider()
    st.subheader("CIA-Status")
    for key, val in st.session_state.cia.items():
        label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[key]
        st.caption(f"{label}: {val}%")
        st.progress(val / 100)
    
    if st.button("Simulation Hard-Reset"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- SZENARIEN & LOGIK ---

# PHASE 1: SETUP (Maximumsprinzip-Training)
if st.session_state.scene == "setup":
    st.title("📂 Strategische Schutzbedarfsfeststellung")
    st.info("Analysieren Sie das System 'SaniPlan 2.0' (nach BSI-Standard).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**System-Inhalt:**")
        st.markdown("- Kundendaten (Name, IBAN, Tür-Codes)\n- Kalkulationen & Angebote\n- Einsatzplanung der Monteure")
    
    with col2:
        c_req = st.select_slider("Bedarf Vertraulichkeit", ["Normal", "Hoch", "Sehr Hoch"])
        i_req = st.select_slider("Bedarf Integrität", ["Normal", "Hoch", "Sehr Hoch"])
        a_req = st.select_slider("Bedarf Verfügbarkeit", ["Normal", "Hoch", "Sehr Hoch"])

    if st.button("Analyse einloggen"):
        # Logik: Tür-Codes & IBAN machen Vertraulichkeit/Integrität mindestens "Hoch"
        if c_req != "Normal" and i_req != "Normal":
            st.success("Korrekt. Das Maximumsprinzip stuft das System als SCHUTZBEDARF: HOCH ein.")
            st.session_state.budget += 20000
        else:
            st.error("Fehleinschätzung! Bei Verlust von Tür-Codes droht Existenzgefahr. Budget gekürzt.")
            st.session_state.budget -= 10000
        st.session_state.scene = "main"
        st.rerun()

# PHASE 2: DAS MANAGEMENT-SPIEL
elif st.session_state.scene == "main":
    st.title(f"🏢 Rechenzentrum-Management - Tag {st.session_state.day}")
    
    # KATALOG DER MAẞNAHMEN (TOMs)
    toms = {
        "Verschlüsselung (C)": {"cost": 12000, "desc": "Schützt vor Datenabfluss bei Diebstahl.", "impact": "C"},
        "Redundante Server (A)": {"cost": 25000, "desc": "Verhindert Ausfallzeiten (Hochverfügbarkeit).", "impact": "A"},
        "Digitale Signaturen (I)": {"cost": 15000, "desc": "Sichert die Unveränderbarkeit von Rechnungen.", "impact": "I"},
        "Security Awareness Training": {"cost": 8000, "desc": "Senkt Phishing-Risiko um 60%.", "impact": "ALL"},
        "ISO 27001 Audit": {"cost": 35000, "desc": "Erhöht Reputation und senkt Bußgeld-Risiko.", "impact": "REP"}
    }

    tab1, tab2, tab3 = st.tabs(["🛒 TOM-Marktplatz", "📊 Risiko-Analyse", "📜 Logbuch"])

    with tab1:
        cols = st.columns(2)
        for i, (name, details) in enumerate(toms.items()):
            with cols[i % 2]:
                st.write(f"### {name}")
                st.caption(details['desc'])
                if name in st.session_state.inventory:
                    st.button(f"✅ Installiert", disabled=True, key=name)
                elif st.button(f"Investieren: {details['cost']}€", key=name):
                    if st.session_state.budget >= details['cost']:
                        st.session_state.budget -= details['cost']
                        st.session_state.inventory.add(name)
                        add_log(f"Maßnahme implementiert: {name}")
                        st.rerun()
                    else:
                        st.error("Nicht genügend Budget!")

    with tab2:
        st.write("### Aktuelle Bedrohungslage")
        risk = random.randint(10, 80)
        st.write(f"Geschätztes Restrisiko: {risk}%")
        st.progress(risk / 100)
        st.caption("Faktoren: Zero-Day-Exploits, Menschliches Versagen, Ungepatchte Systeme.")

    with tab3:
        for l in st.session_state.logs[:10]:
            st.text(l)

    st.divider()
    
    if st.button("➡️ NÄCHSTER TAG (Simulation starten)"):
        st.session_state.day += 1
        
        # ZUFALLS-EVENT GENERATOR
        event = random.random()
        
        # Phishing Angriff
        if event < 0.3:
            add_log("Phishing-Welle gegen die Buchhaltung!", "warn")
            if "Security Awareness Training" not in st.session_state.inventory:
                st.session_state.cia['C'] -= 25
                st.session_state.reputation -= 15
                add_log("Mitarbeiter hat Login-Daten preisgegeben!", "danger")
            else:
                add_log("Angriff durch geschultes Personal erkannt.", "info")

        # Ransomware Angriff
        elif event < 0.5:
            add_log("Ransomware 'Silver-Data' detektiert!", "danger")
            if "Redundante Server (A)" not in st.session_state.inventory:
                st.session_state.cia['A'] -= 40
                add_log("System steht still. Keine Monteur-Einsätze möglich.", "danger")
            else:
                add_log("Backup-Systeme erfolgreich hochgefahren.", "info")

        # DSGVO Prüfung
        elif event < 0.6:
            add_log("Unangekündigte DSGVO-Prüfung!", "warn")
            if st.session_state.cia['C'] < 80:
                fine = st.session_state.budget * 0.04
                st.session_state.budget -= fine
                add_log(f"Bußgeld verhängt: {fine:,.0f} € (Art. 83 DSGVO)", "danger")
            else:
                add_log("Prüfung bestanden. Compliance-Status exzellent.", "info")

        # Gewinn/Verlust Check
        if any(v <= 0 for v in st.session_state.cia.values()) or st.session_state.budget < 0:
            st.session_state.scene = "game_over"
        
        st.rerun()

# PHASE 3: GAME OVER
elif st.session_state.scene == "game_over":
    st.error("🚨 SYSTEM COLLAPSE 🚨")
    st.title("Unternehmens-Insolvenz")
    st.write(f"Sie haben die kritische Infrastruktur {st.session_state.day} Tage lang geschützt.")
    
    st.subheader("Post-Mortem-Analyse:")
    if st.session_state.budget < 0:
        st.write("- Finanzieller Ruin durch Bußgelder und fehlende Investitionsplanung.")
    else:
        st.write("- Kritischer Verlust der CIA-Schutzziele (Integrität oder Verfügbarkeit).")
    
    st.markdown("""
    **Was Sie für die nächste Prüfung wissen müssen:**
    - Das **Restrisiko** bleibt immer bestehen.
    - **Integrität** bedeutet: Schutz vor unbefugter Änderung.
    - **TOMs** müssen regelmäßig auf Wirksamkeit geprüft werden (**PDCA-Zyklus**).
    """)
    
    if st.button("Neue Simulation starten"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
