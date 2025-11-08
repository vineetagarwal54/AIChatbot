"""
Hugging Face API Client using official huggingface_hub SDK
Supports Meta Llama and other instruction-tuned models
"""
import logging
import time
from config import HUGGINGFACE_API_KEY, HUGGINGFACE_DEFAULT_MODEL, HUGGINGFACE_FALLBACK_MODEL, TEMPERATURE, MAX_TOKENS

try:
    from huggingface_hub import InferenceClient
    HF_CLIENT = InferenceClient(token=HUGGINGFACE_API_KEY) if HUGGINGFACE_API_KEY else None
except ImportError:
    HF_CLIENT = None
    logging.warning("huggingface_hub not installed. Install with: pip install huggingface-hub")

def call(model: str, prompt: str, temperature: float = TEMPERATURE, max_tokens: int = MAX_TOKENS) -> str:
    """
    Call Hugging Face Inference API with fallback support
    
    Args:
        model: Model name (e.g., "meta-llama/Llama-3.2-3B-Instruct")
        prompt: The prompt to send
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
    
    Returns:
        Generated text response or error message
    """
    if not HUGGINGFACE_API_KEY:
        return "Error: Hugging Face API key not configured"
    
    # Try primary model
    result = _try_model(model, prompt, temperature, max_tokens)
    if not result.startswith("Error"):
        return result
    
    # Try fallback model if primary fails
    logging.warning(f"Primary model {model} failed, trying fallback {HUGGINGFACE_FALLBACK_MODEL}")
    result = _try_model(HUGGINGFACE_FALLBACK_MODEL, prompt, temperature, max_tokens)
    
    return result

def _try_model(model: str, prompt: str, temperature: float, max_tokens: int, retries: int = 3) -> str:
    """
    Try calling a specific Hugging Face model using official SDK (chat_completion)
    """
    if not HF_CLIENT:
        return "Error: Hugging Face client not initialized (install huggingface-hub)"
    
    for attempt in range(retries):
        try:
            logging.info(f"Calling Hugging Face model: {model} (attempt {attempt + 1}/{retries})")
            
            # Use chat_completion API for conversational models
            response = HF_CLIENT.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.9
            )
            
            # Extract content from response
            if response and response.choices:
                content = response.choices[0].message.content
                if content and len(content) > 10:
                    logging.info(f"✅ Hugging Face success: {len(content)} chars")
                    return content.strip()
            
        except Exception as e:
            error_str = str(e).lower()
            
            # Handle model loading
            if "loading" in error_str or "503" in error_str:
                wait_time = 20
                logging.info(f"Model {model} loading... waiting {wait_time}s")
                time.sleep(wait_time)
                continue
            
            # Handle rate limiting
            if "rate" in error_str or "429" in error_str:
                wait_time = 5 * (attempt + 1)
                logging.warning(f"Rate limited, waiting {wait_time}s")
                time.sleep(wait_time)
                continue
            
            # Handle auth errors
            if "401" in error_str or "unauthorized" in error_str:
                return "Error: Invalid Hugging Face API key"
            
            # Handle model not found
            if "404" in error_str or "not found" in error_str:
                logging.error(f"Model {model} not found or not accessible")
                return f"Error: Model {model} not available"
            
            # Generic error
            logging.error(f"Hugging Face error: {e}")
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
                continue
    
    return f"Error: Failed to get response from {model} after {retries} attempts"

def test_connection() -> bool:
    """Test if Hugging Face API is working"""
    if not HUGGINGFACE_API_KEY:
        return False
    
    test_prompt = "Hello, how are you?"
    result = _try_model(HUGGINGFACE_DEFAULT_MODEL, test_prompt, 0.7, 50, retries=1)
    
    return not result.startswith("Error")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🤖 Testing Hugging Face API Client")
    print("=" * 80)
    
    # Test connection
    print("\n[Test 1] Connection test...")
    if test_connection():
        print("✅ Connection successful!")
    else:
        print("❌ Connection failed - check API key")
    
    # Test query
    print("\n[Test 2] Sample query...")
    test_query = """You are a helpful assistant for Plywood Studio.

Question: What is marine plywood?

Answer:"""
    
    response = call(HUGGINGFACE_DEFAULT_MODEL, test_query)
    print(f"Response: {response[:200]}...")
    print(f"Status: {'✅ PASS' if not response.startswith('Error') else '❌ FAIL'}")
    
    print("\n" + "=" * 80)
