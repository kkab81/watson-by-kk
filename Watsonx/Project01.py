from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from genai.credentials import Credentials
from genai.model import Model
from genai.schemas import GenerateParams


import openai
import json
import requests

# make sure you have a .env file under ibm-generative-ai root with
# GENAI_KEY=<your-genai-key>
# GENAI_API=<genai-api-endpoint>
load_dotenv()

#Method 1: using .env variables and below two statements
#api_key = os.getenv("GENAI_KEY", None)
#api_url = os.getenv("GENAI_API", None)
#Method 2: Ends

#mtheod2 start: using obsolute paths
# Get the path to the project folder
project_folder = os.path.abspath(os.path.dirname(__file__))

# Set the path to your configuration files
api_key_file = os.path.join(project_folder, "config", "api_key.txt")
api_url_file = os.path.join(project_folder, "config", "api_url.txt")

# Set the path to your configuration GPT files
gpt_key_file = os.path.join(project_folder, "config", "gpt_api_key.txt")
gpt_url_file = os.path.join(project_folder, "config", "gpt_url.txt")

# Read the API key and API URL from the configuration files
with open(api_key_file, "r") as f:
    api_key = f.read().strip()
    print("API key: ", api_key)

with open(api_url_file, "r") as f:
    api_url = f.read().strip()
    print("API URL: ", api_url)

# Read the API key and API URL from the configuration files
with open(gpt_key_file, "r") as f:
    gpt_key = f.read().strip()
    print("GPT key: ", gpt_key)

with open(gpt_url_file, "r") as f:
    gpt_url = f.read().strip()
    print("API URL: ", gpt_url)
    
# chatgpt configuration
headers = {
        "Authorization": f"Bearer {gpt_key}",
        "Content-Type": "application/json",
    }


# Method2 ended

# credentials object to access the LLM service
creds = Credentials(api_key, api_endpoint=api_url) 

# Instantiate parameters for text generation
params = GenerateParams(decoding_method="sample", max_new_tokens=900)

# Instantiate a model proxy object to send your requests
flan_ul2 = Model("google/flan-ul2", params=params, credentials=creds)
gpt_neoxt_chat_base = Model("gpt-neoxt-chat-base-20b", params=params, credentials=creds)

global_var_selected_opt = flan_ul2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_dropdown_response', methods=['POST'])
def get_dropdown_response():
    selected_option = request.form.get('selected_option')
    global global_var_selected_opt 
    global_var_selected_opt = selected_option

    # Process the selected option and generate the AI response
    # Replace this with your actual AI response generation logic based on the selected option
    ai_response = "You selected: " + selected_option
    print('selected_option ',selected_option)
    
    return jsonify({'response': ai_response})

@app.route('/get_response', methods=['POST'])
def get_response():
    global global_var_selected_opt
    model_from = ' '
    user_input = request.form.get('user_input')
    if global_var_selected_opt == 'gpt_neoxt_chat_base':
        model_name = gpt_neoxt_chat_base
        model_from = 'watsonx'  
    elif global_var_selected_opt == 'flan_ul2':
        model_name = flan_ul2
        model_from = 'watsonx'  
    elif global_var_selected_opt == 'chat_gpt':
        model_name = 'chat_gpt'
        model_from = 'openAI'
    else:
        model_name = flan_ul2
        model_from = 'watsonx'   
    #selected_option = request.form.get('selected_option')
    print('selected_option passed ',global_var_selected_opt)
    print('mode_name selected: ', model_name)
    #prompts = ["Hello! How are you?", "How's the weather?",
    #           "what's the temprature today in Bangalore?",]
    
    if model_from == 'watsonx':
        prompts = []
        prompts.append(user_input)
        print(prompts)   
        
        #for response in flan_ul2.generate(prompts):
        for response in model_name.generate(prompts):
            print(response.generated_text)
        
        # Process the user input and generate the AI response
        # Replace this with your actual AI response generation logic
        #ai_response = "I understand you said: " + user_input
        ai_response =  response.generated_text
    elif model_from == 'openAI':
        messages = [
            {
            "role": "user",
            #"content": content,
            "content": "How are you, message form kk",
            }
        ]

        data = {
            "model": 'gpt-3.5-turbo',
            "messages": messages,
            }

        print('calling chatgpt ',data)
        response = requests.post(gpt_url, headers=headers, data=json.dumps(data))
        gpt_response = response.json()
        print('GPT Response ',gpt_response['error']['message'])
        ai_response = gpt_response['error']['message']
        #return jsonify(chatGPTResults)      

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)
