import streamlit as st
import random

# --- 1. INITIALISIERUNG (Absolut sicher) ---
def init_game(force=False):
    if 'game' not in st.session_state or force:
        st.session_state.game = {
            'day': 1, 'ap': 5, 'budget': 2500000, 'ceo_trust': 50,
            'cia': {'C': 60, 'I': 60, 'A': 60},
            'stress': 0, 'risk': 40, 'xp': 0,
            'staff': {'Admins': 1, 'Security': 0},
            'layers': 0, 
            'logs': ["> SYSTEM BOOT: Willkommen, Cyber-Rekrut!"],
            'active_incidents': [],
            'decisions_made': 0,
            'game_over': False, 'won': False,
            'mode': 'tactical',
            'unlocked_tools': []
        }

init_game()
g = st.session_state.game

def add_log(msg, type="info"):
    icons = {"info": "ℹ️", "warn": "⚠️", "error": "🚨", "lvl": "🆙"}
    g['logs'].insert(0, f"{icons.get(type, '🔹')} [T-{g['day']}] {msg}")

# --- 2. INTEL-DATENBANK (Dein Master-Wissen) ---
INTEL = {
    "10 Schichten (BSI)": "Stell dir das wie eine Burg vor. Schicht 1 ist die Mauer (Infrastruktur), Schicht 10 ist der Tresor (Anwendung).",
    "47 Gefährdungen": "Das sind die 'Endgegner' des BSI. Von G 0.1 (Feuer) bis G 0.47 (Hacker). Jede Schicht blockt andere Gegner ab.",
    "Maximumprinzip": "Die schwächste Stelle, die am wichtigsten ist, bestimmt alles. Wenn deine App super sicher ist, aber der Server im Regen steht, hast du Schutzbedarf 'Hoch'.",
    "GoBD & Integrität": "Integrität heißt: Niemand hat an den Daten gefummelt. Laut GoBD müssen Rechnungen 10 Jahre lang unveränderbar bleiben.",
    "EU AI Act & Social Scoring": "Social Scoring ist 'Unannehmbar' (verboten). Wer Punkte für gutes Benehmen verteilt, fliegt raus!",
    "PDCA-Zyklus": "Dein täglicher Rhythmus: Planen (Plan), Bauen (Do), Testen (Check), Verbessern (Act).",
    "DSGVO Art. 83": "Die 'Todesstrafe' für Firmen: Bis zu 20 Mio. Euro Strafe bei Datenverlust."
}

# --- 3. UI STYLE (Cyberpunk & Scannable) ---
st.set_page_config(page_title="CISO Command: Rookie Edition", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #00ff41; font-family: 'Segoe UI', sans-serif; }
    .status-card { background: #1a1a1a; border: 2px solid #00ff41; padding: 10px; border-radius: 10px; text-align: center; color: white; }
    .terminal { background: #000; border: 1px solid #ff00ff; padding: 10px; height: 350px; overflow-y: auto; font-family: 'Courier New'; font-size: 0.9em; }
    .action-btn { font-size: 1.2em !important; height: 3em !important; }
    .cia-label { font-size: 1.1em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (Power-Ups & Wissen) ---
with st.sidebar:
    st.title("🛡️ DEIN ARSENAL")
    st.write(f"**Level:** {g['xp'] // 100} | **XP:** {g['xp']}")
    st.divider()
    st.subheader("👨‍🔧 Crew-Status")
    st.write(f"Admins: {'👤' * g['staff']['Admins']}")
    st.write(f"Security: {'🕵️' * g['staff']['Security']}")
    if st.button("Spezialist anheuern (250k €)"):
        if g['budget'] >= 250000:
            g['staff']['Security'] += 1; g['budget'] -= 250000; add_log("Neuer Security-Experte im Team!"); st.rerun()
    st.divider()
    st.subheader("📖 Intel-Lexikon")
    search = st.text_input("Was bedeutet...?")
    for k, v in INTEL.items():
        if not search or search.lower() in k.lower():
            with st.expander(k): st.write(v)

# --- 5. DASHBOARD ---
st.title("🎮 CISO Command: Silver-Data Defender")
st.write("### Mission: Überlebe 25 Tage und bestehe das BSI-Audit!")

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f"<div class='status-card'>💰 BUDGET<br><span style='font-size:1.5em'>{g['budget']:,} €</span></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='status-card'>⚡ AKTIONEN<br><span style='font-size:1.5em'>{g['ap']} / 5</span></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='status-card'>📈 CEO TRUST<br><span style='font-size:1.5em'>{g['ceo_trust']}%</span></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='status-card'>🗓️ TAG<br><span style='font-size:1.5em'>{g['day']} / 25</span></div>", unsafe_allow_html=True)

st.divider()

# --- CIA & PDCA Visuals ---


cia_cols = st.columns(3)
cia_names = {"C": "🔒 Vertraulichkeit", "I": "💎 Integrität", "A": "⚡ Verfügbarkeit"}
for i, (k, v) in enumerate(g['cia'].items()):
    cia_cols[i].markdown(f"<div class='cia-label'>{cia_names[k]}</div>", unsafe_allow_html=True)
    cia_cols[i].progress(max(0, min(100, v)))

# --- 6. GAME OVER / WIN ---
if g['game_over']:
    st.error("💀 GAME OVER! Die Firma wurde gehackt. Die Admins haben gekündigt."); st.stop()
if g['won']:
    st.balloons(); st.success("🏆 LEGENDÄR! Du hast das Audit mit Bravour bestanden!"); st.stop()

# --- 7. TACTICAL CENTER ---
left, right = st.columns([2, 1])

with left:
    # INCIDENT MANAGEMENT
    if g['active_incidents']:
        st.subheader("🔥 KRITISCHE ALARME!")
        for inc in g['active_incidents']:
            if st.button(f"ANGRIFF ABWEHREN: {inc} (1 AP)", type="primary"):
                if g['ap'] >= 1:
                    g['ap'] -= 1; g['active_incidents'].remove(inc); g['xp'] += 50; g['decisions_made'] += 1
                    g['cia']['I'] = min(100, g['cia']['I'] + 15); add_log(f"{inc} wurde zerschlagen!", "lvl"); st.rerun()

    # TACTICAL TABS
    st.subheader("🛠️ Deine Strategie (PDCA)")
    t1, t2, t3 = st.tabs(["🏗️ DO: Bauen", "🔍 CHECK: Testen", "⚖️ ACT: Regeln"])
    
    with t1:
        st.write("**BSI-Verteidigungsschichten**")
        if st.button(f"Schicht {g['layers']+1} von 10 hochfahren (150k € | 2 AP)"):
            if g['ap'] >= 2 and g['budget'] >= 150000 and g['layers'] < 10:
                g['ap'] -= 2; g['budget'] -= 150000; g['layers'] += 1; g['xp'] += 100; g['decisions_made'] += 1
                g['cia']['A'] += 10; g['cia']['I'] += 5; g['risk'] -= 5; add_log(f"Schicht {g['layers']} ist online!"); st.rerun()
        
        if st.button("Kaffee-Runde für Admins (Stress senken) (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['stress'] = max(0, g['stress'] - 20); g['decisions_made'] += 1
                add_log("Die Admins sind wieder motiviert!"); st.rerun()

    with t2:
        if st.button("Großer Sicherheits-Scan (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['stress'] += 10; g['decisions_made'] += 1
                if random.random() > (0.7 - g['staff']['Security']*0.1):
                    g['active_incidents'].append(random.choice(["SQL-Injektion", "Ransomware", "G 0.18"]))
                    add_log("Hacker entdeckt!", "error")
                else: add_log("Systeme scheinen sauber."); st.rerun()

    with t3:
        if st.button("EU AI Act Check (1 AP)"):
            if g['ap'] >= 1:
                g['ap'] -= 1; g['decisions_made'] += 1; g['mode'] = 'event'; st.rerun()

with right:
    st.subheader("📟 Log-Konsole")
    log_content = "".join([f"<div style='margin-bottom:4px;'>{l}</div>" for l in g['logs']])
    st.markdown(f"<div class='terminal'>{log_content}</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🌞 TAG BEENDEN"):
        # Übernacht-Events
        g['day'] += 1; g['ap'] = 5; g['stress'] = max(0, g['stress'] - 5)
        for k in g['cia']: g['cia'][k] -= random.randint(3, 10)
        
        if g['day'] > 25: g['won'] = True
        if any(v <= 0 for v in g['cia'].values()) or g['budget'] <= 0 or g['stress'] >= 100: g['game_over'] = True
        
        # Alle 5 Tage ein "Boss-Event" (Audit)
        if g['day'] % 5 == 0: g['mode'] = 'boss'
        else: g['mode'] = 'tactical'
        st.rerun()

# --- 8. SPEZIAL-MODI (Events & Boss) ---
if g['mode'] == 'event':
    st.markdown("---")
    with st.container():
        st.subheader("🧩 Zufällige Begegnung!")
        evs = [
            ("Ein Praktikant will 'Social Scoring' für die Kantine einführen.", "Sofort verbieten (EU AI Act)", "Klingt lustig, machen wir"),
            ("Was besagt das Maximumprinzip?", "Der höchste Schutzbedarf zählt", "Der günstigste Schutz zählt"),
            ("GoBD-Prüfung: Wer darf Rechnungen nachträglich ändern?", "Niemand (Integrität!)", "Nur der Chef")
        ]
        text, o1, o2 = random.choice(evs)
        st.info(text)
        if st.button(o1):
            g['xp'] += 150; g['ceo_trust'] += 10; g['mode'] = 'tactical'; add_log("Richtig entschieden!"); st.rerun()
        if st.button(o2):
            g['budget'] -= 200000; g['ceo_trust'] -= 20; g['mode'] = 'tactical'; add_log("Das war ein Fehler!", "error"); st.rerun()

if g['mode'] == 'boss':
    st.markdown("---")
    st.subheader("👔 BOSS-FIGHT: Das Vorstands-Meeting!")
    st.write("Der Vorstand will Ergebnisse sehen. Beantworte die Fachfrage richtig!")
    q = "Was passiert laut DSGVO Art. 83 bei einem schweren Datenleck?"
    if st.button("Bis zu 20 Mio. € oder 4% Umsatz Strafe"):
        g['budget'] += 500000; g['xp'] += 300; g['mode'] = 'tactical'; add_log("Vorstand ist begeistert!", "lvl"); st.rerun()
    if st.button("Ein einfaches Entschuldigungsschreiben reicht"):
        g['budget'] -= 500000; g['ceo_trust'] -= 30; g['mode'] = 'tactical'; add_log("Vorstand ist fassungslos!", "error"); st.rerun()
