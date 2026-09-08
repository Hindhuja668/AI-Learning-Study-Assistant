import ollama
import json


def generate_quiz(course_content):

    prompt = f"""
You are an AI quiz generator.

Create a quiz based ONLY on the following course material:

{course_content}

Create exactly 5 multiple-choice questions.

IMPORTANT:
- Every question must have 4 REAL answer options.
- The options MUST be based on the course material.
- NEVER use placeholder text such as "Option A", "Option B", "Option C", or "Option D".
- Each option must be a meaningful possible answer.
- There must be exactly ONE correct answer for each question.
- The "answer" value must indicate the index of the correct option.
- 0 means the first option.
- 1 means the second option.
- 2 means the third option.
- 3 means the fourth option.

Return ONLY valid JSON.

Use this structure:

{{
    "questions": [
        {{
            "question": "A real question from the course material",
            "options": [
                "A real answer",
                "Another possible answer",
                "Another possible answer",
                "Another possible answer"
            ],
            "answer": 0
        }}
    ]
}}

Do NOT copy the example values above.
Generate completely new questions and real options from the course material.

Do not add markdown.
Do not add explanations.
"""

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = response["message"]["content"]

    quiz = json.loads(text)

    return quiz