from openai import OpenAI
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from config import OPENAIKEY
client = OpenAI(api_key=OPENAIKEY)

def query_openai(query, context):
    """
    Send a query with context to OpenAI API.
    """
    prompt = f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"
    print(prompt)
    response = client.completions.create(model="GPT-4o",
    prompt=prompt,
    max_tokens=300)
    return response.choices[0].text.strip()