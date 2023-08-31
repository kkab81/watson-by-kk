from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form.get('user_input')

    # make sure you have a .env file under ibm-generative-ai root with
    # GENAI_KEY=<your-genai-key>
    # GENAI_API=<genai-api-endpoint>
    load_dotenv()
    api_key = os.getenv("GENAI_KEY", None)
    api_url = os.getenv("GENAI_API", None)
    creds = Credentials(api_key, api_endpoint=api_url) # credentials object to access the LLM service

    # Instantiate parameters for text generation
    params = GenerateParams(decoding_method="sample", max_new_tokens=900)

    # Instantiate a model proxy object to send your requests
    flan_ul2 = Model("google/flan-ul2", params=params, credentials=creds)

    #prompts = ["Hello! How are you?", "How's the weather?",
    #           "what's the temprature today in Bangalore?",]
    print(user_input, type(user_input))
    prompts = []
    prompts.append(user_input)
    print(prompts)    
    for response in flan_ul2.generate(prompts):
        print(response.generated_text)
    
    # Process the user input and generate the AI response
    # Replace this with your actual AI response generation logic
    #ai_response = "I understand you said: " + user_input
    ai_response =  response.generated_text

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
