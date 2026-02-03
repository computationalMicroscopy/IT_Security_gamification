import streamlit as st
import random
import time

# --- 1. INITIALISIERUNG (Stabil gegen Abstürze) ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2000000, 'ceo_trust': 50,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'stress': 10, 'risk': 30, 'xp': 0,
            'layers': 0, 'specialization': None,
            'logs': ["> SYSTEM INITIALISIERT. WILLKOMMEN CISO."],
            'active_incidents': [], 'decisions_made': 0,
            'game_over': False, 'won': False, 'mode': 'tactical',
            'news': "BSI meldet ruhige Lage im Cyberraum."
        }

init_game()
g = st.session_state.game

# Sicherheits-Funktion für Fortschrittsbalken
def clamp(val):
    return max(0.0, min(1.0, float(val) / 100.0))

def add_log(msg, type="info"):
    icon = {"info": "🔹", "warn": "⚠️", "error": "🚨", "lvl": "⭐"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [Tag {g['day']}] {msg}")

# --- 2. INTEL-DATENBANK (UNGEKÜRZT) ---
INTEL = {
    "10 Schichten (BSI)": "Infrastruktur, Netz, IT-Systeme, Anwendungen, Prozesse etc. Jede Schicht reduziert die Risk Exposure.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 bis G 0.47) laut BSI. Jede Entscheidung kontert spezifische Gefährdungen.",
    "Maximumprinzip": "Das Schutzniveau richtet sich nach dem Baustein mit dem höchsten Schutzbedarf (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Buchführung. Fokus: Integrität und Unveränderbarkeit digitaler Daten.",
    "EU AI Act": "Risikoklassen für KI. Social Scoring ist 'unannehmbar' und somit verboten (Dok. 15).",
    "DSGVO Art. 83": "Strafmaß: Bis zu 20 Mio. € oder 4% des weltweiten Vorjahresumsatzes.",
    "PDCA-Zyklus": "Plan-Do-Check-Act. Der Standardprozess für Managementsysteme (ISO 27001 / BSI)."
}

# --- 3. UI & DESIGN ---
st.set_page_config(page_title="CISO Tactical 4.5", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #00e5ff; font-family: 'Consolas', monospace; }
    .metric-card { background: #0f171e; border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; text-align: center; }
    .terminal-box { background: #000; border: 1px solid #ff00ff; padding: 15px; height: 300px; overflow-y: auto; font-size: 0.85em; }
    .news-ticker { background: #1a1a1a; color: #ff00ff; padding: 5px; border-radius: 5px; border: 1px dashed #ff00ff; margin-bottom: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📟 CORE INTEL")
    st.write("**Gefährdungslage:**")
    st.progress(clamp(g['risk'])) # BUGFIX: Clamp sorgt für Werte zw. 0 und 1
    st.divider()
    st.subheader("Lexikon")
    search = st.text_input("Suchen...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)
    if st.button("HARD RESET"): init_game(True); st.rerun()

# --- 5. DASHBOARD ---
st.title("🛡️ CISO Command: Silver-Data (v4.5)")
st.markdown(f"<div class='news-ticker'>📡 NEWS-FEED: {g['news']}</div>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.markdown(f"<div class='metric-card'>💰 BUDGET<br><b style='font-size:1.5em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-card'>⚡ AKTIONEN<br><b style='font-size:1.5em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-card'>🗓️ TAG<br><b style='font-size:1.5em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-card'>🏆 XP<br><b style='font-size:1.5em'>{g['xp']}</b></div>", unsafe_allow_html=True)

st.divider()

# CIA PROGRESS (Bugfixed with clamp)

c_cols = st.columns(3)
cia_labels = {"C": "🔒 Vertraulichkeit", "I": "💎 Integrität", "A": "⚡ Verfügbarkeit"}
for i, (k, v) in enumerate(g['cia'].items()):
    c_cols[i].write(f"**{cia_labels[k]}: {v}%**")
    c_cols[i].progress(clamp(v))

# --- 6. GAME OVER / WIN ---
if g['game_over']:
    st.error("🚨 MISSION GESCHEITERT: Silver-Data ist offline."); st.stop()
if g['won']:
    st.balloons(); st.success("🏆 AUDIT BESTANDEN! Du bist der Champion."); st.stop()

# --- 7. DYNAMISCHES GAMEPLAY ---
col_main, col_side = st.columns([2, 1])

with col_main:
    # SPEZIALISIERUNG
    if g['day'] >= 5 and g['specialization'] is None:
        st.info("📣 STRATEGISCHE WEICHENSTELLUNG")
        c_s1, c_s2 = st.columns(2)
        if c_s1.button("☁️ CLOUD FOKUS (+Budget)"):
            g['specialization'] = 'Cloud'; g['budget'] += 300000; g['decisions_made'] += 1; st.rerun()
        if c_s2.button("🏰 ON-PREM FOKUS (+Integrität)"):
            g['specialization'] = 'OnPrem'; g['cia']['I'] += 15; g['decisions_made'] += 1; st.rerun()
        st.stop()

    # TACTICAL INTERFACE
    st.subheader("🛠️ Operations Center")
    t1, t2, t3 = st.tabs(["🏗️ Do: Aufbau", "🔍 Check: Audit", "⚖️ Act: Compliance"])
    
    with t1:
        if g['layers'] < 10:
            if st.button(f"BSI-Schicht {g['layers']+1} implementieren (150k € | 2 AP)"):
                if g['ap'] >= 2 and g['budget'] >= 150000:
                    g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1; g['xp'] += 100
                    g['cia']['A'] += 10; g['risk'] -= 5; g['decisions_made'] += 1
                    add_log(f"Schicht {g['layers']} gesichert."); st.rerun()
        
        if st.button("Awareness-Training (40k € | 1 AP)"):
            if g['ap'] >= 1 and g['budget'] >= 40000:
                g['ap'] -= 1; g['budget'] -= 40000; g['cia']['C'] += 10; g['decisions_made'] += 1
                add_log("Mitarbeiter sensibilisiert."); st.rerun()

    with t2:
        if st.button("Vulnerability Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['decisions_made'] += 1
                if random.random() > 0.6:
                    g['active_incidents'].append(random.choice(["SQL-Injektion", "Schwachstelle G 0.18"]))
                    add_log("GEFAHR DETEKTIERT!", "error")
                else: add_log("Scan sauber."); st.rerun()

    with t3:
        if st.button("GoBD & AI Act Prüfung (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['decisions_made'] += 1; g['mode'] = 'quiz'; st.rerun()

    # INCIDENTS
    if g['active_incidents']:
        st.markdown("### 🚨 AKUT-BEDROHUNGEN")
        for inc in g['active_incidents']:
            if st.button(f"FIX: {inc} (1 AP)"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['xp'] += 150; g['cia']['I'] += 10
                    add_log(f"{inc} behoben."); st.rerun()

with col_side:
    st.subheader("📟 System-Log")
    log_box = "".join([f"<div style='margin-bottom:4px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal-box'>{log_box}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🌞 TAG BEENDEN", type="primary"):
        g['day'] += 1; g['ap'] = 5
        # Werte-Zerfall
        for k in g['cia']: g['cia'][k] -= random.randint(3, 8)
        # News-Generator für Abwechslung
        news_list = [
            "BSI warnt vor Phishing-Welle!", "Neuer EU AI Act Entwurf sorgt für Unruhe.",
            "Stromausfall im Nachbarbezirk - USV testen!", "Zero-Day Lücke in Layer 3 entdeckt.",
            "Vorstand verlangt GoBD-Bericht."
        ]
        g['news'] = random.choice(news_list)
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
        st.rerun()

# --- 8. QUIZ-MODUS ---
if g['mode'] == 'quiz':
    st.markdown("---")
    with st.container():
        st.subheader("⚖️ Compliance-Frage")
        q = random.choice([
            ("Darf Silver-Data Social Scoring für Mitarbeiter nutzen?", "Nein, verboten laut AI Act", "Ja, zur Motivationssteigerung"),
            ("Was besagt das Maximumprinzip (Dok. 12)?", "Höchster Schutzbedarf einer Komponente gilt für das System", "Nur die billigste Lösung zählt"),
            ("Was fordert die GoBD für digitale Belege?", "Unveränderbarkeit (Integrität)", "Schicke Formatierung")
        ])
        st.write(f"**Situation:** {q[0]}")
        if st.button(q[1]):
            g['xp'] += 200; g['mode'] = 'tactical'; add_log("Korrekt!"); st.rerun()
        if st.button(q[2]):
            g['budget'] -= 200000; g['mode'] = 'tactical'; add_log("Falsch! Bußgeld fällig.", "error"); st.rerun()
