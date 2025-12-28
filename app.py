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
        
        # Try models that work with free tier (gemini-2.0-flash has limit 0 on free tier)
        # Order: gemini-1.5-flash (best for free tier), then gemini-pro
        models_to_try = ['gemini-1.5-flash', 'gemini-pro']
        last_error = None
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(user_message)
                return jsonify({
                    'response': response.text
                })
            except Exception as e:
                error_str = str(e)
                last_error = error_str
                # If it's a quota error, provide helpful message
                if '429' in error_str or 'quota' in error_str.lower():
                    return jsonify({
                        'error': f'API quota exceeded. Please wait a moment and try again, or check your Google AI Studio quota limits. Error: {error_str[:200]}'
                    }), 429
                # Continue to next model if this one fails
                continue
        
        # If all models failed, return error
        if '429' in str(last_error) or 'quota' in str(last_error).lower():
            return jsonify({
                'error': 'API quota exceeded. Please wait a few minutes and try again. Check your quota at https://ai.dev/usage?tab=rate-limit'
            }), 429
        else:
            return jsonify({
                'error': f'Failed to use any available model. Last error: {last_error[:300]}'
            }), 500
    
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

