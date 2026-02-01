import streamlit as st
import random
import time

# --- KONFIGURATION ---
st.set_page_config(page_title="CORE: Cyber Resilience Engine", layout="wide")

# --- CUSTOM CSS FÜR CYBER-LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0a0a0a; color: #00d4ff; }
    .stButton>button { border: 1px solid #00d4ff; background-color: #001a33; color: white; transition: 0.3s; }
    .stButton>button:hover { background-color: #00d4ff; color: black; box-shadow: 0 0 15px #00d4ff; }
    .status-box { padding: 20px; border: 1px solid #333; border-radius: 10px; background: #111; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISIERUNG ---
if 'init' not in st.session_state:
    st.session_state.update({
        'init': True,
        'scene': 'setup',
        'budget': 50000,
        'integrity': 100,
        'availability': 100,
        'confidentiality': 100,
        'day': 1,
        'inventory': [],
        'threat_level': 10,
        'logs': ["System online. Warte auf Analyse..."]
    })

def add_log(msg):
    st.session_state.logs.insert(0, f"Tag {st.session_state.day} - {msg}")

# --- SPIEL-MECHANIKEN ---

def apply_event(impact_type, value):
    if impact_type == "C": st.session_state.confidentiality -= value
    if impact_type == "I": st.session_state.integrity -= value
    if impact_type == "A": st.session_state.availability -= value
    st.session_state.confidentiality = max(0, min(100, st.session_state.confidentiality))
    st.session_state.integrity = max(0, min(100, st.session_state.integrity))
    st.session_state.availability = max(0, min(100, st.session_state.availability))

# --- UI ELEMENTE ---

# Sidebar für Echtzeit-Metriken (CIA-Triade)
with st.sidebar:
    st.title("🛡️ CORE Dashboard")
    st.metric("Budget", f"{st.session_state.budget:,} €")
    st.divider()
    st.subheader("CIA-Status (BSI-Konformität)")
    st.write(f"Vertraulichkeit: {st.session_state.confidentiality}%")
    st.progress(st.session_state.confidentiality / 100)
    st.write(f"Integrität: {st.session_state.integrity}%")
    st.progress(st.session_state.integrity / 100)
    st.write(f"Verfügbarkeit: {st.session_state.availability}%")
    st.progress(st.session_state.availability / 100)
    st.divider()
    if st.button("Reset Simulation"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# --- HAUPT-LOGIK ---

# 1. SETUP: SCHUTZBEDARFSANALYSE
if st.session_state.scene == "setup":
    st.title("📂 Phase 1: Schutzbedarfsfeststellung")
    st.markdown("""
    Bevor Sie das System verteidigen, müssen Sie es nach dem **BSI-Maximumsprinzip** bewerten.
    Wählen Sie den Schutzbedarf für die neue Cloud-Infrastruktur.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        c_need = st.select_slider("Schutzziel Vertraulichkeit", ["Normal", "Hoch", "Sehr Hoch"])
    with col2:
        i_need = st.select_slider("Schutzziel Integrität", ["Normal", "Hoch", "Sehr Hoch"])
    with col3:
        a_need = st.select_slider("Schutzziel Verfügbarkeit", ["Normal", "Hoch", "Sehr Hoch"])

    if st.button("Analyse finalisieren"):
        if i_need == "Sehr Hoch" or a_need == "Sehr Hoch":
            st.session_state.budget += 10000
            add_log("Kritische Infrastruktur erkannt. Zusatzbudget bewilligt.")
        st.session_state.scene = "management"
        st.rerun()

# 2. MANAGEMENT: DAS HAUPTSPIEL
elif st.session_state.scene == "management":
    st.title(f"🗓️ Einsatztag {st.session_state.day}")
    
    col_main, col_logs = st.columns([2, 1])
    
    with col_main:
        st.subheader("Verfügbare Maßnahmen (TOMs)")
        
        toms = {
            "Firewall-Cluster (A/C)": {"cost": 15000, "boost": 20},
            "IDS/IPS System (I)": {"cost": 12000, "boost": 15},
            "Mitarbeiter-Schulung (Mitwirkungspflicht)": {"cost": 5000, "boost": 10},
            "Backup-Konzept (A)": {"cost": 8000, "boost": 25},
            "Verschlüsselung (C)": {"cost": 10000, "boost": 20}
        }
        
        cols = st.columns(2)
        for i, (name, data) in enumerate(toms.items()):
            with cols[i % 2]:
                if st.button(f"Kaufen: {name} ({data['cost']}€)"):
                    if st.session_state.budget >= data['cost'] and name not in st.session_state.inventory:
                        st.session_state.budget -= data['cost']
                        st.session_state.inventory.append(name)
                        add_log(f"Investition getätigt: {name}")
                        st.rerun()
                    elif name in st.session_state.inventory:
                        st.info("Bereits implementiert.")
                    else:
                        st.error("Budget unzureichend!")

    with col_logs:
        st.subheader("System-Log")
        for log in st.session_state.logs[:8]:
            st.caption(log)

    st.divider()
    
    if st.button("➡️ Tag beenden & Bedrohungen prüfen"):
        st.session_state.day += 1
        # ZUFALLS-EVENTS (Basierend auf Material)
        event_roll = random.random()
        
        if event_roll < 0.4: # 40% Chance auf Angriff
            attack_type = random.choice(["Phishing", "Ransomware", "Manipulation"])
            add_log(f"🚨 ANGRIFF DETEKTIERT: {attack_type}")
            
            if attack_type == "Phishing":
                if "Mitarbeiter-Schulung (Mitwirkungspflicht)" not in st.session_state.inventory:
                    apply_event("C", 30)
                    add_log("Mitarbeiter klickte auf Link. Daten abgeflossen!")
                else:
                    add_log("Angriff durch geschulte Mitarbeiter abgewehrt.")
            
            elif attack_type == "Ransomware":
                if "Backup-Konzept (A)" not in st.session_state.inventory:
                    apply_event("A", 40)
                    add_log("Systeme verschlüsselt! Massive Ausfallzeit.")
                else:
                    st.session_state.budget -= 2000
                    add_log("Backups eingespielt. Geringer finanzieller Schaden.")
                    
            elif attack_type == "Manipulation":
                if "IDS/IPS System (I)" not in st.session_state.inventory:
                    apply_event("I", 35)
                    add_log("Integrität korrumpiert! Falsche Daten im Umlauf.")
                else:
                    add_log("IDS hat die Manipulation blockiert.")
        else:
            add_log("Ruhiger Tag. Systemstabilität normal.")
            st.session_state.budget += 5000 # Laufender Ertrag
        
        # Check Lose/Win
        if st.session_state.confidentiality <= 0 or st.session_state.integrity <= 0 or st.session_state.availability <= 0:
            st.session_state.scene = "game_over"
        st.rerun()

# 3. GAME OVER
elif st.session_state.scene == "game_over":
    st.error("💀 TOTALAUSFALL")
    st.header("Das Unternehmen ist insolvent.")
    st.write(f"Sie haben {st.session_state.day} Tage überlebt.")
    st.markdown("""
    **Analyse der Katastrophe:**
    Ein Schutzziel der CIA-Triade ist auf 0% gefallen. Gemäß BSI-Grundschutz wurde das 
    **Restrisiko** falsch eingeschätzt oder die **Mitwirkungspflicht** der Mitarbeiter vernachlässigt.
    """)
    if st.button("Neustart"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
