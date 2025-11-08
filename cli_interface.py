"""
Main pipeline with smart LLM client (supports both OpenAI and Hugging Face)
"""
import time
import argparse
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler("pipeline.log"),
                              logging.StreamHandler()])

from cache_store import get as cache_get, set as cache_set
from router import build_prompt
from llm_client_langchain import call as llm_call  # Now with LangChain RAG!
from postprocess import secure_output
from config import CACHE_TTL_SECONDS
from guardrails import apply_guardrails, is_business_related

def run_pipeline(question: str):
    """
    Run the intelligent pipeline with smart LLM routing
    """
    logging.info(f"Starting pipeline for question: {question}")
    
    # Step 0: Check if question is business-related
    if not is_business_related(question):
        logging.warning(f"Off-topic question rejected: {question}")
        return "I'm sorry, but I can only answer questions related to plywood products, doors, laminates, and our Plywood Studio business. Please ask me about our products, brands (Centuryply, Sainik, Greenply), specifications, pricing, or store location."
    
    # Step 1: Check cache
    cached = cache_get(question)
    if cached:
        logging.info(f"Cache hit for question: {question}")
        return cached
    
    # Step 2: Use simple context (no vector retrieval for now)
    simple_context = "You are a helpful AI assistant. Answer questions clearly and concisely."
    
    # Step 3: Build prompt
    model, prompt = build_prompt(question, simple_context)
    logging.info("Assembled prompt:")
    logging.info(prompt)
    
    # Step 4: Call LLM (smart routing between OpenAI/HuggingFace)
    start_llm = time.time()
    answer = llm_call(model, prompt)
    llm_latency = int((time.time() - start_llm) * 1000)  # in milliseconds
    logging.info(f"LLM latency: {llm_latency}ms")
    
    # Step 5: Post-process
    post_processed = secure_output(answer)
    
    # Step 6: Apply guardrails
    secured = apply_guardrails(post_processed)
    
    # Step 7: Cache result
    cache_set(question, secured, CACHE_TTL_SECONDS)
    logging.info(f"Cached answer for question: {question}")
    
    return secured

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the intelligent RAG pipeline")
    parser.add_argument("--question", type=str, required=True, help="The question to answer")
    args = parser.parse_args()
    
    try:
        response = run_pipeline(args.question)
        print(f"\n🤖 Response: {response}")
    except Exception as e:
        print(f"❌ Error: {e}")
        if "API keys" in str(e):
            print("\n💡 Quick Setup:")
            print("1. Get free Hugging Face token: https://huggingface.co/settings/tokens")
            print("2. Add it to your .env file: HUGGINGFACE_API_KEY=your_token_here")
            print("3. Set USE_HUGGINGFACE=true in .env")

# Example usage:
# python main_smart.py --question "What is artificial intelligence?"