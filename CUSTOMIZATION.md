# 🔧 Business Customization Guide

## Quick Start: Customize for Your Business

This chatbot is designed to be easily customized for any business. Follow this guide to make it yours!

## 📝 **Step 1: Basic Business Information**

Edit `business_config.py` and update these fields:

```python
# Company Information
COMPANY_NAME = "Acme Plywood & Lumber"  # ← Your business name
COMPANY_TAGLINE = "Premium wood products for contractors and DIY enthusiasts"
BUSINESS_TYPE = "lumber"  # Options: retail, manufacturing, services, etc.

# Contact Information  
BUSINESS_PHONE = "+1 (555) 987-6543"
BUSINESS_EMAIL = "sales@acmeplywood.com"
BUSINESS_ADDRESS = "123 Industrial Ave, Woodville, TX 75123"
BUSINESS_WEBSITE = "www.acmeplywood.com"
```

## 🏪 **Step 2: Product Categories**

Define your main product lines:

```python
PRODUCT_CATEGORIES = {
    "premium": {
        "name": "Premium Plywood",
        "description": "High-grade plywood for furniture and cabinets",
        "examples": ["Grade A Birch", "Grade A Oak", "Marine Grade"]
    },
    "construction": {
        "name": "Construction Grade", 
        "description": "Structural plywood for building projects",
        "examples": ["OSB Sheathing", "CDX Plywood", "Pressure Treated"]
    },
    "specialty": {
        "name": "Specialty Products",
        "description": "Unique products for specific applications", 
        "examples": ["Fire Retardant", "Flexible Plywood", "UV Resistant"]
    }
}
```

## 🛠️ **Step 3: Services Offered**

List what your business provides:

```python
SERVICES = [
    "Custom cutting and sizing",
    "Delivery within 50-mile radius",
    "Expert product consultation", 
    "Bulk ordering and storage",
    "Contractor account management",
    "Technical specifications support",
    "Project planning assistance"
]
```

## 💰 **Step 4: Pricing Strategy**

Configure pricing information:

```python
PRICING_NOTES = {
    "bulk_discounts": "10+ sheets: 5% off, 25+ sheets: 10% off, 50+ sheets: 15% off",
    "contractor_pricing": "Special wholesale rates for licensed contractors",
    "delivery_fee": "Free delivery on orders over $500, $75 fee for smaller orders",
    "payment_terms": "Net 30 terms available for approved business accounts"
}
```

## 🎨 **Step 5: Brand Colors**

Match your brand identity:

```python
BRAND_COLORS = {
    "primary": "#2E7D32",      # Forest Green
    "secondary": "#8BC34A",    # Light Green  
    "accent": "#FF9800",       # Orange
    "text": "#263238",         # Dark Blue-Gray
    "background": "#F1F8E9"    # Very Light Green
}
```

## 🤖 **Step 6: Chatbot Knowledge Base**

In `llm_client_hybrid.py`, update the knowledge base with your specific information:

### **Product Knowledge Example:**
```python
"products": [
    "We specialize in premium hardwood plywood including Birch, Oak, and Maple varieties. Our Grade A products feature smooth, defect-free surfaces perfect for furniture making.",
    "Construction grade options include OSB sheathing, CDX plywood, and pressure-treated materials suitable for structural applications.",
    "Marine grade plywood uses waterproof adhesives and void-free construction, ideal for boat building and high-moisture environments."
]
```

### **Pricing Information:**
```python
"pricing": [
    "Our Grade A Birch plywood starts at $89.99 per 4'x8' sheet in 18mm thickness. Volume discounts begin at 10 sheets.",
    "Construction grade OSB is available from $45.99 per sheet. Contractor pricing available with approved accounts.",
    "Custom cutting services are $2.50 per linear foot. Free cutting on orders over $200."
]
```

### **Service Details:**
```python
"services": [
    "We offer free delivery within 50 miles on orders over $500. Same-day delivery available for in-stock items.",
    "Our expert staff provides technical consultation for project planning and material selection.",
    "Contractor accounts include NET-30 terms, special pricing, and dedicated account management."
]
```

## 📞 **Step 7: Contact Integration**

Update contact responses:

```python
QUICK_RESPONSES = {
    "contact": f"Reach us at {BUSINESS_PHONE} or visit our showroom at {BUSINESS_ADDRESS}. Online orders at {BUSINESS_WEBSITE}.",
    "hours": "We're open Monday-Friday 7AM-6PM, Saturday 8AM-5PM. Closed Sundays.",
    "emergency": "For urgent contractor needs, call our emergency line at +1 (555) 987-WOOD."
}
```

## 🌐 **Step 8: Web Interface Customization**

In `business_chatbot.py`, update the HTML interface:

### **Company Header:**
```html
<div class="chat-header">
    <h1>🏗️ Acme Plywood & Lumber AI Assistant</h1>
    <p>Expert guidance for all your wood product needs</p>
</div>
```

### **Business Info Bar:**
```html
<div class="business-info">
    <strong>📍 Location:</strong> 123 Industrial Ave, Woodville, TX • 
    <strong>📞 Phone:</strong> (555) 987-6543 • 
    <strong>🕒 Hours:</strong> Mon-Fri 7AM-6PM, Sat 8AM-5PM
</div>
```

### **Quick Questions:**
```html
<button class="quick-question" onclick="askQuestion('What plywood grades are available?')">🏷️ Available Grades</button>
<button class="quick-question" onclick="askQuestion('Do you offer contractor pricing?')">💰 Contractor Pricing</button>
<button class="quick-question" onclick="askQuestion('What delivery options do you have?')">🚛 Delivery Info</button>
```

## 🧪 **Step 9: Test Your Customization**

1. **Start the chatbot:** `python business_chatbot.py`
2. **Test common questions:**
   - "What products do you offer?"
   - "Do you have bulk pricing?"
   - "What are your business hours?"
   - "Can you deliver to [your area]?"

3. **Verify branding:** Check that colors, company name, and information are correct

## 📊 **Step 10: Advanced Customization**

### **Industry-Specific Terminology**
Update responses to use your industry's language and terminology.

### **Integration with Business Systems**
Consider adding:
- Inventory checking
- Order placement
- Account status lookup
- Appointment scheduling

### **Analytics Tracking**
Monitor which questions are asked most frequently to improve your knowledge base.

## 🎯 **Common Business Types & Adaptations**

### **Retail Business:**
- Focus on product availability, store hours, returns
- Add inventory checking features
- Include loyalty program information

### **Manufacturing:**
- Emphasize technical specifications, custom orders
- Include lead times and production capabilities
- Add quality certifications and standards

### **Service Business:**
- Highlight service offerings, scheduling, pricing
- Include service area coverage
- Add technician availability and expertise

## 💡 **Pro Tips**

1. **Keep it Updated:** Regularly update pricing and product information
2. **Monitor Performance:** Track response times and customer satisfaction
3. **Gather Feedback:** Ask customers about their chatbot experience
4. **Expand Knowledge:** Add new products and services as your business grows
5. **Train Staff:** Ensure your team knows about the chatbot capabilities

## 🚀 **Ready to Launch?**

Once you've customized everything:

1. **Test thoroughly** with real business scenarios
2. **Train your staff** on the chatbot features  
3. **Add the chatbot link** to your website
4. **Promote to customers** via email, social media
5. **Monitor and improve** based on usage patterns

Your AI business chatbot is now ready to serve customers 24/7! 🎉