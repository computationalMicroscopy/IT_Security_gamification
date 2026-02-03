import streamlit as st
import random
import time

# --- 1. INITIALISIERUNG (Mit komplexem Bayes-Netz) ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2000000, 'ceo_trust': 50,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'risk': 30, 'xp': 0, 'layers': 0, 'specialization': None,
            'logs': ["> BAYES-CORE ONLINE. ANALYSIERE SCHWACHSTELLEN..."],
            'active_incidents': [], 'game_over': False, 'won': False, 'mode': 'tactical',
            'news': "BSI meldet: Silver-Data GmbH steht im Fokus von Phishing-Banden.",
            # BAYES-NETZ PARAMETER
            'p_technical_fail': 0.1,  # Wahrscheinlichkeit für technisches Versagen
            'p_human_error': 0.1,     # Wahrscheinlichkeit für Mitarbeiterfehler
            'p_external_attack': 0.1, # Wahrscheinlichkeit für Hacker
            'ai_learning_rate': 0.02
        }

init_game()
g = st.session_state.game

def clamp(val): return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "🔹", "warn": "⚠️", "error": "🚨", "ai": "🧠"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [T-{g['day']}] {msg}")

# --- 2. ERWEITERTER AUDIT-POOL (PDF-Wissen) ---
AUDIT_POOL = [
    ("Marketing will 'Social Scoring' für Kundenbindung. Erlaubt?", "Nein, verboten (EU AI Act)", "Ja, als High-Risk Einstufung"),
    ("Was besagt das Maximumprinzip nach Dok. 12?", "Schutzbedarf der kritischsten Komponente zählt", "Höchste Kosten bestimmen den Schutz"),
    ("GoBD: Was ist das Hauptziel bei digitalen Rechnungen?", "Unveränderbarkeit (Integrität)", "Schnelle Archivierung"),
    ("DSGVO Art. 83: Wie hoch ist die max. Strafe?", "20 Mio. € oder 4% Weltumsatz", "5 Mio. € oder 1% Weltumsatz"),
    ("Was bedeutet 'Integrität' in der CIA-Triade?", "Daten sind korrekt und unverändert", "Daten sind jederzeit abrufbar"),
    ("Ein System in Schicht 4 hat Schutzbedarf 'Hoch'. Der Rest 'Basis'. Gesamtniveau?", "Hoch (Maximumprinzip)", "Basis (Mittelwert)"),
    ("Welche Phase im PDCA-Zyklus prüft die Wirksamkeit?", "Check", "Act"),
    ("Gefährdung G 0.18: Was wird hier beschrieben?", "Fehlbedienung/Technisches Versagen", "Gezielter Hackerangriff"),
    ("EU AI Act: Was ist ein Beispiel für 'unannehmbares Risiko'?", "Social Scoring durch Behörden/Firmen", "KI-basierte Spamfilter"),
    ("BSI-Grundschutz: Was ist das Ziel der Schichtenbildung?", "Defense in Depth / Tiefenverteidigung", "Reduzierung der Stromkosten")
]

# --- 3. UI & ANIMATIONEN ---
st.set_page_config(page_title="CISO HUD 6.0: Singularity", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #00e5ff; font-family: 'Consolas', monospace; }
    .hud-card { background: rgba(15, 23, 30, 0.9); border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,229,255,0.1); }
    .mission-box { background: linear-gradient(90deg, #000428, #004e92); padding:15px; border-radius:10px; border-left: 5px solid #ff00ff; margin-bottom: 20px; }
    .ai-brain { color: #ff00ff; font-weight: bold; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
    .terminal { background: #000; border: 1px solid #00e5ff; height: 300px; overflow-y: auto; font-size: 0.8em; padding: 10px; color: #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SZENARIO ERKLÄRUNG (Mission Briefing) ---
st.markdown(f"""
    <div class='mission-box'>
        <h2 style='margin:0; color:#ff00ff;'>🎯 SZENARIO: SILVER-DATA GOLD TRADING</h2>
        <p style='margin:5px 0 0 0; color:white;'>
            Du bist CISO der <b>Silver-Data GmbH</b>. Wir handeln mit physischem Gold. 
            Unsere IT verwaltet Transaktionen und Tresor-Logistik. <br>
            <b>DEIN AUFTRAG:</b> Überlebe 25 Tage. Implementiere die <b>10 BSI-Schichten</b>. 
            Das <b>Bayes-Netz</b> der Angreifer lernt aus jeder Lücke in deiner Verteidigung!
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='hud-card'>💰 BUDGET<br><b style='font-size:1.5em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='hud-card'>⚡ AKTIONEN<br><b style='font-size:1.5em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='hud-card'>🗓️ TAG<br><b style='font-size:1.5em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
ai_threat = int((g['p_technical_fail'] + g['p_human_error'] + g['p_external_attack']) * 33.3)
c4.markdown(f"<div class='hud-card' style='border-color:#ff00ff'>🧠 BAYES-RISK<br><b class='ai-brain' style='font-size:1.5em'>{ai_threat}%</b></div>", unsafe_allow_html=True)

st.divider()

# CIA Triade
cia_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "🔒 Vertraulichkeit", "I": "💎 Integrität", "A": "⚡ Verfügbarkeit"}[k]
    cia_cols[i].write(f"**{label}: {v}%**")
    cia_cols[i].progress(clamp(v))

# --- 6. GAME ENGINE ---
if g['game_over']: st.error("🚨 AUDIT FEHLGESCHLAGEN. Silver-Data ist insolvent."); st.stop()
if g['won']: st.balloons(); st.success("🏆 ZERTIFIZIERUNG ERREICHT!"); st.stop()

col_main, col_term = st.columns([2, 1])

with col_main:
    # ZUFALLS-EVENTS (Bayes-gesteuert)
    if g['active_incidents']:
        for inc in g['active_incidents']:
            st.error(f"🔥 INCIDENT: {inc}")
            if st.button(f"Gegenmaßnahme (1 AP)", key=inc):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['cia']['I'] += 10; add_log(f"{inc} gestoppt.")
                    st.rerun()

    st.subheader("🎮 Tactical Command")
    tabs = st.tabs(["🏗️ BSI-Defense", "🔍 Audit & Scan", "⚖️ Governance"])
    
    with tabs[0]:
        if st.button(f"BSI-Schicht {g['layers']+1} ausrollen (150k € | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000 and g['layers'] < 10:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1
                # Bayes-Update: Risiko sinkt
                g['p_external_attack'] = max(0.05, g['p_external_attack'] - 0.04)
                add_log(f"Schicht {g['layers']} gesichert. Hacker-Erfolgschance sinkt."); st.rerun()

    with tabs[1]:
        if st.button("Vulnerability Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'random_event'; st.rerun()

    with tabs[2]:
        if st.button("Compliance-Audit (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

with col_term:
    st.subheader("📟 System-Log")
    log_box = "".join([f"<div style='margin-bottom:4px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_box}</div>", unsafe_allow_html=True)
    
    if st.button("⏭️ TAG BEENDEN", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        # BAYES-LERNEN: KI analysiert Schwachstellen
        g['p_human_error'] += 0.02 + (0.01 * (10 - g['layers']))
        g['p_external_attack'] += 0.03
        
        # Würfel basierend auf Bayes-Wahrscheinlichkeiten
        if random.random() < g['p_external_attack']:
            g['active_incidents'].append(f"Hacker-Angriff G 0.{random.randint(10,47)}")
        if random.random() < g['p_human_error']:
            g['active_incidents'].append("Mitarbeiter-Fehler (Social Engineering)")
            
        for k in g['cia']: g['cia'][k] -= random.randint(4, 10)
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
        st.rerun()

# --- 7. DYNAMISCHE MODI (Audit & Zufall) ---
if g['mode'] == 'audit':
    st.markdown("---")
    q, a_correct, a_wrong = random.choice(AUDIT_POOL)
    st.info(f"**AUDIT-FRAGE:** {q}")
    if st.button(a_correct):
        g['xp'] += 200; g['budget'] += 50000; g['mode'] = 'tactical'; add_log("Audit bestanden!", "info"); st.rerun()
    if st.button(a_wrong):
        g['budget'] -= 200000; g['mode'] = 'tactical'; add_log("Compliance-Verstoß!", "error"); st.rerun()

if g['mode'] == 'random_event':
    st.markdown("---")
    events = [
        ("Ein USB-Stick liegt auf dem Parkplatz.", "Vernichten", "Anschließen zum Prüfen"),
        ("Software-Update für Tresor-Steuerung verfügbar.", "Erst in Sandbox testen (PDCA)", "Sofort einspielen"),
        ("Marketing will KI-Gesichtsscan für Kunden.", "EU AI Act prüfen", "Kundenkomfort priorisieren")
    ]
    ev, opt1, opt2 = random.choice(events)
    st.warning(f"**ZUFALLS-EVENT:** {ev}")
    if st.button(opt1): g['xp'] += 100; g['mode'] = 'tactical'; add_log("Sicher reagiert."); st.rerun()
    if st.button(opt2): g['cia']['C'] -= 20; g['mode'] = 'tactical'; add_log("Sicherheitsrisiko ignoriert!", "error"); st.rerun()

with st.sidebar:
    st.title("📚 INTEL")
    st.write("Szenario: Silver-Data HQ")
    st.write("Ziel: BSI-Konformität")
    search = st.text_input("Spickzettel (PDF-Wissen)...")
    intel_data = {
        "BSI Schichten": "Die 10 Ebenen der Verteidigung (Defense in Depth).",
        "GoBD": "Sichert die Integrität digitaler Finanzdaten.",
        "EU AI Act": "Regelt KI-Risiken. Social Scoring = Verboten.",
        "Maximumprinzip": "Die schwächste, aber wichtigste Stelle bestimmt den Schutzbedarf.",
        "PDCA": "Plan-Do-Check-Act. Kontinuierliche Verbesserung."
    }
    for k, v in intel_data.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
