import streamlit as st
import random

# --- 1. ABSOLUT ROBUSTE INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1,
            'ap': 4,
            'budget': 1500000, 
            'rep': 50,
            'cia': {'C': 60, 'I': 60, 'A': 60},
            'logs': ["> SYSTEM INITIALIZED. WAITING FOR COMMAND..."],
            'active_incident': None,
            'decisions_made': 0,
            'game_over': False,
            'won': False,
            'daily_event_active': False,
            'intro_seen': False
        }

init_game()
g = st.session_state.game

def add_log(msg, style="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    g['logs'].insert(0, f"<span style='color:{colors.get(style)}'>[Tag {g['day']}] {msg}</span>")

# --- 2. INTEL-DATENBANK (DAS GLOSSAR) ---
INTEL = {
    "10 Schichten (BSI)": "Struktur des IT-Grundschutzes: Umfasst Infrastruktur, Netznetze, IT-Systeme, Anwendungen und Prozesse.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 - G 0.47) laut BSI-Kompendium, die als Basis für Risikoanalysen dienen.",
    "Maximumprinzip": "Ein Konzept zur Schutzbedarfsfeststellung. Der Schutzbedarf einer Anwendung bestimmt den Bedarf der darunterliegenden Infrastruktur.",
    "GoBD": "Grundsätze zur ordnungsgemäßen Führung und Aufbewahrung von Büchern, Aufzeichnungen und Unterlagen in elektronischer Form.",
    "Integrität": "Sicherstellung der Korrektheit von Daten und Systemfunktionen. Schutz vor unbefugter Modifikation.",
    "DSGVO Art. 83": "Regelt die Bedingungen für die Verhängung von Geldbußen bei Datenschutzverletzungen.",
    "EU AI Act": "Reguliert KI-Systeme basierend auf ihrem Risiko. Verbietet unter anderem Social Scoring.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Methode zur Steuerung und ständigen Verbesserung des Informationssicherheitsmanagementsystems (ISMS).",
    "Verfügbarkeit": "Gewährleistung, dass autorisierte Benutzer bei Bedarf Zugang zu Informationen und Systemen haben."
}

# --- 3. UI & STYLING ---
st.set_page_config(page_title="Silver-Data: CISO Command", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace; }
    .stat-box { background: #111; border: 1px solid #00ff41; padding: 15px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.85em; border-left: 4px solid #ff00ff; }
    .stButton>button { border: 1px solid #00ff41; background: #0b0e14; color: #00ff41; width: 100%; font-weight: bold; }
    .stButton>button:hover { background: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    .event-card { background: #161b22; border: 2px solid #f2cc60; padding: 20px; border-radius: 10px; }
    .story-header { color: #ff00ff; font-size: 1.5em; text-transform: uppercase; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. STORYLINE INTRO ---
if not g['intro_seen']:
    st.markdown("<div class='event-card'>", unsafe_allow_html=True)
    st.markdown("<div class='story-header'>Eingehende Nachricht: Priorität CRITICAL</div>", unsafe_allow_html=True)
    st.write("""
    **Betreff: Deine Ernennung zum CISO der Silver-Data GmbH**
    
    Silver-Data ist der größte Gold-Händler der Region. Wir verarbeiten täglich Millionen-Transaktionen. 
    Aber wir haben ein Problem: Das Bundesamt für Sicherheit in der Informationstechnik (BSI) hat ein **Full-Scope-Audit** angekündigt. 
    In genau **25 Tagen** entscheidet sich die Zukunft dieser Firma.
    
    **Deine Mission:**
    1. Bereite das Unternehmen auf das Audit vor (25 Tage überleben).
    2. Verhindere einen System-Kollaps. Wenn Vertraulichkeit, Integrität oder Verfügbarkeit (CIA) auf 0 fallen, ist das Spiel vorbei.
    3. Verwalte das Budget weise. Bußgelder nach DSGVO oder Fehlentscheidungen können uns in den Ruin treiben.
    
    Nutze die **Intel-Datenbank** in der Sidebar. Wer keine Ahnung von den Regeln hat, wird scheitern. 
    Viel Erfolg, CISO. Wir zählen auf dich.
    """)
    if st.button("Simulation starten"):
        g['intro_seen'] = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("📟 INTEL-ZENTRALE")
    st.divider()
    st.subheader("📚 Sicherheits-Glossar")
    search = st.text_input("Begriff suchen...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k):
                st.write(v)

# --- 6. GAME OVER & WIN CHECKS ---
if g['game_over']:
    st.error("🚨 MISSION FEHLGESCHLAGEN: Die Silver-Data GmbH hat die Kontrolle verloren.")
    if st.button("Simulation Neustarten"):
        init_game(True); st.rerun()
    st.stop()

if g['won']:
    st.balloons()
    st.success(f"🏆 AUDIT BESTANDEN! Die Silver-Data GmbH ist zertifiziert. Du hast {g['decisions_made']} Aufgaben erledigt.")
    if st.button("Erneut spielen"):
        init_game(True); st.rerun()
    st.stop()

# --- 7. DASHBOARD ---
st.title("🛡️ Command: Silver-Data CISO")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-box'>💰 BUDGET<br><b style='color:white'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>⚡ AKTIONEN<br><b style='color:white'>{g['ap']} / 4</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>🗓️ TAG<br><b style='color:white'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-box'>⚖️ TASKS<br><b style='color:white'>{g['decisions_made']}</b></div>", unsafe_allow_html=True)

st.divider()



cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "Vertraulichkeit", "I": "Integrität", "A": "Verfügbarkeit"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 8. TACTICAL OPERATIONS ---
col_act, col_log = st.columns([2, 1])

with col_act:
    if not g['daily_event_active']:
        st.subheader("🛠️ Verfügbare Maßnahmen")
        t1, t2, t3 = st.tabs(["🏗️ Bauen", "🔍 Prüfen", "⚖️ Regeln"])
        
        with t1:
            if st.button("Technische Infrastruktur-Härtung (120k € | 2 AP)"):
                if g['ap'] >= 2 and g['budget'] >= 120000:
                    g['ap'] -= 2; g['budget'] -= 120000; g['decisions_made'] += 1
                    g['cia']['A'] += 15; g['cia']['I'] += 10; add_log("Infrastruktur-Upgrade durchgeführt."); st.rerun()
            if st.button("Personal-Schulung Security Awareness (40k € | 1 AP)"):
                if g['ap'] >= 1 and g['budget'] >= 40000:
                    g['ap'] -= 1; g['budget'] -= 40000; g['decisions_made'] += 1
                    g['cia']['C'] += 15; add_log("Mitarbeitersensibilisierung abgeschlossen."); st.rerun()

        with t2:
            if st.button("Sicherheits-Audit der Systeme (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['decisions_made'] += 1
                    if random.random() > 0.4:
                        g['active_incident'] = random.choice(["SQL-Injection", "Phishing-Angriff"])
                        add_log("ALARM: Sicherheitslücke detektiert!", "error")
                    else: add_log("Systemcheck unauffällig."); st.rerun()

        with t3:
            if st.button("KI-Projektprüfung nach EU AI Act (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['decisions_made'] += 1
                    add_log("Prüfung der KI-Systematik eingeleitet."); st.rerun()

        if g['active_incident']:
            st.error(f"⚠️ AKTIVER INCIDENT: {g['active_incident']}")
            if st.button("Krisenreaktion einleiten (1 AP)"):
                g['ap'] -= 1; g['decisions_made'] += 1; g['active_incident'] = None
                g['cia']['I'] += 15; add_log("Bedrohung neutralisiert."); st.rerun()
    else:
        st.markdown("<div class='event-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Unvorhergesehenes Ereignis")
        evs = [
            ("Ein USB-Stick wurde auf dem Firmenparkplatz gefunden.", "Im Fundbüro abgeben", "An Arbeitsplatzrechner prüfen"),
            ("Der Vorstand fordert Zugriff auf alle Passwörter.", "Zugriff verweigern", "Zugriff gewähren"),
            ("Was besagt das Maximumprinzip im IT-Grundschutz?", "Der höchste Schutzbedarf wird übernommen", "Der durchschnittliche Schutzbedarf wird berechnet"),
            ("Marketing will Social Scoring für Kunden einführen.", "Projekt stoppen", "Projekt genehmigen"),
            ("GoBD: Wer ist für die Integrität digitaler Belege verantwortlich?", "Der Systemadministrator", "Der gesetzliche Vertreter des Unternehmens")
        ]
        text, o1, o2 = random.choice(evs)
        st.write(f"**Situation:** {text}")
        if st.button(o1): 
            g['decisions_made'] += 1; g['daily_event_active'] = False; g['day'] += 1; g['ap'] = 4; st.rerun()
        if st.button(o2): 
            # Falsche Entscheidungen ziehen hier unsichtbar Werte ab
            if "Social Scoring" in text or "Vorstand" in text:
                g['budget'] *= 0.95; g['rep'] -= 20
            g['decisions_made'] += 1; g['daily_event_active'] = False; g['day'] += 1; g['ap'] = 4; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_log:
    st.subheader("📟 Terminal")
    logs_html = "".join([f"<div style='margin-bottom:5px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{logs_html}</div>", unsafe_allow_html=True)
    
    if not g['daily_event_active'] and g['ap'] == 0:
        if st.button("⏭️ TAG BEENDEN"):
            g['daily_event_active'] = True
            for k in g['cia']: g['cia'][k] -= random.randint(5, 12) # Täglicher Verschleiß
            st.rerun()

# --- 9. WIN/LOSS CONDITIONS ---
if g['day'] > 25: g['won'] = True
if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True

st.divider()
