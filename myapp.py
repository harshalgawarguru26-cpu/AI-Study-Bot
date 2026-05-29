
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import threading
import os
import PdfReader 




import subprocess

current_process = None

# def speak(text):

#     global current_process

#     # Stop previous speech
#     if current_process:
#         current_process.kill()

#     # PowerShell TTS
#     command = f'''
#     Add-Type -AssemblyName System.Speech;
#     $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer;
#     $speak.Speak("{text}");
#     '''

#     current_process = subprocess.Popen(
#         ["powershell", "-Command", command]
#     )
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

if "messages" not in st.session_state:
    st.session_state.messages = []
    
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
                # speak(summary)

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
            # speak(ai_reply)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_reply
            }
        )

    except Exception as e:
        st.error(f"Error: {e}")


