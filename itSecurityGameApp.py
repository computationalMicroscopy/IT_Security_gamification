import streamlit as st

# --- INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'node': 'LVL1_BSI',
        'budget': 250000,
        'rep': 100,
        'score': 0,
        'day': 1,
        'history': []
    }

def nav(target):
    st.session_state.game['node'] = target
    st.rerun()

# --- FACH-GLOSSAR (Exakt aus deinen PDFs) ---
KNOWLEDGE = {
    "10_SCHICHTEN": "Die Systematik des BSI-Grundschutzes umfasst 10 Schichten (Dok. 16, Aufgabe 2d).",
    "47_GEF": "Es gibt exakt 47 elementare Gefährdungen (G 0.1 bis G 0.47) (Dok. 16, Abschnitt I).",
    "MAX_PRINZIP": "Der höchste Schutzbedarf einer Komponente bestimmt das Gesamtniveau (Dok. 12, S. 24).",
    "GOBD": "Grundsätze zur ordnungsgemäßen Buchführung (Dok. 13). Wichtig für die Integrität von Finanzdaten.",
    "ART83_DSGVO": "Bußgelder bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes (Dok. 15).",
    "MITWIRKUNG": "Mitarbeiter müssen Gefahren melden und Richtlinien einhalten (Dok. 16, Abschnitt I).",
    "EU_AI_ACT": "KI-Systeme werden in Risikoklassen unterteilt (Unannehmbar, Hoch, Transparenz, Minimal) (Dok. 15).",
    "PDCA": "Plan-Do-Check-Act (Deming-Zyklus) zur ständigen Verbesserung (Dok. 16)."
}

# --- UI STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .terminal { border: 2px solid #58a6ff; padding: 25px; background: #161b22; border-radius: 10px; border-left: 10px solid #58a6ff; }
    .stat-box { background: #010409; border: 1px solid #30363d; padding: 10px; border-radius: 5px; text-align: center; color: #58a6ff; }
    .glossary-card { background: #1c2128; border: 1px solid #f2cc60; padding: 15px; border-radius: 8px; color: #f2cc60; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# --- STORY NODES ---
NODES = {
    # LEVEL 1: BSI SYSTEMATIK
    'LVL1_BSI': {
        'title': "🛠️ Level 1: Die BSI-Zertifizierung",
        'text': "Dein erster Tag bei Silver-Data. Die Revision prüft dich: 'Wie viele Schichten umfasst die Systematik des BSI-Grundschutzes?'",
        'options': [
            ("Es sind 10 Schichten.", "LVL2_GEFAHR"),
            ("Es sind 8 Basis-Bausteine.", "FAIL_BSI")
        ],
        'glossary': ["10_SCHICHTEN"]
    },
    'FAIL_BSI': {
        'title': "❌ Audit durchgefallen",
        'text': "Falsch! Dokument 16, Aufgabe 2d sagt klar: 10 Schichten. Die Revision entzieht dir die Leitung.",
        'options': [("Neu starten", "LVL1_BSI")]
    },

    # LEVEL 2: ELEMENTARE GEFÄHRDUNGEN
    'LVL2_GEFAHR': {
        'title': "🔥 Level 2: Das Kompendium",
        'text': "Gut! Jetzt ernsthaft: Gegen wie viele elementare Gefährdungen müssen wir jeden Baustein (z.B. 'Allgemeiner Client') prüfen?",
        'options': [
            ("Gegen alle 47 elementaren Gefährdungen.", "LVL3_SANIPLAN"),
            ("Gegen die 14 TOMs des BSI.", "FAIL_GEFAHR")
        ],
        'glossary': ["47_GEF"]
    },
    'FAIL_GEFAHR': {
        'title': "❌ Gefahrenunterschätzung",
        'text': "TOMs sind Maßnahmen, keine Gefährdungen! (Dok. 16, Abs. I). Du hast eine Bedrohung übersehen.",
        'options': [("Zurück", "LVL2_GEFAHR")]
    },

    # LEVEL 3: SCHUTZBEDARFSANALYSE (SaniPlan Transfer)
    'LVL3_SANIPLAN': {
        'title': "🕵️ Level 3: Szenario SaniPlan 2.0",
        'text': "Wir übernehmen 'SaniPlan 2.0'. Kundendaten (Tür-Codes) sind 'Sehr Hoch', der Lagerbestand ist 'Normal'. Was ist der Gesamtschutzbedarf?",
        'options': [
            ("Sehr Hoch (Maximumsprinzip).", "LVL4_LOGS"),
            ("Hoch (Durchschnitt aus allen Werten).", "FAIL_MAX")
        ],
        'glossary': ["MAX_PRINZIP", "GOBD"]
    },
    'FAIL_MAX': {
        'title': "📉 Haftungsfalle",
        'text': "Falsch! Das BSI-Maximumsprinzip (Dok. 12, S. 24) ist Gesetz. Bei 'Hoch' würdest du die Tür-Codes vernachlässigen!",
        'options': [("Korrigieren", "LVL3_SANIPLAN")]
    },

    # LEVEL 4: LOG-DOSSIER ANALYSE (Operation Silver-Data)
    'LVL4_LOGS': {
        'title': "📟 Level 4: Operation Silver-Data",
        'text': "Ein Angriff! Log-Fragment: 'SELECT * FROM prices WHERE id = 1 OR 1=1;'. Was passiert hier?",
        'options': [
            ("SQL-Injection (Angriff auf Integrität & Vertraulichkeit).", "LVL5_BARCLAYS"),
            ("Phishing-Versuch (Angriff auf die Mitwirkung).", "FAIL_LOGS")
        ]
    },

    # LEVEL 5: MENSCH & RECHT (Phishing & DSGVO)
    'LVL5_BARCLAYS': {
        'title': "📧 Level 5: Die Barclays-Falle",
        'text': "Eine Mail: 'Update erforderlich!'. Ein Mitarbeiter klickt. 5.000 IBANs sind weg. Welche Strafe droht laut Art. 83 DSGVO?",
        'options': [
            ("Bis zu 4% des weltweiten Jahresumsatzes.", "LVL6_AI"),
            ("Ein Bußgeld von pauschal 50.000 €.", "FAIL_DSGVO")
        ],
        'glossary': ["ART83_DSGVO", "MITWIRKUNG"]
    },

    # LEVEL 6: KI & ZUKUNFT (EU AI Act)
    'LVL6_AI': {
        'title': "🤖 Level 6: Der EU AI Act",
        'text': "Silver-Data will eine KI zur 'sozialen Bewertung' der Kunden einführen. In welche Risikoklasse fällt das laut EU AI Act?",
        'options': [
            ("Unannehmbares Risiko (Verboten).", "WIN"),
            ("Hohes Risiko (Zulassungspflichtig).", "FAIL_AI")
        ],
        'glossary': ["EU_AI_ACT"]
    },

    'WIN': {
        'title': "🏆 MASTER OF SECURITY",
        'text': "Du hast alle Inhalte von Lernfeld 4 gemeistert. Silver-Data ist sicher!",
        'options': [("Spiel neu starten", "LVL1_BSI")]
    }
}

# --- ENGINE ---
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='stat-box'>💰 BUDGET: {st.session_state.game['budget']:,}€</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'>🏆 SCORE: {st.session_state.game['score']}</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='stat-box'>⚖️ REPUTATION: {st.session_state.game['rep']}%</div>", unsafe_allow_html=True)

st.divider()

current = NODES[st.session_state.game['node']]
st.subheader(current['title'])
st.markdown(f"<div class='terminal'>{current['text']}</div>", unsafe_allow_html=True)

if 'glossary' in current:
    st.write("### 📖 Erforderliches Wissen (PDF-Check):")
    for g in current['glossary']:
        st.markdown(f"<div class='glossary-card'><b>{g}:</b> {KNOWLEDGE[g]}</div>", unsafe_allow_html=True)

st.write("### Deine Entscheidung:")
for label, target in current['options']:
    if st.button(label):
        # Bei Fehlern Reputation abziehen
        if "FAIL" in target:
            st.session_state.game['rep'] -= 20
            st.session_state.game['budget'] -= 50000
        else:
            st.session_state.game['score'] += 100
        nav(target)

st.divider()
