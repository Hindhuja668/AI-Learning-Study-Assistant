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
Do not use markdown.
Do not add explanations.
Do not return multiple JSON objects.

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

Generate completely new questions and real options from the course material.
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

    text = response["message"]["content"].strip()

    # Remove markdown code fences if the AI adds them
    if text.startswith("```"):
        text = text.replace("```json", "", 1)
        text = text.replace("```", "", 1).strip()

    # Find the first JSON object
    start = text.find("{")

    if start == -1:
        raise ValueError("AI did not return valid JSON.")

    text = text[start:]

    # Decode only the first JSON object.
    # This prevents 'Extra data' errors if the AI adds text after the JSON.
    decoder = json.JSONDecoder()
    quiz, _ = decoder.raw_decode(text)

    # Basic validation
    if "questions" not in quiz:
        raise ValueError("Quiz JSON does not contain questions.")

    if len(quiz["questions"]) != 5:
        raise ValueError(
            f"Expected 5 questions, but received {len(quiz['questions'])}."
        )

    for question in quiz["questions"]:

        if "question" not in question:
            raise ValueError("A question is missing the question field.")

        if "options" not in question:
            raise ValueError("A question is missing options.")

        if len(question["options"]) != 4:
            raise ValueError("Each question must have exactly 4 options.")

        if "answer" not in question:
            raise ValueError("A question is missing the answer index.")

        if question["answer"] not in [0, 1, 2, 3]:
            raise ValueError("Answer index must be 0, 1, 2, or 3.")

    return quiz