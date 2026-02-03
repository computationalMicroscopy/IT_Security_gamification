import streamlit as st
import random

# --- 1. ABSOLUT ROBUSTE INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1,
            'ap': 4,
            'budget': 800000,
            'rep': 50,
            'cia': {'C': 60, 'I': 60, 'A': 60},
            'logs': ["> SYSTEM READY. Welcome to Silver-Data Command."],
            'active_incident': None,
            'game_over': False,
            'won': False
        }

init_game()

def add_log(msg, style="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    st.session_state.game['logs'].insert(0, f"<span style='color:{colors.get(style)}'>[Tag {st.session_state.game['day']}] {msg}</span>")

# --- 2. DAS CYBER-LEXIKON (Glossar) ---
LEXIKON = {
    "10 Schichten (BSI)": "Struktur des IT-Grundschutzes. Jede Ebene (von Infrastruktur bis Anwendung) muss abgesichert werden.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 bis G 0.47), die laut BSI die Basis jeder Risikoanalyse bilden.",
    "Maximumprinzip": "Das Schutzniveau eines IT-Verbunds richtet sich nach dem Baustein mit dem höchsten Schutzbedarf (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Buchführung. Fordert Integrität (Unveränderbarkeit) digitaler Daten (Dok. 13).",
    "DSGVO Art. 83": "Strafmaß: Bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes bei schweren Datenlecks.",
    "EU AI Act": "Risikoklassen: Unannehmbar (Verboten, z.B. Social Scoring), Hoch (Strenge Auflagen), Minimal.",
    "Authentizität": "Prüfbarkeit der Herkunft. Ein Teilaspekt der Integrität nach BSI-Definition.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Der Motor für kontinuierliche Verbesserung in der Informationssicherheit."
}

# --- 3. UI & STYLING ---
st.set_page_config(page_title="Silver-Data: CISO Command", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace; }
    .stat-box { background: #111; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.85em; border-left: 4px solid #ff00ff; }
    .stButton>button { border: 1px solid #00ff41; background: #0b0e14; color: #00ff41; width: 100%; height: 3.5em; font-weight: bold; }
    .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (Szenario & Lexikon) ---
with st.sidebar:
    st.title("📟 COMMAND INTEL")
    st.info("**Szenario:** Silver-Data GmbH verwaltet Goldreserven. In 10 Tagen findet das BSI-Audit statt. Deine CIA-Werte sinken täglich durch technisches Altern und Hacker-Angriffe. Halte die Firma stabil!")
    st.divider()
    st.subheader("📚 Cyber-Lexikon")
    query = st.text_input("Begriff suchen...", help="Nutze das Wissen aus den PDFs!")
    for k, v in LEXIKON.items():
        if not query or query.lower() in k.lower():
            with st.expander(k):
                st.write(v)

# --- 5. GAME OVER & WIN CHECKS ---
g = st.session_state.game
if g.get('game_over'):
    st.error("🚨 MISSION FEHLGESCHLAGEN: Die Silver-Data GmbH wurde gehackt oder ist insolvent.")
    if st.button("Simulation Neustarten"):
        init_game(force=True)
        st.rerun()
    st.stop()

if g.get('won'):
    st.balloons()
    st.success("🏆 AUDIT BESTANDEN! Du bist ein Master-CISO.")
    if st.button("Erneut spielen"):
        init_game(force=True)
        st.rerun()
    st.stop()

# --- 6. DASHBOARD ---
st.title("🛡️ CISO Strategy Command: Silver-Data")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-box'>💰 BUDGET<br><b style='font-size:1.4em; color:white'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>⚡ AKTIONEN<br><b style='font-size:1.4em; color:white'>{g['ap']} AP</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>🗓️ TAG<br><b style='font-size:1.4em; color:white'>{g['day']} / 10</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-box'>📈 RUF<br><b style='font-size:1.4em; color:white'>{g['rep']}%</b></div>", unsafe_allow_html=True)

st.divider()

# CIA PROGRESS BARS
st.write("### 🔒 Aktueller CIA-Schutzstatus")

cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 7. TACTICAL OPERATIONS ---
col_act, col_log = st.columns([2, 1])

with col_act:
    st.subheader("🛠️ Verfügbare Operationen")
    t1, t2, t3 = st.tabs(["🏗️ Bauen (Do)", "🔍 Scannen (Check)", "⚖️ Compliance (Act)"])
    
    with t1:
        if st.button("BSI-Schichten 1-5 härten (120k € | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 120000:
                g['ap'] -= 2
                g['budget'] -= 120000
                g['cia']['A'] += 20; g['cia']['I'] += 15
                add_log("Infrastruktur nach BSI-Standard gehärtet.")
                st.rerun()
        if st.button("Awareness-Training (30k € | 1 AP)"):
            if g['ap'] >= 1 and g['budget'] >= 30000:
                g['ap'] -= 1
                g['budget'] -= 30000
                g['cia']['C'] += 15
                add_log("Mitarbeiter gegen Phishing (Barclays-Methode) geschult.")
                st.rerun()

    with t2:
        if st.button("Schwachstellen-Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1
                if random.random() > 0.5:
                    g['active_incident'] = "SQL"
                    add_log("KRITISCH: SQL-Injection in Preis-Datenbank gefunden!", "error")
                else:
                    add_log("Scan sauber. Keine Anomalien detektiert.")
                st.rerun()

    with t3:
        st.warning("Prüfung: Geplanter Einsatz von 'Social Scoring' KI.")
        choice = st.radio("Einstufung laut EU AI Act?", ["Hochrisiko", "Unannehmbares Risiko (Verboten)"], index=None)
        if st.button("Urteil fällen (1 AP)"):
            if g['ap'] >= 1 and choice:
                g['ap'] -= 1
                if choice == "Unannehmbares Risiko (Verboten)":
                    st.success("Korrekt! Projekt gestoppt.")
                    g['rep'] += 10
                else:
                    st.error("FALSCH! DSGVO-Bußgeld fällig (4% vom Budget).")
                    g['budget'] *= 0.96
                    g['rep'] -= 20
                st.rerun()

    # INCIDENT MANAGEMENT
    if g.get('active_incident') == "SQL":
        st.markdown("<div style='border:2px solid #ff00ff; padding:15px; border-radius:5px;'>", unsafe_allow_html=True)
        st.error("🚨 AKTIVER ANGRIFF: Preismanipulation (GoBD-Gefahr!)")
        if st.button("Incident lösen (1 AP)"):
            g['ap'] -= 1
            g['active_incident'] = None
            g['cia']['I'] = min(100, g['cia']['I'] + 30)
            add_log("Datenintegrität wiederhergestellt.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_log:
    st.subheader("📟 Terminal")
    logs_html = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{logs_html}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🌞 TAG BEENDEN"):
        g['day'] += 1
        g['ap'] = 4
        for k in g['cia']: g['cia'][k] -= random.randint(5, 12) # Werte-Verschleiß
        add_log("Neuer Arbeitstag. Bedrohungslage hat sich verschärft.", "warn")
        
        if g['day'] > 10: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0:
            g['game_over'] = True
        st.rerun()
