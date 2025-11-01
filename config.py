# central configuration for the pipeline
import os
from dotenv import load_dotenv

load_dotenv()

# Environment variables
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY: str | None = os.getenv("HUGGINGFACE_API_KEY")

# Model Configuration
USE_HUGGINGFACE = os.getenv("USE_HUGGINGFACE", "false").lower() == "true"

# OpenAI Models
OPENAI_DEFAULT_MODEL = "gpt-3.5-turbo"

# Hugging Face Models
HUGGINGFACE_DEFAULT_MODEL = "google/flan-t5-large"  # Excellent for Q&A

# Select default model based on configuration
if USE_HUGGINGFACE:
    DEFAULT_MODEL = HUGGINGFACE_DEFAULT_MODEL
else:
    DEFAULT_MODEL = OPENAI_DEFAULT_MODEL

TEMPERATURE = 0.2
MAX_TOKENS = 512

# Cache 
CACHE_TTL_SECONDS = 1800 # 30 minutes
VECTOR_TOP_K = 2  # number of top results to retrieve