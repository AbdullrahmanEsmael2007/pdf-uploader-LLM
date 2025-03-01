from openai import OpenAI


def answer_question(question, context,api_key):
    PROMPT = f"""
        You are a helpful assistant. You have been given some text from a document.
        A user is asking you a question about the document. You should respond to their question
        based only on the information provided in the document. Do not make up a filename or use
        any information that is not provided in the text. Instead, make up a reasonable filename
        based on the content of the document or say you do not know. Answer their question in
        the form of a single short sentence or phrase.
        The document is:  {str(context)}
        The user is asking: {str(question)}
    """

    response = llm_response(PROMPT,api_key)

    return response

def llm_response(prompt,api_key):
    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages = [
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content

