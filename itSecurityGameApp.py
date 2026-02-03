import streamlit as st
import time
import random

# --- KONFIGURATION & STYLES ---
st.set_page_config(page_title="Silver-Data: Text-Adventure", layout="centered")

st.markdown("""
    <style>
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    .cursor { display: inline-block; width: 10px; height: 20px; background: #00ff41; animation: blink 1s infinite; }
    .stApp { background-color: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; }
    .terminal-text { line-height: 1.6; font-size: 1.1em; white-space: pre-wrap; }
    .glossary-box { background: #1a1a1a; border: 1px solid #444; padding: 10px; border-radius: 5px; color: #aaa; font-size: 0.9em; margin-top: 20px; }
    .stButton>button { background-color: #003300; color: #00ff41; border: 1px solid #00ff41; width: 100%; text-align: left; padding: 10px; }
    .stButton>button:hover { background-color: #00ff41; color: #000; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISIERUNG ---
if 'adventure' not in st.session_state:
    st.session_state.adventure = {
        'node': 'START',
        'history': [],
        'budget': 150000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'inventory': [],
        'max_prinzip_done': False
    }

def navigate(node_name):
    st.session_state.adventure['node'] = node_name
    st.rerun()

# --- GLOSSAR-FUNKTION (Abkürzungen erklären) ---
def show_glossary(terms):
    with st.expander("📖 Abkürzungsverzeichnis für diese Szene"):
        definitions = {
            "CIA": "**C**onfidentiality (Vertraulichkeit), **I**ntegrity (Integrität), **A**vailability (Verfügbarkeit). Die drei Grundpfeiler der IT-Sicherheit.",
            "BSI": "**B**undesamt für **S**icherheit in der **I**nformationstechnik. Die deutsche Behörde für Cybersicherheit.",
            "TOM": "**T**echnisch-**O**rganisatorische **M**aßnahmen. Konkrete Schritte (wie Backups oder Passwörter), um Daten zu schützen.",
            "DSGVO": "**D**aten**s**chutz-**G**rund**v**er**o**rdnung. Strenges EU-Gesetz zum Schutz personenbezogener Daten.",
            "PDCA": "**P**lan-**D**o-**C**heck-**A**ct. Ein Zyklus zur kontinuierlichen Verbesserung (Deming-Zyklus).",
            "Maximumsprinzip": "BSI-Methode: Der höchste Schutzbedarf eines Einzelteils bestimmt den Schutzbedarf des Gesamtsystems."
        }
        for term in terms:
            if term in definitions:
                st.write(definitions[term])

# --- DIE STORY-NODES ---
nodes = {
    'START': {
        'text': """**MONTAG, 08:00 UHR. ZENTRALE DER SILVER-DATA GMBH.**

Du betrittst dein Büro als neuer IT-Sicherheitsbeauftragter. Auf deinem Monitor blinkt eine Nachricht der Geschäftsführung:
'Unsere Preislisten für Silberschmuck im Webshop zeigen 0,00 € an! Wir verlieren jede Minute Geld!'

Bevor du den Serverraum betrittst, musst du die Lage einschätzen. Welches Schutzziel wurde hier primär verletzt?""",
        'options': [
            {'label': 'Integrität (I) - Die Daten wurden unzulässig verändert.', 'next': 'ANALYSIS_START'},
            {'label': 'Verfügbarkeit (A) - Der Server ist komplett offline.', 'next': 'WRONG_CIA_START'}
        ],
        'glossary': ['CIA']
    },
    'WRONG_CIA_START': {
        'text': "Fehler! Der Shop ist zwar online, aber die Daten sind falsch. Das ist ein klassischer Bruch der **Integrität**. Versuche es erneut.",
        'options': [{'label': 'Zurück zum Start', 'next': 'START'}],
        'glossary': ['CIA']
    },
    'ANALYSIS_START': {
        'text': """**DIE ANALYSE**

Gut erkannt. Um Fördermittel für die Verteidigung zu erhalten, musst du den Schutzbedarf nach dem **Maximumsprinzip** des **BSI** festlegen.
Silver-Data speichert:
1. Gold-Preise (Manipulation = Ruin)
2. Kundendaten & IBANs (Verlust = DSGVO Bußgeld)

Wie stufst du das System ein?""",
        'options': [
            {'label': 'Normal - Ein kleiner Schaden wäre verkraftbar.', 'next': 'BAD_ANALYSIS'},
            {'label': 'Sehr Hoch - Existenzbedrohende Schäden bei Manipulation.', 'next': 'GOOD_ANALYSIS'}
        ],
        'glossary': ['BSI', 'Maximumsprinzip', 'DSGVO']
    },
    'BAD_ANALYSIS': {
        'text': "Die Geschäftsführung hält dich für leichtsinnig. Wenn IBANs und Goldpreise im Spiel sind, ist 'Normal' lebensgefährlich. Budget wurde gekürzt.",
        'options': [{'label': 'Mit geringem Budget weitermachen', 'next': 'OFFICE_DAY_1'}],
        'setup_action': lambda: st.session_state.adventure.update({'budget': 80000})
    },
    'GOOD_ANALYSIS': {
        'text': "Exzellent! Du hast die Gefahr erkannt. Du erhältst das volle Budget für **TOM** (Technisch-Organisatorische Maßnahmen).",
        'options': [{'label': 'Das Büro einrichten', 'next': 'OFFICE_DAY_1'}],
        'glossary': ['TOM'],
        'setup_action': lambda: st.session_state.adventure.update({'budget': 180000})
    },
    'OFFICE_DAY_1': {
        'text': """**DEIN DASHBOARD**

Du hast nun Zugriff auf das System. Plötzlich erhältst du eine Mail (Barclays-Szenario aus deinem Training): 
'Update erforderlich! Bestätigen Sie Ihren Token.' 

Einige Mitarbeiter haben bereits geklickt. Dies betrifft die **Vertraulichkeit**. Wie reagierst du im Sinne des **PDCA**-Zyklus?""",
        'options': [
            {'label': 'Plan/Do: Sofortige Awareness-Schulung für alle Mitarbeiter.', 'next': 'EVENT_PHISHING_WIN'},
            {'label': 'Check: Erstmal beobachten, wer noch alles klickt.', 'next': 'EVENT_PHISHING_LOSE'}
        ],
        'glossary': ['PDCA', 'CIA']
    },
    'EVENT_PHISHING_WIN': {
        'text': "Erfolg! Durch die Schulung melden Mitarbeiter weitere Mails. Du hast einen Datenabfluss verhindert.",
        'options': [{'label': 'Nächste Herausforderung', 'next': 'RANSOMWARE_SCENE'}],
    },
    'EVENT_PHISHING_LOSE': {
        'text': "Katastrophe! Während du beobachtest, exfiltrieren Hacker 5.000 Kundendatensätze. Die Datenschutzbehörde droht mit **DSGVO**-Bußgeldern.",
        'options': [{'label': 'Schaden begrenzen', 'next': 'RANSOMWARE_SCENE'}],
        'setup_action': lambda: st.session_state.adventure['cia'].update({'C': 40}),
        'glossary': ['DSGVO']
    },
    'RANSOMWARE_SCENE': {
        'text': """**DER BLACKOUT**

Ein lauter Alarm schrillt. Die Serverplatten rattern. Eine Nachricht erscheint: 
'All files encrypted. Pay 2 BTC.'
Die **Verfügbarkeit** deines Webshops bricht ein. Hast du vorgesorgt?""",
        'options': [
            {'label': 'Backup Cluster (3-2-1 Regel) aktivieren', 'next': 'WIN'},
            {'label': 'Lösegeld bezahlen (Budget opfern)', 'next': 'LOSE_MONEY'}
        ],
        'glossary': ['CIA']
    },
    'WIN': {
        'text': "SIEG! Du hast Silver-Data gerettet. Die Prüfer sind beeindruckt von deinem Wissen über IT-Grundschutz und Schutzziele.",
        'options': [{'label': 'Neu starten', 'next': 'START'}]
    }
}

# --- RENDER LOGIC ---
node = nodes[st.session_state.adventure['node']]

st.title("📟 OPERATION: SILVER-DATA")
st.subheader("Text-Adventure / Simulations-Modus")

# Animierter Fortschrittsbalken
cols = st.columns(3)
cols[0].metric("Budget", f"{st.session_state.adventure['budget']}€")
cols[1].metric("Reputation", f"{st.session_state.adventure['cia']['C']}%")
cols[2].metric("Tag", "1 / 4")

st.divider()

# Terminal Animation (Simuliert durch st.write)
st.markdown(f"<div class='terminal-text'>{node['text']}</div><div class='cursor'></div>", unsafe_allow_html=True)

st.write("---")

# Buttons für Interaktion
for opt in node['options']:
    if st.button(opt['label']):
        if 'setup_action' in node:
            node['setup_action']()
        navigate(opt['next'])

# Glossar anzeigen
if 'glossary' in node:
    show_glossary(node['glossary'])

# Hilfe-Bereich
with st.sidebar:
    st.header("Status-Monitor")
    st.write(f"Vertraulichkeit: {st.session_state.adventure['cia']['C']}%")
    st.write(f"Integrität: {st.session_state.adventure['cia']['I']}%")
    st.write(f"Verfügbarkeit: {st.session_state.adventure['cia']['A']}%")
    
    st.progress(st.session_state.adventure['cia']['C'] / 100)
    st.info("Tipp: Achte auf das Maximumsprinzip bei der ersten Analyse!")
