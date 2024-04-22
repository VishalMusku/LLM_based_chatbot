import openai
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)

def generate_response(context, question, model_name="gpt-4-0125-preview"):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "assistant", "content": context},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except openai.Error as e:
        return f"An error occurred: {e}"
