import streamlit as st
import random
import time

# --- 1. INITIALISIERUNG ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2000000, 'ceo_trust': 50,
            'cia': {'C': 65, 'I': 65, 'A': 65},
            'stress': 0, 'risk': 30, 'xp': 0,
            'layers': 0, 'specialization': None,
            'logs': ["> INITIALISIERUNG ABGESCHLOSSEN. SYSTEME BEREIT."],
            'active_incidents': [], 'decisions_made': 0,
            'game_over': False, 'won': False, 'mode': 'tactical'
        }

init_game()
g = st.session_state.game

def add_log(msg, type="info"):
    icon = {"info": "🔹", "warn": "⚠️", "error": "🚨", "lvl": "⭐"}.get(type, "•")
    g['logs'].insert(0, f"{icon} [Tag {g['day']}] {msg}")

# --- 2. INTEL-DATENBANK (UNGEKÜRZT) ---
INTEL = {
    "10 Schichten (BSI)": "Infrastruktur, Netz, IT-Systeme, Anwendungen, Prozesse etc. Jede Schicht reduziert die Risk Exposure.",
    "47 Gefährdungen": "Elementare Bedrohungen (G 0.1 bis G 0.47) laut BSI. Jede Entscheidung kontert spezifische Gefährdungen.",
    "Maximumprinzip": "Das Schutzniveau richtet sich nach dem Baustein mit dem höchsten Schutzbedarf (Dok. 12).",
    "GoBD": "Grundsätze zur ordnungsgemäßen Buchführung. Fokus: Integrität und Unveränderbarkeit digitaler Daten.",
    "EU AI Act": "Risikoklassen für KI. Social Scoring ist 'unannehmbar' und somit verboten.",
    "DSGVO Art. 83": "Strafmaß: Bis zu 20 Mio. € oder 4% des weltweiten Vorjahresumsatzes.",
    "PDCA-Zyklus": "Plan-Do-Check-Act. Der Standardprozess für Managementsysteme (ISO 27001 / BSI)."
}

# --- 3. UI & DESIGN ---
st.set_page_config(page_title="CISO Tactical 4.0", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #00e5ff; font-family: 'Consolas', monospace; }
    .metric-card { background: #0f171e; border: 1px solid #00e5ff; padding: 15px; border-radius: 8px; text-align: center; }
    .terminal-box { background: #000; border: 1px solid #ff00ff; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("📟 CORE INTEL")
    st.write(f"**Status:** {'🟢 Stabil' if g['risk'] < 40 else '🔴 Kritisch'}")
    st.progress(g['risk'] / 100)
    st.divider()
    st.subheader("Lexikon (PDF-Wissen)")
    search = st.text_input("Suche...")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)

# --- 5. DASHBOARD ---
st.title("🛡️ CISO Command: Silver-Data 2026")
m1, m2, m3, m4 = st.columns(4)
m1.markdown(f"<div class='metric-card'>💰 BUDGET<br><b style='font-size:1.5em'>{g['budget']:,} €</b></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-card'>⚡ AKTIONEN<br><b style='font-size:1.5em'>{g['ap']} / 5</b></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-card'>🗓️ TAG<br><b style='font-size:1.5em'>{g['day']} / 25</b></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-card'>🏆 XP<br><b style='font-size:1.5em'>{g['xp']}</b></div>", unsafe_allow_html=True)

st.divider()

# CIA PROGRESS

c_cols = st.columns(3)
for i, (k, v) in enumerate(g['cia'].items()):
    label = {"C": "🔒 Vertraulichkeit", "I": "💎 Integrität", "A": "⚡ Verfügbarkeit"}[k]
    c_cols[i].write(f"**{label}: {v}%**")
    c_cols[i].progress(max(0, min(100, v)))

# --- 6. GAME OVER / WIN ---
if g['game_over']:
    st.error("🚨 MISSION FEHLGESCHLAGEN. Die Silver-Data GmbH wurde vom Markt genommen."); st.stop()
if g['won']:
    st.balloons(); st.success("🏆 AUDIT BESTANDEN! Du hast Silver-Data in ein digitales Fort verwandelt."); st.stop()

# --- 7. DYNAMISCHES GAMEPLAY ---
col_main, col_side = st.columns([2, 1])

with col_main:
    # SPEZIALISIERUNGS-EVENT AN TAG 5
    if g['day'] == 5 and g['specialization'] is None:
        st.warning("📣 STRATEGISCHE ENTSCHEIDUNG ERFORDERLICH!")
        st.write("Der Vorstand verlangt eine klare Marschrichtung. Das beeinflusst deine Tools!")
        c_spec1, c_spec2 = st.columns(2)
        if c_spec1.button("☁️ CLOUD FIRST (Fokus auf Flexibilität & AI)"):
            g['specialization'] = 'Cloud'; g['budget'] += 200000; g['decisions_made'] += 1; st.rerun()
        if c_spec2.button("🏰 ON-PREMISE (Fokus auf maximale Kontrolle)"):
            g['specialization'] = 'OnPrem'; g['budget'] -= 100000; g['cia']['I'] += 10; g['decisions_made'] += 1; st.rerun()
        st.stop()

    # ACTION TABS (Variieren je nach Tag und Spezialisierung)
    st.subheader("🛠️ Tactical Operations Center")
    tabs = st.tabs(["🏗️ Do: Bauen", "🔍 Check: Audit", "⚖️ Act: Governance"])
    
    with tabs[0]:
        # Dynamischer Button-Text und Effekt
        if g['layers'] < 10:
            if st.button(f"BSI-Schicht {g['layers']+1}: {'Cloud-Security' if g['specialization']=='Cloud' else 'Hardware-Härtung'} (150k € | 2 AP)"):
                if g['ap'] >= 2 and g['budget'] >= 150000:
                    with st.status("Implementierung läuft..."):
                        time.sleep(1)
                        g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1; g['xp'] += 100
                        g['cia']['A'] += 12; g['risk'] -= 4; g['decisions_made'] += 1
                    st.toast(f"Schicht {g['layers']} aktiv!", icon="✅"); st.rerun()
        
        if g['specialization'] == 'Cloud':
            if st.button("Serverless Patch Management (1 AP)"):
                if g['ap'] >= 1: g['ap'] -= 1; g['cia']['A'] += 5; g['decisions_made'] += 1; add_log("Automatisches Patching aktiv."); st.rerun()

    with tabs[1]:
        st.write("Überprüfe deine Abwehr.")
        if st.button("Deep Vulnerability Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['stress'] += 10; g['decisions_made'] += 1
                if random.random() > 0.6:
                    g['active_incidents'].append(random.choice(["SQL-Injection", "Ransomware-Versuch"]))
                    add_log("Bedrohung entdeckt!", "error")
                else: add_log("Scan unauffällig."); st.rerun()

    with tabs[2]:
        if st.button("KI-Projekt nach EU AI Act prüfen (1 AP)"):
            if g['ap'] >= 1: g['ap'] -= 1; g['mode'] = 'quiz'; g['decisions_made'] += 1; st.rerun()

    # INCIDENT MANAGEMENT
    if g['active_incidents']:
        st.markdown("### 🚨 AKUTGEFAHR!")
        for inc in g['active_incidents']:
            with st.expander(f"GEFAHR: {inc}", expanded=True):
                st.write("Sofortige Reaktion erforderlich (Kosten: 1 AP)")
                if st.button(f"Gegenmaßnahme für {inc} einleiten"):
                    if g['ap'] >= 1:
                        g['ap'] -= 1; g['active_incidents'].remove(inc); g['cia']['I'] += 10; g['xp'] += 150
                        add_log(f"{inc} neutralisiert."); st.rerun()

with col_side:
    st.subheader("📟 System-Logs")
    log_box = "".join([f"<div style='margin-bottom:5px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal-box'>{log_box}</div>", unsafe_allow_html=True)
    
    st.divider()
    with st.chat_message("assistant"):
        st.write(f"**CEO:** 'Tag {g['day']}. Denken Sie an die GoBD-Konformität! Unser Ruf steht auf dem Spiel.'")
    
    if st.button("🌞 TAG BEENDEN", type="primary", use_container_width=True):
        # TAGS-ENDE-LOGIK
        g['day'] += 1; g['ap'] = 5; g['stress'] = max(0, g['stress'] - 5)
        for k in g['cia']: g['cia'][k] -= random.randint(4, 9)
        if g['active_incidents']: g['cia']['I'] -= 20; add_log("Unbehandelte Incidents fressen Integrität!", "error")
        
        # RISIKO-MATRIX AKTUALISIEREN
        
        
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0: g['game_over'] = True
        st.rerun()

# --- 8. QUIZ-MODUS (KEINE HINWEISE) ---
if g['mode'] == 'quiz':
    st.markdown("---")
    with st.container():
        st.subheader("⚖️ Compliance-Prüfung")
        q_data = random.choice([
            ("Marketing will 'Social Scoring' für Bonusprogramme. Dein Urteil laut EU AI Act?", "Verboten (Unannehmbar)", "Erlaubt (Minimales Risiko)"),
            ("Was besagt das Maximumprinzip nach Dok. 12?", "Höchster Schutzbedarf einer Komponente gilt für den Verbund", "Durchschnittlicher Schutzbedarf reicht aus"),
            ("Was ist das Hauptziel der GoBD im IT-Kontext?", "Integrität und Unveränderbarkeit der Belege", "Maximale Geschwindigkeit der Buchung")
        ])
        st.info(q_data[0])
        q_c1, q_c2 = st.columns(2)
        if q_c1.button(q_data[1]):
            g['xp'] += 200; g['ceo_trust'] += 10; g['mode'] = 'tactical'; add_log("Fachfrage korrekt beantwortet!"); st.rerun()
        if q_c2.button(q_data[2]):
            g['budget'] -= 150000; g['ceo_trust'] -= 15; g['mode'] = 'tactical'; add_log("Falsches Urteil gefällt!", "error"); st.rerun()
