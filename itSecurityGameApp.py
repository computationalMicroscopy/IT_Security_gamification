import streamlit as st

# --- INITIALISIERUNG DER SESSION STATES ---
if 'page' not in st.session_state:
    st.session_state.page = "start"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'history' not in st.session_state:
    st.session_state.history = []

def change_page(page_name):
    st.session_state.page = page_name

# --- DESIGN-ANPASSUNGEN ---
st.set_page_config(page_title="Cyber-Incident: Operation Silver-Data", page_icon="🛡️")

# --- GAME LOGIC & PAGES ---

# STARTSEITE
if st.session_state.page == "start":
    st.title("🛡️ Cyber-Incident: Operation Silver-Data")
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&q=80&w=1000") # Symbolbild IT-Sicherheit
    st.markdown("""
    Willkommen, Agent. Sie sind IT-Spezialist bei der **Ruhr-IT Solutions GmbH**. 
    Heute ist Montag, der 27. August 2025. Ein kritischer Notruf erreicht Sie: 
    Der Meisterbetrieb **Müller Sanitär & Heizung** wird angegriffen.
    
    Ihr Ziel: Analysieren Sie die Bedrohung, schützen Sie die 'SaniPlan 2.0' Software und klären Sie die Verantwortlichkeiten nach BSI-Grundschutz.
    """)
    if st.button("Mission starten"):
        change_page("briefing")

# BRIEFING
elif st.session_state.page == "briefing":
    st.header("📍 Das Szenario: SaniPlan 2.0")
    st.info("Software-Status: 'SaniPlan 2.0' läuft auf einem lokalen Server und verarbeitet sensible Kundendaten, Bankverbindungen und Tür-Codes.")
    
    st.write("Meister Müller ist in Panik: *'Was passiert, wenn diese Daten geklaut werden? Wie wichtig ist die Absicherung?'*")
    
    st.subheader("Aufgabe 1: Die CIA-Triade")
    st.write("Erklären Sie Herrn Müller die drei Grundwerte der Informationssicherheit:")
    
    choice = st.radio("Was bedeutet 'Integrität' in diesem Zusammenhang?", [
        "Dass nur Berechtigte die Daten lesen können.",
        "Dass Daten korrekt, vollständig und unverändert bleiben.",
        "Dass das System immer funktioniert, wenn der Monteur es braucht."
    ])
    
    if st.button("Antwort einloggen"):
        if choice == "Dass Daten korrekt, vollständig und unverändert bleiben.":
            st.session_state.score += 10
            st.success("Richtig! Das ist die Integrität[cite: 13].")
            change_page("incident")
        else:
            st.error("Falsch. Das war entweder Vertraulichkeit oder Verfügbarkeit[cite: 13].")

# INCIDENT
elif st.session_state.page == "incident":
    st.header("🚨 ALARM: Der E-Mail-Server-Hack")
    st.markdown("""
    Während Sie Müller beraten, geschieht es: Der E-Mail-Server der **SellTec AG** (einem Partner) wurde gehackt und verschlüsselt! [cite: 12]
    Ein Mitarbeiter, **Herr Müller (Buchhaltung)**, hat auf einen Phishing-Link geklickt[cite: 12].
    """)
    
    st.subheader("Die Krisen-Analyse")
    st.write("Auf welcher Ebene entsteht hier laut BSI eine Krise? [cite: 12]")
    
    q2 = st.multiselect("Wähle alle zutreffenden Ebenen:", 
                        ["Systemausfall (Betriebsstillstand)", "Reputationsschaden", "Menschliches Versagen / Konflikt"])
    
    if st.button("Analyse abschließen"):
        if set(q2) == {"Systemausfall (Betriebsstillstand)", "Reputationsschaden", "Menschliches Versagen / Konflikt"}:
            st.session_state.score += 20
            st.success("Perfekt! Sie haben alle Krisenebenen erkannt[cite: 12].")
            change_page("responsibility")
        else:
            st.warning("Da fehlt noch was. Ein Hack betrifft Technik, Ruf und Organisation gleichermaßen[cite: 12].")

# VERANTWORTLICHKEIT
elif st.session_state.page == "responsibility":
    st.header("⚖️ Wer trägt die Schuld?")
    st.write("""
    Herr Müller behauptet: *'Ich bin nicht verantwortlich. IT-Sicherheit ist Aufgabe der IT-Abteilung!'* [cite: 12]
    Wie bewerten Sie das nach BSI-Standard?
    """)
    
    choice = st.selectbox("Ihre fachliche Einschätzung:", [
        "Herr Müller hat recht. Er ist nur Anwender.",
        "Herr Müller verstößt gegen die Mitwirkungspflicht. Jeder Mitarbeiter ist verantwortlich[cite: 12].",
        "Nur die Geschäftsführung ist verantwortlich."
    ])
    
    if st.button("Urteil fällen"):
        if "Mitwirkungspflicht" in choice:
            st.session_state.score += 20
            st.success("Korrekt! Laut BSI kann kein Mitarbeiter die Verantwortung komplett abschieben[cite: 12].")
            change_page("final")
        else:
            st.error("Nicht ganz. Das BSI betont die Eigenverantwortung und Mitwirkungspflicht aller[cite: 12].")

# FINALE
elif st.session_state.page == "final":
    st.balloons()
    st.title("🏆 Mission beendet!")
    st.write(f"Ihre Punktzahl: {st.session_state.score} / 50")
    
    st.markdown("""
    ### Zusammenfassung Ihrer Erkenntnisse:
    - **CIA-Triade**: Sie wissen nun, dass Vertraulichkeit, Integrität und Verfügbarkeit das Fundament bilden[cite: 13].
    - **Schutzbedarfsanalyse**: Für SaniPlan 2.0 gilt das **Maximumsprinzip** – der kritischste Parameter bestimmt den Schutzbedarf (hier: HOCH).
    - **PDCA-Zyklus**: Sicherheit ist ein Prozess, kein Zustand[cite: 12].
    """)
    
    if st.button("Spiel neu starten"):
        st.session_state.page = "start"
        st.session_state.score = 0
        st.rerun()

# --- SIDEBAR ---
with st.sidebar:
    st.header("📊 Status")
    st.write(f"Aktuelle Punkte: {st.session_state.score}")
    st.divider()
    st.write("📖 **Quellen:**")
    st.caption("Basierend auf 'Lernfeld 4' Materialien von Dr. Yahiatène (Schuljahr 2025-2026)[cite: 12, 13, 14].")
