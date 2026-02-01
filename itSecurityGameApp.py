import streamlit as st
import random
import time

# --- KONFIGURATION ---
st.set_page_config(page_title="Silver-Data: Cyber Resilience", layout="wide")

# CSS für Terminal-Look und Animationen
st.markdown("""
    <style>
    .reportview-container { background: #0d1117; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #238636 , #2ea043); }
    .terminal { background-color: #010409; color: #7d8590; padding: 15px; border-radius: 5px; border: 1px solid #30363d; font-family: 'Courier New', monospace; height: 300px; overflow-y: auto; }
    .stButton>button { border-radius: 4px; height: 3em; background-color: #21262d; color: #c9d1d9; border: 1px solid #30363d; }
    .stButton>button:hover { border-color: #8b949e; background-color: #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALISIERUNG ---
if 'game_active' not in st.session_state:
    st.session_state.game_active = True
    st.session_state.step = "analysis" # Start mit Schutzbedarfsanalyse
    st.session_state.budget = 100000
    st.session_state.day = 1
    st.session_state.cia = {"C": 100, "I": 100, "A": 100} # Vertraulichkeit, Integrität, Verfügbarkeit
    st.session_state.inventory = []
    st.session_state.logs = ["> Systemstart: Operation Silver-Data initialisiert."]

def add_log(msg):
    st.session_state.logs.insert(0, f"> Tag {st.session_state.day}: {msg}")

# --- SPIELFUNKTIONEN ---

# PHASE 1: SCHUTZBEDARFSANALYSE (BSI Standard)
def render_analysis():
    st.title("📂 Phase 1: Schutzbedarfsfeststellung")
    st.write("""
    **Szenario:** Der Schmuckhändler 'Silver-Data' speichert IBANs, Gold-Preise und Kundendaten. 
    Wende das **Maximumsprinzip** an, um den Schutzbedarf festzulegen.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1: c = st.select_slider("Vertraulichkeit", ["Normal", "Hoch", "Sehr Hoch"])
    with col2: i = st.select_slider("Integrität", ["Normal", "Hoch", "Sehr Hoch"])
    with col3: a = st.select_slider("Verfügbarkeit", ["Normal", "Hoch", "Sehr Hoch"])
    
    if st.button("Analyse finalisieren"):
        if c == "Sehr Hoch" or i == "Sehr Hoch":
            st.success("Korrekt! Aufgrund der Finanzdaten und Goldpreise ist der Bedarf 'Sehr Hoch'.")
            st.session_state.budget += 20000
        else:
            st.warning("Einstufung etwas riskant, aber wir starten die Operation.")
        st.session_state.step = "management"
        st.rerun()

# PHASE 2: DAS MANAGEMENT-SPIEL
def render_management():
    # Dashboard Header
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Budget", f"{st.session_state.budget:,} €")
    c2.metric("Confidentiality", f"{st.session_state.cia['C']}%")
    c3.metric("Integrity", f"{st.session_state.cia['I']}%")
    c4.metric("Availability", f"{st.session_state.cia['A']}%")
    
    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.subheader("🛠️ IT-Grundschutz Maßnahmen (TOMs)")
        
        # Katalog basierend auf BSI Bausteinen
        toms = {
            "BSI Baustein: Sicherer Client": {"cost": 15000, "target": "I", "desc": "Schützt vor Preismanipulation."},
            "Awareness-Training (Mitarbeiter)": {"cost": 8000, "target": "C", "desc": "Verhindert Phishing-Erfolg."},
            "DDoS-Abwehrzentrum": {"cost": 25000, "target": "A", "desc": "Hält den Webshop online."},
            "ISO 27001 Zertifizierung": {"cost": 40000, "target": "ALL", "desc": "Massiver Schutz für alle Bereiche."},
            "Backup & Restore Plan": {"cost": 12000, "target": "A", "desc": "Schnelle Erholung nach Ransomware."}
        }

        for name, data in toms.items():
            col_a, col_b = st.columns([3, 1])
            col_a.write(f"**{name}** - {data['desc']}")
            if name in st.session_state.inventory:
                col_b.write("✅ Aktiv")
            else:
                if col_b.button(f"Kaufen ({data['cost']}€)", key=name):
                    if st.session_state.budget >= data['cost']:
                        st.session_state.budget -= data['cost']
                        st.session_state.inventory.append(name)
                        if data['target'] == "ALL":
                            for k in st.session_state.cia: st.session_state.cia[k] = min(100, st.session_state.cia[k]+20)
                        else:
                            st.session_state.cia[data['target']] = min(100, st.session_state.cia[data['target']]+25)
                        add_log(f"Maßnahme installiert: {name}")
                        st.rerun()
                    else:
                        st.error("Budget zu niedrig!")

    with right:
        st.subheader("📟 Incident Log")
        log_content = "\n".join(st.session_state.logs)
        st.markdown(f"<div class='terminal'>{log_content}</div>", unsafe_allow_html=True)
        
        if st.button("➡️ Tag beenden (Simuliere Angriffe)"):
            st.session_state.day += 1
            simulate_attacks()
            st.rerun()

def simulate_attacks():
    # Zufällige Auswahl aus den BSI elementaren Gefährdungen
    threat = random.choice(["Phishing", "Ransomware", "Manipulation", "Hardware-Defekt", "DSGVO-Prüfung"])
    
    if threat == "Phishing":
        add_log("ACHTUNG: Phishing-Welle gegen die Personalabteilung!")
        if "Awareness-Training (Mitarbeiter)" not in st.session_state.inventory:
            st.session_state.cia["C"] -= 30
            add_log("SCHADEN: Datenabfluss! Vertraulichkeit sinkt.", "danger")
        else:
            add_log("ERFOLG: Mitarbeiter haben den Angriff erkannt.", "success")

    elif threat == "Ransomware":
        add_log("ALARM: Kryptovirus im Hauptserver!")
        if "Backup & Restore Plan" not in st.session_state.inventory:
            st.session_state.cia["A"] -= 40
            add_log("KATASTROPHE: System für Tage offline!", "danger")
        else:
            add_log("ERFOLG: Backups eingespielt. Nur minimaler Ausfall.")

    elif threat == "Manipulation":
        add_log("WARNUNG: Integrität der Preislisten gefährdet!")
        if "BSI Baustein: Sicherer Client" not in st.session_state.inventory:
            st.session_state.cia["I"] -= 25
            add_log("SCHADEN: Goldpreise wurden auf 1€ gesetzt!", "danger")
        else:
            add_log("ERFOLG: Zugriffsbeschränkung hat Manipulation verhindert.")

    elif threat == "DSGVO-Prüfung":
        add_log("INFO: Die Aufsichtsbehörde prüft Silver-Data.")
        if st.session_state.cia["C"] < 70:
            fine = st.session_state.budget * 0.1
            st.session_state.budget -= fine
            add_log(f"STRAFE: Art. 83 DSGVO Verstoß! {fine:,.0f} € Bußgeld.", "danger")
        else:
            add_log("ERFOLG: Compliance-Prüfung bestanden.")

    # Check for Game Over
    if any(val <= 0 for val in st.session_state.cia.values()) or st.session_state.budget <= 0:
        st.session_state.step = "game_over"

# PHASE 3: GAME OVER
def render_game_over():
    st.error("💀 MISSION FEHLGESCHLAGEN: SYSTEM-COLLAPSE")
    st.write(f"Das Unternehmen Silver-Data musste nach {st.session_state.day} Tagen Insolvenz anmelden.")
    st.write("Einer deiner CIA-Werte oder dein Budget ist auf Null gefallen.")
    if st.button("Neu starten"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

# --- MAIN RENDERER ---
if st.session_state.step == "analysis":
    render_analysis()
elif st.session_state.step == "management":
    render_management()
elif st.session_state.step == "game_over":
    render_game_over()
