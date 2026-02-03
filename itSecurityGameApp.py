import streamlit as st
import random

# --- INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'day': 1,
        'ap': 3,
        'budget': 450000,
        'cia': {'C': 80, 'I': 85, 'A': 90},
        'rep': 75,
        'logs': ["> Initializing Neural Link...", "> Login: CISO_ADMIN", "> Status: Critical vulnerabilities detected."],
        'unlocked_intel': set(),
        'incident': None,
        'goal_reached': False
    }

# --- GLOSSAR / INTEL DATABASE ---
INTEL_DB = {
    "10 Schichten": "Die BSI-Systematik unterteilt die IT-Landschaft in 10 Schichten (z.B. Infrastruktur, Netznetze, Anwendungen).",
    "47 Gefährdungen": "Das BSI-Kompendium definiert 47 elementare Gefährdungen (G 0.1 - G 0.47) als Basis für Risikoanalysen.",
    "Maximumprinzip": "Der Schutzbedarf eines Systems entspricht dem höchsten Schutzbedarf seiner Komponenten (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Führung elektronischer Bücher. Fordert Unveränderbarkeit (Integrität).",
    "DSGVO Art. 83": "Geldbußen bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes bei Datenverlust.",
    "EU AI Act": "Reguliert KI nach Risikoklassen: Unannehmbar (verboten), Hoch, Transparenz, Minimal.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Der kontinuierliche Verbesserungsprozess für Informationssicherheit.",
    "Authentizität": "Teilziel der Integrität. Stellt sicher, dass Daten echt und dem Absender zuordbar sind."
}

# --- CSS FÜR SPIEL-OPTIK ---
st.set_page_config(page_title="Silver-Data: Neon Guardian", layout="wide")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;500&display=swap');
    
    .stApp { background-color: #050505; color: #00ffc3; font-family: 'Fira Code', monospace; }
    .main-header { font-size: 3rem; color: #ff00ff; text-shadow: 0 0 10px #ff00ff; text-align: center; }
    .status-card { background: rgba(25, 25, 25, 0.9); border: 1px solid #00ffc3; padding: 15px; border-radius: 5px; box-shadow: 0 0 15px rgba(0, 255, 195, 0.2); }
    .terminal { background: #000; border: 1px solid #ff00ff; color: #ff00ff; padding: 20px; border-radius: 5px; height: 300px; overflow-y: auto; margin-bottom: 20px; }
    .intel-box { background: #111; border-left: 4px solid #00ffc3; padding: 10px; margin: 5px 0; color: #e0e0e0; }
    .stButton>button { background: #1a1a1a; color: #00ffc3; border: 1px solid #00ffc3; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background: #00ffc3; color: #000; box-shadow: 0 0 20px #00ffc3; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTIONEN ---
def add_log(msg):
    st.session_state.game['logs'].insert(0, f"> {msg}")

def process_day():
    st.session_state.game['day'] += 1
    st.session_state.game['ap'] = 3
    # Leichte Verschlechterung der Werte durch "Alltags-Entropie"
    for key in st.session_state.game['cia']:
        st.session_state.game['cia'][key] -= random.randint(1, 5)

# --- SPIEL-LOGIK ---
st.markdown("<h1 class='main-header'>OPERATION: SILVER-DATA</h1>", unsafe_allow_html=True)

# SZENARIO BESCHREIBUNG
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/security-shield.png")
    st.subheader("📍 Szenario: Silver-Data GmbH")
    st.write("""
    **Mission:** Du bist der neue CISO der Silver-Data GmbH. 
    Das Unternehmen verwaltet hochsensible Gold-Handelsdaten und Kunden-IBANs. 
    Die BSI-Zertifizierung steht an, aber Hacker-Gruppen haben dich im Visier.
    
    **Ziel:** Überlebe 10 Tage, halte CIA über 50% und vermeide rechtliche Sanktionen.
    """)
    st.divider()
    st.subheader("📚 Intel-Datenbank (Glossar)")
    search = st.text_input("Begriff suchen...", "").strip()
    for key, val in INTEL_DB.items():
        if not search or search.lower() in key.lower():
            st.markdown(f"<div class='intel-box'><b>{key}:</b><br>{val}</div>", unsafe_allow_html=True)

# STATUS DASHBOARD
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f"<div class='status-card'>💰 BUDGET<br><span style='color:white'>{st.session_state.game['budget']:,} €</span></div>", unsafe_allow_html=True)
with c2: st.markdown(f"<div class='status-card'>⚡ AKTIONEN<br><span style='color:white'>{st.session_state.game['ap']} AP</span></div>", unsafe_allow_html=True)
with c3: st.markdown(f"<div class='status-card'>📈 REPUTATION<br><span style='color:white'>{st.session_state.game['rep']}%</span></div>", unsafe_allow_html=True)
with c4: st.markdown(f"<div class='status-card'>🗓️ TAG<br><span style='color:white'>{st.session_state.game['day']} / 10</span></div>", unsafe_allow_html=True)

st.write("---")

# CIA PROGRESS BARS
st.write("### 🔒 Schutzziele (CIA Triade)")

cols = st.columns(3)
for i, (key, val) in enumerate(st.session_state.game['cia'].items()):
    label = {"C": "Vertraulichkeit (Confidentiality)", "I": "Integrität (Integrity)", "A": "Verfügbarkeit (Availability)"}[key]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, val)))

# HAUPTBEREICH
col_actions, col_terminal = st.columns([2, 1])

with col_actions:
    tab_ops, tab_defense, tab_legal = st.tabs(["🚀 Operationen", "🛡️ BSI-Abwehr", "⚖️ Rechtsabteilung"])
    
    with tab_ops:
        st.write("### Tägliche Operationen")
        if st.button("Logs nach Anomalien scannen (1 AP)"):
            if st.session_state.game['ap'] > 0:
                st.session_state.game['ap'] -= 1
                event = random.choice(["PHISH", "SQL", "CLEAN"])
                if event == "PHISH":
                    st.session_state.game['incident'] = "PHISH"
                    add_log("ALARM: Barclays-Phishing-Mail erkannt!")
                elif event == "SQL":
                    st.session_state.game['incident'] = "SQL"
                    add_log("WARNUNG: SQL-Injection-Versuch auf Preislisten-DB!")
                else:
                    add_log("Systeme sauber. Keine Bedrohung gefunden.")
                st.rerun()

        if st.session_state.game['incident']:
            inc = st.session_state.game['incident']
            st.error(f"⚠️ AKTIVER INCIDENT: {inc}")
            if inc == "PHISH":
                st.write("Ein Mitarbeiter hat geklickt. Wie reagierst du?")
                if st.button("Mitwirkungspflicht einfordern (Schulung) - 1 AP"):
                    st.session_state.game['ap'] -= 1
                    st.session_state.game['incident'] = None
                    st.session_state.game['cia']['C'] += 10
                    add_log("Mitarbeiter geschult. Risiko minimiert.")
                    st.rerun()
            if inc == "SQL":
                st.write("Preise werden manipuliert (GoBD Verstoß!).")
                if st.button("Integritäts-Check & Patch - 1 AP"):
                    st.session_state.game['ap'] -= 1
                    st.session_state.game['incident'] = None
                    st.session_state.game['cia']['I'] += 15
                    add_log("Datenbank-Integrität wiederhergestellt.")
                    st.rerun()

    with tab_defense:
        st.write("### BSI-Grundschutz Ausbau (PDCA)")
        
        if st.button("In 10 Schichten der Systematik investieren (120k € | 2 AP)"):
            if st.session_state.game['budget'] >= 120000 and st.session_state.game['ap'] >= 2:
                st.session_state.game['budget'] -= 120000
                st.session_state.game['ap'] -= 2
                for k in st.session_state.game['cia']: st.session_state.game['cia'][k] += 20
                add_log("BSI-Infrastruktur massiv verstärkt.")
                st.rerun()

    with tab_legal:
        st.write("### Compliance & Audits")
        st.warning("KI-Projekt 'Social Scoring' steht an.")
        if st.button("Risikoanalyse nach EU AI Act (1 AP)"):
            if st.session_state.game['ap'] > 0:
                st.session_state.game['ap'] -= 1
                st.info("Das BSI fragt: Welche Risikoklasse hat Social Scoring?")
                choice = st.radio("Entscheidung:", ["Hohes Risiko", "Unannehmbares Risiko (Verboten)"], index=None)
                if choice == "Unannehmbares Risiko (Verboten)":
                    st.success("Korrekt! Projekt gestoppt. Keine Bußgelder.")
                    st.session_state.game['rep'] += 10
                elif choice:
                    st.error("FALSCH! DSGVO Bußgeld fällig (4% vom Budget).")
                    st.session_state.game['budget'] *= 0.96
                    st.session_state.game['rep'] -= 30
                st.rerun()

with col_terminal:
    st.write("### 📟 Terminal Output")
    log_content = "\n".join(st.session_state.game['logs'])
    st.markdown(f"<div class='terminal'>{log_content}</div>", unsafe_allow_html=True)
    
    if st.button("🌞 TAG BEENDEN"):
        process_day()
        st.rerun()

# GAME OVER LOGIC
if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
    st.error("🚨 GAME OVER - SYSTEM BREACH")
    if st.button("Simulation Neustarten"):
        del st.session_state['game']
        st.rerun()
elif st.session_state.game['day'] > 10:
    st.balloons()
    st.success("🏆 MISSION ERFOLGREICH! Silver-Data ist zertifiziert.")
