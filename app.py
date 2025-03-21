import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in .env file")

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-flash")  # Use the gemini-1.5-flash model

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Flask API'})

@app.route('/process', methods=['POST'])
def process():
    try:
        # Log the incoming request
        print("Processing request...")

        # Get text input
        text = request.json.get('text', '').strip()
        print(f"Text input: {text}")

        if not text:
            raise ValueError("Text input cannot be empty.")

        # Get file if uploaded
        file = request.files.get('file')
        print(f"File uploaded: {file is not None}")

        if file:
            # Process the uploaded file
            image_bytes = file.read()
            image_parts = [{'mime_type': file.content_type, 'data': image_bytes}]
            print("Processing file...")

            # Generate response with both text and image
            response = model.generate_content(
                contents=[text, *image_parts]
            )
        else:
            # Generate response with text only
            print("Processing text only...")
            response = model.generate_content(
                contents=text
            )

        print("Response generated successfully.")
        return jsonify({'response': response.text})

    except ValueError as ve:
        # Handle empty text input
        print(f"Validation error: {str(ve)}")
        return jsonify({'error': str(ve)}), 400

    except Exception as e:
        # Log the error details to the terminal
        print(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Explicitly set the port to 8081
    app.run(debug=True, port=8081)