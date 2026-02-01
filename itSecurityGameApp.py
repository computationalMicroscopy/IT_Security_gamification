import streamlit as st
import random
import time

# --- KONFIGURATION & STYLES ---
st.set_page_config(page_title="Incident Responder: Proc-X", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a05; color: #00ff00; font-family: 'Courier New', Courier, monospace; }
    .stButton>button { border: 1px solid #00ff00; background-color: black; color: #00ff00; }
    .stButton>button:hover { background-color: #003300; border: 1px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALISIERUNG ---
if 'game_state' not in st.session_state:
    # Zufällige Generierung des Szenarios
    assets = ["Bio-Reaktor Steuerung", "Zentrales Kundenregister", "HVAC-Kühlsystem"]
    threats = ["Ransomware-Verschlüsselung", "Daten-Exfiltration", "Integritäts-Manipulation"]
    
    st.session_state.game_state = "intro"
    st.session_state.asset = random.choice(assets)
    st.session_state.threat = random.choice(threats)
    st.session_state.stability = 100
    st.session_state.turn = 0
    st.session_state.log = []

def add_log(msg):
    st.session_state.log.insert(0, f"LOG_{st.session_state.turn:02d}: {msg}")
    st.session_state.turn += 1

# --- GAME ENGINE ---

# SIDEBAR: STATS
with st.sidebar:
    st.title("📟 TERMINAL")
    st.write(f"**Target:** {st.session_state.asset}")
    st.write(f"**Status:** {'ALARM' if st.session_state.stability < 50 else 'STABIL'}")
    st.progress(st.session_state.stability / 100)
    st.divider()
    for entry in st.session_state.log:
        st.caption(entry)

# SCREEN 1: INTRO
if st.session_state.game_state == "intro":
    st.title("⚡ OPERATION: SILENT SHIELD")
    st.write(f"""
    Willkommen, Administrator. 
    Ein unbekannter Akteur hat das System **{st.session_state.asset}** infiltriert. 
    Die Bedrohung wird als **{st.session_state.threat}** eingestuft.
    """)
    
    if st.button("Initialisiere BSI-Notfallprotokoll"):
        st.session_state.game_state = "analysis"
        st.rerun()

# SCREEN 2: SCHUTZBEDARFSANALYSE MIT ZUFALLS-FEEDBACK
elif st.session_state.game_state == "analysis":
    st.header("🔍 Schutzbedarfsfeststellung (Maximum-Prinzip)")
    st.write(f"Bestimmen Sie den Schutzbedarf für {st.session_state.asset} basierend auf der CIA-Triade.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        c = st.selectbox("Vertraulichkeit", ["Normal", "Hoch", "Sehr Hoch"])
    with col2:
        i = st.selectbox("Integrität", ["Normal", "Hoch", "Sehr Hoch"])
    with col3:
        a = st.selectbox("Verfügbarkeit", ["Normal", "Hoch", "Sehr Hoch"])

    if st.button("Analyse einloggen"):
        # Logik-Check: Integrität und Verfügbarkeit sind bei kritischen Systemen meist 'Sehr Hoch'
        correct_guess = (i == "Sehr Hoch" or a == "Sehr Hoch")
        
        if correct_guess:
            add_log("Analyse korrekt. Ressourcen priorisiert.")
            st.session_state.stability += 5
        else:
            impact = random.randint(15, 30)
            add_log(f"Fehleinschätzung! Systemstabilität sinkt um {impact}%.")
            st.session_state.stability -= impact
        
        st.session_state.game_state = "action"
        st.rerun()

# SCREEN 3: DYNAMISCHE ABWEHR
elif st.session_state.game_state == "action":
    st.header("🚨 RESPONSE PHASE")
    st.write(f"Der Angriff (**{st.session_state.threat}**) erreicht die nächste Stufe!")
    
    # Zufällige Ereignisse generieren
    events = [
        "Ein Administrator-Konto wurde kompromittiert!",
        "Der Backup-Server antwortet nicht mehr.",
        "Mitarbeiter melden seltsame Pop-ups an ihren Terminals."
    ]
    st.warning(random.choice(events))
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Isoliere das betroffene Netzwerk-Segment"):
            if random.random() > 0.3: # 70% Erfolgswahrscheinlichkeit
                add_log("Isolation erfolgreich. Ausbreitung gestoppt.")
                st.session_state.stability += 10
            else:
                add_log("Isolation fehlgeschlagen. Angreifer nutzt Tunnel.")
                st.session_state.stability -= 25
            
    with col2:
        if st.button("Führe Forensik-Scan durch (PDCA-Zyklus)"):
            add_log("Scan läuft... Schwachstelle identifiziert.")
            st.session_state.stability -= 5 # Zeitverlust kostet Stabilität
            st.info("Schwachstelle gefunden: Ungepatchter VPN-Zugang.")

    if st.session_state.stability <= 0:
        st.session_state.game_state = "game_over"
        st.rerun()
    elif st.session_state.turn > 5:
        st.session_state.game_state = "victory"
        st.rerun()

# SCREEN 4: GAME OVER / VICTORY
elif st.session_state.game_state == "game_over":
    st.error("💀 SYSTEM COLLAPSE")
    st.write("Das Restrisiko hat das Unternehmen zerstört. Die Integrität der Daten ist verloren.")
    if st.button("Neustart"):
        del st.session_state['game_state']
        st.rerun()

elif st.session_state.game_state == "victory":
    st.balloons()
    st.success("🏆 ANGRIFF ABGEWEHRT")
    st.write(f"Sie haben das System mit einer Rest-Stabilität von {st.session_state.stability}% gerettet.")
    st.write("Wichtige TOMs (Technisch-Organisatorische Maßnahmen) wurden dokumentiert.")
    if st.button("Neue Schicht antreten"):
        del st.session_state['game_state']
        st.rerun()
