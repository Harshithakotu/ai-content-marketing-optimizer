import os
from groq import Groq
from dotenv import load_dotenv

# Load .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file!")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# --------------------------
# Content Optimization
# --------------------------
def optimize_content(text: str) -> str:
    """
    Send the input text to Groq for marketing optimization.
    Returns the optimized text.
    """
    # Prompt to guide Groq
    prompt = f"""
    You are a marketing copy expert. 
    Take the following text and rewrite it to be highly engaging, persuasive, and optimized for social media marketing. 
    Make it clear, exciting, and attention-grabbing while keeping the meaning intact.
    
    Original text:
    {text}
    
    Optimized text:
    """

    try:
        response = client.generate(
            model="groq-1.0",
            prompt=prompt,
            max_tokens=300  # adjust as needed
        )
        
        # Groq returns a list of completions
        optimized_text = response.output_text.strip() if hasattr(response, "output_text") else str(response)
        return optimized_text

    except Exception as e:
        print(f"Groq API error: {e}")
        return text  # fallback to original if something goes wrong

# --------------------------
# AB Testing Recommendations
# --------------------------
def generate_recommendations(text: str) -> str:
    """
    Generate recommendations for AB Testing.
    Currently uses Groq optimization as placeholder.
    """
    try:
        optimized = optimize_content(text)
        return f"Optimized version: {optimized[:100]}..."  # preview snippet
    except Exception as e:
        print("AB recommendation error:", e)
        return f"Consider improving content: {text[:100]}..."
