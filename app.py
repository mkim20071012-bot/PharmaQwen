import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="PharmaQwen",
    page_icon="🧬",
    layout="centered"
)

st.title("PharmaQwen 🧬")
st.caption("Your personal pharmacy study assistant")

SYSTEM_PROMPT = """
You are PharmaQwen, an academic study assistant
for a first-year pharmacy student.

Your responsibilities:
- Explain pharmaceutical and biomedical concepts.
- Generate challenging university-level MCQs.
- Correct answers with detailed explanations.
- Help with organic and general chemistry.
- Explain cytology, embryology, physiology,
  anatomy, botany and other pharmacy subjects.

Teaching rules:
- Be scientifically accurate and structured.
- Explain difficult concepts step by step.
- When giving an MCQ quiz, ask one question at a time
  and wait for the student's answer.
- Never reveal the correct answer before the student
  has attempted the question.
- Never invent scientific references.
"""

client = OpenAI(
    api_key=st.secrets["AI_GRID_API_KEY"],
    base_url="https://app.ai-grid.io/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask PharmaQwen anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("PharmaQwen is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="Qwen3-30B-A3B-Thinking",
                    messages=st.session_state.messages,
                    max_tokens=1500,
                    timeout=120
                )

                answer = response.choices[0].message.content

            except Exception as e:
                answer = f"Something went wrong: {e}"

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
