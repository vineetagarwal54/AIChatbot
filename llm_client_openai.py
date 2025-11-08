"""
OpenAI LLM Client - Real AI intelligence using GPT models
"""
import logging
from openai import OpenAI
from config import OPENAI_API_KEY, TEMPERATURE, MAX_TOKENS

# Initialize OpenAI client
client = None
if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        logging.info("OpenAI client initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize OpenAI client: {e}")

def call(model: str, prompt: str, temperature: float = TEMPERATURE, max_tokens: int = MAX_TOKENS) -> str:
    """
    Call OpenAI API with the given prompt
    """
    if not client:
        return "Error: OpenAI client not initialized. Check your API key."
    
    try:
        logging.info(f"Calling OpenAI {model} with prompt length: {len(prompt)}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a knowledgeable assistant for Plywood Studio, a premium plywood, doors, and laminate supplier in Hyderabad. Provide accurate, helpful, and detailed information about products, specifications, and services."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        answer = response.choices[0].message.content.strip()
        
        # Log token usage
        usage = response.usage
        logging.info(f"OpenAI response: {len(answer)} chars, tokens: {usage.total_tokens} (prompt: {usage.prompt_tokens}, completion: {usage.completion_tokens})")
        
        return answer
        
    except Exception as e:
        error_msg = str(e)
        logging.error(f"OpenAI API error: {error_msg}")
        
        # Return more specific error messages
        if "authentication" in error_msg.lower() or "api key" in error_msg.lower():
            return "Error: Invalid OpenAI API key"
        elif "rate limit" in error_msg.lower():
            return "Error: Rate limit exceeded. Please try again later."
        elif "quota" in error_msg.lower():
            return "Error: API quota exceeded"
        else:
            return f"Error: OpenAI API call failed - {error_msg}"

def test_connection() -> bool:
    """Test if OpenAI API is working"""
    try:
        result = call("gpt-3.5-turbo", "Say 'Hello' if you can hear me.", temperature=0, max_tokens=10)
        return not result.startswith("Error:")
    except:
        return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing OpenAI connection...")
    if test_connection():
        print("✅ OpenAI API is working!")
        
        # Test a real query
        print("\nTesting a real query...")
        response = call("gpt-3.5-turbo", "What is marine plywood and what is it used for?")
        print(f"\nResponse: {response}")
    else:
        print("❌ OpenAI API connection failed. Check your API key.")
