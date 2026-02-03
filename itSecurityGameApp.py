import streamlit as st
import random
import time

# --- 1. DATENBANK DER INHALTLICHEN TIEFE (VOLLSTÄNDIG) ---
KNOWLEDGE_POOL = [
    {"q": "GoBD: Ein Mitarbeiter löscht die digitale Signatur einer Eingangsrechnung. Problem?", "a": "Ja, Verstoß gegen Unveränderbarkeit/Integrität", "b": "Nein, solange die PDF noch lesbar ist", "correct": "a", "topic": "GoBD"},
    {"q": "EU AI Act: Das System nutzt 'Emotion Recognition' bei Mitarbeitern. Einstufung?", "a": "Unannehmbares Risiko (Verboten)", "b": "Hochrisiko (Erlaubt mit Auflagen)", "correct": "a", "topic": "AI Act"},
    {"q": "BSI Schicht 10: Warum reicht eine Firewall allein nicht aus?", "a": "Defense in Depth erfordert Schutz auf jeder Ebene", "b": "Firewalls wirken nur auf Schicht 3/4", "correct": "a", "topic": "BSI"},
    {"q": "Maximumprinzip: Ein Hilfssystem vernetzt mit Hauptserver (Hoch). Schutzbedarf?", "a": "Hoch (Erbt vom kritischsten System)", "b": "Basis (Durchschnittsbildung)", "correct": "a", "topic": "BSI"},
    {"q": "DSGVO Art. 83: Datenleck bei Kundenadressen wurde nicht gemeldet. Strafe?", "a": "Bis zu 20 Mio. € oder 4% Jahresumsatz", "b": "Maximal 50.000 € Bußgeld", "correct": "a", "topic": "Recht"},
    {"q": "PDCA: Backups schlagen fehl. In welcher Phase handelst du zur Korrektur?", "a": "Act (Verbesserungsmaßnahmen einleiten)", "b": "Check (Nur Analyse)", "correct": "a", "topic": "PDCA"},
    {"q": "Integrität (CIA): Wie sicherst du Gold-Bestandslisten gegen Manipulation?", "a": "Prüfsummen und digitale Signaturen", "b": "Tägliche Verfügbarkeits-Backups", "correct": "a", "topic": "CIA"},
    {"q": "Gefährdung G 0.18: Ein Admin konfiguriert den Hauptrouter falsch. Kategorie?", "a": "Fehlbedienung / Technisches Versagen", "b": "Vorsätzliche Handlung / Sabotage", "correct": "a", "topic": "BSI"},
    {"q": "EU AI Act: KI zur Kreditwürdigkeitsprüfung von Gold-Käufern. Kategorie?", "a": "Hochrisiko (Strenge Auflagen)", "b": "Minimales Risiko", "correct": "a", "topic": "AI Act"},
    {"q": "BSI-Grundschutz: Was ist ein 'Baustein'?", "a": "Ein Modul mit Sicherheitsanforderungen", "b": "Ein physischer Server", "correct": "a", "topic": "BSI"}
]

# --- 2. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2500000,
            'cia': {'C': 70, 'I': 70, 'A': 70},
            'risk': 30, 'xp': 0, 'layers': 0, 'mode': 'tactical',
            'logs': ["> MISSION START: SILVER-DATA HQ BEREIT."],
            'active_incidents': [], 'game_over': False, 'won': False,
            'ai_knowledge': 0.1, 'p_audit': 0.05
        }

init_game()
g = st.session_state.game

def clamp(val): return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "ℹ️", "warn": "⚠️", "error": "🚨", "ai": "🧠"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [Tag {g['day']}] {msg}")

# --- 3. UI & ANIMATIONEN ---
st.set_page_config(page_title="CISO Command 8.0", layout="wide")
st.markdown("""
    <style>
    @keyframes glitch { 0% { text-shadow: 2px 0 red; } 50% { text-shadow: -2px 0 blue; } 100% { text-shadow: 2px 0 red; } }
    @keyframes pulse-red { 0% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); } 70% { box-shadow: 0 0 0 15px rgba(255, 0, 0, 0); } 100% { box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); } }
    
    .stApp { background-color: #050a0f; color: #d0d0d0; font-family: 'Consolas', monospace; }
    .hud-header { background: linear-gradient(90deg, #16222a, #3a6073); padding: 20px; border-radius: 10px; border-bottom: 4px solid #00e5ff; }
    .glitch-text { animation: glitch 1s infinite; color: #00e5ff; font-weight: bold; }
    .metric-box { background: #0f171e; border: 1px solid #00e5ff; padding: 10px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #ff00ff; color: #00ff41; padding: 10px; height: 350px; overflow-y: auto; font-size: 0.85em; border-radius: 5px; }
    .incident-alert { background: #330000; border: 2px solid #ff0000; padding: 10px; animation: pulse-red 2s infinite; border-radius: 5px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SZENARIO & ANLEITUNG ---
with st.expander("📖 SPIELANLEITUNG & MISSION-BRIEFING", expanded=True):
    st.markdown("""
    ### Willkommen, CISO!
    Du leitest die Sicherheit der **Silver-Data GmbH** (Goldhandel). Dein Ziel ist das erfolgreiche BSI-Audit an **Tag 25**.
    
    **Deine Werkzeuge:**
    1.  **Do (Implementation):** Baue die 10 BSI-Schichten auf. Jede Schicht senkt das Angriffsrisiko.
    2.  **Check (Monitoring):** Nutze Scans, um Schwachstellen zu finden, bevor die KI es tut.
    3.  **Act (Compliance):** Beantworte Audit-Fragen korrekt, um Bußgelder (DSGVO/AI Act) zu vermeiden.
    
    **Die Bedrohung:**
    Ein **Bayessches Netzwerk** (KI) lernt aus deinen Fehlern. Wenn deine Integrität (I) sinkt oder Schichten fehlen, steigen die Chancen für Hacks und unangekündigte Audits!
    """)

st.markdown("<div class='hud-header'><h1 class='glitch-text'>🛡️ CISO COMMAND v8.0</h1></div>", unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.markdown(f"<div class='metric-box'>💰 BUDGET<br><b style='font-size:1.4em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-box'>⚡ AKTIONEN<br><b style='font-size:1.4em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-box'>📊 BSI-LAYERS<br><b style='font-size:1.4em'>{g['layers']} / 10</b></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-box'>📅 TAG<br><b style='font-size:1.4em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)

st.divider()

# CIA Triad & PDCA Integration

cia_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "🔒 Confidentiality", "I": "💎 Integrity", "A": "⚡ Availability"}[k]
    cia_cols[i].write(f"**{label}: {v}%**")
    cia_cols[i].progress(clamp(v))

# --- 6. GAME ENGINE ---
if g['game_over']: st.error("💀 SYSTEMAUSFALL: Silver-Data wurde geschlossen."); st.stop()
if g['won']: st.balloons(); st.success("🏆 AUDIT BESTANDEN! Gold-Standard erreicht."); st.stop()

col_main, col_side = st.columns([2, 1])

with col_main:
    if g['active_incidents']:
        st.subheader("🚨 AKTIVE ALARME")
        for inc in g['active_incidents']:
            st.markdown(f"<div class='incident-alert'><b>WARNUNG:</b> {inc} erkannt!</div>", unsafe_allow_html=True)
            if st.button(f"Gegenmaßnahme (1 AP)", key=inc):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['cia']['I'] += 10; add_log(f"Fix: {inc}")
                    st.rerun()

    st.subheader("🕹️ Tactical Interface")
    t1, t2, t3 = st.tabs(["🏗️ Bauen (Do)", "🔍 Prüfen (Check)", "⚖️ Regeln (Act)"])
    
    with t1:
        if st.button(f"BSI-Schicht {g['layers']+1} (150k € | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000 and g['layers'] < 10:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1; g['p_audit'] += 0.04
                add_log(f"Schicht {g['layers']} aktiv."); st.rerun()
        
    with t2:
        if st.button("Deep Scan: Schwachstellen (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

    with t3:
        if st.button("Governance-Revision (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

with col_side:
    st.subheader("🧠 KI-Status")
    st.write(f"KI-Lerneffekt: {int(g['ai_knowledge']*100)}%")
    st.progress(clamp(g['ai_knowledge']*100))
    
    st.subheader("📟 HUD Log")
    log_box = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_box}</div>", unsafe_allow_html=True)
    
    if st.button("⏭️ TAG BEENDEN", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        g['ai_knowledge'] += 0.04 + (0.01 * (10 - g['layers']))
        for k in g['cia']: g['cia'][k] -= random.randint(4, 9)
        if random.random() < g['ai_knowledge']:
            g['active_incidents'].append(f"Bayes-Leak G 0.{random.randint(1,47)}")
        if random.random() < g['p_audit']: g['mode'] = 'audit'
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
        st.rerun()

# --- 7. VOLLSTÄNDIGER AUDIT-MODUS ---
if g['mode'] == 'audit':
    st.markdown("---")
    
    st.subheader("📋 COMPLIANCE-AUDIT")
    q_data = random.choice(KNOWLEDGE_POOL)
    st.info(f"**THEMA: {q_data['topic']}**\n\n{q_data['q']}")
    
    c_a, c_b = st.columns(2)
    if c_a.button(f"A: {q_data['a']}"):
        if q_data['correct'] == 'a':
            g['xp'] += 300; g['budget'] += 50000; g['mode'] = 'tactical'
            add_log("Audit bestanden!", "info"); st.rerun()
        else:
            g['budget'] -= 250000; g['mode'] = 'tactical'
            add_log("Audit fehlgeschlagen!", "error"); st.rerun()
    if c_b.button(f"B: {q_data['b']}"):
        if q_data['correct'] == 'b':
            g['xp'] += 300; g['budget'] += 50000; g['mode'] = 'tactical'
            add_log("Audit bestanden!", "info"); st.rerun()
        else:
            g['budget'] -= 250000; g['mode'] = 'tactical'
            add_log("Audit fehlgeschlagen!", "error"); st.rerun()

with st.sidebar:
    st.title("📚 INTEL-CORE")
    search = st.text_input("Suchen...")
    intel_content = {
        "GoBD": "Revisionssicherheit und Integrität digitaler Belege (10 Jahre Aufbewahrung).",
        "EU AI Act": "Verbot von Social Scoring. Hochrisiko-KI erfordert Dokumentation.",
        "Maximumprinzip": "Höchster Schutzbedarf einer Komponente gilt für das Gesamtsystem.",
        "CIA": "Confidentiality, Integrity, Availability.",
        "Art. 83 DSGVO": "Bußgelder bis zu 20 Mio. € oder 4% Jahresumsatz.",
        "G 0.18": "BSI-Gefährdung: Fehlbedienung und technisches Versagen."
    }
    for k, v in intel_content.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
