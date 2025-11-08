# logic for guardrails
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BANNED_WORDS = {"kill", "bomb","attack","shoot"}

# Keywords related to plywood/shop business
BUSINESS_KEYWORDS = {
    # Products
    "plywood", "ply", "wood", "marine", "commercial", "waterproof", "bwp", "mr", "boiling water proof",
    "door", "doors", "flush", "panel", "laminate", "veneer", "hardware", "handle", "hinge",
    # Brands & Product Names
    "century", "centuryply", "sainik", "greenply", "club", "prime", "bond", "710", "club prime",
    # Business related
    "shop", "store", "studio", "plywood studio", "buy", "purchase", "price", "cost", "rate",
    "specification", "specs", "size", "thickness", "quality", "grade", "gst",
    "location", "address", "contact", "hyderabad", "goshamahal", "indiamart",
    "delivery", "order", "stock", "available", "warranty", "installation", "product", "products",
    # Technical terms
    "moisture", "termite", "adhesive", "layer", "core", "sheet", "board",
    "furniture", "cabinet", "interior", "exterior", "construction", "renovation",
    # Generic business terms (more lenient)
    "what", "tell", "about", "information", "details", "explain", "describe"
}

# PII PATTERNS

PII_PATTERNS = [
    (r"\b\d{12}\b", "[REDACTED_AADHAAR]"), # aadhaar
    (r"\b\d{10}\b", "[REDACTED_PHONE]"), # Phone number
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[REDACTED_EMAIL]") # email
]

def is_business_related(question: str) -> bool:
    """
    Check if the question is related to plywood/shop business
    More lenient version that allows generic questions
    
    Args:
        question: The user's question
        
    Returns:
        True if related to business, False otherwise
    """
    question_lower = question.lower()
    
    # First, check for clearly off-topic phrases (check BEFORE keyword matching)
    off_topic_keywords = [
        "prime minister", "president", "politician", "election", "government", "ministry",
        "celebrity", "actor", "actress", "movie", "film", "cinema", "bollywood",
        "sport", "cricket", "football", "basketball", "tennis", "player",
        "weather", "temperature", "rain", "climate",
        "tell me a joke", "joke", "funny story",
        "what is python", "programming", "coding", "software",
        "who is", "who was", "biography"
    ]
    
    for off_topic in off_topic_keywords:
        if off_topic in question_lower:
            logger.warning(f"Question rejected (off-topic keyword: {off_topic})")
            return False
    
    # Check for greetings (always allow)
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "thanks", "thank you"]
    if any(greeting in question_lower for greeting in greetings):
        return True
    
    # Very short questions (3 words or less) - be more lenient
    if len(question.split()) <= 3:
        # Check if any word is a business keyword
        for word in question.split():
            word_clean = word.lower().strip('?.,!')
            if word_clean in BUSINESS_KEYWORDS:
                logger.info(f"Short question approved (matched: {word_clean})")
                return True
    
    # Check for business-related keywords
    for keyword in BUSINESS_KEYWORDS:
        if keyword in question_lower:
            logger.info(f"Question is business-related (matched: {keyword})")
            return True
    
    # Check for common business questions
    business_patterns = [
        r"\bwhat.*(?:sell|offer|have|stock|provide|supply)\b",
        r"\b(?:where|location|address|find|visit)\b",
        r"\b(?:how|can|do you)\b.*(?:help|assist|contact|reach)\b",
        r"\b(?:tell|about|information)\b.*(?:you|your|company|business)\b",
    ]
    
    for pattern in business_patterns:
        if re.search(pattern, question_lower):
            logger.info("Question matches business pattern")
            return True
    
    # Default: allow the question (more lenient approach)
    logger.info("Question allowed (lenient mode)")
    return True

def apply_guardrails(text: str) -> str:
    """
    Apply guardrails to the text
    """
    original_text = text
    # 1. Check for banned words
    for word in BANNED_WORDS:
        if word.lower() in text.lower():
            logger.warning(f"Banned word found: {word}")
            text = text.replace(word, "BANNED_CONTENT")
            
    # 2. Check for PII
    for pattern, replacement in PII_PATTERNS:
        text = re.sub(pattern, replacement, text)
    
    if original_text != text:
        logger.info("Guardrails modified the output")
    
    else:
        logging.info("Guardrails did not modify the output")
    
    return text