# Business Configuration - Customize this for your business
"""
BUSINESS CONFIGURATION
Edit this file to customize the chatbot for your specific business needs
"""

# Company Information
COMPANY_NAME = "Plywood Studio"
COMPANY_TAGLINE = "Premium plywood, doors and laminate solutions since 2022"
BUSINESS_TYPE = "plywood"  # Change this to your business type

# Contact Information
BUSINESS_PHONE = "+91 (Available on IndiaMART)"
BUSINESS_EMAIL = "Contact via IndiaMART platform"
BUSINESS_ADDRESS = "5-5-983, 5-5-982/1, Goshamahal, Hyderabad-500012, Telangana, India"
BUSINESS_WEBSITE = "www.indiamart.com/plywoodstudio"

# Business Hours
BUSINESS_HOURS = {
    "monday": "8:00 AM - 6:00 PM",
    "tuesday": "8:00 AM - 6:00 PM", 
    "wednesday": "8:00 AM - 6:00 PM",
    "thursday": "8:00 AM - 6:00 PM",
    "friday": "8:00 AM - 6:00 PM",
    "saturday": "9:00 AM - 4:00 PM",
    "sunday": "Closed"
}

# Product Categories (customize for your business)
PRODUCT_CATEGORIES = {
    "wooden_plywood": {
        "name": "Wooden Plywood",
        "description": "High-quality wooden plywood for construction and furniture",
        "examples": ["Centuryply Club Prime Plywood", "Centuryply Bond 710 Plywood", "Sainik MR Plywood", "Greenply Plywood"]
    },
    "wooden_doors": {
        "name": "Wooden Doors", 
        "description": "Premium wooden doors and flush doors for residential and commercial use",
        "examples": ["Greenply Plywood Flush Door", "Wooden Panel Polish Door", "Plywood Laminate Door"]
    },
    "laminate_sheets": {
        "name": "Laminate Sheets",
        "description": "Decorative laminate sheets for interior applications",
        "examples": ["Wooden Laminated Sheets", "1.5mm Sunmica Laminated Sheet", "1mm Brown Laminated Sheet"]
    },
    "door_hardware": {
        "name": "Door Hardware",
        "description": "Quality locks and hardware for doors",
        "examples": ["Quba Vault Main Door Rim Lock", "Security Locks", "Door Accessories"]
    }
}

# Services Offered
SERVICES = [
    "Wholesale trading of plywood and doors",
    "Wide range of branded plywood (Centuryply, Sainik, Greenply)", 
    "Custom door solutions",
    "Laminate sheet supply",
    "Door hardware and locks",
    "Quality assurance and certification",
    "GST compliant billing",
    "IndiaMART verified supplier"
]

# Pricing Information (customize as needed)
PRICING_NOTES = {
    "bulk_discounts": "Volume discounts available for orders over 10 sheets",
    "contractor_pricing": "Special rates for contractors and builders",
    "delivery_fee": "Free delivery on orders over $500 within 50 miles",
    "payment_terms": "Net 30 terms available for approved accounts"
}

# Business Specialties 
SPECIALTIES = [
    "Authorized dealer for premium brands (Centuryply, Sainik, Greenply)",
    "Wide variety of plywood grades and thicknesses",
    "Quality wooden doors and flush doors",
    "Decorative laminate sheets",
    "Established since 2022 in Hyderabad",
    "Partnership firm with 5-25 Cr annual turnover",
    "GST registered and IndiaMART verified",
    "Expert knowledge of wood products"
]

# Chatbot Personality
CHATBOT_PERSONALITY = {
    "tone": "professional and helpful",
    "expertise_level": "expert knowledge of products and applications",
    "response_style": "clear, informative, and business-focused"
}

# Color Scheme (for web interface)
BRAND_COLORS = {
    "primary": "#8B4513",      # Brown - change to your brand color
    "secondary": "#D2B48C",    # Light brown
    "accent": "#A0522D",       # Darker brown
    "text": "#333333",         # Dark gray
    "background": "#f8f9fa"    # Light gray
}

# Quick Response Templates
QUICK_RESPONSES = {
    "greeting": f"Welcome to {COMPANY_NAME}! I'm your AI assistant for premium plywood, doors, and laminate solutions in Hyderabad.",
    "contact": f"You can reach us through IndiaMART at {BUSINESS_WEBSITE}. We're located at {BUSINESS_ADDRESS}.",
    "hours": "We're a wholesale trading business. Please contact us via IndiaMART for current availability and pricing.",
    "services": f"We offer: {', '.join(SERVICES)}",
    "specialties": f"Our specialties include: {', '.join(SPECIALTIES)}"
}

# Knowledge Base Categories (customize with your product knowledge)
KNOWLEDGE_BASE = {
    "products": {
        "categories": list(PRODUCT_CATEGORIES.keys()),
        "description": "Information about our product lines and specifications"
    },
    "pricing": {
        "categories": ["retail", "bulk", "contractor"],
        "description": "Pricing information and discount structures"
    },
    "services": {
        "categories": ["cutting", "delivery", "consultation"],
        "description": "Services we provide to customers"
    },
    "technical": {
        "categories": ["specifications", "applications", "installation"],
        "description": "Technical information and guidance"
    }
}

# Export for use in other modules
def get_business_config():
    """Return complete business configuration"""
    return {
        "company": {
            "name": COMPANY_NAME,
            "tagline": COMPANY_TAGLINE,
            "type": BUSINESS_TYPE,
            "phone": BUSINESS_PHONE,
            "email": BUSINESS_EMAIL,
            "address": BUSINESS_ADDRESS,
            "website": BUSINESS_WEBSITE,
            "hours": BUSINESS_HOURS
        },
        "products": PRODUCT_CATEGORIES,
        "services": SERVICES,
        "pricing": PRICING_NOTES,
        "specialties": SPECIALTIES,
        "chatbot": CHATBOT_PERSONALITY,
        "branding": BRAND_COLORS,
        "responses": QUICK_RESPONSES,
        "knowledge": KNOWLEDGE_BASE
    }

if __name__ == "__main__":
    print("Business Configuration Loaded")
    print(f"Company: {COMPANY_NAME}")
    print(f"Business Type: {BUSINESS_TYPE}")
    print(f"Contact: {BUSINESS_PHONE}")
    print(f"Services: {len(SERVICES)} services configured")
    print(f"Product Categories: {len(PRODUCT_CATEGORIES)} categories")