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
        
        # Get list of available models and try them
        try:
            available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            # Prioritize models that might work with free tier
            # Try models in order: flash models first (faster, free tier friendly), then pro models
            preferred_order = []
            flash_models = [m for m in available_models if 'flash' in m.lower()]
            pro_models = [m for m in available_models if 'pro' in m.lower() and 'flash' not in m.lower()]
            
            # Prefer flash models, then pro models
            preferred_order = flash_models + pro_models
            
            # If no preferred models, use all available
            if not preferred_order:
                preferred_order = available_models[:5]  # Try first 5 available
        except Exception as e:
            # Fallback to commonly available models
            preferred_order = ['gemini-1.5-flash', 'gemini-2.5-flash', 'gemini-1.5-pro', 'gemini-2.5-pro']
        
        last_error = None
        errors = []
        
        for model_name in preferred_order:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(user_message)
                return jsonify({
                    'response': response.text
                })
            except Exception as e:
                error_str = str(e)
                errors.append(f"{model_name}: {error_str[:100]}")
                last_error = error_str
                # If it's a quota error, provide helpful message but continue trying other models
                if '429' in error_str or ('quota' in error_str.lower() and 'limit: 0' not in error_str):
                    # If quota limit is 0, skip this model; otherwise might be temporary
                    if 'limit: 0' in error_str:
                        continue  # Skip models with 0 quota
                    # For other quota errors, might be rate limit - try next model
                    continue
                # Continue to next model if this one fails
                continue
        
        # If all models failed, return detailed error
        if '429' in str(last_error) or 'quota' in str(last_error).lower():
            return jsonify({
                'error': f'API quota exceeded or no models available. Tried: {", ".join(preferred_order[:5])}. Check your quota at https://ai.dev/usage?tab=rate-limit. Last error: {last_error[:200]}'
            }), 429
        else:
            return jsonify({
                'error': f'Failed to use any available model. Tried: {", ".join(preferred_order[:5])}. Errors: {" | ".join(errors[:3])}'
            }), 500
    
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

