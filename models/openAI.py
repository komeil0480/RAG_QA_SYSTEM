from openai import OpenAI
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from config import OPENAIKEY

client = OpenAI(api_key=OPENAIKEY)

def query_openai(query, context):
    print("----------------------------------------------------------------")
    print("Using API Key:", OPENAIKEY)  # Avoid printing sensitive information in production
    """
    Send a query with context to OpenAI API.
    """
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    print(prompt)
    # try:
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-4o" if specified in your documentation
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     return None