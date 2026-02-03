import streamlit as st
import random
import time

# --- 1. DATENBANK DER INHALTLICHEN TIEFE (VOLLSTÄNDIG) ---
KNOWLEDGE_POOL = [
    {"q": "GoBD: Ein Mitarbeiter löscht die digitale Signatur einer Eingangsrechnung. Problem?", "correct": "Ja, Verstoß gegen Unveränderbarkeit/Integrität", "wrong": "Nein, solange die PDF noch lesbar ist", "topic": "GoBD"},
    {"q": "EU AI Act: Das System nutzt 'Emotion Recognition' bei Mitarbeitern. Einstufung?", "correct": "Unannehmbares Risiko (Verboten)", "wrong": "Hochrisiko (Erlaubt mit Auflagen)", "topic": "AI Act"},
    {"q": "BSI Schicht 10: Warum reicht eine Firewall allein nicht aus?", "correct": "Defense in Depth erfordert Schutz auf jeder Ebene", "wrong": "Firewalls wirken nur auf Schicht 3/4", "topic": "BSI"},
    {"q": "Maximumprinzip: Ein Hilfssystem vernetzt mit Hauptserver (Hoch). Schutzbedarf?", "correct": "Hoch (Erbt vom kritischsten System)", "wrong": "Basis (Durchschnittsbildung)", "topic": "BSI"},
    {"q": "DSGVO Art. 83: Datenleck bei Kundenadressen wurde nicht gemeldet. Strafe?", "correct": "Bis zu 20 Mio. € oder 4% Jahresumsatz", "wrong": "Maximal 50.000 € Bußgeld", "topic": "Recht"},
    {"q": "PDCA: Backups schlagen fehl. In welcher Phase handelst du zur Korrektur?", "correct": "Act (Verbesserungsmaßnahmen einleiten)", "wrong": "Check (Nur Analyse)", "topic": "PDCA"},
    {"q": "Integrität (CIA): Wie sicherst du Gold-Bestandslisten gegen Manipulation?", "correct": "Prüfsummen und digitale Signaturen", "wrong": "Tägliche Verfügbarkeits-Backups", "topic": "CIA"},
    {"q": "Gefährdung G 0.18: Ein Admin konfiguriert den Hauptrouter falsch. Kategorie?", "correct": "Fehlbedienung / Technisches Versagen", "wrong": "Vorsätzliche Handlung / Sabotage", "topic": "BSI"},
    {"q": "EU AI Act: KI zur Kreditwürdigkeitsprüfung von Gold-Käufern. Kategorie?", "correct": "Hochrisiko (Strenge Auflagen)", "wrong": "Minimales Risiko", "topic": "AI Act"},
    {"q": "BSI-Grundschutz: Was ist ein 'Baustein'?", "correct": "Ein Modul mit Sicherheitsanforderungen", "wrong": "Ein physischer Server", "topic": "BSI"}
]

# --- 2. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2500000,
            'cia': {'C': 70, 'I': 70, 'A': 70},
            'risk': 30, 'xp': 0, 'layers': 0, 'mode': 'tactical',
            'logs': ["> ENTROPIE-MODUL AKTIVIERT. VIEL ERFOLG."],
            'active_incidents': [], 'game_over': False, 'won': False,
            'ai_knowledge': 0.1, 'p_audit': 0.05,
            'ceo_trust': 50, 'last_q_shuffled': [] # Speicher für geshuffelte Antworten
        }

init_game()
g = st.session_state.game

def clamp(val): return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "ℹ️", "warn": "⚠️", "error": "🚨", "ai": "🧠", "trust": "🤝"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [Tag {g['day']}] {msg}")

# --- 3. UI & ANIMATIONEN ---
st.set_page_config(page_title="CISO Command 9.0", layout="wide")
st.markdown("""
    <style>
    @keyframes glitch { 0% { text-shadow: 2px 0 red; } 50% { text-shadow: -2px 0 blue; } 100% { text-shadow: 2px 0 red; } }
    .stApp { background-color: #050a0f; color: #d0d0d0; font-family: 'Consolas', monospace; }
    .hud-header { background: linear-gradient(90deg, #16222a, #3a6073); padding: 20px; border-radius: 10px; border-bottom: 4px solid #00e5ff; }
    .glitch-text { animation: glitch 1.5s infinite; color: #00e5ff; font-weight: bold; }
    .metric-box { background: #0f171e; border: 1px solid #00e5ff; padding: 10px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #ff00ff; color: #00ff41; padding: 10px; height: 300px; overflow-y: auto; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SZENARIO & ANLEITUNG ---
with st.expander("📖 MISSION-BRIEFING & STRATEGIE", expanded=False):
    st.markdown("""
    ### Silver-Data GmbH: Goldhandel-Sicherung
    **Ziel:** Überlebe bis Tag 25. 
    **Neu:** Deine Entscheidungen beeinflussen den **CEO-Trust**. Sinkt dieser auf 0, wirst du gefeuert. Hoher Trust schaltet Budget-Boni frei.
    **Random Audit:** Antworten sind nun bei jedem Audit an zufälligen Positionen.
    """)

st.markdown("<div class='hud-header'><h1 class='glitch-text'>🛡️ CISO COMMAND v9.0</h1></div>", unsafe_allow_html=True)

# --- 5. DASHBOARD ---
m1, m2, m3, m4, m5 = st.columns(5)
m1.markdown(f"<div class='metric-box'>💰 BUDGET<br><b>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-box'>⚡ AKTIONEN<br><b>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-box'>📊 LAYERS<br><b>{g['layers']} / 10</b></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-box'>📅 TAG<br><b>{g['day']} / 25</b></div>", unsafe_allow_html=True)
m5.markdown(f"<div class='metric-box'>🤝 TRUST<br><b>{g['ceo_trust']}%</b></div>", unsafe_allow_html=True)

st.divider()

# CIA Triad
cia_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "🔒 Conf.", "I": "💎 Integ.", "A": "⚡ Avail."}[k]
    cia_cols[i].write(f"**{label}: {v}%**")
    cia_cols[i].progress(clamp(v))

# --- 6. GAME ENGINE ---
if g['game_over'] or g['ceo_trust'] <= 0: st.error("💀 GAME OVER: Du wurdest terminiert."); st.stop()
if g['won']: st.balloons(); st.success("🏆 ZERTIFIZIERT!"); st.stop()

col_main, col_side = st.columns([2, 1])

with col_main:
    # ACTIONS MIT MEHR HANDLUNGSSPIELRAUM
    st.subheader("🕹️ Strategische Operationen")
    t1, t2, t3, t4 = st.tabs(["🏗️ Bauen", "🔍 Analyse", "🤝 Politik", "⚖️ Audit"])
    
    with t1:
        if st.button(f"BSI-Schicht {g['layers']+1} (150k | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1
                add_log(f"Schicht {g['layers']} implementiert."); st.rerun()
                
    with t2:
        if st.button("Honeypot aufstellen (1 AP | Senkt KI-Wissen)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['ai_knowledge'] = max(0.05, g['ai_knowledge'] - 0.1)
                add_log("KI wurde in Honeypot gelockt!", "ai"); st.rerun()

    with t3:
        if st.button("Reporting an CEO (1 AP | +Trust)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['ceo_trust'] = min(100, g['ceo_trust'] + 15)
                add_log("CEO ist beeindruckt.", "trust"); st.rerun()

    with t4:
        if st.button("Freiwilliges Audit (1 AP | +XP/-Risk)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

with col_side:
    st.subheader("🧠 KI-Bayes-Risk")
    st.write(f"Wahrscheinlichkeit Hack: {int(g['ai_knowledge']*100)}%")
    st.progress(clamp(g['ai_knowledge']*100))
    
    st.subheader("📟 HUD Log")
    log_box = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_box}</div>", unsafe_allow_html=True)
    
    if st.button("⏭️ TAG BEENDEN", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        g['ai_knowledge'] += 0.04 + (0.01 * (10 - g['layers']))
        for k in g['cia']: g['cia'][k] -= random.randint(4, 9)
        g['ceo_trust'] -= 5 # Täglicher Trust-Verlust durch Bürokratie
        if random.random() < g['ai_knowledge']:
            g['active_incidents'].append(f"Leak G 0.{random.randint(1,47)}")
        if random.random() < g['p_audit']: g['mode'] = 'audit'
        st.rerun()

# --- 7. RANDOMISIERTER AUDIT-MODUS ---
if g['mode'] == 'audit':
    st.markdown("---")
    # Frage auswählen
    q_data = random.choice(KNOWLEDGE_POOL)
    
    # NEU: Zufällige Anordnung der Antworten
    if 'current_audit_q' not in st.session_state or st.session_state.current_audit_q != q_data['q']:
        options = [(q_data['correct'], True), (q_data['wrong'], False)]
        random.shuffle(options)
        st.session_state.current_audit_options = options
        st.session_state.current_audit_q = q_data['q']

    st.subheader(f"📋 Audit: {q_data['topic']}")
    st.info(q_data['q'])
    
    for text, is_correct in st.session_state.current_audit_options:
        if st.button(text, use_container_width=True):
            if is_correct:
                st.success("Korrekt!")
                g['budget'] += 50000; g['ceo_trust'] += 10; g['mode'] = 'tactical'
                add_log("Audit bestanden!"); del st.session_state.current_audit_q; st.rerun()
            else:
                st.error("Falsch!")
                g['budget'] -= 200000; g['ceo_trust'] -= 20; g['mode'] = 'tactical'
                add_log("Audit verpatzt!", "error"); del st.session_state.current_audit_q; st.rerun()

with st.sidebar:
    st.title("📚 INTEL-CORE")
    search = st.text_input("Suchen...")
    intel_content = {
        "GoBD": "Revisionssicherheit und Integrität digitaler Belege.",
        "EU AI Act": "Verbot von Social Scoring. Hochrisiko-KI braucht Doku.",
        "Maximumprinzip": "Höchster Schutzbedarf einer Komponente = System-Niveau.",
        "CIA": "Confidentiality, Integrity, Availability.",
        "Art. 83 DSGVO": "Strafen bis 20 Mio. € oder 4% Umsatz."
    }
    for k, v in intel_content.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
