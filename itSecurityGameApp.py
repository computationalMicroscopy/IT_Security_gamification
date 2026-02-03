import streamlit as st
import random
import time

# --- 1. DATENBANK DER INHALTLICHEN TIEFE (VOLLSTÄNDIG & UNGEKÜRZT) ---
# Jede Frage referenziert ein spezifisches Lernziel der Unterlagen
KNOWLEDGE_POOL = [
    {"q": "GoBD: Ein Mitarbeiter löscht versehentlich die digitale Signatur einer Eingangsrechnung. Problem?", "a": "Ja, Verstoß gegen Unveränderbarkeit/Integrität", "b": "Nein, solange die PDF noch lesbar ist", "correct": "a", "topic": "GoBD"},
    {"q": "EU AI Act: Das System zur Überwachung der Tresore nutzt 'Emotion Recognition' bei Mitarbeitern. Einstufung?", "a": "Unannehmbares Risiko (Verboten)", "b": "Hochrisiko (Erlaubt mit Auflagen)", "correct": "a", "topic": "AI Act"},
    {"q": "BSI Schicht 10 (Anwendungen): Warum reicht eine Firewall allein nicht aus?", "a": "Defense in Depth erfordert Schutz auf jeder Ebene", "b": "Firewalls wirken nur auf Schicht 3/4", "correct": "a", "topic": "BSI"},
    {"q": "Maximumprinzip: Ein Hilfssystem (Basis) ist mit dem Haupttransaktionsserver (Hoch) vernetzt. Schutzbedarf?", "a": "Hoch (Erbt vom kritischsten System)", "b": "Basis (Durchschnittsbildung)", "correct": "a", "topic": "BSI"},
    {"q": "DSGVO Art. 83: Ein Datenleck bei Gold-Kundenadressen wurde nicht gemeldet. Strafe?", "a": "Bis zu 20 Mio. € oder 4% Jahresumsatz", "b": "Maximal 50.000 € Bußgeld", "correct": "a", "topic": "Recht"},
    {"q": "PDCA: Du stellst fest, dass Backups fehlschlagen. In welcher Phase handelst du zur Korrektur?", "a": "Act (Verbesserungsmaßnahmen einleiten)", "b": "Check (Nur Analyse)", "correct": "a", "topic": "PDCA"},
    {"q": "Integrität (CIA): Wie stellst du sicher, dass Gold-Bestandslisten nicht manipuliert wurden?", "a": "Prüfsummen und digitale Signaturen", "b": "Tägliche Verfügbarkeits-Backups", "correct": "a", "topic": "CIA"},
    {"q": "Gefährdung G 0.18: Ein Admin konfiguriert den Hauptrouter falsch. Welche Kategorie?", "a": "Fehlbedienung / Technisches Versagen", "b": "Vorsätzliche Handlung / Sabotage", "correct": "a", "topic": "BSI"},
    {"q": "Schutzbedarf 'Sehr Hoch': Was ist die Konsequenz für die Infrastruktur?", "a": "Redundante Standorte und strikte Zugriffskontrolle", "b": "Einfache Passwortsperre reicht", "correct": "a", "topic": "BSI"},
    {"q": "EU AI Act: Silver-Data nutzt KI zur Kreditwürdigkeitsprüfung von Gold-Käufern. Kategorie?", "a": "Hochrisiko (Strenge Auflagen/Dokumentation)", "b": "Minimales Risiko (Keine Auflagen)", "correct": "a", "topic": "AI Act"},
    {"q": "GoBD: Wie lange müssen Buchungsbelege im Goldhandel revisionssicher aufbewahrt werden?", "a": "10 Jahre", "b": "5 Jahre", "correct": "a", "topic": "GoBD"},
    {"q": "Verfügbarkeit (CIA): Der Gold-Webshop ist 2 Stunden offline. Welcher Wert sinkt?", "a": "Availability (A)", "b": "Confidentiality (C)", "correct": "a", "topic": "CIA"},
    {"q": "BSI-Grundschutz: Was ist ein 'Baustein'?", "a": "Ein Modul mit spezifischen Sicherheitsanforderungen", "b": "Ein physischer Server im Keller", "correct": "a", "topic": "BSI"},
    {"q": "Social Scoring (AI Act): Ein Bonusprogramm bewertet das soziale Verhalten der Kunden. Erlaubt?", "a": "Nein, strikt untersagt", "b": "Ja, bei Einwilligung", "correct": "a", "topic": "AI Act"}
]

# --- 2. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2500000,
            'cia': {'C': 70, 'I': 70, 'A': 70},
            'risk': 30, 'xp': 0, 'layers': 0, 'mode': 'tactical',
            'logs': ["> MISSION START: SILVER-DATA HQ GESICHERT."],
            'active_incidents': [], 'game_over': False, 'won': False,
            # BAYES-KI PARAMETER (Dynamisch lernend)
            'ai_knowledge': 0.1, # KI lernt Schwachstellen
            'p_audit': 0.05,      # Chance auf plötzliches Audit
            'history': []        # Verlauf für KI-Analyse
        }

init_game()
g = st.session_state.game

def clamp(val): return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "ℹ️", "warn": "⚠️", "error": "🚨", "ai": "🧠"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [Tag {g['day']}] {msg}")

# --- 3. UI & HUD DESIGN ---
st.set_page_config(page_title="CISO Tactical 7.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #d0d0d0; font-family: 'Consolas', monospace; }
    .hud-header { background: linear-gradient(90deg, #16222a, #3a6073); padding: 20px; border-radius: 10px; border-bottom: 4px solid #00e5ff; margin-bottom: 25px; }
    .metric-box { background: #0f171e; border: 1px solid #00e5ff; padding: 10px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #ff00ff; color: #00ff41; padding: 10px; height: 350px; overflow-y: auto; font-size: 0.85em; }
    .ai-box { background: #1a001a; border: 1px solid #ff00ff; padding: 10px; border-radius: 5px; color: #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SZENARIO & LERNZIELE ---
st.markdown(f"""
    <div class='hud-header'>
        <h1 style='margin:0; color:#00e5ff;'>🛡️ CISO COMMAND: SILVER-DATA v7.0</h1>
        <p style='margin:10px 0 0 0; color:#fff;'>
            <b>Szenario:</b> Goldhandels-Plattform (Kritische Infrastruktur). 
            <b>Ziel:</b> Compliance nach GoBD, DSGVO und EU AI Act sicherstellen. 
            Implementiere alle 10 BSI-Schichten (Defense in Depth) und bestehe die Bayes-Audits.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---

m1, m2, m3, m4 = st.columns(4)
m1.markdown(f"<div class='metric-box'>💰 BUDGET<br><b style='font-size:1.4em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-box'>⚡ AKTIONEN<br><b style='font-size:1.4em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-box'>📊 SCHICHTEN<br><b style='font-size:1.4em'>{g['layers']} / 10</b></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-box'>📅 TAG<br><b style='font-size:1.4em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)

st.divider()

# CIA-STATUS MIT PDCA-PHASEN
c_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "🔒 Confidentiality", "I": "💎 Integrity", "A": "⚡ Availability"}[k]
    c_cols[i].write(f"**{label}: {v}%**")
    c_cols[i].progress(clamp(v))

# --- 6. GAME ENGINE & KI-LOGIK ---
if g['game_over']: st.error("💀 MISSION FEHLGESCHLAGEN."); st.stop()
if g['won']: st.balloons(); st.success("🏆 AUDIT BESTANDEN!"); st.stop()

col_main, col_side = st.columns([2, 1])

with col_main:
    # BAYES-NETZ: WAHRSCHEINLICHKEIT VON INCIDENTS BERECHNEN
    # P(Hack | Lücke) steigt, wenn CIA niedrig ist oder Schichten fehlen
    if g['active_incidents']:
        st.subheader("🚨 AKUTE BEDROHUNGEN")
        for inc in g['active_incidents']:
            st.warning(f"KRITISCH: {inc}")
            if st.button(f"Gegenmaßnahme einleiten (1 AP)", key=inc):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['cia']['I'] += 10
                    add_log(f"Angriff {inc} neutralisiert."); st.rerun()

    # TACTICAL INTERFACE
    st.subheader("🕹️ CISO Operations")
    t1, t2, t3 = st.tabs(["🏗️ Do: Implementation", "🔍 Check: Monitoring", "⚖️ Act: Compliance"])
    
    with t1:
        if st.button(f"BSI-Schicht {g['layers']+1} aktivieren (150k € | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000 and g['layers'] < 10:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1
                g['p_audit'] += 0.05 # Mehr Schichten = Mehr Aufmerksamkeit vom Auditor
                add_log(f"Schicht {g['layers']} (BSI Baustein) aktiv."); st.rerun()
        
        if st.button("Awareness-Kampagne (DSGVO/GoBD) (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['cia']['C'] += 5; g['cia']['I'] += 5; add_log("Mitarbeiter sensibilisiert."); st.rerun()

    with t2:
        if st.button("Großer Schwachstellen-Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

    with t3:
        if st.button("Vorstands-Meeting: Reporting (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'audit'; st.rerun()

with col_side:
    st.subheader("🧠 KI-Analyse (Bayes)")
    ai_risk = int(g['p_audit'] * 100)
    st.markdown(f"<div class='ai-box'>Audit-Wahrscheinlichkeit: {ai_risk}%<br>KI-Lerneffekt: {int(g['ai_knowledge']*100)}%</div>", unsafe_allow_html=True)
    
    st.subheader("📟 HUD Log")
    log_box = "".join([f"<div>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_box}</div>", unsafe_allow_html=True)
    
    if st.button("🌞 TAG BEENDEN", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        # Werte-Zerfall & KI-Wachstum
        g['ai_knowledge'] += 0.03 + (0.01 * (10 - g['layers']))
        for k in g['cia']: g['cia'][k] -= random.randint(4, 9)
        
        # Bayes-Würfel für Angriffe
        if random.random() < g['ai_knowledge']:
            g['active_incidents'].append(f"G {random.randint(1,47)} - Hackerangriff")
        
        # Chance auf plötzliches Audit
        if random.random() < g['p_audit']:
            g['mode'] = 'audit'
            
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
        st.rerun()

# --- 7. VOLLSTÄNDIGER AUDIT-MODUS (DYNAMIC) ---
if g['mode'] == 'audit':
    st.markdown("---")
    st.subheader("📋 UNANGEKÜNDIGTES AUDIT / COMPLIANCE-CHECK")
    # Wählt eine zufällige Frage aus dem massiven Pool
    q_data = random.choice(KNOWLEDGE_POOL)
    st.info(f"**THEMA: {q_data['topic']}**\n\n{q_data['q']}")
    
    btn_a = st.button(f"A: {q_data['a']}")
    btn_b = st.button(f"B: {q_data['b']}")
    
    if btn_a or btn_b:
        user_choice = "a" if btn_a else "b"
        if user_choice == q_data['correct']:
            st.success("KORREKT! Bonus-XP und Budget gesichert.")
            g['xp'] += 300; g['budget'] += 50000; g['mode'] = 'tactical'
            add_log(f"Audit {q_data['topic']} bestanden.", "lvl")
        else:
            st.error("FALSCH! Bußgeld und Reputationsverlust.")
            g['budget'] -= 250000; g['cia']['I'] -= 20; g['mode'] = 'tactical'
            add_log(f"Fehler bei {q_data['topic']}!", "error")
        st.rerun()

# --- SIDEBAR WISSEN (UNGEKÜRZT) ---
with st.sidebar:
    st.title("📚 INTEL-REPOSITORIUM")
    search = st.text_input("Suchen (z.B. AI Act, GoBD)...")
    intel_content = {
        "GoBD": "Grundsätze zur ordnungsgemäßen Führung und Aufbewahrung von Büchern, Aufzeichnungen und Unterlagen in elektronischer Form. Zentral: Integrität & Nachvollziehbarkeit.",
        "EU AI Act": "Risikobasierter Ansatz für KI. Verbotet Social Scoring und biometrische Identifizierung in Echtzeit. Strenge Dokumentation für Hochrisiko-KI.",
        "BSI Schichten": "Modell zur Tiefenverteidigung. Reicht von Schicht 1 (Infrastruktur) bis Schicht 10 (Anwendungen).",
        "Maximumprinzip": "In einem Verbund bestimmt der Baustein mit dem höchsten Schutzbedarf das Gesamtniveau des Verbunds.",
        "CIA-Triade": "Confidentiality (Vertraulichkeit), Integrity (Integrität/Echtheit), Availability (Verfügbarkeit).",
        "PDCA": "Plan-Do-Check-Act: Methode zur kontinuierlichen Verbesserung von IT-Sicherheitsprozessen.",
        "Art. 83 DSGVO": "Regelt Geldbußen. Schwere Verstöße kosten bis zu 20 Mio. Euro oder 4% des globalen Vorjahresumsatzes."
    }
    for k, v in intel_content.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
