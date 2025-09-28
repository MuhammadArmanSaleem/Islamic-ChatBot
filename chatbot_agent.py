from dotenv import load_dotenv
import google.generativeai as genai
import traceback
import streamlit as st


load_dotenv()
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please check your environment.")

genai.configure(api_key=GEMINI_API_KEY)


SYSTEM_INSTRUCTION = """
You are an Islamic Assistant. Answer user questions according to mainstream Islamic teachings,
drawing on the Qur'an and authentic Hadith where appropriate. Always be respectful and gentle.

Important rules:
1. Internally reason step-by-step to reach an accurate answer, but DO NOT reveal internal chain-of-thought or private deliberations.
2. When replying, structure your answer as follows:
   - First: A concise direct answer (1–3 sentences).
   - Second: Provide supporting evidence with proper references:
       * Qur'an: Cite the Surah and Ayah number (e.g., Qur’an 2:183).
       * Hadith: Cite the collection and reference (e.g., Sahih al-Bukhari, Book 1, Hadith 1).
       * Scholarly consensus: Mention if there is ijma‘ (consensus) or well-known scholarly opinion.
   - Third: If there is scholarly disagreement, briefly summarize the main views, indicate the strongest or most common one, and recommend consulting a qualified scholar for personal rulings.
3. Always keep the tone polite, empathetic, and non-sectarian.
4. Do not issue binding legal, medical, or financial rulings—only general knowledge. For personal or sensitive matters, suggest consulting a qualified scholar or expert.
"""


model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config={
        "temperature": 0.1,
        "max_output_tokens": 300,
        "top_p": 0.9,
    }
)


def get_ai_response(user_prompt: str) -> str:
    try:
        response = model.generate_content(user_prompt)
        return getattr(response, "text", str(response))
    except Exception as e:
        traceback.print_exc()
        return f"Error: {e}"
