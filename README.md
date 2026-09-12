# AI Learning & Study Assistant

An AI-powered learning assistant designed to help college students learn from their course materials using Artificial Intelligence.

## 📌 Project Overview

The AI Learning & Study Assistant allows students to upload PDF course materials and interact with them using AI. It provides course-based question answering, quiz generation, personalized study plans, and progress tracking.

## 🎯 Problem Statement

Students often spend a lot of time reading lengthy course materials, preparing questions, creating quizzes, and planning their studies manually.

This project provides an AI-powered solution that simplifies these tasks and supports personalized learning from course materials.

## 💡 Objectives

- Analyze course materials provided as PDF files.
- Answer questions based on uploaded course content.
- Generate quizzes automatically.
- Create personalized study plans.
- Track student learning progress.
- Provide an easy-to-use learning interface.

## ✨ Key Features

### 📄 PDF Course Analysis
Students can upload PDF course materials for processing and analysis.

### 💬 Course-Based Q&A
The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from course materials and generate answers.

### 📝 AI Quiz Generation
Automatically generates quizzes based on the uploaded course content.

### 📅 Personalized Study Plan
Creates a study plan based on the student's learning requirements.

### 📊 Progress Tracking
Tracks quiz and learning progress to help students understand their performance.

## 🤖 How the AI Solution Works

1. Student uploads a course PDF.
2. The PDF content is extracted and processed.
3. The content is converted into embeddings.
4. Relevant content is stored and retrieved using ChromaDB.
5. The RAG system retrieves relevant information for user questions.
6. Ollama and Qwen-based AI processing generate responses.
7. The system provides answers, quizzes, study plans, and progress information.

## 🛠️ Technologies Used

- Python
- Streamlit
- Ollama
- Qwen 2.5 3B
- ChromaDB
- PyPDF
- Retrieval-Augmented Generation (RAG)

## ⚙️ Project Structure

```text
AI ASSISTANT/
│
├── app.py
├── rag.py
├── quiz.py
├── study_plan.py
├── progress.py
├── requirements.txt
├── README.md
└── .gitignore