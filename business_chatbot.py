# Simple Plywood Chatbot without complex dependencies
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import time, uuid, logging
import uvicorn
from datetime import datetime

# Use the working components
from cache_store import get as cache_get, set as cache_set
from llm_client_hybrid import call as llm_call
from postprocess import secure_output
from guardrails import apply_guardrails
from config import CACHE_TTL_SECONDS

app = FastAPI(
    title="🏗️ Plywood Studio AI Assistant",
    description="Intelligent assistant for Plywood Studio - Premium plywood, doors and laminate solutions in Hyderabad",
    version="1.0.0"
)

# Simple in-memory plywood knowledge base
PLYWOOD_KNOWLEDGE = {
    "grades": """
    PLYWOOD GRADES:
    - Grade A: Smooth, paintable surface, no knots or defects. Best for furniture and cabinets. Premium pricing.
    - Grade B: Solid surface with minor defects, small knots allowed. Good for painted surfaces. Mid-range pricing.
    - Grade C: Knots and small holes allowed, rough surface. Suitable for structural applications. Budget-friendly.
    - Grade D: Larger knots and holes allowed. Lowest cost option for backing and hidden elements.
    """,
    
    "types": """
    PLYWOOD TYPES:
    - Interior Plywood: For indoor use only, moisture-resistant adhesives. Applications: furniture, cabinets, shelving.
    - Exterior Plywood: Waterproof adhesives, weather-resistant. Applications: siding, outdoor furniture.
    - Marine Plywood: Highest quality waterproof construction, no voids. Applications: boat building, docks.
    - Structural Plywood: Engineered for load-bearing applications. Applications: flooring, roofing, wall sheathing.
    """,
    
    "specifications": """
    STANDARD SPECIFICATIONS:
    Thicknesses: 3mm (1/8"), 6mm (1/4"), 9mm (3/8"), 12mm (1/2"), 15mm (5/8"), 18mm (3/4"), 25mm (1")
    Sizes: 4'x8' (most common), 4'x4', 5'x5', custom cuts available
    Wood Species: Birch (strong), Oak (premium), Pine (economical), Poplar (paint-grade), Maple (furniture-grade)
    """,
    
    "pricing": """
    PRICING STRUCTURE:
    - Grade A Birch 18mm: $89.99/sheet
    - Grade B Birch 12mm: $54.99/sheet  
    - Marine Grade 18mm: $125.99/sheet
    - Structural OSB 18mm: $45.99/sheet
    
    BULK DISCOUNTS:
    - 10+ sheets: 5% discount
    - 25+ sheets: 10% discount
    - 50+ sheets: 15% discount
    - 100+ sheets: 20% discount
    """,
    
    "services": """
    OUR SERVICES:
    - Custom cutting to size
    - Edge banding application
    - Local delivery (within 50 miles)
    - Bulk ordering and storage
    - Technical consultation
    - Project planning assistance
    - Contractor accounts available
    """
}

class ChatMessage(BaseModel):
    message: str
    user_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    response_time_ms: int

def get_relevant_context(query: str) -> str:
    """Get relevant plywood information based on the query"""
    query_lower = query.lower()
    relevant_context = []
    
    # Check which knowledge sections are relevant
    if any(word in query_lower for word in ['grade', 'quality', 'a grade', 'b grade', 'c grade', 'd grade']):
        relevant_context.append(PLYWOOD_KNOWLEDGE['grades'])
    
    if any(word in query_lower for word in ['type', 'interior', 'exterior', 'marine', 'structural']):
        relevant_context.append(PLYWOOD_KNOWLEDGE['types'])
    
    if any(word in query_lower for word in ['size', 'thickness', 'dimension', 'spec', 'species', 'birch', 'oak']):
        relevant_context.append(PLYWOOD_KNOWLEDGE['specifications'])
    
    if any(word in query_lower for word in ['price', 'cost', 'pricing', 'discount', 'bulk']):
        relevant_context.append(PLYWOOD_KNOWLEDGE['pricing'])
    
    if any(word in query_lower for word in ['service', 'delivery', 'cutting', 'contractor']):
        relevant_context.append(PLYWOOD_KNOWLEDGE['services'])
    
    # If no specific context found, include basic info
    if not relevant_context:
        relevant_context = [PLYWOOD_KNOWLEDGE['types'], PLYWOOD_KNOWLEDGE['grades']]
    
    return "\n\n".join(relevant_context)

def build_plywood_prompt(query: str) -> tuple[str, str]:
    """Build specialized prompt for plywood business"""
    from config import DEFAULT_MODEL
    
    context = get_relevant_context(query)
    
    prompt_template = """You are an expert plywood business assistant. Use the following information to answer the customer's question accurately and helpfully.

PLYWOOD BUSINESS INFORMATION:
{context}

CUSTOMER QUESTION: {query}

Please provide a helpful, professional response. If pricing is mentioned, note that prices may vary and suggest contacting for current quotes. If technical specifications are needed, provide accurate information from the context above.

RESPONSE:"""

    prompt = prompt_template.format(context=context, query=query)
    return DEFAULT_MODEL, prompt

def run_plywood_chat(message: str, user_id: str | None = None) -> ChatResponse:
    """Process plywood business chat message"""
    start_time = time.time()
    
    # Check cache
    cached = cache_get(message)
    if cached:
        return ChatResponse(
            response=cached,
            timestamp=datetime.now().isoformat(),
            response_time_ms=int((time.time() - start_time) * 1000)
        )
    
    # Build specialized prompt
    model, prompt = build_plywood_prompt(message)
    
    # Call LLM
    try:
        raw_response = llm_call(model, prompt)
        processed = secure_output(raw_response)
        final_response = apply_guardrails(processed)
        
        # Add business-specific formatting
        if "price" in message.lower() or "cost" in message.lower():
            final_response += "\n\n💰 *Prices subject to change. Contact us for current pricing and bulk discounts.*"
        
        if "stock" in message.lower() or "availability" in message.lower():
            final_response += "\n\n📦 *Please contact us to check current inventory levels.*"
        
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        final_response = "I apologize, but I'm experiencing technical difficulties. Please try again or contact our sales team directly for assistance with your plywood needs."
    
    # Cache the response
    total_time = int((time.time() - start_time) * 1000)
    cache_set(message, final_response, CACHE_TTL_SECONDS)
    
    return ChatResponse(
        response=final_response,
        timestamp=datetime.now().isoformat(),
        response_time_ms=total_time
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint for plywood business queries"""
    if not message.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        return run_plywood_chat(message.message, message.user_id)
    except Exception as e:
        logging.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    """Beautiful plywood business chat interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏗️ Plywood Studio AI Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #8B4513 0%, #D2B48C 100%);
            height: 100vh; display: flex; justify-content: center; align-items: center;
        }
        .chat-container {
            width: 90%; max-width: 900px; height: 90vh;
            background: white; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            display: flex; flex-direction: column; overflow: hidden;
        }
        .chat-header {
            background: linear-gradient(135deg, #8B4513, #A0522D);
            color: white; padding: 20px; text-align: center;
        }
        .chat-header h1 { font-size: 28px; margin-bottom: 8px; }
        .chat-header p { opacity: 0.9; font-size: 16px; }
        .business-info {
            background: #f8f9fa; padding: 15px; border-bottom: 1px solid #e0e0e0;
            font-size: 14px; color: #666;
        }
        .chat-messages {
            flex: 1; padding: 20px; overflow-y: auto; background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px; padding: 15px 18px; border-radius: 18px; max-width: 85%;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .user-message {
            background: linear-gradient(135deg, #007bff, #0056b3); color: white;
            margin-left: auto; border-bottom-right-radius: 5px;
        }
        .bot-message {
            background: white; color: #333; border: 1px solid #e0e0e0; 
            border-bottom-left-radius: 5px;
        }
        .chat-input-container {
            padding: 20px; background: white; border-top: 1px solid #e0e0e0;
            display: flex; gap: 12px;
        }
        .chat-input {
            flex: 1; padding: 15px 20px; border: 2px solid #ddd;
            border-radius: 25px; font-size: 16px; outline: none;
            transition: border-color 0.3s;
        }
        .chat-input:focus { border-color: #8B4513; }
        .send-button {
            padding: 15px 30px; background: linear-gradient(135deg, #8B4513, #A0522D); 
            color: white; border: none; border-radius: 25px; cursor: pointer;
            font-weight: bold; transition: transform 0.2s;
        }
        .send-button:hover { transform: translateY(-2px); }
        .quick-questions {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px; margin: 15px 0; padding: 0 5px;
        }
        .quick-question {
            padding: 10px 15px; background: linear-gradient(135deg, #e9ecef, #dee2e6); 
            border: none; border-radius: 20px; cursor: pointer; font-size: 14px;
            transition: all 0.3s; text-align: center;
        }
        .quick-question:hover { 
            background: linear-gradient(135deg, #8B4513, #A0522D); 
            color: white; transform: translateY(-2px);
        }
        .typing { opacity: 0.7; font-style: italic; }
        .response-time { font-size: 12px; color: #999; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🏗️ Plywood Studio AI Assistant</h1>
            <p>Premium plywood, doors and laminate solutions in Hyderabad since 2022</p>
        </div>
        
        <div class="business-info">
            <strong>📍 Location:</strong> Goshamahal, Hyderabad • <strong>🏷️ Brands:</strong> Centuryply, Sainik, Greenply • <strong>⭐ Rating:</strong> 5.0 stars on IndiaMART
        </div>
        
        <div class="chat-messages" id="chatMessages">
            <div class="message bot-message">
                <strong>🤖 Plywood Studio Assistant:</strong><br>
                Welcome to Plywood Studio! I'm here to help you with:
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li><strong>Wooden Plywood:</strong> Centuryply, Sainik, Greenply brands</li>
                    <li><strong>Wooden Doors:</strong> Flush doors, panel doors, laminate doors</li>
                    <li><strong>Laminate Sheets:</strong> Various thicknesses and finishes</li>
                    <li><strong>Door Hardware:</strong> Quality locks and accessories</li>
                    <li><strong>Business Info:</strong> Location, contact, and services</li>
                </ul>
                Ask me anything about our products or services!
            </div>
            
            <div class="quick-questions">
                <button class="quick-question" onclick="askQuestion('What plywood brands do you carry?')">🏷️ Our Brands</button>
                <button class="quick-question" onclick="askQuestion('What types of doors are available?')">� Door Options</button>
                <button class="quick-question" onclick="askQuestion('Where is Plywood Studio located?')">� Location & Contact</button>
                <button class="quick-question" onclick="askQuestion('Do you have laminate sheets?')">� Laminate Sheets</button>
                <button class="quick-question" onclick="askQuestion('What door hardware do you offer?')">� Door Hardware</button>
                <button class="quick-question" onclick="askQuestion('How can I contact Plywood Studio?')">� Contact Us</button>
            </div>
        </div>
        
        <div class="chat-input-container">
            <input type="text" id="chatInput" class="chat-input" 
                   placeholder="Ask about our plywood brands, doors, laminate sheets, or business info..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="send-button" onclick="sendMessage()">Send 📤</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, 'user');
            input.value = '';

            const typingId = addMessage('🔍 Searching our plywood database...', 'bot', true);

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                
                const data = await response.json();
                document.getElementById(typingId).remove();
                
                const responseHtml = data.response.replace(/\\n/g, '<br>') + 
                    `<div class="response-time">⏱️ Response time: ${data.response_time_ms}ms</div>`;
                addMessage(responseHtml, 'bot');
                
            } catch (error) {
                document.getElementById(typingId).remove();
                addMessage('❌ Sorry, I encountered an error. Please try again or contact our sales team.', 'bot');
            }
        }

        function addMessage(content, sender, isTyping = false) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            const messageId = 'msg-' + Date.now();
            messageDiv.id = messageId;
            messageDiv.className = `message ${sender}-message ${isTyping ? 'typing' : ''}`;
            
            if (sender === 'user') {
                messageDiv.innerHTML = `<strong>👤 You:</strong><br>${content}`;
            } else {
                messageDiv.innerHTML = `<strong>🤖 Plywood Expert:</strong><br>${content}`;
            }
            
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            return messageId;
        }

        function askQuestion(question) {
            document.getElementById('chatInput').value = question;
            sendMessage();
        }
    </script>
</body>
</html>
    """

@app.get("/api/business-info")
async def get_business_info():
    """Get plywood business information"""
    return {
        "company": "Premium Plywood Solutions",
        "specialties": ["Interior Plywood", "Exterior Plywood", "Marine Grade", "Structural Plywood"],
        "services": ["Custom Cutting", "Bulk Orders", "Delivery", "Technical Consultation"],
        "grades_available": ["Grade A", "Grade B", "Grade C", "Grade D"],
        "contact": "Contact through this chat interface for pricing and availability"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "Plywood Studio AI Assistant"}

if __name__ == "__main__":
    print("🚀 Starting Plywood Studio AI Assistant...")
    print("🏗️ Specialized for plywood business queries!")
    print("💻 Web Interface: http://localhost:8001")
    print("📋 Business Info API: http://localhost:8001/api/business-info")
    print("🎯 Ready to assist with plywood products, pricing, and specifications!")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)