import streamlit as st

# --- STATE INITIALISIERUNG ---
if 'game' not in st.session_state:
    st.session_state.game = {
        'node': 'ACT1_START',
        'budget': 200000,
        'rep': 100,
        'day': 1,
        'inventory': [],
        'flags': {}
    }

def nav(target):
    st.session_state.game['node'] = target
    st.rerun()

# --- FACHWISSEN-DATENBANK (Referenz auf deine PDFs) ---
KNOWLEDGE = {
    "10_SCHICHTEN": "Die Systematik des BSI-Grundschutzes umfasst exakt 10 Schichten (Dok. 16, Aufgabe 2d).",
    "47_GEF": "Es gibt 47 elementare Gefährdungen (G 0.1 bis G 0.47) im IT-GSK (Dok. 16, Abs. I).",
    "GOBD": "Grundsätze zur ordnungsgemäßen Führung und Aufbewahrung von Büchern in elektronischer Form (Dok. 13).",
    "DSGVO_FINE": "Bußgelder bis zu 20 Mio. € oder 4% des weltweiten Jahresumsatzes (Dok. 15, Aufgabe E).",
    "AUTHENTIZITAET": "Authentizität ist nach BSI ein Teilziel der Integrität (Dok. 16, Aufgabe 2e).",
    "PDCA": "Plan-Do-Check-Act: Der Deming-Zyklus zur Weiterentwicklung der Sicherheit (Dok. 16).",
    "MAX_PRINZIP": "Der Gesamtschutzbedarf richtet sich nach der höchsten Kategorie (Dok. 12, S. 24)."
}

# --- UI STYLE ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Consolas', monospace; }
    .terminal { border: 2px solid #58a6ff; padding: 20px; background: #161b22; border-radius: 10px; border-left: 10px solid #58a6ff; }
    .stat-box { background: #010409; border: 1px solid #30363d; padding: 10px; border-radius: 5px; text-align: center; }
    .glossary { background: #1c2128; border: 1px solid #f2cc60; padding: 10px; color: #f2cc60; font-size: 0.85em; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SPIEL-LOGIK (DIE AKTE) ---
NODES = {
    # AKT 1: GRUNDLAGEN & SYSTEMATIK (Dokument 16)
    'ACT1_START': {
        'title': "🛠️ Akt 1: Die BSI-Zertifizierung",
        'text': """Willkommen im CISO-Office. Bevor wir Silver-Data schützen, prüft der IT-Leiter dein Wissen:
        'Wie viele Schichten umfasst die Systematik des BSI-Grundschutzes laut aktuellem Kompendium?'""",
        'options': [
            ("Es sind 10 Schichten.", "ACT1_47"),
            ("Es sind 8 Basis-Bausteine.", "ACT1_FAIL_1")
        ],
        'glossary': ["10_SCHICHTEN"]
    },
    'ACT1_FAIL_1': {
        'title': "❌ Systemfehler",
        'text': "Falsch! Dokument 16, Aufgabe 2d ist hier eindeutig. Ohne die korrekte Systematik bricht die Analyse zusammen.",
        'options': [("Nochmal lernen", "ACT1_START")]
    },
    'ACT1_47': {
        'title': "🔥 Die elementaren Gefährdungen",
        'text': """Korrekt. Der IT-Leiter nickt. 'Und gegen wie viele <b>elementare Gefährdungen</b> (G 0.1 - G 0.x) müssen wir unsere Bausteine mindestens prüfen?'""",
        'options': [
            ("Gegen 47 Gefährdungen.", "ACT2_SANIPLAN"),
            ("Gegen 14 TOMs.", "ACT1_FAIL_2")
        ],
        'glossary': ["47_GEF"]
    },
    'ACT1_FAIL_2': {
        'title': "❌ Begriffsverwirrung",
        'text': "TOMs sind Maßnahmen, keine Gefährdungen! Schau in Abschnitt I von Dokument 16 nach.",
        'options': [("Zurück", "ACT1_47")]
    },

    # AKT 2: SCHUTZBEDARFSANALYSE (Dokument 13 & 14)
    'ACT2_SANIPLAN': {
        'title': "🕵️ Akt 2: Szenario 'SaniPlan 2.0'",
        'text': """Du sollst nun das Handwerker-System 'SaniPlan 2.0' bewerten. 
        Dort liegen Kundendaten (Tür-Codes) und Rechnungen. 
        Was passiert, wenn die IBANs in den Rechnungen unbemerkt verändert werden?""",
        'options': [
            ("Verlust der Integrität (Finanzielle Schäden nach GoBD).", "ACT2_MAX"),
            ("Verlust der Authentizität (Hardware-Schaden).", "ACT2_FAIL_1")
        ],
        'glossary': ["GOBD", "AUTHENTIZITAET"]
    },
    'ACT2_MAX': {
        'title': "⚖️ Das Maximum-Prinzip",
        'text': """Die Kundendaten sind 'Hoch' eingestuft (DSGVO), der Lagerbestand 'Normal'. 
        Wie lautet der <b>Gesamtschutzbedarf</b> für das System?""",
        'options': [
            ("Gesamtbedarf: Hoch (Maximum-Prinzip).", "ACT3_SILVER"),
            ("Gesamtbedarf: Normal (Mittelwert-Prinzip).", "ACT2_FAIL_2")
        ],
        'glossary': ["MAX_PRINZIP"]
    },
    'ACT2_FAIL_2': {
        'title': "📉 Haftungsrisiko",
        'text': "Falsch! Das BSI schreibt das Maximum-Prinzip vor. Würdest du 'Normal' wählen, haftest du bei einem Datenleck persönlich!",
        'options': [("Korrigieren", "ACT2_MAX")]
    },

    # AKT 3: OPERATION SILVER-DATA (Dokument 12)
    'ACT3_SILVER': {
        'title': "📟 Akt 3: Operation Silver-Data",
        'text': """Montagmorgen. Krisensitzung. Ein Log-Dossier zeigt: 
        <code>'Fragment: clarknoset@gmail.com - Betreff: Barclays Update'</code>.
        Welcher Cyberangriff wird hier vorbereitet?""",
        'options': [
            ("Social Engineering / Phishing.", "ACT3_DSGVO"),
            ("SQL-Injection / Datenbank-Angriff.", "ACT3_FAIL_1")
        ],
        'on_enter': lambda: st.session_state.game.update({'day': 3})
    },
    'ACT3_DSGVO': {
        'title': "🇪🇺 Die Rechtslage",
        'text': """Ein Mitarbeiter hat geklickt. 5.000 Kundendatensätze sind im Darknet. 
        Herr Müller fragt panisch: 'Was droht uns schlimmstenfalls laut DSGVO Art. 83?'""",
        'options': [
            ("Bis zu 4% des Jahresumsatzes.", "ACT4_PDCA"),
            ("Eine Abmahnung durch das BSI.", "ACT3_FAIL_2")
        ],
        'glossary': ["DSGVO_FINE"]
    },

    # AKT 4: NACHHALTIGKEIT (Dokument 15 & 16)
    'ACT4_PDCA': {
        'title': "🔄 Akt 4: Der PDCA-Zyklus",
        'text': """Wir müssen den Schaden beheben und das System dauerhaft verbessern. 
        Welcher Zyklus wird hierfür im IT-Grundschutz angewendet?""",
        'options': [
            ("Der Deming-Zyklus (Plan-Do-Check-Act).", "ACT4_FINAL"),
            ("Das Wasserfall-Modell.", "ACT4_FAIL_1")
        ],
        'glossary': ["PDCA"]
    },
    'ACT4_FINAL': {
        'title': "🛡️ Das Restrisiko",
        'text': """Alles ist umgesetzt. Müller fragt: 'Sind wir jetzt absolut sicher?'""",
        'options': [
            ("Nein, es bleibt ein Restrisiko (Zero-Day/Mensch).", "WIN"),
            ("Ja, 100% Sicherheit ist nun erreicht.", "ACT4_FAIL_2")
        ]
    },
    'WIN': {
        'title': "🏆 CISO-ZERTIFIKAT ERHALTEN",
        'text': "Du hast alle 4 Akte überstanden und die Inhalte von Lernfeld 4 gemeistert!",
        'options': [("Neustart", "ACT1_START")]
    }
}

# --- ENGINE ---
c1, c2, c3 = st.columns(3)
c1.metric("💰 Budget", f"{st.session_state.game['budget']:,}€")
c2.metric("🗓️ Tag", st.session_state.game['day'])
c3.metric("📈 Reputation", f"{st.session_state.game['rep']}%")

st.divider()

current = NODES[st.session_state.game['node']]
st.subheader(current['title'])
st.markdown(f"<div class='terminal'>{current['text']}</div>", unsafe_allow_html=True)

if 'glossary' in current:
    with st.container():
        st.write("---")
        for g in current['glossary']:
            st.markdown(f"<div class='glossary'>💡 <b>Wissen:</b> {KNOWLEDGE[g]}</div>", unsafe_allow_html=True)

st.write("### Deine Entscheidung:")
for label, target in current['options']:
    if st.button(label):
        if 'on_enter' in NODES[target]: NODES[target]['on_enter']()
        nav(target)

st.divider()
