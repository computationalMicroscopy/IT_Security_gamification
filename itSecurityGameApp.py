import streamlit as st

# --- INITIALISIERUNG ---
if 'adventure' not in st.session_state:
    st.session_state.adventure = {
        'node': 'START',
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'day': 1,
        'unlocked_info': []
    }

def navigate(target):
    st.session_state.adventure['node'] = target
    st.rerun()

# --- GLOSSAR ENGINE (Basierend auf deinen PDFs) ---
def get_definition(term):
    definitions = {
        "47 Elementare Gefährdungen": "Das BSI-Kompendium listet genau 47 Standard-Bedrohungen (G 0.1 bis G 0.47), wie Feuer, Malware oder Fehlbedienung.",
        "Mitwirkungspflicht": "Sicherheit ist nicht nur IT-Sache. Mitarbeiter müssen Gefahren melden und Richtlinien einhalten (z.B. bei Phishing).",
        "Restrisiko": "Selbst mit den besten TOMs bleibt ein Risiko (z.B. Zero-Day-Exploits). 100% Sicherheit gibt es nicht.",
        "Bausteine": "Das IT-Grundschutz-Kompendium ist in Bausteine unterteilt (z.B. 'Allgemeiner Client' oder 'Serverraum').",
        "Maximumsprinzip": "Der Schutzbedarf eines Systems richtet sich nach dem höchsten Schutzbedarf einer seiner Komponenten.",
        "DSGVO-Strafmaß": "Verstöße können bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes kosten."
    }
    return definitions.get(term, "")

# --- UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .terminal { background: #010409; border: 2px solid #58a6ff; padding: 20px; border-radius: 10px; color: #adbac7; line-height: 1.6; }
    .stat-bar { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .glossary-box { border-left: 4px solid #f2cc60; background: #1c1c1c; padding: 10px; margin: 10px 0; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- STORY NODES ---
nodes = {
    'START': {
        'title': "🏢 Willkommen bei Silver-Data",
        'text': """Du startest als CISO. Dein Chef, Herr Müller, ist skeptisch: 'Warum brauchen wir das BSI-Gedöns? Reicht nicht ein Virenscanner?'
        Er zeigt dir das <b>IT-Grundschutzkompendium</b>. Weißt du, wie viele <b>elementare Gefährdungen</b> dort gelistet sind, die wir beachten müssen?""",
        'options': [
            ("Es sind genau 47 elementare Gefährdungen.", "STEP_ANALYSIS"),
            ("Es gibt über 1000 verschiedene Gefährdungen.", "FAIL_KNOWLEDGE")
        ],
        'glossary': ["47 Elementare Gefährdungen"]
    },
    'FAIL_KNOWLEDGE': {
        'title': "❌ Wissenslücke",
        'text': "Herr Müller schüttelt den Kopf. 'Wenn Sie nicht einmal die Basis des BSI kennen, wie wollen Sie uns schützen?' Du musst dich erst belesen.",
        'options': [("Nochmal versuchen", "START")]
    },
    'STEP_ANALYSIS': {
        'title': "🕵️ Tag 1: Die Schichten des Grundschutzes",
        'text': """Gut! Wir analysieren den Baustein <b>'Allgemeiner Client'</b>. Ein Mitarbeiter nutzt ein Tablet für den Webshop. 
        Du musst den Schutzbedarf festlegen. Die Kundendaten sind kritisch (DSGVO!), die Preislisten existenzwichtig. 
        Welches Prinzip wendest du an?""",
        'options': [
            ("Das Maximumsprinzip (Höchster Wert zählt)", "STEP_PHISHING"),
            ("Das Durchschnittsprinzip (Mittelwert der Ziele)", "FAIL_ANALYSIS")
        ],
        'glossary': ["Maximumsprinzip", "Bausteine", "DSGVO-Strafmaß"]
    },
    'FAIL_ANALYSIS': {
        'title': "📉 Sicherheitsrisiko",
        'text': "Durch das Durchschnittsprinzip unterschätzt du die Gefahr für die Kundendaten. Ein Audit deckt das auf. Korrigiere deine Analyse!",
        'options': [("Zurück zur Analyse", "STEP_ANALYSIS")]
    },
    'STEP_PHISHING': {
        'title': "📧 Tag 2: Die Barclays-Falle",
        'text': """Eine täuschend echte Mail von 'Barclays' erreicht das Team. 'Token-Update erforderlich!'. 
        Ein Admin will klicken. Du hast keine Technik, die das stoppt. Worauf musst du setzen?""",
        'options': [
            ("Auf die Mitwirkungspflicht (Awareness)", "STEP_RESIDUAL"),
            ("Auf das Restrisiko hoffen", "FAIL_PHISHING")
        ],
        'glossary': ["Mitwirkungspflicht"]
    },
    'FAIL_PHISHING': {
        'title': "💀 System-Kollaps",
        'text': "Ohne Schulung klickt der Admin. Hacker stehlen die Zugangsdaten. Die Integrität ist bei 0%. Silver-Data ist am Ende.",
        'options': [("Neustart", "START")]
    },
    'STEP_RESIDUAL': {
        'title': "🛡️ Tag 3: Das Unvermeidbare",
        'text': """Alle TOMs sind aktiv. Firewalls stehen, Mitarbeiter sind geschult. Herr Müller fragt: 'Sind wir jetzt zu 100% sicher?' 
        Wie lautet deine fachliche Antwort als Fachinformatiker?""",
        'options': [
            ("Nein, es bleibt immer ein Restrisiko.", "WIN_GAME"),
            ("Ja, mit BSI-Grundschutz sind wir unbesiegbar.", "FAIL_REALISM")
        ],
        'glossary': ["Restrisiko"]
    },
    'FAIL_REALISM': {
        'title': "⚠️ Größenwahn",
        'text': "Kurz darauf trifft ein Zero-Day-Exploit das System. Da du keine Notfallpläne hattest (weil du dich 'sicher' fühltest), bricht alles zusammen.",
        'options': [("Zurück zu Tag 3", "STEP_RESIDUAL")]
    },
    'WIN_GAME': {
        'title': "🏆 Zertifizierung bestanden!",
        'text': "Herr Müller ist beeindruckt. Du hast nicht nur die CIA-Ziele geschützt, sondern auch verstanden, dass Sicherheit ein PDCA-Zyklus ist. Silver-Data ist sicher (soweit möglich).",
        'options': [("Nochmal spielen", "START")],
        'glossary': ["Restrisiko", "47 Elementare Gefährdungen"]
    }
}

# --- ENGINE ---
current_node = nodes[st.session_state.adventure['node']]

# Sidebar Stats
with st.sidebar:
    st.header("📊 CISO-Status")
    st.metric("Budget", f"{st.session_state.adventure['budget']} €")
    st.metric("Sicherheits-Level", f"{st.session_state.adventure['cia']['C']}%")
    
    st.divider()
    st.info("Nutze die Glossar-Infos unten im Text, um die richtigen Entscheidungen zu treffen!")

# Hauptfenster
st.title("📟 Operation: Silver-Data Chronicles")
st.write(f"### {current_node['title']}")

st.markdown(f"<div class='terminal'>{current_node['text']}</div>", unsafe_allow_html=True)

# Glossar-Einblendungen (Interaktives Lernen)
if 'glossary' in current_node:
    for term in current_node['glossary']:
        st.markdown(f"<div class='glossary-box'><b>{term}:</b> {get_definition(term)}</div>", unsafe_allow_html=True)

st.write("---")

# Buttons für Entscheidungen
for label, target in current_node['options']:
    if st.button(label):
        navigate(target)
