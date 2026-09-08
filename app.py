import streamlit as st
from PyPDF2 import PdfReader

from rag import add_pdf, ask_question
from quiz import generate_quiz
from study_plan import generate_study_plan
from progress import save_progress, get_progress


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Learning & Study Assistant",
    page_icon="🎓",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------

st.title("🎓 AI Learning & Study Assistant")

st.write(
    "Upload your course material PDF and I will analyze it "
    "for questions, quizzes, study plans, and progress tracking."
)

st.info(
    "💡 Tip: Upload your course PDF, analyze it, "
    "then use AI Quiz, Study Plan, and Course Q&A."
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("🎓 AI Study Assistant")

    st.write(
        "Your personal AI-powered learning companion."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("📚 PDF Course Analysis")
    st.write("💬 Course Q&A")
    st.write("📝 AI Quiz")
    st.write("📅 Study Plan")
    st.write("📊 Progress Tracking")


# -----------------------------
# Session State
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "course_content" not in st.session_state:
    st.session_state.course_content = ""

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "study_plan" not in st.session_state:
    st.session_state.study_plan = None

if "progress_saved" not in st.session_state:
    st.session_state.progress_saved = False


# -----------------------------
# PDF Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "📚 Upload your course material",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button(
        "📖 Analyze Course Material"
    ):

        file_path = (
            f"course_material/{uploaded_file.name}"
        )

        with open(file_path, "wb") as f:
            f.write(
                uploaded_file.getbuffer()
            )

        reader = PdfReader(file_path)

        course_content = ""

        for page in reader.pages:

            text = page.extract_text()

            if text:
                course_content += text + "\n"

        st.session_state.course_content = course_content

        with st.spinner(
            "Analyzing your course material..."
        ):

            add_pdf(file_path)

        st.success(
            "Course material analyzed successfully! 🎉"
        )


# -----------------------------
# Quiz Section
# -----------------------------

if uploaded_file is not None:

    st.subheader("📝 Course Quiz")

    if st.button("🎯 Generate Quiz"):

        if not st.session_state.course_content:

            st.warning(
                "Please analyze your PDF before generating the quiz."
            )

        else:

            with st.spinner(
                "Generating your quiz..."
            ):

                st.session_state.quiz_data = (
                    generate_quiz(
                        st.session_state.course_content
                    )
                )

            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.session_state.progress_saved = False

            st.rerun()


# -----------------------------
# Display Quiz
# -----------------------------

if (
    st.session_state.quiz_data
    and st.session_state.quiz_index < 5
):

    current = (
        st.session_state.quiz_data["questions"][
            st.session_state.quiz_index
        ]
    )

    st.markdown(
        f"### Question "
        f"{st.session_state.quiz_index + 1}/5"
    )

    st.write(
        current["question"]
    )

    selected_option = st.radio(
        "Choose your answer:",
        current["options"],
        key=f"q{st.session_state.quiz_index}"
    )

    if st.button("➡️ Next Question"):

        st.session_state.quiz_answers[
            st.session_state.quiz_index
        ] = selected_option

        correct_answer = current["options"][
            current["answer"]
        ]

        if selected_option == correct_answer:

            st.session_state.quiz_score += 1

            st.success(
                "✅ Correct!"
            )

        else:

            st.error(
                f"❌ Wrong! Correct answer: "
                f"{correct_answer}"
            )

        st.session_state.quiz_index += 1

        if st.session_state.quiz_index < 5:

            st.rerun()


# -----------------------------
# Final Quiz Score
# -----------------------------

if (
    st.session_state.quiz_data
    and st.session_state.quiz_index >= 5
):

    st.markdown(
        "## 🎉 Quiz Completed!"
    )

    score = st.session_state.quiz_score

    # Save progress only once
    if not st.session_state.progress_saved:

        save_progress(
            score,
            5
        )

        st.session_state.progress_saved = True

    st.success(
        f"Your Score: {score}/5"
    )

    if score == 5:

        st.balloons()

        st.write(
            "🏆 Excellent! Perfect score!"
        )

    elif score >= 3:

        st.write(
            "👍 Good job! Keep practicing."
        )

    else:

        st.write(
            "📚 Keep learning and try again!"
        )


    # -----------------------------
    # Answer Review
    # -----------------------------

    st.markdown(
        "### 📋 Answer Review"
    )

    for i, question in enumerate(
        st.session_state.quiz_data["questions"]
    ):

        correct = question["options"][
            question["answer"]
        ]

        user_answer = (
            st.session_state.quiz_answers.get(
                i,
                "Not answered"
            )
        )

        st.write(
            f"**Question {i + 1}**"
        )

        st.write(
            f"Your Answer: {user_answer}"
        )

        st.write(
            f"Correct Answer: {correct}"
        )

        if user_answer == correct:

            st.success("Correct ✅")

        else:

            st.error("Incorrect ❌")


    # -----------------------------
    # Retake Quiz
    # -----------------------------

    if st.button("🔄 Retake Quiz"):

        st.session_state.quiz_index = 0
        st.session_state.quiz_score = 0
        st.session_state.quiz_answers = {}
        st.session_state.progress_saved = False

        st.rerun()


# -----------------------------
# Study Plan
# -----------------------------

if uploaded_file is not None:

    st.subheader(
        "📅 AI Study Plan"
    )

    study_hours = st.number_input(
        "How many hours can you study per day?",
        min_value=1,
        max_value=12,
        value=2
    )

    if st.button(
        "📚 Generate Study Plan"
    ):

        if not st.session_state.course_content:

            st.warning(
                "Please analyze your PDF before generating "
                "a study plan."
            )

        else:

            with st.spinner(
                "Creating your personalized study plan..."
            ):

                study_plan = generate_study_plan(
                    st.session_state.course_content,
                    study_hours
                )

            st.session_state.study_plan = study_plan


    if st.session_state.study_plan:

        st.markdown(
            "### 🗓️ Your Study Plan"
        )

        st.write(
            st.session_state.study_plan
        )


# -----------------------------
# Progress Dashboard
# -----------------------------

if uploaded_file is not None:

    st.subheader(
        "📊 Your Progress"
    )

    progress = get_progress()

    if progress:

        total_quizzes = len(progress)

        best_score = max(
            item["score"]
            for item in progress
        )

        total_score = sum(
            item["score"]
            for item in progress
        )

        average_score = (
            total_score / total_quizzes
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📝 Quizzes Completed",
                total_quizzes
            )

        with col2:

            st.metric(
                "🏆 Best Score",
                f"{best_score}/5"
            )

        with col3:

            st.metric(
                "📈 Average Score",
                f"{average_score:.1f}/5"
            )

        st.progress(
            min(best_score / 5, 1.0)
        )

        st.caption(
            "Progress based on your completed quizzes."
        )

    else:

        st.info(
            "Complete a quiz to start tracking "
            "your progress."
        )


# -----------------------------
# Course Q&A
# -----------------------------

if uploaded_file is not None:

    st.subheader(
        "💬 Ask Your Course Material"
    )

    st.caption(
        "The answer will be based on the PDFs "
        "you have analyzed."
    )

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )


    question = st.chat_input(
        "Ask a question about your course..."
    )


    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(
                question
            )


        with st.chat_message("assistant"):

            with st.spinner(
                "Searching your course material..."
            ):

                answer = ask_question(
                    question
                )

            st.markdown(
                answer
            )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )