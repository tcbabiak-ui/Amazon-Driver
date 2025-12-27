from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from pathlib import Path

# Get the base directory (api folder's parent)
BASE_DIR = Path(__file__).parent.parent
app = Flask(__name__, 
            template_folder=str(BASE_DIR / 'templates'), 
            static_folder=str(BASE_DIR / 'static'),
            static_url_path='/static')
CORS(app)

# Initialize Gemini API (Vercel uses environment variables)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory(app.static_folder, filename)

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
        
        # Try different models in order of preference
        models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'gemini-2.0-flash']
        model = None
        last_error = None
        
        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                # Test if model works by generating content
                response = model.generate_content(user_message)
                return jsonify({
                    'response': response.text
                })
            except Exception as e:
                last_error = str(e)
                continue
        
        # If all models failed, return error
        return jsonify({
            'error': f'Failed to use any available model. Last error: {last_error}'
        }), 500
    
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

# Export app for Vercel
# Vercel will automatically detect the Flask app
if __name__ == "__main__":
    app.run(debug=True)

