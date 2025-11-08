"""
Web Search Tool - Search for product specifications and information
"""
import logging
import requests
from typing import Optional, List, Dict
from config import SERPER_API_KEY

def search_web(query: str, num_results: int = 3) -> Optional[str]:
    """
    Search the web for information using Serper API (Google Search)
    Falls back to DuckDuckGo if Serper is not available
    """
    logging.info(f"Web search for: {query}")
    
    # Try Serper API (Google Search) first
    if SERPER_API_KEY and SERPER_API_KEY != "your_serper_api_key_here":
        result = _search_with_serper(query, num_results)
        if result:
            return result
    
    # Fallback to DuckDuckGo Instant Answer
    result = _search_with_duckduckgo(query)
    if result:
        return result
    
    logging.warning("Web search failed or unavailable")
    return None

def _search_with_serper(query: str, num_results: int) -> Optional[str]:
    """Search using Serper API (Google Search)"""
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": SERPER_API_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": num_results
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Extract organic results
        results = []
        if "organic" in data:
            for item in data["organic"][:num_results]:
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                if title and snippet:
                    results.append(f"**{title}**\n{snippet}")
        
        if results:
            context = "\n\n".join(results)
            logging.info(f"Serper API returned {len(results)} results")
            return f"Web Search Results:\n\n{context}"
        
    except Exception as e:
        logging.warning(f"Serper API search failed: {e}")
    
    return None

def _search_with_duckduckgo(query: str) -> Optional[str]:
    """Search using DuckDuckGo Instant Answer API (free, no API key)"""
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1
        }
        
        # Add user agent to avoid blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Try to get abstract or definition
        abstract = data.get("AbstractText", "")
        definition = data.get("Definition", "")
        
        if abstract and len(abstract) > 50:
            logging.info("DuckDuckGo returned abstract")
            source = data.get("AbstractSource", "web")
            return f"**Information from {source}:**\n\n{abstract}"
        elif definition and len(definition) > 50:
            logging.info("DuckDuckGo returned definition")
            source = data.get("DefinitionSource", "dictionary")
            return f"**Definition from {source}:**\n\n{definition}"
        
        # Try related topics
        related = data.get("RelatedTopics", [])
        if related:
            snippets = []
            for topic in related[:3]:
                if isinstance(topic, dict) and "Text" in topic:
                    text = topic.get("Text", "")
                    if len(text) > 30:  # Only meaningful snippets
                        snippets.append(text)
            
            if snippets:
                context = "\n\n• ".join(snippets)
                logging.info(f"DuckDuckGo returned {len(snippets)} related topics")
                return f"**Related Information:**\n\n• {context}"
        
        logging.info("DuckDuckGo returned no useful results")
        
    except Exception as e:
        logging.warning(f"DuckDuckGo search failed: {e}")
    
    return None

def search_product_specs(product_name: str, brand: str = None) -> Optional[str]:
    """
    Search for specific product specifications
    """
    if brand:
        query = f"{brand} {product_name} specifications features details"
    else:
        query = f"{product_name} specifications features details plywood"
    
    return search_web(query, num_results=2)

# Simple test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test searches
    print("Testing web search...")
    print("\n" + "="*80)
    
    result = search_product_specs("Century Bond 710", "Centuryply")
    if result:
        print(result)
    else:
        print("No results found")
    
    print("\n" + "="*80)
    result = search_web("What is marine plywood used for?")
    if result:
        print(result)
    else:
        print("No results found")
