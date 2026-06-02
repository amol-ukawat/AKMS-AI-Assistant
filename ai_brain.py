from google import genai
from config import GEMINI_API_KEY

def ai_reply(command):

    # No API Key
    if not GEMINI_API_KEY or GEMINI_API_KEY.strip() == "":
        return "AI Brain is not configured. Please add your Gemini API key in config.py."

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=command
        )

        return response.text

    except Exception as e:

        error = str(e)

        print("AI Error:", error)

        if "429" in error:
            return "My AI brain quota is exhausted. Please try again later."

        elif "503" in error:
            return "My AI brain is busy right now. Please try again later."

        elif "404" in error:
            return "AI model not found."

        elif "API key" in error:
            return "Invalid Gemini API key."

        else:
            return "AI Brain is currently unavailable."