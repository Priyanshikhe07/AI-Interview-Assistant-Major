import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GENAI API KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_questions(resume_text):

    prompt = f"""
You are a Senior Technical Interviewer at a top product-based company.

Analyze the candidate's resume and generate realistic interview questions.

Rules:

1. Do not simply repeat technologies mentioned in the resume.
2. Generate questions that test practical understanding, problem-solving ability, project knowledge, and real-world application.
3. Include follow-up questions that an experienced interviewer might ask.
4. Questions should gradually increase in difficulty.
5. Questions must feel like they are asked in actual technical interviews at companies such as TCS, Infosys, Accenture, Cognizant, Wipro, Deloitte, Amazon, Microsoft, and Google.
6. Include scenario-based and project-based questions.
7. If projects are mentioned, ask questions about design decisions, scalability, optimization, challenges faced, and improvements.
8. Avoid theoretical textbook questions unless necessary.

Generate:

5 Easy Technical Questions

10 Medium Technical Questions

10 Advanced Technical Questions

5 HR / Behavioral Questions

Format the output with numbering and categories.

Resume:

{resume_text}
"""

    response = model.generate_content(prompt)

    return response.text