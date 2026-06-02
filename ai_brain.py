from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def ai_reply(command):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents="Answer in simple student-friendly language, short and clear: " + command
        )

        return response.text

    except Exception as e:
        print("AI Error:", e)

        error = str(e)

        if "429" in error:
            return "My AI brain limit is over for now. Please try again after some time."

        elif "503" in error:
            return "My AI brain is busy right now. Please try again in a few minutes."

        elif "404" in error:
            return "This AI model is not available. Please change the model name."

        else:
            return "I am having trouble connecting to my AI brain."