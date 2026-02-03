import streamlit as st
import random
import time

# --- 1. INITIALISIERUNG (Absolut stabil) ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2000000, 'ceo_trust': 50,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'stress': 10, 'risk': 30, 'xp': 0,
            'layers': 0, 'specialization': None,
            'logs': ["> SYSTEM ONLINE. BSI-AUDIT IN 25 TAGEN."],
            'active_incidents': [], 'decisions_made': 0,
            'game_over': False, 'won': False, 'mode': 'tactical',
            'news': "BSI meldet: Erhöhte Phishing-Gefahr für Gold-Händler."
        }

init_game()
g = st.session_state.game

def clamp(val):
    return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "🔹", "warn": "⚠️", "error": "🚨", "lvl": "⭐"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [T-{g['day']}] {msg}")

# --- 2. INTEL-DATENBANK (UNGEKÜRZT) ---
INTEL = {
    "10 Schichten (BSI)": "Infrastruktur bis Anwendung. Jede Schicht senkt die Risk Exposure massiv.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 - G 0.47) laut BSI. Jede Schicht blockt spezifische Angriffe.",
    "Maximumprinzip": "Schutzbedarf der kritischsten Komponente bestimmt das Gesamtniveau (Dok. 12).",
    "GoBD": "Vorgaben für digitale Buchführung. Fokus: Integrität & Unveränderbarkeit digitaler Daten.",
    "EU AI Act": "Verbot von Social Scoring. Dokumentationspflicht für Hochrisiko-KI (Dok. 15).",
    "DSGVO Art. 83": "Geldbußen bis zu 20 Mio. € oder 4% des Jahresumsatzes.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Der Standard für ISMS-Verbesserungen."
}

# --- 3. ANIMATIONEN & STYLING ---
st.set_page_config(page_title="CISO Command HUD", layout="wide")
st.markdown(f"""
    <style>
    @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(0, 229, 255, 0.4); }} 70% {{ box-shadow: 0 0 0 10px rgba(0, 229, 255, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(0, 229, 255, 0); }} }}
    @keyframes alert-pulse {{ 0% {{ border-color: #ff0000; }} 50% {{ border-color: #550000; }} 100% {{ border-color: #ff0000; }} }}
    
    .stApp {{ background-color: #050a0f; color: #00e5ff; font-family: 'Consolas', monospace; }}
    .hud-card {{ background: rgba(15, 23, 30, 0.9); border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; animation: pulse 2s infinite; }}
    .incident-card {{ border: 2px solid #ff0000; animation: alert-pulse 1s infinite; padding: 10px; background: #220000; border-radius: 5px; }}
    .terminal-box {{ background: #000; border: 1px solid #00e5ff; padding: 10px; height: 300px; overflow-y: auto; font-size: 0.8em; }}
    .mission-header {{ background: linear-gradient(90deg, #004e92, #000428); padding: 20px; border-radius: 10px; border-bottom: 3px solid #ff00ff; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. MISSION BRIEFING (Das Ziel) ---
st.markdown(f"""
    <div class='mission-header'>
        <h2 style='margin:0; color:#ff00ff;'>🎯 MISSION: OPERATION GOLDEN SHIELD</h2>
        <p style='margin:5px 0 0 0; color:white;'>
            <b>Szenario:</b> Du bist CISO der <i>Silver-Data GmbH</i> (Gold-Handel). <br>
            <b>Ziel:</b> Überlebe <b>25 Tage</b> bis zum BSI-Audit. Maximiere die <b>BSI-Schichten (10)</b> und halte 
            <b>Vertraulichkeit, Integrität & Verfügbarkeit</b> über 0%.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("📟 HUD INTEL")
    st.write("**Gefährdungslage:**")
    st.progress(clamp(g['risk']))
    st.divider()
    st.subheader("Wissens-Datenbank")
    search = st.text_input("Suchen...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
    if st.button("Simulation Neustarten"): init_game(True); st.rerun()

# --- 6. DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='hud-card'>💰 BUDGET<br><b style='font-size:1.5em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='hud-card'>⚡ AKTIONEN<br><b style='font-size:1.5em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='hud-card'>🗓️ TAG<br><b style='font-size:1.5em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
audit_readiness = g['layers'] * 10
c4.markdown(f"<div class='hud-card' style='border-color:#ff00ff'>📋 AUDIT-READY<br><b style='font-size:1.5em'>{audit_readiness}%</b></div>", unsafe_allow_html=True)

st.divider()

# CIA TRIAD VISUALS

cia_cols = st.columns(3)
cia_labels = {"C": "🔒 Vertraulichkeit", "I": "💎 Integrität", "A": "⚡ Verfügbarkeit"}
for i, (k, v) in enumerate(g['cia'].items()):
    cia_cols[i].write(f"**{cia_labels[k]}: {v}%**")
    cia_cols[i].progress(clamp(v))

# --- 7. GAME ENGINE ---
if g['game_over']:
    st.snow()
    st.error("🚨 SYSTEM COLLAPSE. Silver-Data wurde liquidiert."); st.stop()
if g['won']:
    st.balloons()
    st.success("🏆 AUDIT BESTANDEN! Silver-Data ist nun BSI-zertifiziert."); st.stop()

col_main, col_term = st.columns([2, 1])

with col_main:
    # ANIMIERTES INCIDENT BOARD
    if g['active_incidents']:
        st.markdown("### 🚨 AKTIVE ANGRIFFE!")
        for inc in g['active_incidents']:
            st.markdown(f"<div class='incident-card'>ACHTUNG: {inc} erkannt!</div>", unsafe_allow_html=True)
            if st.button(f"Gegenmaßnahme für {inc} (1 AP)", key=inc):
                if g['ap'] >= 1:
                    with st.spinner("Verschlüsselung wird abgewehrt..."):
                        time.sleep(0.5)
                        g['ap'] -= 1; g['active_incidents'].remove(inc); g['cia']['I'] += 10; g['xp'] += 150
                    st.toast(f"{inc} neutralisiert!", icon="🛡️"); st.rerun()

    # TACTICAL HUD
    st.subheader("🛠️ Tactical Operations")
    tabs = st.tabs(["🏗️ Bauen (Do)", "🔍 Prüfen (Check)", "⚖️ Regeln (Act)"])
    
    with tabs[0]:
        if g['layers'] < 10:
            if st.button(f"BSI-Schicht {g['layers']+1} hochfahren (150k € | 2 AP)"):
                if g['ap'] >= 2 and g['budget'] >= 150000:
                    g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1; g['xp'] += 100
                    g['cia']['A'] += 10; g['risk'] -= 5
                    add_log(f"Schicht {g['layers']} implementiert."); st.rerun()
        
        if st.button("Security Awareness Training (40k € | 1 AP)"):
            if g['ap'] >= 1 and g['budget'] >= 40000:
                g['ap'] -= 1; g['budget'] -= 40000; g['cia']['C'] += 10
                add_log("Mitarbeiter geschult."); st.rerun()

    with tabs[1]:
        if st.button("Schwachstellen-Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1
                if random.random() > 0.6:
                    g['active_incidents'].append(random.choice(["SQL-Injektion", "Ransomware"]))
                    add_log("BEDROHUNG GEFUNDEN!", "error")
                else: add_log("Scan sauber."); st.rerun()

    with tabs[2]:
        if st.button("GoBD & AI Act Revision (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['mode'] = 'quiz'; st.rerun()

with col_term:
    st.subheader("📟 System-Log")
    log_box = "".join([f"<div style='margin-bottom:4px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal-box'>{log_box}</div>", unsafe_allow_html=True)
    
    st.divider()
    st.info(f"📡 NEWS: {g['news']}")
    if st.button("⏭️ TAG BEENDEN", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        for k in g['cia']: g['cia'][k] -= random.randint(4, 9)
        if g['active_incidents']: g['cia']['I'] -= 15; add_log("Incident-Schaden über Nacht!", "error")
        
        news_list = ["BSI warnt vor G 0.18!", "CEO fordert AI-Bericht.", "Neues DSGVO-Urteil.", "Patchday steht an."]
        g['news'] = random.choice(news_list)
        
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
        st.rerun()

# --- 8. QUIZ-MODUS ---
if g['mode'] == 'quiz':
    st.markdown("---")
    with st.container():
        st.subheader("⚖️ Compliance-Check")
        q = random.choice([
            ("Darf Silver-Data Social Scoring einführen?", "Nein (EU AI Act)", "Ja (Marketing-Tool)"),
            ("Was fordert die GoBD für Belege?", "Unveränderbarkeit (Integrität)", "Nur Lesbarkeit"),
            ("Maximumprinzip: Was bestimmt den Schutzbedarf?", "Die kritischste Anwendung", "Der Durchschnitt")
        ])
        st.write(f"**Frage:** {q[0]}")
        qc1, qc2 = st.columns(2)
        if qc1.button(q[1]):
            g['xp'] += 200; g['mode'] = 'tactical'; add_log("Korrekte Entscheidung!"); st.rerun()
        if qc2.button(q[2]):
            g['budget'] -= 200000; g['mode'] = 'tactical'; add_log("Compliance-Fehler!", "error"); st.rerun()
