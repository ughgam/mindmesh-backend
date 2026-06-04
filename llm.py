import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "real-key")) # Prefer the .env key, but second works as a fallback.

def generate_rag_response(query: str, retrieved_chunks: list) -> str:
    """
    Constructs a highly constrained prompt and generates a response using Gemini 2.5 Flash.
    """
    context_block = "\n\n--- NEXT EXCERPT ---\n\n".join(retrieved_chunks)
    
    system_instruction = """
    You are MindMesh, an AI assistant that retrieves and synthesizes information strictly from a user's personal knowledge base.
    
    RULES:
    1. Answer the user's query using ONLY the information provided in the 'Context Excerpts' below.
    2. Do NOT use outside knowledge or pre-trained information.
    3. If the answer is not contained in the context, explicitly say: "I don't have enough information in your saved articles to answer this."
    4. Keep your answer to the point, structured, and easy to read.
    """
    
    user_prompt = f"Context Excerpts:\n{context_block}\n\nUser Question: {query}"
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
            )
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "An error occurred while generating the AI response. Please try again."
