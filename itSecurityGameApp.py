import streamlit as st
import random

# --- 1. ROBUSTE INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1,
            'ap': 4,
            'budget': 1500000, 
            'rep': 60,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'logs': ["> INITIALIZING LONG-TERM DEFENSE PROTOCOL..."],
            'active_incident': None,
            'decisions_made': 0,
            'game_over': False,
            'won': False,
            'daily_event_active': False
        }

init_game()
g = st.session_state.game

def add_log(msg, style="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    g['logs'].insert(0, f"<span style='color:{colors.get(style)}'>[Tag {g['day']}] {msg}</span>")

# --- 2. INTEL-DATENBANK (GLOSSAR) ---
INTEL = {
    "10 Schichten (BSI)": "Struktur des IT-Grundschutzes: Infrastruktur, Netz, IT-Systeme, Anwendungen, etc.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 - G 0.47) wie Feuer, Hacker oder Fehlbedienung (Dok. 16).",
    "Maximumprinzip": "Der Schutzbedarf eines Systems richtet sich nach der kritischsten Komponente (Dok. 12).",
    "GoBD Integrität": "Unveränderbarkeit digitaler Belege ist Pflicht. Integrität muss gewahrt bleiben (Dok. 13).",
    "DSGVO Art. 83": "Geldbußen bis zu 4% des Jahresumsatzes bei schweren Datenschutzverstößen.",
    "EU AI Act": "Verbot von Social Scoring (Unannehmbar). Strenge Regeln für Hochrisiko-KI (Dok. 15).",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Methode zur kontinuierlichen Verbesserung des ISMS.",
    "Authentizität": "Echtheit und Nachweisbarkeit der Herkunft von Daten. Teil der Integrität."
}

# --- 3. UI & STYLING ---
st.set_page_config(page_title="CISO Simulator 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace; }
    .stat-box { background: #111; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.85em; border-left: 4px solid #ff00ff; }
    .stButton>button { border: 1px solid #00ff41; background: #0b0e14; color: #00ff41; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    .event-card { background: #161b22; border: 2px solid #f2cc60; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📟 INTEL CENTER")
    st.info("**Szenario:** Silver-Data GmbH. Du hast 25 Tage bis zum großen Audit. Jede Entscheidung zählt!")
    st.divider()
    st.subheader("📚 Sicherheits-Glossar")
    search = st.text_input("Begriff suchen...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k):
                st.write(v)

# --- 5. GAME LOGIC ---
if g['game_over']:
    st.error("🚨 SYSTEM COLLAPSE: Die Firma Silver-Data ist insolvent oder wurde gehackt.")
    if st.button("Simulation Neustarten"):
        init_game(True); st.rerun()
    st.stop()

if g['won']:
    st.balloons()
    st.success(f"🏆 AUDIT BESTANDEN! Du hast {g['decisions_made']} Entscheidungen getroffen.")
    if st.button("Erneut spielen"):
        init_game(True); st.rerun()
    st.stop()

# --- 6. DASHBOARD ---
st.title("🛡️ CISO Defense Command")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-box'>💰 BUDGET<br><b style='color:white'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>⚡ AKTIONEN (AP)<br><b style='color:white'>{g['ap']} / 4</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>🗓️ TAG<br><b style='color:white'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-box'>⚖️ TASKS DONE<br><b style='color:white'>{g['decisions_made']}</b></div>", unsafe_allow_html=True)

st.divider()

cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 7. TACTICAL OPERATIONS ---
col_act, col_log = st.columns([2, 1])

with col_act:
    if not g['daily_event_active']:
        st.subheader("🛠️ Taktische Maßnahmen")
        t1, t2, t3 = st.tabs(["🏗️ Bauen (Do)", "🔍 Scannen (Check)", "⚖️ Compliance (Act)"])
        
        with t1:
            if st.button("BSI-Schichten absichern (100k € | 2 AP)"):
                if g['ap'] >= 2 and g['budget'] >= 100000:
                    g['ap'] -= 2; g['budget'] -= 100000; g['decisions_made'] += 1
                    g['cia']['A'] += 15; g['cia']['I'] += 10; add_log("Infrastruktur gehärtet."); st.rerun()
            if st.button("Awareness Training (30k € | 1 AP)"):
                if g['ap'] >= 1 and g['budget'] >= 30000:
                    g['ap'] -= 1; g['budget'] -= 30000; g['decisions_made'] += 1
                    g['cia']['C'] += 15; add_log("Mitarbeiter geschult."); st.rerun()

        with t2:
            if st.button("System-Audit (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['decisions_made'] += 1
                    if random.random() > 0.4:
                        g['active_incident'] = random.choice(["SQL", "Ransomware"])
                        add_log("ALARM: Bedrohung gefunden!", "error")
                    else: add_log("Audit unauffällig."); st.rerun()

        with t3:
            st.write("Rechtliche Prüfungen")
            if st.button("Prüfung: AI Act (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['decisions_made'] += 1
                    add_log("AI Act Compliance wird geprüft..."); st.rerun()

        if g['active_incident']:
            st.error(f"⚠️ INCIDENT: {g['active_incident']}")
            if st.button("Incident lösen (1 AP)"):
                g['ap'] -= 1; g['decisions_made'] += 1; g['active_incident'] = None
                g['cia']['I'] += 15; add_log("Bedrohung neutralisiert."); st.rerun()
    else:
        st.markdown("<div class='event-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Flash-Event!")
        evs = [
            ("Ein USB-Stick liegt auf dem Parkplatz.", "Abgeben (Ruf +)", "Einstecken (Risiko!)"),
            ("CEO fordert Admin-Rechte ohne Schulung.", "Verweigern (CIA +)", "Erlauben (Rep +)"),
            ("Audit-Frage: Was besagt das Maximumprinzip?", "Höchster Schutzbedarf gilt (Korrekt)", "Mittelwert gilt (Falsch)")
        ]
        text, o1, o2 = random.choice(evs)
        st.write(text)
        if st.button(o1): 
            g['decisions_made'] += 1; g['daily_event_active'] = False; g['day'] += 1; g['ap'] = 4; st.rerun()
        if st.button(o2): 
            g['decisions_made'] += 1; g['daily_event_active'] = False; g['day'] += 1; g['ap'] = 4; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_log:
    st.subheader("📟 Terminal")
    logs_html = "".join([f"<div style='margin-bottom:5px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{logs_html}</div>", unsafe_allow_html=True)
    
    if not g['daily_event_active'] and g['ap'] == 0:
        if st.button("⏭️ NÄCHSTER TAG"):
            g['daily_event_active'] = True
            for k in g['cia']: g['cia'][k] -= random.randint(4, 10)
            st.rerun()

if g['day'] > 25: g['won'] = True
if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
st.divider()
