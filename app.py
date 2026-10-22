import streamlit as st
import google.generativeai as genai

# Configurazione della pagina
st.set_page_config(
    page_title="Tutor di Filosofia - Sofia",
    page_icon="🏛️",
    layout="centered"
)

# Styling CSS per rendere la grafica accattivante e moderna
st.markdown("""
<style>
    .main-title {
        color: #1A365D;
        text-align: center;
        font-family: 'Georgia', serif;
    }
    .sub-title {
        color: #2C7A7B;
        text-align: center;
        margin-bottom: 25px;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🏛️ Sofia - Tutor di Filosofia</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Spazio di dialogo maieutico per gli studenti del triennio</p>", unsafe_allow_html=True)

# Recupero della chiave API dai secrets di Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("🔑 Chiave API mancante. Configura GEMINI_API_KEY nei Secrets di Streamlit.")
    st.stop()

# System Prompt di Sofia
SYSTEM_INSTRUCTION = """
Ruolo: Sei "Sofia", un Tutor Didattico di Filosofia appassionato, empatico e guida socratica per studenti del triennio della scuola superiore (3°, 4° e 5° anno).

Regole:
1. Poni domande socrate per guidare lo studente invece di dare subito la soluzione pronta.
2. Collega il pensiero dei filosofi a problemi attuali ed esempi pratici della vita quotidiana.
3. Se spieghi un concetto, mantieni un linguaggio chiaro, usa analogie e concludi SEMPRE con una domanda di verifica o uno spunto di riflessione.
4. Mantieni un tono motivante, incoraggiante e senza giudizio.
"""

# Inizializzazione del modello Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

# Gestione della sessione di chat
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Selezione dell'anno scolastico per contestualizzare la conversazione
anno = st.sidebar.selectbox(
    "Seleziona la tua classe:",
    ["3° Anno (Antica e Medievale)", "4° Anno (Moderna e Illuminismo)", "5° Anno (Ottocento, Novecento e Contemporanea)"]
)

st.sidebar.info(f"💡 **Suggerimento:** Chiedi a Sofia di aiutarti a capire un concetto, ad analizzare un testo o a preparare un'interrogazione per la classe: {anno}.")

# Visualizzazione dei messaggi precedenti
for message in st.session_state.chat.history:
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# Input dello studente
if prompt := st.chat_input("Di cosa vorresti parlare oggi in filosofia?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Invio del messaggio a Gemini con il contesto dell'anno selezionato
    contextual_prompt = f"[Studente del {anno}]: {prompt}"
    response = st.session_state.chat.send_message(contextual_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
