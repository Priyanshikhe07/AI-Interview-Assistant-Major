def generate_questions(resume_text):

    questions = []

    if "python" in resume_text.lower():
        questions.append(
            "Explain Python decorators."
        )

    if "machine learning" in resume_text.lower():
        questions.append(
            "What is overfitting?"
        )

    if "data structures" in resume_text.lower():
        questions.append(
            "Difference between Stack and Queue?"
        )

    return questions