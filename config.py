# central configuration for the pipeline
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY: str | None = os.getenv("HUGGINGFACE_API_KEY")
SERPER_API_KEY: str | None = os.getenv("SERPER_API_KEY")

# Model Configuration
USE_HUGGINGFACE = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"

# OpenAI Models
OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"
OPENAI_SMART_MODEL = "gpt-4o-mini"  # More intelligent for complex queries

# Hugging Face Models
HUGGINGFACE_DEFAULT_MODEL = "meta-llama/Llama-3.2-3B-Instruct"  # Meta Llama 3.2 (free tier compatible)
HUGGINGFACE_FALLBACK_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # Backup Mistral model

# Select default model based on configuration
if USE_HUGGINGFACE:
    DEFAULT_MODEL = HUGGINGFACE_DEFAULT_MODEL
else:
    DEFAULT_MODEL = OPENAI_DEFAULT_MODEL

TEMPERATURE = 0.7  # Increased for more creative responses
MAX_TOKENS = 800  # Increased for detailed answers

# Cache 
CACHE_TTL_SECONDS = 1800 # 30 minutes
VECTOR_TOP_K = 2  # number of top results to retrieve