# 🏗️ Plywood Studio AI Chatbot

A modern AI-powered chatbot for Plywood Studio - your premium plywood, doors, and laminate solution provider in Hyderabad.

## � Live Demo

![Plywood Studio Chatbot Interface](chatbot-interface.png)

*Modern ChatGPT-style interface with real-time responses and business-specific knowledge*

## �🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis server

### Installation
```bash
# 1. Clone and setup
git clone https://github.com/vineetagarwal54/AIChatbot.git
cd AIChatbot
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start Redis (using Docker)
docker run -d --name redis-chatbot -p 6379:6379 redis:latest

# 4. Configure environment (optional)
copy .env.template .env
# Edit .env with your API keys if needed

# 5. Start the chatbot
python business_chatbot.py
```

Visit **http://localhost:8001** to use the chatbot!

## 🏢 About Plywood Studio

**Location:** Goshamahal, Hyderabad-500012, Telangana  
**Established:** 2022  
**Rating:** ⭐ 5.0 stars on IndiaMART  
**GST:** 36ABCFP0708R1ZW  

### Our Products
- **�️ Premium Plywood:** Centuryply, Sainik, Greenply
- **🚪 Wooden Doors:** Flush doors, Panel doors, Laminate doors  
- **📄 Laminate Sheets:** Various thicknesses and finishes
- **🔒 Door Hardware:** Quality locks and accessories

## 🤖 Features

- **Instant Responses:** AI-powered customer support 24/7
- **Business Knowledge:** Specialized information about our products
- **Modern Interface:** ChatGPT-style user experience
- **Hybrid Intelligence:** Works with or without internet APIs
- **Mobile Friendly:** Responsive design for all devices

## 📁 Key Files

- `business_chatbot.py` - Main web application
- `cli_interface.py` - Command-line interface
- `business_config.py` - Business information and customization
- `llm_client_hybrid.py` - AI response system
- `cache_store.py` - Redis caching for fast responses

## � Try These Questions

- "What plywood brands do you carry?"
- "Where is Plywood Studio located?"
- "Do you have flush doors available?"
- "What are your laminate sheet options?"
- "How can I contact you?"

## �️ Technical Stack

- **Backend:** FastAPI (Python)
- **AI:** Hugging Face + OpenAI APIs (with fallback system)
- **Caching:** Redis
- **Frontend:** Modern HTML/CSS/JavaScript
- **Deployment:** Self-hosted with Docker support

## 📞 Contact

Visit us in Hyderabad or contact through IndiaMART for product inquiries and quotes.

---

*Built for Plywood Studio - Premium plywood solutions since 2022* 🏗️