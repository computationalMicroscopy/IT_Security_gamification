import streamlit as st
import time

# --- INITIALISIERUNG ---
if 'adventure' not in st.session_state:
    st.session_state.adventure = {
        'node': 'START',
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'day': 1,
        'history': []
    }

# --- HILFSFUNKTIONEN ---
def navigate(target):
    st.session_state.adventure['node'] = target
    st.rerun()

def explain(term):
    definitions = {
        "CIA-Triade": "Die drei Grundwerte der Informationssicherheit: **C**onfidentiality (Vertraulichkeit), **I**ntegrity (Integrität) und **A**vailability (Verfügbarkeit).",
        "TOM": "**T**echnisch-**O**rganisatorische **M**aßnahmen: Konkrete Schritte zum Schutz (z.B. Backups, Zäune, Schulungen).",
        "PDCA-Zyklus": "Der Deming-Zyklus (**P**lan-**D**o-**C**heck-**A**ct) zur kontinuierlichen Verbesserung der Sicherheit.",
        "DSGVO": "EU-Verordnung. Verstöße können Bußgelder bis zu 4% des Jahresumsatzes nach sich ziehen.",
        "Maximumsprinzip": "BSI-Vorgabe: Der höchste Schutzbedarf einer Komponente bestimmt das Gesamtniveau des Systems.",
        "Restrisiko": "Das verbleibende Risiko nach Umsetzung aller Maßnahmen. 100% Sicherheit gibt es nicht."
    }
    return definitions.get(term, "Definition folgt in Kürze.")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-window { 
        background: #010409; 
        border: 2px solid #00ff41; 
        padding: 25px; 
        border-radius: 5px; 
        min-height: 250px;
        box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
    }
    .glossary-card { 
        background: #161b22; 
        border-left: 5px solid #58a6ff; 
        padding: 10px; 
        margin-top: 20px;
        color: #c9d1d9;
    }
    .stButton>button { 
        background-color: #21262d; 
        color: #00ff41; 
        border: 1px solid #30363d; 
        width: 100%; 
        transition: 0.3s;
    }
    .stButton>button:hover { border-color: #00ff41; background-color: #00ff41; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- STORY NODES ---
nodes = {
    'START': {
        'title': "📡 BRIEFING: OPERATION SILVER-DATA",
        'text': "Du bist der neue CISO bei 'Silver-Data'. Hacker haben die Goldpreise im Webshop manipuliert. Die Geschäftsführung verlangt eine sofortige Strategie. Wie beginnst du?",
        'options': [
            ("Schutzbedarfsanalyse nach BSI einleiten", "ANALYSIS"),
            ("Einfach neue Hardware kaufen", "FAIL_HARDWARE")
        ],
        'glossary': ["CIA-Triade", "PDCA-Zyklus"]
    },
    'FAIL_HARDWARE': {
        'title': "⚠️ AKTIONISMUS-FEHLER",
        'text': "Du kaufst blind Firewalls. Die Geschäftsführung fragt: 'Was genau schützen wir damit?'. Da du keine Analyse hast, wird das Budget gestrichen. Du musst planvoller vorgehen!",
        'options': [("Zurück zum Planen (PDCA)", "START")],
        'glossary': ["PDCA-Zyklus"]
    },
    'ANALYSIS': {
        'title': "🕵️ TAG 1: DAS MAXIMUMSPRINZIP",
        'text': "Du untersuchst die Datenbestände: \n1. Kundendaten (IBANs/Adressen) \n2. Interne Preislisten für Schmuck. \n\nWie stufst du das System ein?",
        'options': [
            ("Sehr Hoch - Ein Ausfall oder Leak wäre fatal.", "DAY2_PHISHING"),
            ("Normal - Wir sind ein kleiner Händler.", "FAIL_ANALYSIS")
        ],
        'glossary': ["Maximumsprinzip", "DSGVO"],
        'on_enter': lambda: st.session_state.adventure.update({'day': 1})
    },
    'FAIL_ANALYSIS': {
        'title': "📉 FEHLANALYSE",
        'text': "Wegen der Finanzdaten ist 'Normal' zu wenig. Die Versicherung kündigt den Schutz. Du musst die Risiken ernster nehmen!",
        'options': [("Analyse wiederholen", "ANALYSIS")]
    },
    'DAY2_PHISHING': {
        'title': "📧 TAG 2: DER PHISHING-ANGRIFF",
        'text': "Eine Mail erreicht die Buchhaltung: 'Bestätigen Sie Ihren Barclays-Token'. Ein Mitarbeiter klickt. Die Vertraulichkeit ist gefährdet! Deine Reaktion?",
        'options': [
            ("Sofortige Awareness-Schulung (TOM)", "DAY3_RANSOMWARE"),
            ("Nichts tun, ist nur eine Mail", "FAIL_PHISHING")
        ],
        'glossary': ["TOM", "CIA-Triade"],
        'on_enter': lambda: st.session_state.adventure.update({'day': 2, 'budget': st.session_state.adventure['budget'] + 20000})
    },
    'FAIL_PHISHING': {
        'title': "💀 DATEN-G AU",
        'text': "Hacker exfiltrieren alle IBANs. Die Aufsichtsbehörde verhängt ein Bußgeld von 4% des Umsatzes. Silver-Data ist bankrott.",
        'options': [("Simulation neu starten", "START")],
        'glossary': ["DSGVO"]
    },
    'DAY3_RANSOMWARE': {
        'title': "👾 TAG 3: DIE VERSCHLÜSSELUNG",
        'text': "Morgens sind alle Server gesperrt. Ransomware! Die Verfügbarkeit ist bei 0%. Hast du ein Backup-Konzept?",
        'options': [
            ("3-2-1 Backup-Strategie anwenden", "WIN_GAME"),
            ("Das Lösegeld bezahlen", "FAIL_MONEY")
        ],
        'on_enter': lambda: st.session_state.adventure.update({'day': 3})
    },
    'WIN_GAME': {
        'title': "🏆 MISSION ERFOLGREICH",
        'text': "Die Backups funktionieren! Silver-Data ist nach 4 Stunden wieder online. Die Geschäftsführung befördert dich zum Security Director. Du hast den PDCA-Zyklus perfekt umgesetzt.",
        'options': [("Nochmal spielen", "START")],
        'glossary': ["Restrisiko"]
    },
    'FAIL_MONEY': {
        'title': "💸 FINANZIELLER RUIN",
        'text': "Du zahlst das Lösegeld, aber die Hacker schicken keinen Key. Das Budget ist weg und die Daten auch. Game Over.",
        'options': [("Neustart", "START")]
    }
}

# --- ENGINE ---
# Sicherheits-Check für den Key
if st.session_state.adventure['node'] not in nodes:
    st.session_state.adventure['node'] = 'START'

current_node = nodes[st.session_state.adventure['node']]

# Dashboard-Leiste
col_stat1, col_stat2, col_stat3 = st.columns(3)
col_stat1.metric("💰 Budget", f"{st.session_state.adventure['budget']:,} €")
col_stat2.metric("🗓️ Tag", st.session_state.adventure['day'])
col_stat3.metric("📈 Status", "Aktiv")

st.write("---")

# Szenen-Darstellung
st.subheader(current_node['title'])
st.markdown(f"<div class='terminal-window'>{current_node['text']}</div>", unsafe_allow_html=True)

# Glossar-Einblendung
if 'glossary' in current_node:
    with st.container():
        st.markdown("<div class='glossary-card'><b>Glossar für dieses Kapitel:</b></div>", unsafe_allow_html=True)
        for term in current_node['glossary']:
            st.markdown(f"**{term}:** {explain(term)}")

# Optionen
st.write("### Deine Entscheidung:")
for label, target in current_node['options']:
    if st.button(label):
        if 'on_enter' in nodes[target]:
            nodes[target]['on_enter']()
        navigate(target)

# Hilfsgrafiken
