import streamlit as st
import random

# --- INITIALISIERUNG DES KOMPLEXEN STATES ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'day': 1,
        'budget': 300000,
        'rep': 100,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'unlocked_bausteine': [],
        'incidents_resolved': 0,
        'is_game_over': False,
        'logs': ["> System-Boot abgeschlossen. Warte auf Analyse..."],
        'last_action_feedback': ""
    }

def add_log(msg):
    st.session_state.game['logs'].insert(0, f"[TAG {st.session_state.game['day']}] {msg}")

# --- FACHWISSEN-POOL (PDF-REFERENZEN) ---
FACTS = {
    "BSI": "Die Systematik umfasst 10 Schichten und 47 elementare Gefährdungen.",
    "RECHT": "DSGVO-Bußgeld: Bis zu 4% des Jahresumsatzes. GoBD fordert Integrität.",
    "AI": "EU AI Act: Social Scoring ist ein unannehmbares Risiko (verboten).",
    "CIA": "Authentizität ist ein Teilziel der Integrität (Dok. 16, 2e)."
}

# --- UI DESIGN ---
st.set_page_config(page_title="CISO Command Center", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .stat-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .log-area { background: #010409; border: 1px solid #00ff41; color: #00ff41; padding: 15px; height: 250px; overflow-y: auto; font-size: 0.9em; }
    .action-card { background: #1c2128; border: 1px solid #58a6ff; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- GAME LOGIC ---
if st.session_state.game['is_game_over']:
    st.error("🚨 UNTERNEHMEN KOLLABIERT")
    st.write(f"Du hast {st.session_state.game['day']} Tage überlebt und {st.session_state.game['incidents_resolved']} Incidents gelöst.")
    if st.button("Neustart"):
        del st.session_state['game']
        st.rerun()
    st.stop()

# --- DASHBOARD ---
st.title("🛡️ CISO Command Center: Silver-Data GmbH")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-card'>💰 BUDGET<br><b>{st.session_state.game['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>🔒 CIA-STATUS<br>C: {st.session_state.game['cia']['C']}% | I: {st.session_state.game['cia']['I']}% | A: {st.session_state.game['cia']['A']}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'>🗓️ TAG<br><b>{st.session_state.game['day']}</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-card'>📈 REPUTATION<br><b>{st.session_state.game['rep']}%</b></div>", unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("🛠️ Aktuelle Operationen")
    
    # AKTION 1: Risiko-Analyse (Basierend auf Dok 16)
    with st.expander("🔍 Risiko-Analyse & BSI-Audit durchführen"):
        q = st.radio("Wie viele elementare Gefährdungen müssen laut BSI geprüft werden?", ["30", "47", "100"], index=None)
        if st.button("Audit starten"):
            if q == "47":
                st.session_state.game['budget'] += 20000
                add_log("Audit erfolgreich. Revision gewährt Bonusbudget.")
            else:
                st.session_state.game['budget'] -= 30000
                st.session_state.game['rep'] -= 10
                add_log("Audit fehlgeschlagen! Unkenntnis der BSI-Gefährdungen kostet Reputation.")
            st.rerun()

    # AKTION 2: Investition in TOMs (Dok 15/16)
    with st.expander("🛡️ TOMs implementieren (Plan/Do)"):
        toms = {
            "G 0.19: Awareness-Training (Kosten: 20k)": ("C", 20, 20000, "Phishing-Schutz verbessert."),
            "ISMS.1: Sicherheitsmanagement (Kosten: 50k)": ("I", 30, 50000, "Prozesse nach BSI stabilisiert."),
            "G 0.18: Offline-Backups (Kosten: 40k)": ("A", 40, 40000, "Ransomware-Resilienz erhöht.")
        }
        for name, (stat, val, cost, msg) in toms.items():
            if st.button(name):
                if st.session_state.game['budget'] >= cost:
                    st.session_state.game['budget'] -= cost
                    st.session_state.game['cia'][stat] = min(100, st.session_state.game['cia'][stat] + val)
                    add_log(msg)
                    st.rerun()
                else:
                    st.warning("Budget nicht ausreichend!")

    # AKTION 3: Incident Response (Der Check/Act Teil)
    st.markdown("<div class='action-card'>", unsafe_allow_html=True)
    st.subheader("🚨 Aktueller Incident")
    
    # Zufälliger Incident-Generator basierend auf PDFs
    incidents = [
        {"title": "Barclays-Phishing-Welle", "desc": "Mitarbeiter erhalten Mails zur Token-Verifizierung.", "type": "C", "damage": 30, "fix": "Mitarbeiter-Sperre & Passwort-Reset"},
        {"title": "SQL-Injection im Shop", "desc": "Preise werden auf 0,00€ gesetzt (GoBD-Verstoß!).", "type": "I", "damage": 40, "fix": "Input-Validierung & WAF"},
        {"title": "EU AI Act Verstoß", "desc": "Marketing nutzt verbotenes Social Scoring.", "type": "C", "damage": 50, "fix": "Sofortiger Projektstopp"}
    ]
    active_inc = incidents[st.session_state.game['day'] % len(incidents)]
    st.warning(f"**{active_inc['title']}**: {active_inc['desc']}")
    
    if st.button(f"Reagieren: {active_inc['fix']}"):
        st.session_state.game['incidents_resolved'] += 1
        add_log(f"Incident {active_inc['title']} wurde professionell gelöst.")
        st.session_state.game['day'] += 1
        st.rerun()
    
    if st.button("Ignorieren (Nächster Tag)"):
        st.session_state.game['cia'][active_inc['type']] -= active_inc['damage']
        st.session_state.game['rep'] -= 20
        # DSGVO BUẞGELD (Art. 83)
        if active_inc['type'] == "C":
            fine = 100000
            st.session_state.game['budget'] -= fine
            add_log(f"DSGVO-STRAFE: {fine}€ Bußgeld wegen Datenverlust!")
        st.session_state.game['day'] += 1
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.subheader("📟 System-Logs")
    log_content = "\n".join(st.session_state.game['logs'])
    st.markdown(f"<pre class='log-area'>{log_content}</pre>", unsafe_allow_html=True)
    
    st.subheader("📚 BSI-Handbuch")
    st.info(f"**Wusstest du?** {FACTS[random.choice(list(FACTS.keys()))]}")
    
    # CIA Visualisierung
    
    
# --- GAME OVER CHECK ---
if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
    st.session_state.game['is_game_over'] = True
    st.rerun()
