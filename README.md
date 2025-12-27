# Amazon Driver Tracker - Chat Bot

A modern chatbot application powered by Google's Gemini AI (free tier) that provides an interactive chat interface for Amazon driver tracking assistance.

## Features

- 🤖 AI-powered chatbot using Google Gemini Pro
- 💬 Modern, responsive chat interface
- 🎨 Beautiful gradient UI design
- ⚡ Real-time messaging
- 🔒 Secure API key management

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key (free tier)

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Gemini API key:**
   
   Create a `.env` file in the project root:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   
   To get your free Gemini API key:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the key and paste it in your `.env` file

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

## Project Structure

```
Amazon/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore file
├── templates/
│   └── index.html       # Main HTML template
└── static/
    ├── style.css        # Stylesheet
    └── script.js        # Frontend JavaScript
```

## Usage

1. Start the Flask server
2. Open the application in your browser
3. Type your message in the input field
4. Press Enter or click the send button
5. The AI will respond using Gemini's free tier API

## Notes

- The API key is stored in the `.env` file and is not committed to version control
- The application runs on `http://localhost:5000` by default
- Make sure you have an active internet connection to use the Gemini API

## Troubleshooting

- **API Key Error**: Make sure your `.env` file exists and contains a valid `GEMINI_API_KEY`
- **Port Already in Use**: Change the port in `app.py` if port 5000 is already in use
- **Module Not Found**: Run `pip install -r requirements.txt` to install all dependencies

