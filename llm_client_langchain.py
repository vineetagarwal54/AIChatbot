"""
LangChain-powered Hybrid LLM Client
Intelligent routing with RAG system, web search, and fallbacks
"""
import logging
import random
import re
from config import USE_HUGGINGFACE, OPENAI_API_KEY, HUGGINGFACE_API_KEY, OPENAI_DEFAULT_MODEL

def call(model: str, prompt: str) -> str:
    """
    Intelligent hybrid LLM client with priority chain:
    1. Try Hugging Face (Meta Llama / Mistral) - FREE
    2. Try LangChain RAG (vector search + conversational AI) - if OpenAI available
    3. Try web search for external info
    4. Try direct OpenAI
    5. Fall back to knowledge base
    """
    logging.info(f"Processing with intelligent AI chain: {prompt[:100]}...")
    
    # Extract user question for better routing
    user_question = _extract_user_question(prompt)
    
    # Step 1: Try Hugging Face FIRST (if enabled and API key available)
    if USE_HUGGINGFACE and HUGGINGFACE_API_KEY:
        hf_response = _try_huggingface(model, prompt, user_question)
        if hf_response and not hf_response.startswith("Error"):
            logging.info("✅ Using Hugging Face (Meta Llama) response")
            return hf_response
    
    # Step 2: Try LangChain RAG system (best option if OpenAI available!)
    if OPENAI_API_KEY and not USE_HUGGINGFACE:
        rag_response = _try_rag_system(user_question)
        if rag_response and not rag_response.startswith("Error"):
            logging.info("✅ Using LangChain RAG response")
            return rag_response
    
    # Step 3: Try web search for specifications/detailed info
    if _needs_web_search(user_question):
        web_response = _try_web_search_response(user_question, prompt)
        if web_response and not web_response.startswith("Error"):
            logging.info("✅ Using web-enhanced intelligent response")
            return web_response
    
    # Step 4: Try direct OpenAI (without RAG)
    if OPENAI_API_KEY and not USE_HUGGINGFACE:
        openai_response = _try_openai(model, prompt, user_question)
        if openai_response and not openai_response.startswith("Error"):
            logging.info("✅ Using OpenAI GPT response")
            return openai_response
    
    # Step 5: Fall back to curated responses (last resort)
    logging.info("Using curated fallback response")
    return _generate_curated_response(user_question)

def _extract_user_question(prompt: str) -> str:
    """Extract the actual user question from prompt template"""
    if "Question:" in prompt and "Answer:" in prompt:
        start = prompt.find("Question:") + len("Question:")
        end = prompt.find("Answer:")
        if start > 0 and end > start:
            return prompt[start:end].strip()
    return prompt

def _try_rag_system(user_question: str) -> str:
    """Try LangChain RAG system for intelligent retrieval"""
    try:
        from rag_system import query_rag
        
        logging.info("Querying LangChain RAG system...")
        result = query_rag(user_question)
        
        if result and "answer" in result:
            answer = result["answer"]
            sources = result.get("source_documents", [])
            
            # Validate response quality
            if len(answer) > 50 and not any(err in answer.lower() for err in ['error', 'failed', 'not available']):
                logging.info(f"RAG system returned answer with {len(sources)} source documents")
                return answer
        
    except Exception as e:
        logging.warning(f"RAG system failed: {e}")
    
    return "Error: RAG system unavailable"

def _try_openai(model: str, full_prompt: str, user_question: str) -> str:
    """Try OpenAI API with enhanced context (non-RAG fallback)"""
    try:
        from llm_client_openai import call as openai_call
        
        # Build enhanced prompt with business context
        enhanced_prompt = f"""You are an expert assistant for Plywood Studio, a premium plywood, doors, and laminate supplier in Hyderabad, India.

BUSINESS INFORMATION:
- Company: Plywood Studio (established 2022)
- Location: Goshamahal, Hyderabad-500012, Telangana
- Products: Premium plywood, wooden doors, laminate sheets, door hardware
- Brands: Centuryply (Club Prime, Bond 710), Sainik MR Plywood, Greenply
- Specialties: Wholesale trading, GST registered, 5-star IndiaMART rating

CUSTOMER QUESTION:
{user_question}

INSTRUCTIONS:
- Provide accurate, detailed, and helpful information
- If you don't know specific product details, acknowledge it and provide general guidance
- Be professional yet friendly
- Focus on practical advice for customers
- Mention our location in Hyderabad and how to contact us if relevant

Your response:"""
        
        response = openai_call(model if model != "test" else OPENAI_DEFAULT_MODEL, enhanced_prompt)
        
        # Validate response quality
        if len(response) > 50 and not any(err in response.lower() for err in ['error:', 'failed', 'api key']):
            return response
        
    except Exception as e:
        logging.warning(f"OpenAI call failed: {e}")
    
    return "Error: OpenAI unavailable"

def _needs_web_search(question: str) -> bool:
    """Determine if question needs web search for specifications"""
    question_lower = question.lower()
    
    # Keywords that indicate need for detailed specs
    spec_keywords = [
        'specification', 'specs', 'details', 'properties', 'features',
        'thickness', 'size', 'dimensions', 'grade', 'quality',
        'price', 'cost', 'rate', 'mrp',
        'difference between', 'compare', 'vs', 'versus',
        'advantage', 'disadvantage', 'pros', 'cons',
        'technical', 'composition', 'material',
        'waterproof', 'moisture', 'termite', 'durability'
    ]
    
    return any(keyword in question_lower for keyword in spec_keywords)

def _try_web_search_response(user_question: str, full_prompt: str) -> str:
    """Try to enhance response with web search - works standalone or with AI"""
    try:
        from web_search import search_web, search_product_specs
        
        # Detect if asking about specific product
        question_lower = user_question.lower()
        
        # Search for product specs if product name detected
        brand_keywords = {
            'centuryply': 'Centuryply',
            'century ply': 'Centuryply',
            'bond 710': 'Centuryply Bond 710',
            'club prime': 'Centuryply Club Prime',
            'sainik': 'Sainik',
            'greenply': 'Greenply',
            'marine plywood': 'Marine Plywood',
            'commercial plywood': 'Commercial Plywood',
            'waterproof plywood': 'Waterproof Plywood'
        }
        
        web_context = None
        detected_product = None
        for keyword, brand in brand_keywords.items():
            if keyword in question_lower:
                web_context = search_product_specs(user_question, brand)
                detected_product = brand
                break
        
        # Generic search if no specific product
        if not web_context:
            web_context = search_web(user_question)
        
        # If we got web results, synthesize response
        if web_context:
            # Try to use OpenAI for synthesis if available
            if OPENAI_API_KEY:
                try:
                    from llm_client_openai import call as openai_call
                    
                    enhanced_prompt = f"""You are an expert assistant for Plywood Studio in Hyderabad.

WEB SEARCH RESULTS:
{web_context}

CUSTOMER QUESTION:
{user_question}

Using the web search results above and your knowledge, provide a comprehensive answer.
Mention that for exact specifications and current availability at Plywood Studio, they should contact us via IndiaMART or visit our Goshamahal showroom.

Your response:"""
                    
                    response = openai_call(OPENAI_DEFAULT_MODEL, enhanced_prompt)
                    if not response.startswith("Error"):
                        return response
                except Exception as e:
                    logging.warning(f"OpenAI synthesis failed, using direct web results: {e}")
            
            # Fallback: return formatted web results directly
            intro = f"Based on web search results"
            if detected_product:
                intro = f"Here's information about {detected_product}"
            
            footer = "\n\n💡 **Note:** This information is from web sources. For exact specifications, current stock, and pricing at Plywood Studio, please contact us via IndiaMART (www.indiamart.com/plywoodstudio) or visit our showroom in Goshamahal, Hyderabad."
            
            return f"{intro}:\n\n{web_context}{footer}"
        
    except Exception as e:
        logging.warning(f"Web search enhancement failed: {e}")
    
    return "Error: Web search unavailable"

def _try_huggingface(model: str, full_prompt: str, user_question: str) -> str:
    """Try Hugging Face API with Meta Llama or Mistral models"""
    try:
        from llm_client_huggingface import call as hf_call
        
        # Build enhanced prompt with business context for better responses
        enhanced_prompt = f"""You are an expert assistant for Plywood Studio, a premium plywood, doors, and laminate supplier in Hyderabad, India.

BUSINESS INFORMATION:
- Company: Plywood Studio (established 2022)
- Location: Goshamahal, Hyderabad-500012, Telangana
- Products: Premium plywood, wooden doors, laminate sheets, door hardware
- Brands: Centuryply (Club Prime, Bond 710), Sainik MR Plywood, Greenply

CUSTOMER QUESTION:
{user_question}

INSTRUCTIONS:
Provide accurate, detailed, and helpful information about plywood products. Be professional yet friendly.

Your response:"""
        
        logging.info("Calling Hugging Face (Meta Llama)...")
        response = hf_call(model, enhanced_prompt)
        
        # Validate response quality
        if not response.startswith("Error") and len(response) > 30:
            # Check for common failure patterns
            bad_patterns = ["i don't", "i cannot", "i apologize", "as an ai", "i'm unable"]
            if not any(pattern in response.lower() for pattern in bad_patterns):
                return response
        
    except Exception as e:
        logging.warning(f"Hugging Face call failed: {e}")
    
    return "Error: Hugging Face unavailable"

def _generate_curated_response(user_question: str) -> str:
    """Generate curated response using knowledge base"""
    prompt_lower = user_question.lower()
    
    # Try knowledge base first for detailed answers
    try:
        from knowledge_base import get_knowledge
        kb_response = get_knowledge(user_question)
        if kb_response:
            logging.info("Using knowledge base response")
            return kb_response
    except Exception as e:
        logging.warning(f"Knowledge base lookup failed: {e}")
    
    # Helper for word boundaries
    def contains_word(text, word):
        return re.search(r'\b' + re.escape(word) + r'\b', text) is not None
    
    # Greetings
    if any(contains_word(prompt_lower, word) for word in ['hello', 'hi', 'hey']):
        return random.choice([
            "Hello! Welcome to Plywood Studio. I'm here to help you with premium plywood, doors, and laminate solutions. What can I assist you with today?",
            "Hi there! I'm your Plywood Studio assistant powered by AI. We specialize in branded plywood (Centuryply, Sainik, Greenply), wooden doors, and laminate sheets. What would you like to know?"
        ])
    
    # Business info
    if any(phrase in prompt_lower for phrase in ['your company', 'your business', 'about you', 'established']):
        return "Plywood Studio is a partnership firm established in 2022, located in Goshamahal, Hyderabad. We're GST registered wholesale traders specializing in premium plywood, doors, and laminates with a 5-star IndiaMART rating."
    
    # Specific products
    if 'centuryply' in prompt_lower or 'century ply' in prompt_lower:
        return "Centuryply is one of India's leading plywood brands. We stock Centuryply Club Prime (premium BWP grade with ViroKill technology) and Bond 710 (MR grade with excellent bonding). For detailed specifications and current availability, please contact us via IndiaMART or visit our Goshamahal showroom."
    
    if 'sainik' in prompt_lower:
        return "Sainik MR Plywood is a high-quality marine-grade plywood known for excellent moisture resistance and durability. We stock various grades with 7-ply construction for strength. For specific specifications and pricing, please contact us through IndiaMART or visit our showroom in Goshamahal, Hyderabad."
    
    if 'greenply' in prompt_lower:
        return "Greenply is a trusted eco-friendly plywood brand we carry. We offer Greenply plywood (various grades) and flush doors. Known for E0 grade (low emission) and termite resistance. For detailed specifications, current stock, and pricing, please reach out via IndiaMART or visit us in Hyderabad."
    
    # Doors
    if 'door' in prompt_lower or 'doors' in prompt_lower:
        return "We offer wooden doors including Greenply Flush Doors (smooth surface, ready for paint), Panel Polish Doors (traditional design), and Laminate Doors (modern finish) in standard sizes (7ft x 3ft, 8ft x 4ft) and custom sizes. Contact us via IndiaMART at www.indiamart.com/plywoodstudio."
    
    # Location/contact
    if any(word in prompt_lower for word in ['location', 'address', 'where', 'contact', 'reach']):
        return "Plywood Studio is located at 5-5-983, 5-5-982/1, Goshamahal, Hyderabad-500012, Telangana. Contact us through our IndiaMART page: www.indiamart.com/plywoodstudio for quotes and availability."
    
    # Default
    return "At Plywood Studio, we offer premium plywood (Centuryply, Sainik, Greenply), wooden doors, laminate sheets, and hardware. We're located in Goshamahal, Hyderabad since 2022. For specific product details and pricing, please contact us via IndiaMART or visit our showroom. How can I help you today?"

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    test_queries = [
        "What are the specifications of marine plywood?",
        "Tell me about Centuryply Club Prime",
        "What is the difference between MR and BWP plywood?",
        "Hello, how can you help me?",
        "Where is your store?"
    ]
    
    print("🤖 Testing LangChain-Powered Hybrid AI System")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        print("-" * 80)
        response = call("gpt-3.5-turbo", f"Question: {query}\n\nAnswer: ")
        print(f"🤖 Response: {response[:300]}...")
    
    print("\n" + "=" * 80)
    print("✅ System test complete!")
