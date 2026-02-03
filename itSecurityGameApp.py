import streamlit as st
import random

# --- 1. ROBUSTE INITIALISIERUNG (Fix für alle KeyErrors) ---
def start_simulation():
    st.session_state.game = {
        'day': 1,
        'ap': 4,
        'budget': 750000,
        'rep': 60,
        'cia': {'C': 50, 'I': 50, 'A': 50},
        'logs': ["> SYSTEM BOOT: CISO-Terminal aktiv."],
        'active_incident': None,
        'game_over': False,
        'won': False
    }

if 'game' not in st.session_state:
    start_simulation()

def add_log(msg, type="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    st.session_state.game['logs'].insert(0, f"<span style='color:{colors.get(type)}'>[Tag {st.session_state.game['day']}] {msg}</span>")

# --- 2. INTEL-DATENBANK (Dein Glossar) ---
INTEL_DB = {
    "10 Schichten (BSI)": "Systematik des IT-Grundschutzes. Jede Ebene (von Infrastruktur bis App) muss abgesichert sein.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 bis G 0.47), die laut BSI zwingend geprüft werden müssen.",
    "Maximumprinzip": "Das Schutzniveau des Gesamtsystems richtet sich nach der kritischsten Komponente (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Buchführung. Fordert Integrität (Unveränderbarkeit) von Daten (Dok. 13).",
    "DSGVO Art. 83": "Strafmaß: Bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes bei Datenverlust.",
    "EU AI Act": "Verbot von Social Scoring (Unannehmbar). Strenge Regeln für Hochrisiko-KI.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Die Methode zur ständigen Verbesserung der IT-Sicherheit."
}

# --- 3. UI STYLE ---
st.set_page_config(page_title="CISO Command 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace; }
    .status-card { background: #111; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.9em; border-left: 5px solid #ff00ff; }
    .stButton>button { border: 1px solid #00ff41; background: #0b0e14; color: #00ff41; width: 100%; height: 3em; font-weight: bold; }
    .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SEITENLEISTE (Das Wissen) ---
with st.sidebar:
    st.title("📟 INTEL CENTER")
    st.markdown("**Szenario:** Du hast 14 Tage bis zum Audit. Halte die Firma am Leben.")
    st.divider()
    st.subheader("📚 Sicherheits-Glossar")
    search = st.text_input("Suchen...", help="Begriffe aus den PDFs nachschlagen")
    for key, val in INTEL_DB.items():
        if not search or search.lower() in key.lower():
            with st.expander(key):
                st.write(val)

# --- 5. LOGIK-CHECKS ---
if st.session_state.game['game_over']:
    st.error("🚨 MISSION FEHLGESCHLAGEN: Silver-Data ist insolvent oder gehackt.")
    if st.button("Neu starten"):
        start_simulation()
        st.rerun()
    st.stop()

if st.session_state.game['won']:
    st.balloons()
    st.success("🏆 AUDIT BESTANDEN! Du bist ein Master-CISO.")
    if st.button("Nochmal spielen"):
        start_simulation()
        st.rerun()
    st.stop()

# --- 6. DASHBOARD ---
st.title("🖥️ CISO Command: Silver-Data GmbH")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='status-card'>💰 BUDGET<br><span style='font-size:1.5em; color:white'>{st.session_state.game['budget']:,}€</span></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='status-card'>⚡ AKTIONEN<br><span style='font-size:1.5em; color:white'>{st.session_state.game['ap']} AP</span></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='status-card'>🗓️ TAG<br><span style='font-size:1.5em; color:white'>{st.session_state.game['day']} / 14</span></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='status-card'>🛡️ REPUTATION<br><span style='font-size:1.5em; color:white'>{st.session_state.game['rep']}%</span></div>", unsafe_allow_html=True)

st.divider()

# CIA-VISUALISIERUNG
st.write("### 🔒 Schutzziele-Status (CIA)")

cols = st.columns(3)
for i, (k, v) in enumerate(st.session_state.game['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 7. TACTICAL OPERATIONS ---
left, right = st.columns([2, 1])

with left:
    st.subheader("🛠️ Strategische Maßnahmen")
    t1, t2, t3 = st.tabs(["🏗️ Prävention (Plan/Do)", "🔎 Analyse (Check)", "⚖️ Compliance (Act)"])
    
    with t1:
        if st.button("BSI-Infrastruktur-Härtung (100k€ | 2 AP)"):
            if st.session_state.game['ap'] >= 2 and st.session_state.game['budget'] >= 100000:
                st.session_state.game['ap'] -= 2
                st.session_state.game['budget'] -= 100000
                st.session_state.game['cia']['A'] += 20
                st.session_state.game['cia']['I'] += 10
                add_log("BSI-Schichten 1-5 verstärkt.")
                st.rerun()
        
        if st.button("Awareness-Kampagne (40k€ | 1 AP)"):
            if st.session_state.game['ap'] >= 1 and st.session_state.game['budget'] >= 40000:
                st.session_state.game['ap'] -= 1
                st.session_state.game['budget'] -= 40000
                st.session_state.game['cia']['C'] += 15
                add_log("Mitarbeiter auf Barclays-Phishing sensibilisiert.")
                st.rerun()

    with t2:
        if st.button("Schwachstellen-Scan (1 AP)"):
            if st.session_state.game['ap'] >= 1:
                st.session_state.game['ap'] -= 1
                if random.random() > 0.5:
                    st.session_state.game['active_incident'] = "SQL"
                    add_log("KRITISCH: SQL-Injection in Preisdatenbank gefunden!", "error")
                else:
                    add_log("System-Scan ohne Befund.")
                st.rerun()

    with t3:
        st.warning("Prüfung: Geplanter Einsatz von 'Social Scoring' für Kunden.")
        ans = st.radio("Wie ist Social Scoring im EU AI Act klassifiziert?", ["Hochrisiko", "Unannehmbares Risiko (Verboten)"], index=None)
        if st.button("Rechtliche Prüfung abschließen (1 AP)"):
            if st.session_state.game['ap'] >= 1:
                st.session_state.game['ap'] -= 1
                if ans == "Unannehmbares Risiko (Verboten)":
                    st.success("Korrekt! Projekt gestoppt.")
                    st.session_state.game['rep'] += 15
                else:
                    st.error("FALSCH! DSGVO-Bußgeld fällig (4% vom Budget).")
                    st.session_state.game['budget'] *= 0.96
                    st.session_state.game['rep'] -= 25
                st.rerun()

    if st.session_state.game['active_incident'] == "SQL":
        st.error("🚨 AKTIVER ANGRIFF: Preismanipulation (GoBD-Gefahr!)")
        if st.button("Gegenmaßnahme: Input-Validierung (1 AP)"):
            st.session_state.game['ap'] -= 1
            st.session_state.game['active_incident'] = None
            st.session_state.game['cia']['I'] = min(100, st.session_state.game['cia']['I'] + 30)
            add_log("Datenintegrität wiederhergestellt.")
            st.rerun()

with right:
    st.subheader("📟 Logs")
    log_content = "".join([f"<div>{l}</div>" for l in st.session_state.game['logs']])
    st.markdown(f"<div class='terminal'>{log_content}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🌞 TAG BEENDEN"):
        st.session_state.game['day'] += 1
        st.session_state.game['ap'] = 4
        # Entropie (Werte sinken)
        for k in st.session_state.game['cia']:
            st.session_state.game['cia'][k] -= random.randint(5, 15)
        add_log("Neuer Tag. Die Bedrohungslage hat sich verschärft.")
        
        if st.session_state.game['day'] > 14:
            st.session_state.game['won'] = True
        if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
            st.session_state.game['game_over'] = True
        st.rerun()
