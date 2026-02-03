import streamlit as st
import time

# --- INITIALISIERUNG DES SPIELZUSTANDS ---
if 'adventure' not in st.session_state:
    st.session_state.adventure = {
        'node': 'START',
        'budget': 200000,
        'cia': {'C': 100, 'I': 100, 'A': 100},
        'score': 0,
        'day': 1,
        'inventory': [],
        'logs_analysed': False
    }

def navigate(target):
    st.session_state.adventure['node'] = target
    st.rerun()

# --- FACH-GLOSSAR (Die harten Fakten aus den PDFs) ---
def get_glossary(term):
    defs = {
        "10 Schichten": "Die Systematik des BSI-Grundschutzes umfasst 10 Schichten (nicht 8!), in die die Bausteine unterteilt sind.",
        "GoBD": "Grundsätze zur ordnungsgemäßen Führung und Aufbewahrung von Büchern, Aufzeichnungen und Unterlagen in elektronischer Form.",
        "Authentizität": "Nach BSI ein Teilziel der Integrität. Es stellt sicher, dass der Absender auch wirklich derjenige ist, der er vorgibt zu sein.",
        "Elementare Gefährdungen": "Es gibt exakt 47 (G 0.1 bis G 0.47). Sie bilden die Basis jeder Risikoanalyse.",
        "Art. 83 DSGVO": "Regelt die Geldbußen: Bis zu 20 Mio. Euro oder 4% des gesamten weltweit erzielten Jahresumsatzes.",
        "Mitwirkungspflicht": "Mitarbeiter sind verpflichtet, aktiv an der Sicherheit mitzuwirken (Meldung von Vorfällen, Awareness)."
    }
    return defs.get(term, "Definition wird geladen...")

# --- UI DESIGN ---
st.set_page_config(page_title="CISO Simulator 2026", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .terminal-window { border: 2px solid #58a6ff; padding: 20px; background: #161b22; border-radius: 10px; }
    .stat-card { background: #0d1117; border: 1px solid #30363d; padding: 10px; border-radius: 5px; text-align: center; }
    .glossary-item { color: #f2cc60; font-size: 0.9em; margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- STORY NODES ---
nodes = {
    'START': {
        'title': "🚀 Phase 1: Die Übernahme",
        'text': """Du startest als CISO bei der Silver-Data GmbH. Der Chef, Herr Müller, ist nervös. 
        Er hat gehört, dass das <b>IT-Grundschutzkompendium</b> die Basis für alles ist. 
        Er testet dich direkt: 'Sagen Sie mal, wie viele Schichten umfasst die Systematik des BSI-Grundschutzes eigentlich?'""",
        'options': [
            ("Es sind genau 10 Schichten.", "STEP_47"),
            ("Es sind 8 Basis-Bausteine.", "FAIL_SYSTEMATIK")
        ],
        'glossary': ["10 Schichten"]
    },
    'FAIL_SYSTEMATIK': {
        'title': "⚠️ Wissenslücke",
        'text': "Herr Müller runzelt die Stirn. 'Das steht aber anders im Kompendium!' (Dokument 16, Aufgabe 2d). Du musst die Schichten erst richtig lernen.",
        'options': [("Nochmal versuchen", "START")]
    },
    'STEP_47': {
        'title': "🏢 Phase 2: Die Gefährdungslage",
        'text': """Korrekt! Herr Müller ist beeindruckt. Jetzt geht es ans Eingemachte. 
        'Wir müssen die Risiken bewerten. Wie viele <b>elementare Gefährdungen</b> müssen wir laut BSI mindestens gegen unsere Bausteine prüfen?'""",
        'options': [
            ("Wir müssen alle 47 elementaren Gefährdungen prüfen.", "STEP_ANALYSIS_SANIPLAN"),
            ("Es reicht, die Top 10 Bedrohungen zu prüfen.", "FAIL_47")
        ],
        'glossary': ["Elementare Gefährdungen"]
    },
    'STEP_ANALYSIS_SANIPLAN': {
        'title': "🕵️ Phase 3: Schutzbedarfsanalyse (SaniPlan 2.0 / Silver-Data)",
        'text': """Du analysierst das System 'Silver-Data ERP'. Wir haben: 
        1. Kundendaten (IBANs/Tür-Codes) -> Rechtlich kritisch (DSGVO).
        2. Preislisten -> Finanziell kritisch (GoBD).
        Welchen Schutzbedarf legst du nach dem <b>Maximumsprinzip</b> für die <b>Integrität</b> fest?""",
        'options': [
            ("Hoch/Sehr Hoch - Wegen GoBD und finanziellen Risiken.", "STEP_DOSSIER"),
            ("Normal - Wir können Fehler später korrigieren.", "FAIL_GOBD")
        ],
        'glossary': ["GoBD", "Maximumsprinzip", "Authentizität"]
    },
    'STEP_DOSSIER': {
        'title': "📟 Phase 4: Operation Silver-Data (Log-Analyse)",
        'text': """Ein Alarm schrillt! Ein 'Log-Dossier' wurde erstellt. Du siehst folgendes Fragment: 
        <code>'SELECT * FROM users WHERE id = 1 OR 1=1; --'</code> und eine IP aus einem fremden Netz.
        Was liegt hier vor und welches Schutzziel ist primär bedroht?""",
        'options': [
            ("SQL-Injection - Bedrohung der Vertraulichkeit (C).", "STEP_PHISHING_BARCLAYS"),
            ("DDoS-Angriff - Bedrohung der Verfügbarkeit (A).", "FAIL_DOSSIER")
        ]
    },
    'STEP_PHISHING_BARCLAYS': {
        'title': "📧 Phase 5: Der menschliche Faktor",
        'text': """Die Barclays-Phishing-Mail (Dokument 12) macht die Runde. Ein Mitarbeiter fragt: 
        'Muss ich das melden? Ich hab doch nur kurz draufgeklickt.'
        Auf welches Prinzip des Grundschutzes verweist du?""",
        'options': [
            ("Auf die Mitwirkungspflicht der Mitarbeiter.", "STEP_RESTRISIKO"),
            ("Auf das Prinzip der totalen technischen Überwachung.", "FAIL_MITWIRKUNG")
        ],
        'glossary': ["Mitwirkungspflicht", "Art. 83 DSGVO"]
    },
    'STEP_RESTRISIKO': {
        'title': "🛡️ Phase 6: Das Restrisiko",
        'text': """Du hast Firewalls (T), Schulungen (O) und Backups installiert. 
        Die Geschäftsführung will wissen: 'Sind wir jetzt zu 100% sicher vor Cyberangriffen?'""",
        'options': [
            ("Nein, es bleibt immer ein Restrisiko (z.B. Zero-Day).", "WIN_GAME"),
            ("Ja, wir sind nun absolut sicher.", "FAIL_RESTRISIKO")
        ],
        'glossary': ["Restrisiko"]
    },
    'WIN_GAME': {
        'title': "🏆 ZERTIFIZIERUNG ERREICHT!",
        'text': """Glückwunsch! Du hast Silver-Data erfolgreich abgesichert.
        Du hast alle Hürden des BSI-Grundschutzes genommen:
        - Die 10 Schichten korrekt identifiziert.
        - Das Maximumsprinzip angewandt.
        - Die 47 Gefährdungen berücksichtigt.
        - Die DSGVO-Bußgelder (4% Umsatz) verhindert.""",
        'options': [("Simulation neu starten", "START")]
    }
}

# --- ENGINE ---
# Fallback für Node-Wechsel
if st.session_state.adventure['node'] not in nodes:
    st.session_state.adventure['node'] = 'START'

current = nodes[st.session_state.adventure['node']]

# Dashboard
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='stat-card'>💰 BUDGET<br>{st.session_state.adventure['budget']:,}€</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-card'>🛡️ CIA-LEVEL<br>{st.session_state.adventure['cia']['C']}%</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-card'>📚 WISSEN<br>LF 4 Komplett</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='stat-card'>⚖️ COMPLIANCE<br>DSGVO OK</div>", unsafe_allow_html=True)

st.write("---")

# Hauptinhalt
st.subheader(current['title'])
st.markdown(f"<div class='terminal-window'>{current['text']}</div>", unsafe_allow_html=True)

# Glossar-Einblendungen
if 'glossary' in current:
    st.write("### 📖 Fachwissen für diese Phase:")
    for g in current['glossary']:
        st.markdown(f"<div class='glossary-item'><b>{g}:</b> {get_glossary(g)}</div>", unsafe_allow_html=True)

# Optionen
st.write("### Deine Entscheidung:")
for label, target in current['options']:
    if st.button(label):
        # Einfaches Budget-Handling pro Schritt
        st.session_state.adventure['budget'] -= 5000
        navigate(target)

# Grafiken zur Unterstützung
st.write("---")
