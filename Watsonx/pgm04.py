#Program: an example of built-in async capabilities of generating texts from the LLM 
#         service at much higher response rate than sending an individual request only 
#         after completing the previous request.
import os
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams

load_dotenv()
api_key = os.getenv("GENAI_KEY", None) 
api_url = os.getenv("GENAI_API", None)
creds = Credentials(api_key, api_endpoint=api_url)

print("\n------------- Example (Async Greetings)-------------\n")

params = GenerateParams(
    decoding_method="sample",
    max_new_tokens=20,
    min_new_tokens=10,
    temperature=0.7,
)
flan_ul2 = Model("google/flan-t5-xxl", params=params, credentials=creds)


#greeting = "Hello! How are you?"
greeting = "Hello! How old are you?"
lots_of_greetings = [greeting] * 50
num_of_greetings = len(lots_of_greetings)
num_said_greetings = 0

# yields batch of results that are produced asynchronously and in parallel
for result in flan_ul2.generate_async(lots_of_greetings):
    num_said_greetings += 1
    print("[Progress {:.2f}]".format(num_said_greetings/num_of_greetings*100.0))
    print("\t {}".format(result.generated_text))

