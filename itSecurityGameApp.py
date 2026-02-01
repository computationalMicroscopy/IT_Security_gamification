import streamlit as st
import time

# --- INITIALISIERUNG ---
if 'step' not in st.session_state:
    st.session_state.step = "intro"
if 'security_level' not in st.session_state:
    st.session_state.security_level = 50  # Startwert Sicherheit
if 'integrity_corrupted' not in st.session_state:
    st.session_state.integrity_corrupted = False
if 'logs' not in st.session_state:
    st.session_state.logs = []

def log_event(event):
    st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] {event}")

# --- UI SETTINGS ---
st.set_page_config(page_title="Silent Leak: Operation Deepwater", layout="wide")

# --- CSS FÜR TERMINAL-LOOK ---
st.markdown("""
    <style>
    .reportview-container { background: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #262730; color: white; }
    .stProgress > div > div > div > div { background-color: #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: SYSTEM STATUS ---
with st.sidebar:
    st.title("📟 System-Monitor")
    st.metric("Netzwerk-Stabilität", f"{st.session_state.security_level}%")
    st.progress(st.session_state.security_level / 100)
    
    st.subheader("Ereignis-Protokoll")
    for log in st.session_state.logs[:5]:
        st.caption(log)
    
    if st.button("System Reset"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --- HAUPT-LOGIK ---

# 1. INTRO
if st.session_state.step == "intro":
    st.title("🌊 Operation Deepwater")
    st.subheader("Standort: Wasserwerk 'Aqua-Tech' Nord")
    st.markdown("""
    Sie wurden als IT-Sicherheitsbeauftragter mitten in der Nacht gerufen. 
    Das Fernwartungssystem der Chlorierungsanlage zeigt seltsame Anomalien. 
    
    Ein unbekannter Akteur scheint Zugriff auf das System **'HydroControl 4.0'** zu haben. 
    Dieses System verwaltet Chemikalien-Dosierungen und Kundendaten für die Abrechnung.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Schutzbedarfsanalyse starten"):
            st.session_state.step = "analysis"
            st.rerun()
    with col2:
        st.warning("⚠️ Die Zeit läuft. Jede Sekunde ohne Analyse erhöht das Restrisiko.")

# 2. SCHUTZBEDARFSANALYSE (Interaktive Tabelle)
elif st.session_state.step == "analysis":
    st.header("📋 Phase 1: Schutzbedarfsanalyse (Maximumsprinzip)")
    st.write("Bewerten Sie die Risiken für 'HydroControl 4.0' gemäß BSI-Standard.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        v_conf = st.select_slider("Vertraulichkeit (Kundendaten)", ["Normal", "Hoch", "Sehr Hoch"], value="Normal")
    with c2:
        v_int = st.select_slider("Integrität (Chemikalien-Mix)", ["Normal", "Hoch", "Sehr Hoch"], value="Normal")
    with c3:
        v_avail = st.select_slider("Verfügbarkeit (Wasserfluss)", ["Normal", "Hoch", "Sehr Hoch"], value="Normal")

    if st.button("Analyse bestätigen"):
        # Logik basierend auf PDFs: Integrität beim Wasserwerk ist lebenswichtig (Sehr Hoch)
        if v_int == "Sehr Hoch":
            st.success("Korrekt! Eine Manipulation der Chemikalien (Integrität) ist existenzbedrohend (Leib und Leben).")
            st.session_state.security_level += 10
        else:
            st.error("Gefährliche Fehleinschätzung! Wenn die Integrität der Mischverhältnisse sinkt, besteht Lebensgefahr.")
            st.session_state.security_level -= 20
        
        log_event(f"Analyse abgeschlossen. Gesamt-Schutzbedarf: SEHR HOCH (Maximumsprinzip).")
        st.session_state.step = "incident_loop"
        st.rerun()

# 3. DER INCIDENT (Dynamische Entscheidungen)
elif st.session_state.step == "incident_loop":
    st.header("🚨 KRITISCHER ZWISCHENFALL")
    st.error("WARNUNG: Die Sensorwerte für den Chlorgehalt steigen unkontrolliert an, obwohl die Anzeige im Dashboard 'Normal' meldet!")
    
    st.write("Das ist ein klassischer Angriff auf die **Integrität**. Was tun Sie?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Not-Abschaltung des Systems (Verfügbarkeit opfern)"):
            log_event("System-Shutdown initiiert.")
            st.session_state.security_level += 20
            st.session_state.step = "consequence_shutdown"
            st.rerun()
            
    with col2:
        if st.button("Passwort des Admin-Accounts ändern"):
            log_event("Passwort geändert. Angriff läuft weiter.")
            st.session_state.security_level -= 30
            st.session_state.step = "consequence_fail"
            st.rerun()

# 4. KONSEQUENZEN
elif st.session_state.step == "consequence_shutdown":
    st.success("✅ Kluge Entscheidung!")
    st.write("""
    Durch die Priorisierung der **Integrität** vor der **Verfügbarkeit** haben Sie eine Vergiftung des Trinkwassers verhindert. 
    Zwar ist die Stadt nun ohne Wasser, aber die Gefahr für Leib und Leben ist gebannt.
    """)
    if st.button("Abschlussbericht erstellen"):
        st.session_state.step = "final"
        st.rerun()

elif st.session_state.step == "consequence_fail":
    st.error("❌ KATASTROPHE")
    st.write("""
    Eine Passwortänderung reicht nicht aus, wenn der Angreifer bereits eine Backdoor im System hat. 
    Während Sie tippten, wurde eine toxische Menge Chlor freigesetzt. Das Restrisiko hat sich realisiert.
    """)
    if st.button("Vor den Untersuchungsausschuss treten"):
        st.session_state.step = "final"
        st.rerun()

# 5. FINALE & REFLEKTION
elif st.session_state.step == "final":
    st.title("🏁 Mission beendet")
    st.metric("Finaler Sicherheits-Score", f"{st.session_state.security_level}%")
    
    st.subheader("Ihre Learnings nach Dr. Yahiatène:")
    st.write("- **Maximumsprinzip:** Sie haben gelernt, dass der höchste Einzelwert den Gesamtschutzbedarf bestimmt.")
    st.write("- **CIA-Triade im Konflikt:** Manchmal muss man die Verfügbarkeit opfern, um die Integrität zu retten.")
    st.write("- **Mitwirkungspflicht:** Technik allein rettet nicht, es sind Ihre Entscheidungen.")
    
    if st.button("Neues Szenario (Reset)"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
