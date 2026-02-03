import streamlit as st
import random
import time

# --- 1. INITIALISIERUNG (Mit KI-Gedächtnis) ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2000000, 'ceo_trust': 50,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'stress': 10, 'risk': 30, 'xp': 0,
            'layers': 0, 'specialization': None,
            'logs': ["> SYSTEM ONLINE. BAYES-NETZWERK ANALYSIERT BEDROHUNGEN."],
            'active_incidents': [], 'decisions_made': 0,
            'game_over': False, 'won': False, 'mode': 'tactical',
            'news': "BSI meldet: KI-gestützte Angriffe nehmen zu.",
            # --- NEUE KI PARAMETER ---
            'ai_aggressiveness': 0.1, # Start-Wahrscheinlichkeit
            'ai_learned_vulnerabilities': 0, # Wie viel die KI über dich weiß
            'last_attack_success': False
        }

init_game()
g = st.session_state.game

def clamp(val):
    return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "🔹", "warn": "⚠️", "error": "🚨", "lvl": "⭐", "ai": "🧠"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [T-{g['day']}] {msg}")

# --- 2. INTEL-DATENBANK (UNGEKÜRZT) ---
INTEL = {
    "Bayessches Netzwerk (KI)": "Berechnet Wahrscheinlichkeiten für Angriffe basierend auf deinen Lücken. Je länger du wartest, desto 'sicherer' ist sich die KI, wo sie zuschlagen muss.",
    "10 Schichten (BSI)": "Infrastruktur bis Anwendung. Jede Schicht senkt die Risk Exposure.",
    "Maximumprinzip": "Schutzbedarf der kritischsten Komponente bestimmt das Gesamtniveau (Dok. 12).",
    "GoBD": "Vorgaben für digitale Buchführung. Fokus: Integrität digitaler Daten.",
    "EU AI Act": "Verbot von Social Scoring. Dokumentationspflicht für Hochrisiko-KI.",
    "DSGVO Art. 83": "Geldbußen bis zu 20 Mio. € oder 4% des Jahresumsatzes.",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Der Motor deines ISMS."
}

# --- 3. UI & ANIMATIONEN ---
st.set_page_config(page_title="CISO HUD: AI-Invasion", layout="wide")
st.markdown(f"""
    <style>
    @keyframes scanline {{ 0% {{ top: 0%; }} 100% {{ top: 100%; }} }}
    .stApp {{ background-color: #050a0f; color: #00e5ff; font-family: 'Consolas', monospace; }}
    .hud-card {{ background: rgba(15, 23, 30, 0.9); border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,229,255,0.2); }}
    .ai-alert {{ border: 2px solid #ff00ff; background: #1a001a; padding: 10px; border-radius: 5px; animation: pulse 1.5s infinite; }}
    @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
    .terminal-box {{ background: #000; border: 1px solid #00e5ff; padding: 10px; height: 320px; overflow-y: auto; font-size: 0.8em; color: #00ff41; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. MISSION BRIEFING ---
st.markdown(f"""
    <div style='background: linear-gradient(90deg, #000428, #004e92); padding:15px; border-radius:10px; border-left: 5px solid #ff00ff;'>
        <h2 style='margin:0; color:#ff00ff;'>🧠 KI-BEDROHUNG AKTIV: BAYES-SHADOW</h2>
        <p style='margin:5px 0 0 0; color:white;'>
            Die Angreifer nutzen ein Bayessches Netzwerk. <b>Die KI lernt aus deiner Untätigkeit.</b> 
            Jeder Tag ohne Scan erhöht ihre Erfolgschance!
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. DASHBOARD ---
st.write("")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='hud-card'>💰 BUDGET<br><b style='font-size:1.5em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='hud-card'>⚡ AKTIONEN<br><b style='font-size:1.5em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='hud-card'>🗓️ TAG<br><b style='font-size:1.5em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
# KI-Bereitschaft anzeigen
ai_prob = min(100, int(g['ai_aggressiveness'] * 100))
c4.markdown(f"<div class='hud-card' style='border-color:#ff00ff'>🧠 KI-POWER<br><b style='font-size:1.5em'>{ai_prob}%</b></div>", unsafe_allow_html=True)

st.divider()

# CIA TRIAD
cia_cols = st.columns(3)
cia_labels = {"C": "🔒 Vertraulichkeit", "I": "💎 Integrität", "A": "⚡ Verfügbarkeit"}
for i, (k, v) in enumerate(g['cia'].items()):
    cia_cols[i].write(f"**{cia_labels[k]}: {v}%**")
    cia_cols[i].progress(clamp(v))

# --- 6. GAME ENGINE LOGIK ---
if g['game_over']: st.error("🚨 KRITISCHER SYSTEMAUSFALL."); st.stop()
if g['won']: st.balloons(); st.success("🏆 AUDIT BESTANDEN!"); st.stop()

col_main, col_term = st.columns([2, 1])

with col_main:
    # BAYES-HACK SCENARIOS
    if g['active_incidents']:
        st.subheader("⚠️ LIVENETZ-HACKS (KI-gesteuert)")
        for inc in g['active_incidents']:
            st.markdown(f"<div class='ai-alert'>🚨 KI-ANGRIFF: {inc} nutzt deine Schwachstellen!</div>", unsafe_allow_html=True)
            if st.button(f"Gegenangriff starten (1 AP)", key=inc):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['cia']['I'] += 10
                    add_log(f"KI-Hack {inc} gestoppt!", "ai"); st.rerun()

    # TACTICAL HUD
    st.subheader("🎮 Command Console")
    tabs = st.tabs(["🏗️ Verteidigung", "🔍 KI-Gegenmaßnahme", "⚖️ Compliance"])
    
    with tabs[0]:
        if st.button(f"BSI-Schicht {g['layers']+1} (150k € | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1
                g['ai_aggressiveness'] = max(0.1, g['ai_aggressiveness'] - 0.05)
                add_log("Verteidigung gestärkt. KI-Wahrscheinlichkeit sinkt."); st.rerun()

    with tabs[1]:
        if st.button("KI-Verwirrungstaktik / Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['ai_learned_vulnerabilities'] = 0
                if random.random() < g['ai_aggressiveness']:
                    g['active_incidents'].append(random.choice(["Neural-Exploit", "Bayes-Injection"]))
                    add_log("KI hat deinen Scan gekontert!", "error")
                else: add_log("KI-Daten korrumpiert. Wir sind wieder sicher."); st.rerun()

    with tabs[2]:
        if st.button("Revision (GoBD/AI Act)"):
            g['mode'] = 'quiz'; st.rerun()

with col_term:
    st.subheader("📟 HUD-LOG")
    log_box = "".join([f"<div style='margin-bottom:4px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal-box'>{log_box}</div>", unsafe_allow_html=True)
    
    if st.button("⏭️ NÄCHSTER TAG", type="primary", use_container_width=True):
        g['day'] += 1; g['ap'] = 5
        # KI LERNT ÜBER NACHT (Bayessches Wachstum)
        g['ai_aggressiveness'] += 0.05 + (0.02 * (10 - g['layers']))
        
        # Würfeln, ob KI angreift
        if random.random() < g['ai_aggressiveness']:
            g['active_incidents'].append(f"G {random.randint(1,47)}")
            add_log("Die KI hat eine Lücke gefunden!", "error")
        
        for k in g['cia']: g['cia'][k] -= random.randint(4, 10)
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()): g['game_over'] = True
        st.rerun()

# --- 7. QUIZ ---
if g['mode'] == 'quiz':
    st.markdown("---")
    q = random.choice([
        ("Ist Social Scoring laut EU AI Act erlaubt?", "Nein", "Ja"),
        ("Was besagt das Maximumprinzip?", "Höchster Schutzbedarf zählt", "Durchschnitt zählt"),
        ("Was schützt die Integrität laut GoBD?", "Unveränderbarkeit der Daten", "Passwortlänge")
    ])
    st.info(f"**Audit-Frage:** {q[0]}")
    if st.button(q[1]): g['xp'] += 200; g['mode'] = 'tactical'; add_log("Korrekt!"); st.rerun()
    if st.button(q[2]): g['budget'] -= 200000; g['mode'] = 'tactical'; add_log("Fehler!", "error"); st.rerun()

with st.sidebar:
    st.title("📚 INTEL-CORE")
    search = st.text_input("Suchen...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
