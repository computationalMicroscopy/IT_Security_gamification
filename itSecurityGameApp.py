import streamlit as st
import random

# --- 1. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2000000, 'rep': 50,
            'cia': {'C': 60, 'I': 60, 'A': 60},
            'stress': 5, 'risk_exposure': 40,
            'staff': {'Admins': 1, 'Legal': 0, 'Security': 0},
            'layers': 0, # BSI Schichten 0-10
            'logs': ["> SYSTEM BOOT. WELCOME TO SILVER-DATA HQ."],
            'active_incidents': [],
            'decisions_made': 0,
            'game_over': False, 'won': False,
            'mode': 'tactical' # tactical, board, event
        }

init_game()
g = st.session_state.game

def add_log(msg, style="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff", "board": "#00d4ff"}
    g['logs'].insert(0, f"<span style='color:{colors.get(style)}'>[T-{g['day']}] {msg}</span>")

# --- 2. INTEL-DATENBANK ---
INTEL = {
    "BSI Schichten": "Modell mit 10 Ebenen (von Infrastruktur bis Anwendung). Höhere Schichten setzen sichere untere Schichten voraus.",
    "Maximumprinzip": "Die kritischste Komponente bestimmt das Gesamtniveau (Dok. 12).",
    "GoBD": "Vorgaben für digitale Buchführung (Integrität/Unveränderbarkeit).",
    "EU AI Act": "Verbot von Social Scoring. Hochrisiko-KI braucht Dokumentation (Dok. 15).",
    "Gefährdung G 0.18": "Fehlbedienung oder technisches Versagen (BSI Elementar-Gefährdung).",
    "DSGVO Art. 83": "Strafen bis 20 Mio. € oder 4% Umsatz (Dok. 15)."
}

# --- 3. UI STYLE ---
st.set_page_config(page_title="CISO Tactical 3.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #030303; color: #00ff41; font-family: 'Fira Code', monospace; }
    .status-card { background: #111; border: 1px solid #00ff41; padding: 10px; border-radius: 4px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 10px; height: 320px; overflow-y: auto; font-size: 0.8em; line-height: 1.2; }
    .incident-alert { background: #330000; border: 2px solid #ff0000; padding: 15px; color: white; margin: 10px 0; font-weight: bold; }
    .sidebar-intel { background: #1a1a1a; padding: 10px; border-radius: 5px; border-left: 3px solid #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📟 MISSION INTEL")
    st.markdown("---")
    st.subheader("👨‍💻 Dein Team")
    st.write(f"Admins: {g['staff']['Admins']} | Legal: {g['staff']['Legal']} | Security: {g['staff']['Security']}")
    if st.button("Spezialist einstellen (200k €)"):
        if g['budget'] >= 200000:
            role = random.choice(['Legal', 'Security'])
            g['staff'][role] += 1; g['budget'] -= 200000; add_log(f"{role}-Experte eingestellt."); st.rerun()
    st.markdown("---")
    st.subheader("📚 Knowledge Base")
    query = st.text_input("Suche...")
    for k, v in INTEL.items():
        if not query or query.lower() in k.lower():
            with st.expander(k): st.write(v)

# --- 5. DASHBOARD ---
st.title("🛡️ CISO Command: Project Silver-Data")
d1, d2, d3, d4, d5 = st.columns(5)
d1.markdown(f"<div class='status-card'>💰 BUDGET<br><b style='color:white'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
d2.markdown(f"<div class='status-card'>⚡ AP<br><b style='color:white'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
d3.markdown(f"<div class='status-card'>📉 RISK<br><b style='color:white'>{g['risk_exposure']}%</b></div>", unsafe_allow_html=True)
d4.markdown(f"<div class='status-card'>🏗️ BSI LAYERS<br><b style='color:white'>{g['layers']} / 10</b></div>", unsafe_allow_html=True)
d5.markdown(f"<div class='status-card'>🗓️ TAG<br><b style='color:white'>{g['day']} / 25</b></div>", unsafe_allow_html=True)

st.divider()

# CIA INDICATORS

c_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    c_cols[i].progress(max(0, min(100, v)))
    c_cols[i].write(f"<small>{label}: {v}%</small>", unsafe_allow_html=True)

# --- 6. GAME ENGINE ---
if g['game_over']:
    st.error("🚨 MISSION ABGEBROCHEN. Silver-Data ist gefallen."); st.stop()
if g['won']:
    st.balloons(); st.success("🏆 ZERTIFIZIERUNG ERREICHT! Silver-Data ist sicher."); st.stop()

# MODUS: BOARD MEETING (Alle 5 Tage)
if g['day'] % 5 == 0 and g['mode'] == 'board':
    st.markdown("<div class='status-card' style='border-color: #00d4ff;'>", unsafe_allow_html=True)
    st.subheader("🏛️ Vorstandssitzung: Quartalsbericht")
    questions = [
        ("Der Vorstand fragt: Gilt das Maximumprinzip auch für Cloud-Systeme?", "Ja (Dok. 12)", "Nur für On-Premise"),
        ("Warum müssen wir GoBD-Vorgaben einhalten?", "Für die Integrität der Finanzdaten", "Nur für die IT-Verfügbarkeit"),
        ("Marketing will eine KI zur Gesichtserkennung. Dein Urteil?", "Zulässig nach EU AI Act", "Verboten (Social Scoring)")
    ]
    q, a1, a2 = random.choice(questions)
    st.write(f"**Frage:** {q}")
    col_q1, col_q2 = st.columns(2)
    if col_q1.button(a1):
        g['budget'] += 100000; g['rep'] += 10; g['mode'] = 'tactical'; g['day'] += 1; g['ap'] = 5; add_log("Vorstand beeindruckt. Budget erhöht.", "board"); st.rerun()
    if col_q2.button(a2):
        g['budget'] -= 300000; g['rep'] -= 20; g['mode'] = 'tactical'; g['day'] += 1; g['ap'] = 5; add_log("Vorstand rügt dich. Budget gekürzt.", "error"); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# MODUS: TACTICAL (Standard)
col_main, col_term = st.columns([2, 1])

with col_main:
    # INCIDENTS FIRST
    if g['active_incidents']:
        for inc in g['active_incidents']:
            st.markdown(f"<div class='incident-alert'>🚨 {inc} aktiv! AP-Kosten für Lösung: 1</div>", unsafe_allow_html=True)
            if st.button(f"Gegenmaßnahme: {inc}"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['decisions_made'] += 1
                    g['cia']['I'] += 10; add_log(f"Bedrohung {inc} eliminiert."); st.rerun()

    # ACTIONS
    st.subheader("🎯 Tactical Operations")
    tabs = st.tabs(["🏗️ BSI-Defense", "🔍 Audit & Scan", "⚖️ Governance"])
    
    with tabs[0]:
        st.write("Baue die 10 Schichten des Grundschutzes auf.")
        if st.button(f"BSI Schicht {g['layers']+1} implementieren (150k € | 2 AP)"):
            if g['layers'] < 10 and g['ap'] >= 2 and g['budget'] >= 150000:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1; g['decisions_made'] += 1
                g['risk_exposure'] -= 5; g['cia']['A'] += 10; add_log(f"Schicht {g['layers']} aktiv."); st.rerun()
    
    with tabs[1]:
        if st.button("Vulnerability Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['stress'] += 10; g['decisions_made'] += 1
                if random.random() > (0.8 - (g['staff']['Security']*0.1)):
                    g['active_incidents'].append(random.choice(["SQL-Injection", "Brute Force", "G 0.18"]))
                    add_log("Schwachstelle gefunden!", "error")
                else: add_log("Scan sauber."); st.rerun()

    with tabs[2]:
        if st.button("Interne Revision (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['decisions_made'] += 1
                g['rep'] += 5; add_log("Dokumentation nach GoBD geprüft."); st.rerun()

with col_term:
    st.subheader("📟 Terminal")
    log_content = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_content}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("⏭️ TAG BEENDEN"):
        # Übernacht-Effekte
        g['stress'] = max(0, g['stress'] - (5 + g['staff']['Admins']))
        for k in g['cia']: g['cia'][k] -= random.randint(2, 6)
        
        if g['active_incidents']:
            for _ in g['active_incidents']:
                g['cia']['I'] -= 10; g['budget'] -= 50000
            add_log("Nicht gelöste Bedrohungen haben Schaden verursacht!", "error")
        
        # Check Sieg/Niederlage
        if g['day'] >= 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0 or g['stress'] >= 100: g['game_over'] = True
        
        # Board Meeting Trigger
        if g['day'] % 5 == 0: g['mode'] = 'board'
        else: g['day'] += 1; g['ap'] = 5
        st.rerun()
