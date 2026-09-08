import streamlit as st
from rag import add_pdf, ask_question


st.set_page_config(
    page_title="AI Learning & Study Assistant",
    page_icon="🎓"
)

st.title("🎓 AI Learning & Study Assistant")

st.write(
    "Upload your course material PDF and I will analyze it "
    "for questions, quizzes, and study assistance."
)

uploaded_file = st.file_uploader(
    "📚 Upload your course material",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("📖 Analyze Course Material"):

        file_path = f"course_material/{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Analyzing your course material..."):

            add_pdf(file_path)

        st.success(
            "Course material analyzed successfully! 🎉"
        )

    st.subheader("Ask your course material")
    st.caption("The answer will be based on the PDFs you have analyzed.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about your course...")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching your course material..."):
                answer = ask_question(question)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})