# Modern ChatGPT-style Plywood Studio Chatbot
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

class ChatMessage(BaseModel):
    message: str
    user_id: str | None = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    response_time_ms: int

@app.get("/", response_class=HTMLResponse)
async def chat_interface():
    """Modern ChatGPT-style interface for Plywood Studio"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏗️ Plywood Studio AI Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: #f7f7f8;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .chat-header h1 {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .chat-header p {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .business-badge {
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            margin-top: 10px;
            font-size: 12px;
            display: inline-block;
        }
        
        .chat-container {
            flex: 1;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
            display: flex;
            flex-direction: column;
            height: calc(100vh - 80px);
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .message-wrapper {
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }
        
        .message-wrapper.user {
            flex-direction: row-reverse;
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            flex-shrink: 0;
        }
        
        .bot-avatar {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .user-avatar {
            background: linear-gradient(135deg, #10a37f 0%, #1a7f64 100%);
            color: white;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            font-size: 15px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        
        .bot-message {
            background: white;
            border: 1px solid #e1e8ed;
            color: #374151;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .user-message {
            background: #10a37f;
            color: white;
        }
        
        .message-time {
            font-size: 11px;
            opacity: 0.6;
            margin-top: 4px;
        }
        
        .welcome-section {
            text-align: center;
            padding: 40px 20px;
            background: white;
            border-radius: 12px;
            margin: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .welcome-title {
            font-size: 24px;
            font-weight: 600;
            color: #374151;
            margin-bottom: 12px;
        }
        
        .welcome-subtitle {
            color: #6b7280;
            margin-bottom: 24px;
        }
        
        .suggestions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin-top: 24px;
        }
        
        .suggestion-card {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: left;
        }
        
        .suggestion-card:hover {
            background: #f3f4f6;
            border-color: #10a37f;
            transform: translateY(-1px);
        }
        
        .suggestion-icon {
            font-size: 20px;
            margin-bottom: 8px;
        }
        
        .suggestion-title {
            font-weight: 600;
            color: #374151;
            margin-bottom: 4px;
            font-size: 14px;
        }
        
        .suggestion-desc {
            color: #6b7280;
            font-size: 12px;
        }
        
        .chat-input-section {
            padding: 20px;
            background: white;
            border-top: 1px solid #e5e7eb;
        }
        
        .input-wrapper {
            max-width: 800px;
            margin: 0 auto;
            position: relative;
        }
        
        .input-container {
            display: flex;
            align-items: flex-end;
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 24px;
            padding: 12px;
            transition: border-color 0.2s ease;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        
        .input-container:focus-within {
            border-color: #10a37f;
        }
        
        .chat-input {
            flex: 1;
            border: none;
            outline: none;
            padding: 8px 12px;
            font-size: 16px;
            resize: none;
            max-height: 120px;
            min-height: 24px;
            font-family: inherit;
        }
        
        .send-button {
            width: 40px;
            height: 40px;
            border: none;
            background: #10a37f;
            color: white;
            border-radius: 50%;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            margin-left: 8px;
        }
        
        .send-button:hover:not(:disabled) {
            background: #0f8c6c;
            transform: scale(1.05);
        }
        
        .send-button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .typing-indicator {
            display: none;
            padding: 20px;
            text-align: center;
        }
        
        .typing-dots {
            display: inline-flex;
            gap: 4px;
        }
        
        .typing-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10a37f;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes typing {
            0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
            40% { transform: scale(1); opacity: 1; }
        }
        
        @media (max-width: 768px) {
            .chat-messages {
                padding: 16px;
            }
            
            .message-content {
                max-width: 85%;
            }
            
            .suggestions {
                grid-template-columns: 1fr;
            }
            
            .chat-input-section {
                padding: 16px;
            }
        }
        
        /* Scrollbar styling */
        .chat-messages::-webkit-scrollbar {
            width: 6px;
        }
        
        .chat-messages::-webkit-scrollbar-track {
            background: transparent;
        }
        
        .chat-messages::-webkit-scrollbar-thumb {
            background: #d1d5db;
            border-radius: 3px;
        }
        
        .chat-messages::-webkit-scrollbar-thumb:hover {
            background: #9ca3af;
        }
    </style>
</head>
<body>
    <div class="chat-header">
        <h1>🏗️ Plywood Studio AI Assistant</h1>
        <p>Premium plywood, doors and laminate solutions in Hyderabad since 2022</p>
        <div class="business-badge">
            📍 Goshamahal, Hyderabad • ⭐ 5.0 Rating • 🏷️ Centuryply, Sainik, Greenply
        </div>
    </div>
    
    <div class="chat-container">
        <div class="chat-messages" id="chatMessages">
            <div class="welcome-section" id="welcomeSection">
                <div class="welcome-title">👋 Welcome to Plywood Studio!</div>
                <div class="welcome-subtitle">
                    I'm your AI assistant for all plywood, door, and laminate needs. How can I help you today?
                </div>
                
                <div class="suggestions">
                    <div class="suggestion-card" onclick="askQuestion('What plywood brands do you carry?')">
                        <div class="suggestion-icon">🏷️</div>
                        <div class="suggestion-title">Our Brands</div>
                        <div class="suggestion-desc">Centuryply, Sainik, Greenply</div>
                    </div>
                    <div class="suggestion-card" onclick="askQuestion('What types of doors are available?')">
                        <div class="suggestion-icon">🚪</div>
                        <div class="suggestion-title">Door Options</div>
                        <div class="suggestion-desc">Flush, Panel, Laminate doors</div>
                    </div>
                    <div class="suggestion-card" onclick="askQuestion('Where is Plywood Studio located?')">
                        <div class="suggestion-icon">📍</div>
                        <div class="suggestion-title">Location & Contact</div>
                        <div class="suggestion-desc">Goshamahal, Hyderabad</div>
                    </div>
                    <div class="suggestion-card" onclick="askQuestion('Do you have laminate sheets?')">
                        <div class="suggestion-icon">📄</div>
                        <div class="suggestion-title">Laminate Sheets</div>
                        <div class="suggestion-desc">Various thicknesses & finishes</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            <div class="typing-dots">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
            <span style="margin-left: 8px; color: #6b7280;">AI is thinking...</span>
        </div>
        
        <div class="chat-input-section">
            <div class="input-wrapper">
                <div class="input-container">
                    <textarea 
                        id="chatInput" 
                        class="chat-input" 
                        placeholder="Ask about plywood, doors, laminate sheets, or our services..."
                        rows="1"
                        onkeydown="handleKeyPress(event)"
                        oninput="adjustTextareaHeight()"
                    ></textarea>
                    <button class="send-button" onclick="sendMessage()" id="sendButton">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z"/>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let messageCount = 0;
        
        function adjustTextareaHeight() {
            const textarea = document.getElementById('chatInput');
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }
        
        function addMessage(content, isUser = false) {
            const messagesDiv = document.getElementById('chatMessages');
            const welcomeSection = document.getElementById('welcomeSection');
            
            // Hide welcome section after first message
            if (welcomeSection && messageCount === 0) {
                welcomeSection.style.display = 'none';
            }
            
            const messageWrapper = document.createElement('div');
            messageWrapper.className = `message-wrapper ${isUser ? 'user' : 'bot'}`;
            
            const now = new Date();
            const timeStr = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            messageWrapper.innerHTML = `
                <div class="message-avatar ${isUser ? 'user-avatar' : 'bot-avatar'}">
                    ${isUser ? '👤' : '🤖'}
                </div>
                <div class="message-content ${isUser ? 'user-message' : 'bot-message'}">
                    ${content}
                    <div class="message-time">${timeStr}</div>
                </div>
            `;
            
            messagesDiv.appendChild(messageWrapper);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            messageCount++;
        }
        
        function showTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'block';
            const messagesDiv = document.getElementById('chatMessages');
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function hideTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'none';
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const sendButton = document.getElementById('sendButton');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            
            // Clear input and disable button
            input.value = '';
            adjustTextareaHeight();
            sendButton.disabled = true;
            
            // Show typing indicator
            showTypingIndicator();
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        user_id: 'web-user'
                    })
                });
                
                const data = await response.json();
                
                // Hide typing indicator and add bot response
                hideTypingIndicator();
                addMessage(data.response);
                
            } catch (error) {
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error. Please try again.');
                console.error('Error:', error);
            } finally {
                sendButton.disabled = false;
                input.focus();
            }
        }
        
        function askQuestion(question) {
            const input = document.getElementById('chatInput');
            input.value = question;
            sendMessage();
        }
        
        // Focus input on load
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('chatInput').focus();
        });
    </script>
</body>
</html>
"""

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(message: ChatMessage):
    """Enhanced chat endpoint with plywood business focus"""
    start_time = time.time()
    
    try:
        # Check cache first
        cache_key = f"plywood_query:{hash(message.message)}"
        cached_response = cache_get(cache_key)
        
        if cached_response:
            logging.info(f"Cache hit for question: {message.message}")
            processing_time = int((time.time() - start_time) * 1000)
            return ChatResponse(
                response=cached_response,
                timestamp=datetime.now().isoformat(),
                response_time_ms=processing_time
            )
        
        # Build specialized prompt for plywood business
        context = get_relevant_context(message.message)
        prompt_template = """You are an expert assistant for Plywood Studio in Hyderabad. Use the following information to answer the customer's question accurately and helpfully.

PLYWOOD STUDIO INFORMATION:
{context}

CUSTOMER QUESTION: {query}

Please provide a helpful, accurate response focusing on our plywood products, doors, laminate sheets, and services. Be professional and informative."""

        prompt = prompt_template.format(
            context=context,
            query=message.message
        )
        
        # Get LLM response
        llm_start = time.time()
        raw_response = llm_call("gpt-3.5-turbo", prompt)
        llm_time = int((time.time() - llm_start) * 1000)
        logging.info(f"LLM latency: {llm_time}ms")
        
        # Apply safety checks
        safe_response = apply_guardrails(raw_response)
        final_response = secure_output(safe_response)
        
        # Cache the response
        cache_set(cache_key, final_response, CACHE_TTL_SECONDS)
        logging.info(f"Cached answer for question: {message.message}")
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            response=final_response,
            timestamp=datetime.now().isoformat(),
            response_time_ms=processing_time
        )
        
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        processing_time = int((time.time() - start_time) * 1000)
        return ChatResponse(
            response="I apologize, but I'm experiencing some technical difficulties. Please try asking your question again.",
            timestamp=datetime.now().isoformat(),
            response_time_ms=processing_time
        )

def get_relevant_context(query: str) -> str:
    """Get relevant business information based on the query"""
    query_lower = query.lower()
    relevant_context = []
    
    # Business info
    if any(word in query_lower for word in ['business', 'company', 'location', 'address', 'contact', 'about']):
        relevant_context.append("Plywood Studio is a partnership firm established in 2022, located at 5-5-983, 5-5-982/1, Goshamahal, Hyderabad-500012, Telangana. We are GST registered (36ABCFP0708R1ZW) with 5-25 Cr annual turnover and up to 10 employees. We have a 5.0 star rating on IndiaMART.")
    
    # Products
    if any(word in query_lower for word in ['plywood', 'brand', 'product', 'wood']):
        relevant_context.append("We are authorized dealers for premium plywood brands: Centuryply (Club Prime, Bond 710), Sainik MR Plywood, and Greenply. We offer various grades and specifications for different applications.")
    
    # Doors
    if any(word in query_lower for word in ['door', 'doors', 'flush', 'panel']):
        relevant_context.append("Our wooden door range includes: Greenply Plywood Flush Doors, Wooden Panel Polish Doors, and Plywood Laminate Doors. Available in standard and custom sizes.")
    
    # Laminate
    if any(word in query_lower for word in ['laminate', 'sheet', 'sunmica']):
        relevant_context.append("We supply laminate sheets in various thicknesses including 1mm and 1.5mm options, with different finishes and colors for interior decoration.")
    
    # Hardware
    if any(word in query_lower for word in ['hardware', 'lock', 'locks']):
        relevant_context.append("We offer door hardware including Quba Vault Main Door Rim Locks and other quality door accessories.")
    
    # Default context if nothing specific
    if not relevant_context:
        relevant_context = [
            "Plywood Studio specializes in premium plywood, wooden doors, laminate sheets, and door hardware. We carry trusted brands like Centuryply, Sainik, and Greenply.",
            "Located in Goshamahal, Hyderabad since 2022. Contact us via IndiaMART for quotes and availability."
        ]
    
    return "\n\n".join(relevant_context)

@app.get("/api/business-info")
async def get_business_info():
    """Get Plywood Studio business information"""
    return {
        "company": "Plywood Studio",
        "location": "Goshamahal, Hyderabad-500012, Telangana",
        "established": "2022",
        "brands": ["Centuryply", "Sainik", "Greenply"],
        "products": ["Wooden Plywood", "Wooden Doors", "Laminate Sheets", "Door Hardware"],
        "rating": "5.0 stars on IndiaMART",
        "contact": "Available via IndiaMART platform"
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