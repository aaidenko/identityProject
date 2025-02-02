from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

def interpretEmojis(user_input):
    try:
        prompt = f"""
        Given this emoji input: {user_input}, generate three advanced English words and three advanced Korean words, but all of them with English definitions.
        These words should be those that best encapsulate ALL of the emojis, as the emojis have been picked in that combination to try to describe a certain mood.
        Format each as 'Word - Definition'.
        Do not add any extra content to your response outside of the six words and their english definitions. Each word-definition pair should be on their own line.
        """

        response = model.generate_content(prompt)
        text = response.text.strip().split("\n")[:6]

        result = []
        for line in text:
            parts = line.split(" - ", 1)
            word = parts[0].strip()
            definition = parts[1].strip()
            result.append({"word": word, "definition": definition})

        return result
    
    except Exception as e:
        print("Error: ") + e
        return [{"word": "Error", "definition": "Could not generate words. Try again."}] * 6

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/process_input', methods=["POST"])
def process_input():
    data = request.get_json()
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"error": "Invalid input"}), 400
    
    words_and_definitions = interpretEmojis(user_input)
    return jsonify({"output": words_and_definitions})

if __name__ == "__main__":
    app.run(debug=True)