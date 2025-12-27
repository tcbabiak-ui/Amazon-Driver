from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Initialize Gemini API (Vercel uses environment variables)
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
            return jsonify({'error': 'Gemini API key not configured. Please set GEMINI_API_KEY environment variable in Vercel.'}), 500
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate response
        response = model.generate_content(user_message)
        
        return jsonify({
            'response': response.text
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless function handler
def handler(request):
    return app(request.environ, request.start_response)

