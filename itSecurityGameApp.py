import streamlit as st

# --- INITIALISIERUNG (Alle Keys vorhanden!) ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'node': 'START',
        'budget': 250000,
        'rep': 100,
        'score': 0,
        'day': 1,
        'current_level': 1,
        'history': []
    }

def nav(target):
    st.session_state.game['node'] = target
    st.rerun()

# --- FACHWISSEN-DATENBANK (Deine PDFs als Quelle) ---
KNOWLEDGE = {
    "10_SCHICHTEN": "BSI-Systematik: Umfasst 10 Schichten (Dok. 16, Aufgabe 2d).",
    "47_GEF": "Elementare Gefährdungen: Es gibt exakt 47 (G 0.1 bis G 0.47) (Dok. 16, Abs. I).",
    "MAX_PRINZIP": "Maximumsprinzip: Der höchste Schutzbedarf einer Komponente bestimmt das Gesamtniveau (Dok. 12, S. 24).",
    "GOBD": "GoBD: Grundsätze zur ordnungsgemäßen Buchführung. Wichtig für Integrität (Dok. 13).",
    "ART83_DSGVO": "Strafmaß: Bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes (Dok. 15).",
    "EU_AI_ACT": "KI-Risikoklassen: Unannehmbar (verboten), Hoch, Transparenz, Minimal (Dok. 15).",
    "PDCA": "PDCA-Zyklus: Plan-Do-Check-Act zur ständigen Verbesserung (Dok. 16).",
    "AUTHENTIZITAET": "Authentizität: Nach BSI ein Teilziel der Integrität (Dok. 16, 2e)."
}

# --- UI STYLE ---
st.set_page_config(page_title="CISO Expert Simulator", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .terminal { border: 2px solid #58a6ff; padding: 25px; background: #161b22; border-radius: 10px; border-left: 10px solid #58a6ff; min-height: 200px; }
    .stat-box { background: #010409; border: 1px solid #30363d; padding: 10px; border-radius: 5px; text-align: center; color: #58a6ff; font-weight: bold; }
    .glossary-card { background: #1c2128; border: 1px solid #f2cc60; padding: 15px; border-radius: 8px; color: #f2cc60; margin: 15px 0; }
    .stButton>button { width: 100%; text-align: left; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- STORY NODES ---
NODES = {
    # PHASE 1: BSI GRUNDLAGEN
    'START': {
        'title': "🛠️ Phase 1: Die BSI-Zertifizierung",
        'text': "Willkommen CISO. Die Revision prüft dein Wissen über die Systematik des IT-Grundschutzes. Wie viele Schichten umfasst diese?",
        'options': [
            ("Die Systematik umfasst 10 Schichten.", "LEVEL_2"),
            ("Es sind 8 Basis-Bausteine.", "FAIL_BSI")
        ],
        'glossary': ["10_SCHICHTEN"]
    },
    'FAIL_BSI': {
        'title': "❌ Audit Fehlgeschlagen",
        'text': "Falsch! Laut Dokument 16, Aufgabe 2d umfasst die Systematik 10 Schichten. Die Revision zieht dein Budget ein.",
        'options': [("Neu versuchen (Kosten: 20.000€)", "START")],
        'on_enter': lambda: st.session_state.game.update({'budget': st.session_state.game['budget']-20000, 'rep': st.session_state.game['rep']-10})
    },

    # PHASE 2: GEFÄHRDUNGEN
    'LEVEL_2': {
        'title': "🔥 Phase 2: Elementare Gefährdungen",
        'text': "Korrekt. Nun zur Risikoanalyse: Gegen wie viele elementare Gefährdungen (G 0.1 bis G 0.x) muss laut BSI-Kompendium geprüft werden?",
        'options': [
            ("Es sind exakt 47 elementare Gefährdungen.", "LEVEL_3_SANIPLAN"),
            ("Es sind 14 Bedrohungen (THREATS).", "FAIL_GEFAHR")
        ],
        'glossary': ["47_GEF"],
        'on_enter': lambda: st.session_state.game.update({'score': st.session_state.game['score']+100})
    },
    'FAIL_GEFAHR': {
        'title': "❌ Gefahren-Analyse Mangelhaft",
        'text': "Falsch! 'Threats' ist nur das englische Wort. Das Kompendium listet 47 Gefährdungen (Dok. 16, Abs. I).",
        'options': [("Zurück zur Analyse", "LEVEL_2")],
        'on_enter': lambda: st.session_state.game.update({'rep': st.session_state.game['rep']-15})
    },

    # PHASE 3: SANIPLAN & MAXIMUMPRINZIP
    'LEVEL_3_SANIPLAN': {
        'title': "🕵️ Phase 3: Szenario SaniPlan 2.0",
        'text': "Wir analysieren 'SaniPlan 2.0'. Kundendaten (Tür-Codes) sind 'Hoch'. Der Lagerbestand ist 'Normal'. Was ist der Gesamtschutzbedarf?",
        'options': [
            ("Gesamtbedarf: Hoch (Maximumsprinzip).", "LEVEL_4_LOGS"),
            ("Gesamtbedarf: Normal (Wir schützen nur das Wichtigste).", "FAIL_MAX")
        ],
        'glossary': ["MAX_PRINZIP", "GOBD"],
        'on_enter': lambda: st.session_state.game.update({'score': st.session_state.game['score']+100, 'day': 2})
    },
    'FAIL_MAX': {
        'title': "📉 Haftungs-Katastrophe",
        'text': "Falsch! Das BSI-Maximumsprinzip (Dok. 12, S. 24) ist zwingend. Du hast die Tür-Codes der Kunden ignoriert!",
        'options': [("Korrigieren", "LEVEL_3_SANIPLAN")],
        'on_enter': lambda: st.session_state.game.update({'budget': st.session_state.game['budget']-40000})
    },

    # PHASE 4: LOG-ANALYSE SILVER-DATA
    'LEVEL_4_LOGS': {
        'title': "📟 Phase 4: Operation Silver-Data",
        'text': "Ein Log-Dossier erscheint: 'SELECT * FROM users WHERE id = 1 OR 1=1;'. Welcher Angriffstyp ist das?",
        'options': [
            ("SQL-Injection (Angriff auf Integrität & Vertraulichkeit).", "LEVEL_5_DSGVO"),
            ("DDoS-Angriff (Angriff auf Verfügbarkeit).", "FAIL_LOGS")
        ],
        'on_enter': lambda: st.session_state.game.update({'score': st.session_state.game['score']+100})
    },
    'FAIL_LOGS': {
        'title': "❌ Analyse-Fehler",
        'text': "Falsch! Ein SQL-String manipuliert Datenbestände. Das gefährdet die Integrität (Dok. 12).",
        'options': [("Erneut analysieren", "LEVEL_4_LOGS")]
    },

    # PHASE 5: RECHT & KI
    'LEVEL_5_DSGVO': {
        'title': "🇪🇺 Phase 5: DSGVO & EU AI Act",
        'text': "Durch das Leck sind Daten weg. Was droht laut Art. 83 DSGVO maximal? Und was ist 'Social Scoring' laut AI Act?",
        'options': [
            ("4% Umsatz Strafe / Social Scoring ist verboten.", "LEVEL_6_PDCA"),
            ("50.000€ Strafe / Social Scoring ist ein 'Hohes Risiko'.", "FAIL_RECHT")
        ],
        'glossary': ["ART83_DSGVO", "EU_AI_ACT"],
        'on_enter': lambda: st.session_state.game.update({'score': st.session_state.game['score']+100, 'day': 3})
    },
    'FAIL_RECHT': {
        'title': "💀 Rechts-Ruin",
        'text': "Falsch! Social Scoring ist ein 'Unannehmbares Risiko' (verboten). Die DSGVO-Strafe bricht der Firma das Genick.",
        'options': [("Wissen vertiefen", "LEVEL_5_DSGVO")]
    },

    # PHASE 6: PDCA & ABSCHLUSS
    'LEVEL_6_PDCA': {
        'title': "🔄 Phase 6: Der PDCA-Zyklus",
        'text': "Wir müssen das System dauerhaft verbessern. Welchen Zyklus nutzen wir und gehört Authentizität zur Integrität?",
        'options': [
            ("PDCA-Zyklus / Ja, Authentizität ist ein Teilziel.", "WIN"),
            ("Wasserfall-Modell / Nein, das ist ein eigenes Schutzziel.", "FAIL_PDCA")
        ],
        'glossary': ["PDCA", "AUTHENTIZITAET"],
        'on_enter': lambda: st.session_state.game.update({'score': st.session_state.game['score']+100})
    },
    'FAIL_PDCA': {
        'title': "⚠️ Prozess-Fehler",
        'text': "Falsch! Dokument 16, 2e sagt: Authentizität gehört zur Integrität. Ohne PDCA verbessert sich hier nichts.",
        'options': [("Zurück", "LEVEL_6_PDCA")]
    },

    'WIN': {
        'title': "🏆 ZERTIFIZIERTER CISO",
        'text': "Du hast alle Phasen gemeistert! Du kennst das Maximumsprinzip, die 10 Schichten, die 47 Gefährdungen und die DSGVO-Strafen.",
        'options': [("Neustart", "START")]
    }
}

# --- RENDER ENGINE ---
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat-box'>💰 BUDGET: {st.session_state.game['budget']:,}€</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>🏆 SCORE: {st.session_state.game['score']}</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>⚖️ REPUTATION: {st.session_state.game['rep']}%</div>", unsafe_allow_html=True)

st.divider()

if st.session_state.game['node'] not in NODES:
    st.session_state.game['node'] = 'START'

current = NODES[st.session_state.game['node']]
st.subheader(current['title'])
st.markdown(f"<div class='terminal'>{current['text']}</div>", unsafe_allow_html=True)

if 'glossary' in current:
    st.write("### 📖 Erforderliches Fachwissen (Recherche-Hilfe):")
    for g in current['glossary']:
        st.markdown(f"<div class='glossary-card'><b>{g}:</b> {KNOWLEDGE[g]}</div>", unsafe_allow_html=True)

st.write("### Deine Entscheidung:")
for label, target in current['options']:
    if st.button(label):
        if 'on_enter' in NODES[target]:
            NODES[target]['on_enter']()
        nav(target)

st.divider()
