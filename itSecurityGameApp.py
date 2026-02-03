import streamlit as st
import time

# --- INITIALISIERUNG ---
if 'adventure' not in st.session_state:
    st.session_state.adventure = {
        'node': 'START',
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'day': 1,
        'inventory': [],
        'log': []
    }

# --- HILFSFUNKTIONEN ---
def navigate(target):
    st.session_state.adventure['node'] = target
    st.rerun()

def explain(term):
    definitions = {
        "CIA": "**Confidentiality** (Vertraulichkeit), **Integrity** (Integrität), **Availability** (Verfügbarkeit).",
        "TOM": "**Technisch-Organisatorische Maßnahmen**: Maßnahmen zum Schutz von Daten (z.B. Verschlüsselung, Schulung).",
        "PDCA": "**Plan-Do-Check-Act**: Der Deming-Zyklus zur ständigen Verbesserung der Sicherheit.",
        "DSGVO": "**Datenschutz-Grundverordnung**: Gesetz, das bei Datenverlust Bußgelder bis zu 4% des Umsatzes vorsieht.",
        "Maximumsprinzip": "BSI-Regel: Das schwächste Glied (der höchste Schutzbedarf) bestimmt das Gesamtniveau."
    }
    return definitions.get(term, "Keine Definition verfügbar.")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal { background: #010409; border: 1px solid #00ff41; padding: 20px; border-radius: 10px; min-height: 200px; margin-bottom: 20px; border-left: 5px solid #00ff41; }
    .glossary { font-size: 0.85em; color: #8b949e; background: #161b22; padding: 10px; border-radius: 5px; border-left: 3px solid #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- STORY NODES ---
nodes = {
    'START': {
        'title': "📍 MANTEL-HAFEN: DER EINSTIEG",
        'text': "Es ist Montag, 08:15 Uhr. Du bist der neue CISO der **Silver-Data GmbH**. Dein Vorgänger wurde gefeuert, weil Hacker die Gold-Preislisten im Shop manipuliert haben. Die **Integrität** des Systems ist am Boden. Was ist dein erster Schritt?",
        'options': [
            ("Lage analysieren (Schutzbedarfsfeststellung)", "ANALYSIS"),
            ("Sofort neue Firewall kaufen (Budget ausgeben)", "FIREWALL_FAIL")
        ],
        'terms': ["CIA", "I"]
    },
    'FIREWALL_FAIL': {
        'title': "❌ STRATEGISCHER FEHLER",
        'text': "Du kaufst eine Firewall für 50.000€, ohne zu wissen, was du eigentlich schützen willst. Die Geschäftsführung stoppt die Zahlung. 'Erst planen, dann handeln!', schreit der Chef. Du musst zurück an den Start.",
        'options': [("Zurück zur Analyse", "START")],
        'terms': ["PDCA"]
    },
    'ANALYSIS': {
        'title': "🕵️ DIE ANALYSE (MAXIMUMSPRINZIP)",
        'text': "Du untersuchst die Datenbestände: \n1. Kundendaten (IBANs/Adressen) \n2. Interne Preislisten für Silberschmuck. \n\nWie stufst du den Schutzbedarf nach dem **Maximumsprinzip** ein?",
        'options': [
            ("Sehr Hoch - Existenzbedrohend bei Verlust.", "GOOD_ANALYSIS"),
            ("Normal - Ein bisschen Schwund ist immer.", "BAD_ANALYSIS")
        ],
        'terms': ["Maximumsprinzip", "DSGVO"]
    },
    'GOOD_ANALYSIS': {
        'title': "✅ EXZELLENTE EINSCHÄTZUNG",
        'text': "Korrekt! Da Silver-Data mit Finanzdaten und Goldwerten arbeitet, ist der Bedarf 'Sehr Hoch'. Die Bank gewährt dir einen Sicherheitskredit von 50.000€. Weiter zu Tag 2!",
        'options': [("Tag 2: Der Phishing-Angriff", "DAY2_PHISHING")],
        'action': lambda: st.session_state.adventure.update({'budget': st.session_state.adventure['budget'] + 50000, 'day': 2})
    },
    'DAY2_PHISHING': {
        'title': "📧 TAG 2: DIE BARCLAYS-MAIL",
        'text': "In der Finanzabteilung geht eine Mail ein: 'Barclays Token Update erforderlich'. Ein Mitarbeiter klickt. Die **Vertraulichkeit** ist bedroht. Was tust du?",
        'options': [
            ("Sofort Awareness-Schulung einleiten (Plan/Do)", "WIN_PHISHING"),
            ("Die E-Mail ignorieren und hoffen", "LOSE_PHISHING")
        ],
        'terms': ["CIA", "PDCA", "TOM"]
    },
    'WIN_PHISHING': {
        'title': "🏆 MISSION ERFOLGREICH",
        'text': "Du hast die Mitarbeiter geschult und den Angriff gestoppt. Das Unternehmen Silver-Data ist für heute sicher. Du hast bewiesen, dass du die Prinzipien des BSI-Grundschutzes verstanden hast!",
        'options': [("Spiel von vorne beginnen", "START")],
        'terms': ["TOM", "PDCA"]
    }
}

# --- GAME ENGINE ---
current_node = nodes[st.session_state.adventure['node']]

# Dashboard
c1, c2, c3 = st.columns(3)
c1.metric("💰 Budget", f"{st.session_state.adventure['budget']:,} €")
c2.metric("🗓️ Aktueller Tag", st.session_state.adventure['day'])
c3.metric("🔒 CIA Status", f"{st.session_state.adventure['cia']['C']}%")

st.write("---")

# Terminal Output
st.subheader(current_node['title'])
st.markdown(f"<div class='terminal'>{current_node['text']}</div>", unsafe_allow_html=True)

# Glossar-Einblendung
if 'terms' in current_node:
    with st.container():
        st.markdown("<div class='glossary'><b>Begriffs-Erklärung:</b><br>" + 
                    "<br>".join([f"<b>{t}:</b> {explain(t)}" for t in current_node['terms']]) + 
                    "</div>", unsafe_allow_html=True)

st.write("")

# Interaktions-Optionen
for label, target in current_node['options']:
    if st.button(label):
        if 'action' in current_node:
            current_node['action']()
        navigate(target)

# Hintergrundgrafiken zur Verdeutlichung
