from openai import OpenAI
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

client = OpenAI()
app = Flask(_name_)
CORS(app)

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')  # Load API key properly

# Debugging print
print("API Key Loaded" if openai.api_key else "API Key not found")

# Function to get response from OpenAI
def get_openai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": (
                    "You are a professional legal rights assistant. "
                    "Always provide accurate, concise, and friendly legal information. "
                    "If you are unsure about a user's query, suggest that they contact a licensed attorney. "
                    "Do not offer legal advice, only general legal information. "
                    "Keep answers under 200 words unless the user asks for more detail."
                )},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400
        )
        # Ensure GPT doesn't offer advice that could be considered legal
        reply = response.choices[0].message.content.strip()
        if "I am not sure" in reply or "consult a licensed attorney" in reply:
            reply += " Please consult a licensed attorney."
        return reply
    except Exception as e:
        print(f"Error with OpenAI API: {str(e)}")
        return "Sorry, there was an error while processing your request."

# Route to serve the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    
    # Always use OpenAI for the response
    gpt_response = get_openai_response(user_message)
    
    return jsonify({"reply": gpt_response})

if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0', port=8080)