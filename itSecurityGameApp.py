import streamlit as st
import random
import time

# --- 1. DATENBANK DER INHALTLICHEN TIEFE ---
KNOWLEDGE_POOL = [
    {"q": "GoBD: Ein Mitarbeiter löscht die digitale Signatur einer Eingangsrechnung. Problem?", "correct": "Ja, Verstoß gegen Unveränderbarkeit/Integrität", "wrong": "Nein, solange die PDF noch lesbar ist", "topic": "GoBD"},
    {"q": "EU AI Act: Das System nutzt 'Emotion Recognition' bei Mitarbeitern. Einstufung?", "correct": "Unannehmbares Risiko (Verboten)", "wrong": "Hochrisiko (Erlaubt mit Auflagen)", "topic": "AI Act"},
    {"q": "BSI Schicht 10: Warum reicht eine Firewall allein nicht aus?", "correct": "Defense in Depth erfordert Schutz auf jeder Ebene", "wrong": "Firewalls wirken nur auf Schicht 3/4", "topic": "BSI"},
    {"q": "Maximumprinzip: Ein Hilfssystem vernetzt mit Hauptserver (Hoch). Schutzbedarf?", "correct": "Hoch (Erbt vom kritischsten System)", "wrong": "Basis (Durchschnittsbildung)", "topic": "BSI"},
    {"q": "DSGVO Art. 83: Datenleck bei Kundenadressen wurde nicht gemeldet. Strafe?", "correct": "Bis zu 20 Mio. € oder 4% Jahresumsatz", "wrong": "Maximal 50.000 € Bußgeld", "topic": "Recht"},
    {"q": "PDCA: Backups schlagen fehl. In welcher Phase handelst du zur Korrektur?", "correct": "Act (Verbesserungsmaßnahmen einleiten)", "wrong": "Check (Nur Analyse)", "topic": "PDCA"}
]

# --- 2. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2500000,
            'cia': {'C': 70, 'I': 70, 'A': 70},
            'risk': 30, 'xp': 0, 'layers': 0, 'mode': 'tactical',
            'logs': ["> SIEM-CORE INITIALISIERT. MONITORING STARTET."],
            'active_incidents': [], 'game_over': False, 'won': False,
            'ai_knowledge': 0.1, 'p_audit': 0.05,
            'ceo_trust': 50, 'last_q_shuffled': []
        }

init_game()
g = st.session_state.game

def clamp(val): return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "ℹ️", "warn": "⚠️", "error": "🚨", "ai": "🧠", "build": "🏗️"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [Tag {g['day']}] {msg}")

# --- 3. UI & STYLING ---
st.set_page_config(page_title="CISO Command 10.1", layout="wide")
st.markdown("""
    <style>
    @keyframes glitch { 0% { text-shadow: 2px 0 red; } 50% { text-shadow: -2px 0 blue; } 100% { text-shadow: 2px 0 red; } }
    .stApp { background-color: #050a0f; color: #d0d0d0; font-family: 'Consolas', monospace; }
    .hud-header { background: linear-gradient(90deg, #1c1c1c, #004e92); padding: 25px; border-radius: 12px; border-left: 8px solid #00e5ff; margin-bottom: 20px; }
    .glitch-text { animation: glitch 1.5s infinite; color: #00e5ff; }
    .metric-box { background: #0f171e; border: 1px solid #00e5ff; padding: 10px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #ff00ff; color: #00ff41; padding: 10px; height: 300px; overflow-y: auto; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SZENARIO & ANLEITUNG ---
with st.expander("📂 MISSIONS-AKTE: OPERATION GOLDEN SHIELD", expanded=True):
    st.markdown("""
    ### 🏦 Das Szenario
    Die **Silver-Data GmbH** ist ein führender Logistikdienstleister für den physischen Goldhandel. Als neu ernannter CISO verwaltest du eine hochkomplexe IT-Infrastruktur. Die Bedrohungslage ist extrem: Staatliche Akteure nutzen **Bayessche Angriffs-KIs**, um Schwachstellen in Echtzeit zu finden.

    ### 🎯 Dein Ziel
    Erreiche das **Tag-25-Audit** mit einer stabilen CIA-Triade. Du musst die **Compliance** (GoBD, EU AI Act, DSGVO) wahren und eine **Defense-in-Depth-Architektur** (BSI) aufbauen. Das Spiel endet sofort, wenn das Vertrauen des Vorstands (Trust) erlischt oder eine Säule der CIA-Triade auf 0% fällt.

    ### 🛠️ SIEM-System Erklärung
    Ein **SIEM (Security Information and Event Management)** ist das Gehirn deines SOCs (Security Operations Center). Es sammelt Logs aus allen Systemen, analysiert sie in Echtzeit und erkennt Anomalien (z.B. Brute-Force Angriffe), bevor diese Schaden anrichten. Im Spiel blendet es die Bayes-KI, indem es ihre Angriffsmuster vorzeitig aufdeckt.
    """)

st.markdown("<div class='hud-header'><h1 class='glitch-text'>🛡️ CISO COMMAND v10.1</h1></div>", unsafe_allow_html=True)

# --- 5. DASHBOARD ---
m1, m2, m3, m4, m5 = st.columns(5)
m1.markdown(f"<div class='metric-box'>💰 BUDGET<br><b>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-box'>⚡ AKTIONEN<br><b>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-box'>📊 LAYERS<br><b>{g['layers']} / 10</b></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-box'>📅 TAG<br><b>{g['day']} / 25</b></div>", unsafe_allow_html=True)
m5.markdown(f"<div class='metric-box'>🤝 TRUST<br><b>{g['ceo_trust']}%</b></div>", unsafe_allow_html=True)

st.divider()

# CIA Triad Visualization

cia_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "🔒 Confidentiality", "I": "💎 Integrity", "A": "⚡ Availability"}[k]
    cia_cols[i].write(f"**{label}: {v}%**")
    cia_cols[i].progress(clamp(v))

# --- 6. GAME ENGINE ---
if g['game_over'] or g['ceo_trust'] <= 0: st.error("💀 MISSION ABGEBROCHEN: Sicherheitsarchitektur kollabiert."); st.stop()
if g['won']: st.balloons(); st.success("🏆 AUDIT ERFOLGREICH BESTANDEN!"); st.stop()

col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("🏗️ Konstruktions-Zentrum")
    t1, t2, t3, t4 = st.tabs(["🛡️ BSI Schichten", "🔋 Infrastruktur", "🛰️ Sensorik", "⚖️ Compliance"])
    
    with t1:
        st.write("Aufbau der 10 BSI-Schichten zur Risikominimierung.")
        if st.button(f"Nächste BSI-Schicht (150k | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1
                add_log(f"BSI-Layer {g['layers']} zertifiziert.", "build"); st.rerun()
                
    with t2:
        st.write("Physische & Technische Kapazitäten.")
        c_a, c_b = st.columns(2)
        if c_a.button("USV & Redundanz (100k | 1 AP)"):
            if g['ap'] >= 1 and g['budget'] >= 100000:
                g['ap'] -= 1; g['budget'] -= 100000; g['cia']['A'] += 15
                add_log("USV (Unterbrechungsfreie Stromversorgung) aktiv.", "build"); st.rerun()
        if c_b.button("Kryptografie (120k | 1 AP)"):
            if g['ap'] >= 1 and g['budget'] >= 120000:
                g['ap'] -= 1; g['budget'] -= 120000; g['cia']['C'] += 15
                add_log("E2EE (End-to-End Encryption) aktiv.", "build"); st.rerun()

    with t3:
        st.write("Überwachung & KI-Abwehr.")
        if st.button("SIEM-System implementieren (200k | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 200000:
                g['ap'] -= 2; g['budget'] -= 200000; g['ai_knowledge'] = max(0, g['ai_knowledge'] - 0.2)
                add_log("SIEM (Security Information & Event Management) gebucht.", "ai"); st.rerun()

    with t4:
        if st.button("Reporting & Audit-Check (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

with col_side:
    st.subheader("🧠 KI-Prognose (Bayes)")
    st.write(f"Hack-Wahrscheinlichkeit: {int(g['ai_knowledge']*100)}%")
    st.progress(clamp(g['ai_knowledge']*100))
    
    st.subheader("📟 System-Log")
    log_box = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_box}</div>", unsafe_allow_html=True)
    
    if st.button("⏭️ TAG BEENDEN", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        g['ai_knowledge'] += 0.05 + (0.01 * (10 - g['layers']))
        for k in g['cia']: g['cia'][k] -= random.randint(5, 12)
        g['ceo_trust'] -= 3
        if random.random() < g['ai_knowledge']:
            g['active_incidents'].append(f"Incident G 0.{random.randint(1,47)}")
        if random.random() < g['p_audit']: g['mode'] = 'audit'
        st.rerun()

# --- 7. RANDOMISIERTER AUDIT-MODUS ---
if g['mode'] == 'audit':
    st.markdown("---")
    
    q_data = random.choice(KNOWLEDGE_POOL)
    if 'current_audit_q' not in st.session_state or st.session_state.current_audit_q != q_data['q']:
        options = [(q_data['correct'], True), (q_data['wrong'], False)]
        random.shuffle(options)
        st.session_state.current_audit_options = options
        st.session_state.current_audit_q = q_data['q']
    
    st.subheader(f"⚖️ Compliance-Check: {q_data['topic']}")
    st.info(q_data['q'])
    for text, is_correct in st.session_state.current_audit_options:
        if st.button(text, use_container_width=True):
            if is_correct:
                st.success("Bestanden!"); g['budget'] += 50000; g['ceo_trust'] += 10; g['mode'] = 'tactical'
                del st.session_state.current_audit_q; st.rerun()
            else:
                st.error("Verfehlt!"); g['budget'] -= 200000; g['ceo_trust'] -= 20; g['mode'] = 'tactical'
                del st.session_state.current_audit_q; st.rerun()

# --- 8. ÜBERARBEITETES GLOSSAR (VOLLSTÄNDIG) ---
with st.sidebar:
    st.title("📖 CISO-LEXIKON v10.1")
    st.markdown("---")
    search = st.text_input("Begriff suchen...")
    intel_content = {
        "SIEM": "Security Information and Event Management. Ein System zur Aggregation und Analyse von Log-Daten aus verschiedenen Quellen, um Sicherheitsvorfälle (Incidents) in Echtzeit zu erkennen.",
        "BSI IT-Grundschutz": "Ein Standard für Informationssicherheits-Managementsysteme (ISMS). Nutzt Schichten zur Tiefenverteidigung.",
        "CIA-Triade": "Die drei Schutzziele: Vertraulichkeit (Verschlüsselung), Integrität (Unveränderbarkeit) und Verfügbarkeit (Ausfallsicherheit).",
        "EU AI Act": "Gesetz zur Regulierung von KI. Untersagt Manipulation und Social Scoring.",
        "GoBD": "Vorgaben für die IT-gestützte Buchführung. Fordert Revisionssicherheit und Unveränderbarkeit.",
        "USV": "Unterbrechungsfreie Stromversorgung. Schützt die Verfügbarkeit (A) bei Netzausfällen.",
        "Maximumprinzip": "Sicherheitsniveau richtet sich nach der kritischsten Komponente im Netzverbund.",
        "PDCA-Zyklus": "Managementprozess: Plan (Planen), Do (Umsetzen), Check (Messen), Act (Optimieren)."
    }
    for k, v in intel_content.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
