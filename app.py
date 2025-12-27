from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app)

# Initialize Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not GEMINI_API_KEY:
            return jsonify({'error': 'Gemini API key not configured. Please set GEMINI_API_KEY environment variable.'}), 500
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize the model (using gemini-2.0-flash for free tier)
        # Try without models/ prefix first, as GenerativeModel may add it automatically
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate response
        response = model.generate_content(user_message)
        
        return jsonify({
            'response': response.text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

