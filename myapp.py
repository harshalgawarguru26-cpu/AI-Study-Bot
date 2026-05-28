# import os

# import streamlit as st
# from dotenv import load_dotenv
# from groq import Groq

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# MODEL_NAME = "llama-3.1-8b-instant"

# st.set_page_config(page_title="Coding Buddy", page_icon="💻", layout="wide")

# client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# st.markdown(
#     """
#     <style>
#     .main {
#         background: linear-gradient(180deg, #0f172a 0%, #111827 50%, #1f2937 100%);
#         color: #f8fafc;
#     }
#     .stChatInput > div {
#         border: 1px solid #38bdf8;
#         border-radius: 16px;
#         padding: 6px 10px;
#     }
#     .block-container {
#         padding-top: 2rem;
#     }
#     h1, h2, h3 {
#         color: #93c5fd;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# st.title("💻 Coding Buddy")
# st.caption("A ready-to-use coding assistant app for code generation, debugging, and explanations.")

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# with st.sidebar:
#     st.header("Settings")
#     mode = st.selectbox(
#         "Task mode",
#         [
#             "Generate code",
#             "Explain code",
#             "Debug code",
#             "Review code",
#             "Plan a project",
#         ],
#     )
#     temperature = st.slider("Creativity", 0.1, 1.0, 0.4)
#     st.write("### Quick start")
#     st.write("- Ask for code snippets")
#     st.write("- Paste buggy code for debugging")
#     st.write("- Ask for project plans or explanations")

#     if st.button("Clear chat"):
#         st.session_state.messages = []

# system_prompt_map = {
#     "Generate code": "You are an expert coding assistant. Write clean, correct, production-friendly code examples with comments.",
#     "Explain code": "You are a clear and patient coding mentor. Explain code in simple language and include examples when useful.",
#     "Debug code": "You are a code debugging expert. Identify errors, explain the cause, and provide a corrected version.",
#     "Review code": "You are a code reviewer. Provide concise feedback about correctness, style, and potential improvements.",
#     "Plan a project": "You are a software project planning assistant. Provide practical, step-by-step plans with architecture, milestones, and risks.",
# }

# system_prompt = system_prompt_map[mode]

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.write(message["content"])

# user_input = st.chat_input("Ask your coding question here...")

# if user_input:
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     with st.chat_message("user"):
#         st.write(user_input)

#     if client is None:
#         ai_reply = (
#             "GROQ_API_KEY is not set. Add your API key to a `.env` file and restart the app.\n\n"
#             "Example `.env` content:\n"
#             "GROQ_API_KEY=your_api_key_here"
#         )
#     else:
#         with st.spinner("Generating response..."):
#             response = client.chat.completions.create(
#                 model=MODEL_NAME,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     *st.session_state.messages,
#                 ],
#                 temperature=temperature,
#             )
#             ai_reply = response.choices[0].message.content

#     with st.chat_message("assistant"):
#         st.write(ai_reply)

#     st.session_state.messages.append({"role": "assistant", "content": ai_reply})

# st.markdown("---")
# st.caption("Tip: you can ask for Python, JavaScript, SQL, APIs, or architecture help.")

#----------------------------------------------------------------------------------------------------------

import pyttsx3
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import threading
import os
import PdfReader 


# #This code do  work in background..but there is only one message send by user ..It completly read even if user send another response

# speech_lock = threading.Lock()

# def speak(text):

#     def run_speech():

#         with speech_lock:

#             engine = pyttsx3.init()

#             engine.say(text)
#             engine.runAndWait()

#             engine.stop()

#     threading.Thread(target=run_speech).start()





import subprocess

current_process = None

def speak(text):

    global current_process

    # Stop previous speech
    if current_process:
        current_process.kill()

    # PowerShell TTS
    command = f'''
    Add-Type -AssemblyName System.Speech;
    $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
    $speak.Speak("{text}");
    '''

    current_process = subprocess.Popen(
        ["powershell", "-Command", command]
    )
# ========================= |
# Load Environment Variables|
# =========================-|
load_dotenv()

# =========================
# Initialize Groq Client
# =========================
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# Streamlit Page Config
# =========================
st.set_page_config(page_title="AI Study Bot",page_icon="🤖",layout="wide")

# =========================
# App Title
# =========================
st.title("🤖 AI Study Bot")

st.write("Chat with AI and summarize PDFs easily.")

# =========================
# Sidebar
# =========================
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.selectbox(
    "Choose AI Mode",
    [
        "DSA Mentor",
        "Python Teacher",
        "RoadMap Generator",
        "Life Mentor"
    ]
)

# Clear Chat Button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []

# =========================
# AI Personalities
# =========================
system_prompt = ""

if mode == "DSA Mentor":
    system_prompt = ("You are an expert DSA teacher. " "Explain concepts clearly with examples.")

elif mode == "Python Teacher":
    system_prompt = ( "You are a beginner-friendly Python teacher.")

elif mode == "RoadMap Generator":
    system_prompt = ("You create detailed and structured learning roadmaps.")

elif mode == "Life Mentor":
    system_prompt = ("You are a wise and supportive life mentor.")

# =========================
# PDF Upload Section
# =========================
st.subheader("📄 PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

pdf_text = ""

if uploaded_file:

    st.success("✅ PDF uploaded successfully!")

    # Read PDF
    pdf_reader = PdfReader(uploaded_file)

    # Extract text from all pages
    for page in pdf_reader.pages:

        extracted_text = page.extract_text()

        if extracted_text:
            pdf_text += extracted_text

    # Summarize Button
    if st.button("📘 Summarize PDF"):

        with st.spinner("Summarizing PDF..."):

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful assistant that summarizes PDF content."
                            )
                        },
                        {
                            "role": "user",
                            "content": (
                                f"Summarize the following PDF:\n\n{pdf_text}"
                            )
                        }
                    ]
                )

                summary = response.choices[0].message.content

                st.subheader("📝 PDF Summary")
                st.write(summary)
                st.download_button("Download Summary",data=summary,file_name="pdf_summary.txt")
                speak(summary)

            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# Chat Memory
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# Display Previous Messages
# =========================
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# =========================
# Chat Input
# =========================
user_input = st.chat_input("Ask me anything...")

# =========================
# User Sends Message
# =========================
if user_input:

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Generate AI response
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                *st.session_state.messages
            ]
        )

        ai_reply = response.choices[0].message.content

        # Show assistant response
        with st.chat_message("assistant"):
            st.write(ai_reply)
            speak(ai_reply)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

    except Exception as e:
        st.error(f"Error: {e}")


