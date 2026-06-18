from groq import Groq


def ask_question(
    api_key,
    context,
    question
):

    client = Groq(
        api_key=api_key
    )

    prompt = f"""
You are an intelligent PDF analysis assistant.

The provided context may come from one or multiple PDF documents.

Instructions:

1. Answer ONLY using the provided context.
2. If information comes from multiple PDFs, identify and compare them.
3. Highlight similarities and differences when relevant.
4. If information is missing from the context, clearly state that.
5. Use bullet points and structured formatting whenever possible.
6. For resume and job description comparisons:
   - Identify matching skills.
   - Identify missing skills.
   - Explain strengths and weaknesses.
   - Give an overall fit assessment.
7. When comparing documents, mention which PDF the information comes from whenever possible.
8. If the user asks for a summary, provide a concise but complete overview.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=1000
    )

    return (
        response
        .choices[0]
        .message
        .content
    )