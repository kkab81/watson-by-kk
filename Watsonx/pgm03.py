#Program: example of calling the IBM-Generative-AI tokenize function.
import os
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import TokenParams

load_dotenv()
api_key = os.getenv("GENAI_KEY", None) 
api_url = os.getenv("GENAI_API", None)
creds = Credentials(api_key, api_endpoint=api_url)

print("\n------------- Example (Tokenize)-------------\n")

flan_t5 = Model("google/flan-t5-xxl", params=TokenParams, credentials=creds)
sentence = "Hello! How are you?"
tokenized_response = flan_t5.tokenize([sentence], return_tokens=True)

print(f"Token counts: {tokenized_response[0].token_count}")
print(f"Tokenized response: {tokenized_response[0].tokens}")

