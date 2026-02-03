import streamlit as st
import random

# --- 1. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 1500000, 'rep': 50,
            'cia': {'C': 60, 'I': 60, 'A': 60},
            'stress': 10, 'exposure': 20,
            'logs': ["> SYSTEM INITIALIZED. WELCOME CISO."],
            'active_project': None, 'project_progress': 0,
            'incidents': [], 'decisions_made': 0,
            'game_over': False, 'won': False, 'event_active': False
        }

init_game()
g = st.session_state.game

def add_log(msg, style="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    g['logs'].insert(0, f"<span style='color:{colors.get(style)}'>[Tag {g['day']}] {msg}</span>")

# --- 2. INTEL-DATENBANK ---
INTEL = {
    "BSI Schichten": "Infrastruktur, Netz, IT-Systeme, Anwendungen, Prozesse. Jede Ebene muss separat gehärtet werden.",
    "Maximumprinzip": "Schutzbedarf der Anwendung bestimmt das Niveau der Infrastruktur (Dok. 12).",
    "GoBD Integrität": "Digitale Belege müssen unveränderbar (integre) gespeichert werden (Dok. 13).",
    "EU AI Act": "Verbot von Social Scoring (Unannehmbar). Hochrisiko-KI braucht Konformitätsbewertung.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Der Motor deines ISMS. Ohne 'Check' (Audit) ist 'Do' wertlos."
}

# --- 3. UI STYLE ---
st.set_page_config(page_title="CISO Tactical: Silver-Data", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    .stat-metric { background: #111; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 10px; height: 300px; overflow-y: auto; font-size: 0.8em; }
    .critical-card { background: #220000; border: 2px solid #ff0000; padding: 20px; border-radius: 10px; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.7; } }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📟 INTEL-CORE")
    search = st.text_input("Begriff suchen...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
    st.divider()
    if st.button("Simulation Hard-Reset"): init_game(True); st.rerun()

# --- 5. DASHBOARD ---
st.title("🖥️ Silver-Data Command Center")
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Budget", f"{g['budget']:,}€")
m2.metric("Aktionspunkte", f"{g['ap']} / 5")
m3.metric("Stress (Admins)", f"{g['stress']}%", delta=f"{g['stress']-10}%", delta_color="inverse")
m4.metric("Risk Exposure", f"{g['exposure']}%")
m5.metric("Tag", f"{g['day']} / 25")

st.divider()



# CIA & PROGRESS
c_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    c_cols[i].write(f"**{label}**")
    c_cols[i].progress(max(0, min(100, v)))

# --- 6. GAMEPLAY ENGINE ---
if g['game_over']:
    st.error("🚨 KRITISCHES SYSTEMVERSAGEN. Die Silver-Data GmbH ist am Ende."); st.stop()
if g['won']:
    st.balloons(); st.success("🏆 AUDIT BESTANDEN! Silver-Data ist BSI-zertifiziert."); st.stop()

left, right = st.columns([2, 1])

with left:
    # PROJEKT-MANAGER
    st.subheader("🏗️ Langzeit-Projekte")
    if g['active_project']:
        st.info(f"Aktiv: **{g['active_project']}** ({g['project_progress']}% abgeschlossen)")
        p_col1, p_col2 = st.columns(2)
        if p_col1.button("Weiterarbeiten (2 AP | +30%)"):
            if g['ap'] >= 2:
                g['ap'] -= 2; g['project_progress'] += 30; g['decisions_made'] += 1
                if g['project_progress'] >= 100:
                    add_log(f"Projekt abgeschlossen: {g['active_project']}")
                    if "BSI" in g['active_project']: g['cia']['A'] += 30; g['cia']['I'] += 20
                    g['active_project'] = None; g['project_progress'] = 0
                st.rerun()
        if p_col2.button("Projekt abbrechen"):
            g['active_project'] = None; g['project_progress'] = 0; add_log("Projekt gestoppt.", "warn"); st.rerun()
    else:
        if st.button("Start: BSI-Infrastruktur Level 5 (Kosten: 200k €)"):
            if g['budget'] >= 200000:
                g['budget'] -= 200000; g['active_project'] = "BSI-Infrastruktur"; g['decisions_made'] += 1; st.rerun()

    # SCHNELLE AKTIONEN
    st.subheader("⚡ Taktik & Compliance")
    t_cols = st.columns(2)
    if t_cols[0].button("Schwachstellen-Scan (1 AP | Stress +5)"):
        if g['ap'] >= 1:
            g['ap'] -= 1; g['stress'] += 5; g['decisions_made'] += 1
            if random.random() > 0.3:
                g['incidents'].append(random.choice(["SQL-Injektion", "Gefahr G 0.18 (Feuer/Wasser)"]))
                add_log("Bedrohung identifiziert!", "error")
            else: add_log("Scan abgeschlossen. Keine Funde."); st.rerun()
            
    if t_cols[1].button("KI-Compliance Prüfung (1 AP)"):
        if g['ap'] >= 1:
            g['ap'] -= 1; g['decisions_made'] += 1
            st.session_state.event_trigger = "AI_CHECK"; st.rerun()

    # INCIDENT BOARD
    if g['incidents']:
        st.subheader("🚨 Aktive Vorfälle")
        for inc in g['incidents']:
            with st.container():
                st.markdown(f"<div class='critical-card'><b>{inc}</b> detektiert!</div>", unsafe_allow_html=True)
                if st.button(f"Gegenmaßnahme für {inc} (1 AP)"):
                    g['ap'] -= 1; g['incidents'].remove(inc); g['decisions_made'] += 1
                    g['cia']['I'] = min(100, g['cia']['I'] + 10); add_log("Vorfall bereinigt."); st.rerun()

with right:
    st.subheader("📟 Live-Log")
    log_html = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_html}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("⏭️ TAG BEENDEN"):
        g['day'] += 1; g['ap'] = 5; g['stress'] = max(0, g['stress'] - 10)
        # Nacht-Berechnung
        for k in g['cia']: g['cia'][k] -= random.randint(3, 8)
        if g['incidents']: 
            g['cia']['I'] -= 15; g['rep'] -= 10
            add_log("Nicht gelöste Incidents haben Schaden verursacht!", "error")
        
        # Sieg/Niederlage
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0 or g['stress'] >= 100: g['game_over'] = True
        
        # Zufallsevent triggern
        g['event_active'] = True; st.rerun()

# --- 7. MODALE EVENTS (KEINE LÖSUNGSHINWEISE) ---
if g['event_active']:
    st.markdown("---")
    with st.container():
        st.markdown("<div class='critical-card'>", unsafe_allow_html=True)
        st.subheader("📩 Eingehende Entscheidung")
        evs = [
            ("Ein Cloud-Anbieter bietet billiges Backup an. Er speichert aber in einem Land ohne DSGVO-Abkommen.", "Ablehnen", "Annehmen"),
            ("Was ist laut BSI das Kernziel der Integrität?", "Authentizität & Korrektheit", "Verschlüsselung & Passwortschutz"),
            ("Die Admins fordern ein teures Analyse-Tool, um Stress zu senken.", "Tool kaufen (100k €)", "Abbruch der Forderung"),
            ("Ein Kunde möchte sein 'Social Scoring' Ergebnis einsehen.", "Erklären, dass wir das nicht nutzen", "Ergebnis zusenden")
        ]
        text, o1, o2 = random.choice(evs)
        st.write(text)
        if st.button(o1):
            g['decisions_made'] += 1; g['event_active'] = False; add_log("Entscheidung protokolliert."); st.rerun()
        if st.button(o2):
            if "Social Scoring" in text or "Annehmen" in text:
                g['budget'] -= 200000; g['rep'] -= 30; add_log("Schwere Compliance-Lücke gemeldet!", "error")
            g['decisions_made'] += 1; g['event_active'] = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
