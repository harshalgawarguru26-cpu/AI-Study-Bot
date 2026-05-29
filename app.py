import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader

# =========================
# Streamlit Page Config
# =========================
st.set_page_config(page_title="AI Study Bot", page_icon="🤖", layout="wide")

# =========================
# Initialize Groq Client
# =========================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# =========================
# App Title
# =========================
st.title("🤖 AI Study Bot")
st.write("Chat with AI and summarize PDFs easily.")

# =========================
# Sidebar Settings
# =========================
st.sidebar.title("⚙️ Settings")

mode = st.sidebar.selectbox(
    "Choose AI Mode",
    ["DSA Mentor", "Python Teacher", "RoadMap Generator", "Life Mentor"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []

# =========================
# AI System Prompts
# =========================
system_prompts = {
    "DSA Mentor": "You are an expert DSA teacher. Explain concepts clearly with examples.",
    "Python Teacher": "You are a beginner-friendly Python teacher.",
    "RoadMap Generator": "You create detailed and structured learning roadmaps.",
    "Life Mentor": "You are a wise and supportive life mentor."
}

system_prompt = system_prompts[mode]

# =========================
# PDF Summarizer
# =========================
st.subheader("📄 PDF Summarizer")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
pdf_text = ""

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")

    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

    if st.button("📘 Summarize PDF"):
        with st.spinner("Summarizing PDF..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant that summarizes PDF content."
                        },
                        {
                            "role": "user",
                            "content": f"Summarize the following PDF:\n\n{pdf_text}"
                        }
                    ]
                )

                summary = response.choices[0].message.content

                st.subheader("📝 PDF Summary")
                st.write(summary)

                st.download_button(
                    "Download Summary",
                    data=summary,
                    file_name="pdf_summary.txt"
                )

            except Exception as e:
                st.error(f"Error: {e}")

# =========================
# Chat History Display
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# =========================
# Chat Input
# =========================
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Show user message
    st.chat_message("user").write(user_input)

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ]
        )

        ai_reply = response.choices[0].message.content

        # Show assistant response
        st.chat_message("assistant").write(ai_reply)

        # Save assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_reply}
        )

    except Exception as e:
        st.error(f"Error: {e}")