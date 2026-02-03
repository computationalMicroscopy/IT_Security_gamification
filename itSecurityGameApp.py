import streamlit as st
import random

# --- 1. ROBUSTE INITIALISIERUNG ---
def init_game():
    return {
        'day': 1,
        'ap': 4, # Aktionspunkte
        'budget': 600000,
        'cia': {'C': 60, 'I': 60, 'A': 60},
        'rep': 50,
        'logs': ["> SYSTEM BOOT: Initializing Cyber-Defense-Protocol..."],
        'incident': None,
        'game_over': False,
        'won': False,
        'intel_unlocked': False
    }

if 'game' not in st.session_state:
    st.session_state.game = init_game()

def add_log(msg, type="info"):
    colors = {"info": "#00ff41", "warn": "#f2cc60", "error": "#ff00ff"}
    st.session_state.game['logs'].insert(0, f"<span style='color:{colors.get(type)}'>[Tag {st.session_state.game['day']}] {msg}</span>")

# --- 2. INTEGRIERTES GLOSSAR (Intel-Datenbank) ---
INTEL = {
    "BSI 10-Schichten": "Systematik des Grundschutzes (Infrastruktur bis Anwendung). Jede Schicht braucht eigene Bausteine.",
    "47 Gefährdungen": "Das BSI definiert 47 elementare Gefährdungen (G 0.1 - G 0.47), die im Kompendium geprüft werden müssen.",
    "Maximumprinzip": "Das Gesamtsystem erhält den Schutzbedarf seiner kritischsten Komponente (Dok. 12).",
    "GoBD Integrität": "Vorgabe zur Unveränderbarkeit digitaler Belege. Verletzung führt zu rechtlichen Konsequenzen (Dok. 13).",
    "DSGVO Art. 83": "Strafen bei Datenverlust: Bis zu 4% des Jahresumsatzes oder 20 Mio. €.",
    "EU AI Act": "KI-Risikoklassen: Unannehmbar (Verboten), Hoch (Reguliert), Transparenz (Offenlegung).",
    "PDCA-Zyklus": "Plan-Do-Check-Act: Der Motor des ISMS zur ständigen Verbesserung (Dok. 16)."
}

# --- 3. UI & DESIGN (Cyberpunk Terminal) ---
st.set_page_config(page_title="CISO Tactical Simulator", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Fira Code', monospace; }
    .stat-box { background: #111; border: 1px solid #00ff41; padding: 10px; border-radius: 5px; text-align: center; }
    .terminal { background: #000; border: 1px solid #00ff41; padding: 15px; height: 350px; overflow-y: auto; font-size: 0.9em; border-left: 5px solid #00ff41; }
    .sidebar-intel { background: #161b22; padding: 10px; border-radius: 5px; border: 1px solid #f2cc60; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SZENARIO & SIDEBAR ---
with st.sidebar:
    st.title("📟 MISSION: SILVER-DATA")
    st.markdown("""
    **Szenario:** 2026. Die *Silver-Data GmbH* steht vor einem BSI-Audit. 
    Hacker-Kollektive nutzen Sicherheitslücken im Gold-Handelssystem. 
    
    **Deine Mission:** 1. Überlebe 14 Tage (Audit-Vorbereitung).
    2. Halte die CIA-Werte über 30%.
    3. Verhindere die Insolvenz durch Bußgelder.
    """)
    st.divider()
    st.subheader("📚 Intel-Datenbank (Glossar)")
    for key, val in INTEL.items():
        with st.expander(key):
            st.write(val)

# --- 5. GAME OVER / WIN LOGIC ---
if st.session_state.game['game_over']:
    st.error("🚨 SYSTEM COLLAPSE: Die Silver-Data GmbH wurde zerschlagen.")
    if st.button("Simulation Neustarten"):
        st.session_state.game = init_game()
        st.rerun()
    st.stop()

if st.session_state.game['won']:
    st.balloons()
    st.success("🏆 AUDIT BESTANDEN: Silver-Data ist BSI-Zertifiziert!")
    if st.button("Erneuter Durchlauf"):
        st.session_state.game = init_game()
        st.rerun()
    st.stop()

# --- 6. DASHBOARD ---
st.title("🛡️ CISO Defense Command")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-box'>💰 BUDGET<br><b style='color:white'>{st.session_state.game['budget']:,} €</b></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>⚡ AKTIONSPUNKTE<br><b style='color:white'>{st.session_state.game['ap']} / 4</b></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>🗓️ TAG<br><b style='color:white'>{st.session_state.game['day']} / 14</b></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-box'>📈 REPUTATION<br><b style='color:white'>{st.session_state.game['rep']}%</b></div>", unsafe_allow_html=True)

st.divider()

# PROGRESS BARS
st.write("### 🔒 CIA-Status (Schutzziele)")

cols = st.columns(3)
for i, (k, v) in enumerate(st.session_state.game['cia'].items()):
    label = {"C": "Vertraulichkeit (Confidentiality)", "I": "Integrität (Integrity)", "A": "Verfügbarkeit (Availability)"}[k]
    cols[i].write(f"**{label}**")
    cols[i].progress(max(0, min(100, v)))

# --- 7. TACTICAL OPERATIONS ---
col_act, col_log = st.columns([2, 1])

with col_act:
    st.subheader("🛠️ Verfügbare Maßnahmen")
    t1, t2, t3 = st.tabs(["🏗️ Prävention (Do)", "🔍 Analyse (Check)", "⚖️ Compliance (Act)"])
    
    with t1:
        st.write("Investiere in die BSI-Schichten und technische Härtung.")
        if st.button("BSI-Schicht 1-5 absichern (100k € | 2 AP)"):
            if st.session_state.game['ap'] >= 2 and st.session_state.game['budget'] >= 100000:
                st.session_state.game['ap'] -= 2
                st.session_state.game['budget'] -= 100000
                st.session_state.game['cia']['A'] += 20
                st.session_state.game['cia']['I'] += 10
                add_log("Infrastruktur-Härtung nach BSI-Standard abgeschlossen.")
                st.rerun()

        if st.button("Backup-System (G 0.18) einführen (50k € | 1 AP)"):
            if st.session_state.game['ap'] >= 1 and st.session_state.game['budget'] >= 50000:
                st.session_state.game['ap'] -= 1
                st.session_state.game['budget'] -= 50000
                st.session_state.game['cia']['A'] = 100
                add_log("Resilienz gegen Ransomware durch Backups erhöht.")
                st.rerun()

    with t2:
        st.write("Führe Audits durch, um verdeckte Angriffe zu finden.")
        if st.button("System-Scan nach SQL-Injections (1 AP)"):
            if st.session_state.game['ap'] >= 1:
                st.session_state.game['ap'] -= 1
                if random.random() > 0.4:
                    st.session_state.game['incident'] = "SQL"
                    add_log("KRITISCH: SQL-Injection in der Preisliste gefunden (Integritätsverlust!)", "error")
                else:
                    add_log("Scan sauber. Keine Anomalien detektiert.")
                st.rerun()

    with t3:
        st.write("Stelle die rechtliche Konformität sicher.")
        st.warning("Prüfung: Geplante 'Social Scoring' KI für Kunden.")
        if st.button("KI-Projekt nach EU AI Act prüfen (1 AP)"):
            if st.session_state.game['ap'] >= 1:
                st.session_state.game['ap'] -= 1
                ans = st.selectbox("Einstufung laut AI Act?", ["Hohes Risiko", "Unannehmbares Risiko (Verboten)"], index=None)
                if ans == "Unannehmbares Risiko (Verboten)":
                    st.success("Korrekt! Projekt gestoppt. Keine Bußgelder.")
                    st.session_state.game['rep'] += 15
                elif ans:
                    st.error("FALSCH! DSGVO-Bußgeld fällig (4% vom Budget).")
                    st.session_state.game['budget'] *= 0.96
                    st.session_state.game['rep'] -= 20
                st.rerun()

    # INCIDENT MANAGEMENT
    if st.session_state.game['incident'] == "SQL":
        st.markdown("<div style='border:2px solid #ff00ff; padding:10px;'>", unsafe_allow_html=True)
        st.error("🚨 AKTIVER INCIDENT: Preismanipulation (GoBD-Verstoß)")
        if st.button("Gegenmaßnahme: Datenbank-Härtung (1 AP)"):
            st.session_state.game['ap'] -= 1
            st.session_state.game['incident'] = None
            st.session_state.game['cia']['I'] = min(100, st.session_state.game['cia']['I'] + 30)
            add_log("Datenintegrität wiederhergestellt.")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_log:
    st.subheader("📟 System-Terminal")
    logs = "".join([f"<div>{l}</div>" for l in st.session_state.game['logs']])
    st.markdown(f"<div class='terminal'>{logs}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🌞 TAG BEENDEN"):
        st.session_state.game['day'] += 1
        st.session_state.game['ap'] = 4
        # Entropie: CIA sinkt jeden Tag leicht
        for k in st.session_state.game['cia']:
            st.session_state.game['cia'][k] -= random.randint(5, 12)
        add_log("Neuer Tag beginnt. Schutzziele durch Verschleiß gesunken.")
        
        # Sieg/Niederlage Checks
        if st.session_state.game['day'] > 14:
            st.session_state.game['won'] = True
        if any(v <= 0 for v in st.session_state.game['cia'].values()) or st.session_state.game['budget'] <= 0:
            st.session_state.game['game_over'] = True
        st.rerun()
