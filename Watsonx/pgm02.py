# Program for Auto conversion between alice and Bob from Watsonx
import time, os
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams

load_dotenv()
api_key = os.getenv("GENAI_KEY", None) 
api_url = os.getenv("GENAI_API", None)
creds = Credentials(api_key, api_endpoint=api_url)

print("\n------------- Example (Model Talk)-------------\n")

bob_params = GenerateParams(decoding_method="sample", max_new_tokens=25, temperature=1)
alice_params = GenerateParams(decoding_method="sample", max_new_tokens=45, temperature=0)
bob = Model("google/flan-ul2", params=bob_params, credentials=creds)
alice = Model("google/flan-t5-xxl", params=alice_params, credentials=creds)

sentence = "Hello! How are you?"

print(f"[Alice] --> {sentence}")
while True:
    bob_response = bob.generate([sentence])
    # from first batch get first result generated text
    bob_gen = bob_response[0].generated_text
    print(f"[Bob] --> {bob_gen}")

    alice_response = alice.generate([bob_gen])
    # from first batch get first result generated text
    alice_gen = alice_response[0].generated_text
    print(f"[Alice] --> {alice_gen}")

    sentence = alice_gen
    time.sleep(0.5)

