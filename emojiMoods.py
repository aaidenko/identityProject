import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-1.5-flash")

def interpretEmojis(emojis):
    try:
        prompt = "Return 3 difficult, obscure adjectives to describe my mood each in English and Korean that encapsulate the entirety of the mood described by these following emojis: " + emojis + " Your response should only be 6 total words, 3 English and 3 Korean. No other words in your response"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Error: ") + e
        return None

def main():
    emojis = input("Describe your mood using some emojis: ")
    print("\nProcessing...\n")
    result = interpretEmojis(emojis)

    if result:
        print("Generated words: ")
        print(result)
    else:
        print("Failed to generate.")

if __name__ == "__main__":
    main()