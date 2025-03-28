import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
# Initialize Flask app
app = Flask(__name__)
load_dotenv()
# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
print(api_key)
# Prompt template for structured IPC response
prompt_template = """Provide a structured JSON response based on the Indian Penal Code, 1860.
The output should strictly follow this format:

{
  "art section": "[Section Name or Number]",
  "category": "[Category of Crime]",
  "Punishment": "[Punishment as per IPC]",
  "Applicable": "[Who the law applies to]",
  "Brief description": "[Short and unique explanation]"
}

Use concise and clear language. Ensure the details are accurate based on IPC provisions.
"""
@app.route("/")
def home():
    return "Flask app is running!", 200
# Route to get AI response
@app.route("/get_response", methods=["POST"])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get("prompt", "")
        full_prompt = prompt_template + "\nIPC Section: " + user_input

        # Generate response from Gemini AI
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        response = model.generate_content(full_prompt)
        print(full_prompt)
        # Handle cases where response might be interrupted
        
        response_text = response.text

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = 10000  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)