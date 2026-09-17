import ollama


def generate_study_plan(course_content, study_hours):

    prompt = f"""
Create a simple study plan based ONLY on the following course material:

{course_content}

The student can study {study_hours} hours per day.

Create a practical daily study plan.

Include:
- Day number
- Topics to study
- Study time
- Revision time
- Practice time

Keep the plan simple and suitable for a college student.
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

    return response["message"]["content"]
