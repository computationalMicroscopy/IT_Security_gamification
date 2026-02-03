import streamlit as st
import random

# --- 1. ABSOLUT FEHLERSICHERE INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1,
            'ap': 4,
            'budget': 1200000, # Budget erhöht für längere Spieldauer
            'rep': 60,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'logs': ["> INITIALIZING LONG-TERM DEFENSE PROTOCOL..."],
            'active_incident': None,
            'decisions_made': 0,
            'game_over': False,
            'won': False,
            'daily_event_done': False,
            'current_event_text': ""
        }

init_game()
g = st.session_state.game

def add_log(msg, style="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    g['logs'].insert(0, f"<span style='color:{colors.get(style)}'>[Tag {g['day']}] {msg}</span>")

# --- 2. VOLLSTÄNDIGES CYBER-LEXIKON ---
LEXIKON = {
    "10 Schichten (BSI)": "Systematik des IT-Grundschutzes. Umfasst Infrastruktur, Netz, IT-Systeme und Anwendungen.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 bis G 0.47) laut BSI-Kompendium (z.B. Feuer, Hacker, Fehlbedienung).",
    "Maximumprinzip": "Der Schutzbedarf eines Systems wird durch die Komponente mit dem höchsten Bedarf bestimmt (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Buchführung. Fordert Integrität (Unveränderbarkeit) der Daten (Dok. 13).",
    "DSGVO Art. 83": "Strafen bei Verstößen: Bis zu 4% des Jahresumsatzes oder 20 Mio. Euro.",
    "EU AI Act": "Verbot von Social Scoring. Klassifizierung in Unannehmbar, Hoch, Transparenz und Minimal (Dok. 15).",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Methode zur kontinuierlichen Verbesserung des ISMS (Dok. 16).",
    "Authentizität": "Prüfbarkeit der Herkunft und Echtheit. Teilaspekt der Integrität.",
    "Verfügbarkeit (A)": "Sicherstellung, dass Systeme bei Bedarf funktionsfähig sind (Schutz vor DoS/Ausfall)."
}

# --- 3. UI & DESIGN ---
st.set_page_config(page_title="CISO Command: 100-Tasks Edition", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace; }
    .stat-box { background: #111; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.85em; border-left: 4px solid #ff00ff; }
    .stButton>button { border: 1px solid #00ff41; background: #0b0e14; color: #00ff41; width: 100%; height: 3.5em; font-weight: bold; }
    .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    .event-card { background: #1a1a1a; border: 2px solid #f2cc60; padding: 20px; border-radius: 10px; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📟 INTEL DATABASE")
    st.info("**Szenario:** Silver-Data GmbH. 25 Tage bis zum Mega-Audit. 100+ Entscheidungen nötig.")
    st.divider()
    search = st.text_input("Begriff suchen...")
    for k, v in LEXIKON.items():
        if not search or search.lower() in k.lower():
            with st.expander(k):
                st.write(v)

# --- 5. LOGIK-CHECKS ---
if g.get('game_over'):
    st.error("🚨 MISSION FEHLGESCHLAGEN: System-Kollaps oder Insolvenz.")
    if st.button("Simulation Neustarten"):
        init_game(force=True)
        st.rerun()
    st.stop()

if g.get('won'):
    st.balloons()
    st.success(f"🏆 AUDIT BESTANDEN! Du hast {g['decisions_made']} Entscheidungen getroffen und Silver-Data gerettet.")
    if st.button("Erneut spielen"):
        init_game(force=True)
        st.rerun()
    st.stop()

# --- 6. DASHBOARD ---
st.title("🛡️ CISO Command Center: Silver-Data")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-box'>💰 BUDGET<br><b style='font-size:1.4em; color:white'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>⚡ AKTIONEN (AP)<br><b style='font-size:1.4em; color:white'>{g['ap']} / 4</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>🗓️ TAG<br><b style='font-size:1.4em; color:white'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-box'>⚖️ ENTSCHEIDUNGEN<br><b style='font-size:1.4em; color:white'>{g['decisions_made']}</b></div>", unsafe_allow_html=True)

st.divider()

# CIA PROGRESS
st.write("### 🔒 System-Integrität (CIA)")
cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 7. TACTICAL OPERATIONS (Die 100 AP Entscheidungen) ---
col_act, col_log = st.columns([2, 1])

with col_act:
    if not g['daily_event_done']:
        st.subheader("🛠️ Strategische Operationen")
        t1, t2, t3 = st.tabs(["🏗️ Do (Umsetzen)", "🔍 Check (Prüfen)", "⚖️ Act (Compliance)"])
        
        with t1:
            if st.button("BSI-Schichten härten (100k € | 2 AP)"):
                if g['ap'] >= 2 and g['budget'] >= 100000:
                    g['ap'] -= 2; g['budget'] -= 100000; g['decisions_made'] += 1
                    g['cia']['A'] += 15; g['cia']['I'] += 10
                    add_log("Infrastruktur-Update durchgeführt.")
                    st.rerun()
            if st.button("Backup-Konzept (G 0.18) (40k € | 1 AP)"):
                if g['ap'] >= 1 and g['budget'] >= 40000:
                    g['ap'] -= 1; g['budget'] -= 40000; g['decisions_made'] += 1
                    g['cia']['A'] = min(100, g['cia']['A'] + 20)
                    add_log("Resilienz durch Backups erhöht.")
                    st.rerun()

        with t2:
            if st.button("Vulnerability Scan (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['decisions_made'] += 1
                    if random.random() > 0.4:
                        g['active_incident'] = random.choice(["SQL", "PHISH"])
                        add_log("ALARM: Bedrohung detektiert!", "error")
                    else:
                        add_log("Scanergebnis: Keine Anomalien.")
                    st.rerun()

        with t3:
            st.write("Fachfragen-Check (Compliance)")
            if st.button("Prüfung: AI Act & Social Scoring (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['decisions_made'] += 1
                    st.info("Wie ist Social Scoring eingestuft?")
                    # In einem echten AP-Flow müsste hier eine Antwort folgen, für den Flow triggern wir ein Log:
                    add_log("KI-Compliance-Prüfung gestartet.")
                    st.rerun()

        # INCIDENT MANAGEMENT
        if g.get('active_incident'):
            st.error(f"⚠️ AKTIVER INCIDENT: {g['active_incident']}")
            if st.button("Incident bekämpfen (1 AP)"):
                g['ap'] -= 1; g['decisions_made'] += 1
                g['active_incident'] = None
                g['cia']['I'] += 10
                add_log("Bedrohung neutralisiert.")
                st.rerun()
    else:
        # TÄGLICHES FLASH-EVENT (Zwingende Entscheidung)
        st.markdown("<div class='event-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Flash-Event: Unvorhergesehenes Ereignis")
        events = [
            ("Ein Mitarbeiter hat sein Passwort auf einen Post-it geschrieben.", "Post-it entfernen (Ruf +)", "Ignorieren (Budget +)"),
            ("Der CEO will eine unsichere KI-App nutzen.", "Ablehnen (CIA +)", "Erlauben (Reputation +)"),
            ("Ein lokaler Stromausfall droht.", "USV aktivieren (Budget -)", "Abwarten (Risiko!)"),
            ("Audit-Vorbereitung: GoBD Dokumentation fehlt.", "Überstunden anordnen (Rep -)", "Lücke lassen (Risiko!)")
        ]
        ev_text, opt1, opt2 = random.choice(events)
        st.write(ev_text)
        c_ev1, c_ev2 = st.columns(2)
        if c_ev1.button(opt1):
            g['decisions_made'] += 1; g['daily_event_done'] = False
            add_log(f"Event gelöst: {opt1}"); g['day'] += 1; g['ap'] = 4; st.rerun()
        if c_ev2.button(opt2):
            g['decisions_made'] += 1; g['daily_event_done'] = False
            add_log(f"Event gelöst: {opt2}"); g['day'] += 1; g['ap'] = 4; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_log:
    st.subheader("📟 System-Terminal")
    logs_html = "".join([f"<div style='margin-bottom:5px;'>{l}</div>" for l in g['logs']])
    st.markdown(f<div class='terminal'>{logs_html}</div>, unsafe_allow_html=True)
    
    if not g['daily_event_done'] and g['ap'] == 0:
        if st.button("⏭️ TAG BEENDEN & FLASH-EVENT STARTEN"):
            g['daily_event_done'] = True
            # Werte-Verschleiß (Entropie)
            for k in g['cia']: g['cia'][k] -= random.randint(4, 8)
            st.rerun()

# --- 8. WIN/LOSS CHECKS ---
if g['day'] > 25: g['won'] = True
if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True

# --- GRAFIKEN ---
st.divider()
st.write("### Theoretische Grundlagen")
c_img1, c_img2 = st.columns(2)
with c_img1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/CIA_triad.svg/220px-CIA_triad.svg.png", caption="CIA Triade")
with c_img2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/PDCA_Cycle.svg/220px-PDCA_Cycle.svg.png", caption="PDCA Zyklus")
