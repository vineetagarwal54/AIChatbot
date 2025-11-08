"""
Intelligent Knowledge Base - Detailed product information for Plywood Studio
"""

# Comprehensive product knowledge
PLYWOOD_KNOWLEDGE = {
    "marine_plywood": {
        "description": "Marine plywood is the highest grade of plywood, made with waterproof adhesive (BWP - Boiling Water Proof). It's designed to withstand moisture, humidity, and wet conditions.",
        "features": [
            "BWP (Boiling Water Proof) grade adhesive",
            "No voids or gaps in the core layers",
            "High resistance to moisture and humidity",
            "Termite and borer resistant",
            "Durable construction, longer lifespan",
            "Smooth, uniform surface"
        ],
        "applications": "Outdoor furniture, boat building, kitchen cabinets, bathrooms, coastal areas",
        "brands_we_carry": "Sainik MR Plywood, Centuryply Marine Grade",
        "difference_from_regular": "Marine plywood uses BWP glue vs MR (Moisture Resistant) or commercial grade glue in regular plywood. It has no core gaps and is made with better quality veneers."
    },
    
    "commercial_plywood": {
        "description": "Commercial plywood is the most economical grade, suitable for interior applications where moisture exposure is minimal.",
        "features": [
            "Made with urea formaldehyde adhesive",
            "Cost-effective option",
            "Good for dry indoor use",
            "Various thickness options (4mm to 25mm)"
        ],
        "applications": "Indoor furniture, partitions, false ceilings, interior paneling",
        "brands_we_carry": "Centuryply, Greenply commercial grades"
    },
    
    "mr_plywood": {
        "description": "MR (Moisture Resistant) Plywood is made with phenolic adhesive, offering better moisture resistance than commercial plywood.",
        "features": [
            "Phenolic resin adhesive",
            "Moderate moisture resistance",
            "Good strength and durability",
            "Affordable for most applications"
        ],
        "applications": "Home furniture, bedroom furniture, living room furniture, interior applications",
        "brands_we_carry": "Sainik MR Plywood, Centuryply Bond 710"
    },
    
    "bwp_plywood": {
        "description": "BWP (Boiling Water Proof) Plywood uses phenol formaldehyde adhesive for maximum water resistance.",
        "features": [
            "Phenol formaldehyde adhesive",
            "Excellent water resistance",
            "Can withstand boiling water test",
            "Premium quality veneers"
        ],
        "applications": "Kitchens, bathrooms, outdoor furniture, high moisture areas",
        "brands_we_carry": "Centuryply Club Prime, Premium marine grade plywood"
    }
}

BRAND_KNOWLEDGE = {
    "centuryply": {
        "description": "Centuryply is one of India's most trusted and largest plywood brands, known for innovation and quality.",
        "history": "Established in 1986, Centuryply pioneered the concept of branded plywood in India.",
        "products_we_carry": {
            "Club Prime": "Premium BWP grade plywood with ViroKill technology (anti-viral and anti-bacterial)",
            "Bond 710": "MR grade plywood with excellent bonding strength, 7-layer construction for 10mm thickness",
            "Sainik 710": "BWP grade with enhanced moisture resistance"
        },
        "unique_features": "ViroKill technology, 6X Nail Holding Strength, Borer & Termite Proof, Zero Emission",
        "warranty": "Varies by product - typically 5-25 years"
    },
    
    "sainik": {
        "description": "Sainik is a premium plywood brand known for marine-grade quality and durability.",
        "specialty": "Specializes in MR and BWP grade plywood with excellent moisture resistance",
        "products_we_carry": {
            "Sainik MR Plywood": "Moisture resistant grade suitable for all indoor applications",
            "Sainik BWP": "Boiling water proof grade for high moisture areas"
        },
        "unique_features": "7-ply construction for 6mm, no core gaps, uniform thickness, smooth surface",
        "warranty": "Long-term warranty against manufacturing defects"
    },
    
    "greenply": {
        "description": "Greenply is another leading plywood brand in India, known for eco-friendly products.",
        "specialty": "Focus on environmental sustainability and green products",
        "products_we_carry": {
            "Greenply Plywood": "Various grades including MR and BWP",
            "Greenply Flush Doors": "Engineered wooden doors with plywood facing",
            "Greenply Laminates": "Decorative laminates for surfaces"
        },
        "unique_features": "E0 grade (low emission), termite resistant, borer proof",
        "warranty": "Product-specific warranties available"
    }
}

DOOR_KNOWLEDGE = {
    "flush_doors": {
        "description": "Flush doors have a smooth, flat surface made with plywood sheets on a wooden frame.",
        "construction": "Solid wood frame with plywood facing on both sides, hollow or solid core",
        "advantages": "Smooth finish, easy to paint, cost-effective, lightweight (hollow core)",
        "applications": "Interior doors, bedroom doors, bathroom doors",
        "sizes": "Standard: 7ft x 3ft, 7ft x 3.5ft, 8ft x 3ft, 8ft x 4ft (custom sizes available)",
        "brands_we_carry": "Greenply Flush Doors"
    },
    
    "panel_doors": {
        "description": "Panel doors have raised or recessed panels set within a frame, offering traditional aesthetic.",
        "construction": "Solid wood frame with decorative panels",
        "advantages": "Traditional look, elegant design, durable, various panel configurations",
        "applications": "Main doors, bedroom doors, study room doors",
        "finishes_available": "Natural wood, polish finish, painted"
    },
    
    "laminate_doors": {
        "description": "Doors with decorative laminate finish on plywood base.",
        "advantages": "Attractive finish, scratch resistant, easy to maintain, variety of designs",
        "applications": "Modern interiors, commercial spaces, contemporary homes",
        "finishes_available": "Wood grain, solid colors, textured finishes"
    }
}

LAMINATE_KNOWLEDGE = {
    "description": "Decorative laminates are thin sheets bonded to plywood or particleboard for aesthetic appeal.",
    "types": {
        "Sunmica": "Popular brand name, various thicknesses (0.8mm, 1mm, 1.5mm)",
        "Wood grain": "Natural wood patterns",
        "Solid colors": "Plain colors - white, black, cream, etc.",
        "Textured": "Matt, glossy, or textured finishes"
    },
    "applications": "Furniture surfaces, kitchen cabinets, wardrobes, tables, wall paneling",
    "thickness_options": "0.8mm, 1mm, 1.5mm (thicker for horizontal surfaces)",
    "brands_we_carry": "Various brands including Greenply laminates"
}

TECHNICAL_SPECS = {
    "plywood_thickness": {
        "common_sizes": ["4mm", "6mm", "9mm", "12mm", "15mm", "18mm", "25mm"],
        "applications": {
            "4mm": "Backing panels, false ceilings",
            "6mm": "Cabinet backs, drawer bottoms",
            "9mm": "Furniture shutters, partitions",
            "12mm": "Standard furniture, shelves",
            "15mm-18mm": "Heavy duty furniture, countertops",
            "25mm": "Industrial applications, heavy load bearing"
        }
    },
    
    "plywood_grades": {
        "BWP": "Boiling Water Proof - Highest grade, phenol formaldehyde glue",
        "BWR": "Boiling Water Resistant - Phenolic glue, good moisture resistance",
        "MR": "Moisture Resistant - Urea formaldehyde modified, indoor use",
        "Commercial": "Interior grade, minimal moisture resistance"
    }
}

def get_knowledge(topic: str) -> str:
    """Get knowledge about a specific topic"""
    topic_lower = topic.lower()
    
    # Plywood types
    if "marine" in topic_lower:
        info = PLYWOOD_KNOWLEDGE["marine_plywood"]
        return _format_plywood_info("Marine Plywood", info)
    elif "mr plywood" in topic_lower or "moisture resistant" in topic_lower:
        info = PLYWOOD_KNOWLEDGE["mr_plywood"]
        return _format_plywood_info("MR (Moisture Resistant) Plywood", info)
    elif "bwp" in topic_lower or "boiling water" in topic_lower:
        info = PLYWOOD_KNOWLEDGE["bwp_plywood"]
        return _format_plywood_info("BWP (Boiling Water Proof) Plywood", info)
    elif "commercial" in topic_lower:
        info = PLYWOOD_KNOWLEDGE["commercial_plywood"]
        return _format_plywood_info("Commercial Plywood", info)
    
    # Brands
    if "centuryply" in topic_lower or "century ply" in topic_lower:
        return _format_brand_info("Centuryply", BRAND_KNOWLEDGE["centuryply"])
    elif "sainik" in topic_lower:
        return _format_brand_info("Sainik", BRAND_KNOWLEDGE["sainik"])
    elif "greenply" in topic_lower:
        return _format_brand_info("Greenply", BRAND_KNOWLEDGE["greenply"])
    
    # Doors
    if "flush door" in topic_lower:
        return _format_door_info("Flush Doors", DOOR_KNOWLEDGE["flush_doors"])
    elif "panel door" in topic_lower:
        return _format_door_info("Panel Doors", DOOR_KNOWLEDGE["panel_doors"])
    elif "laminate door" in topic_lower:
        return _format_door_info("Laminate Doors", DOOR_KNOWLEDGE["laminate_doors"])
    
    return None

def _format_plywood_info(name: str, info: dict) -> str:
    """Format plywood information"""
    output = f"**{name}**\n\n"
    output += f"{info['description']}\n\n"
    
    if "features" in info and info["features"]:
        output += "**Key Features:**\n"
        for feature in info["features"]:
            output += f"• {feature}\n"
        output += "\n"
    
    if "applications" in info:
        output += f"**Applications:** {info['applications']}\n\n"
    
    if "brands_we_carry" in info:
        output += f"**Available at Plywood Studio:** {info['brands_we_carry']}\n\n"
    
    if "difference_from_regular" in info:
        output += f"**Difference from Regular Plywood:** {info['difference_from_regular']}\n\n"
    
    output += "💡 For specific specifications, current stock, and pricing, contact us via IndiaMART or visit our Goshamahal, Hyderabad showroom."
    
    return output

def _format_brand_info(name: str, info: dict) -> str:
    """Format brand information"""
    output = f"**{name}**\n\n"
    output += f"{info['description']}\n\n"
    
    if "history" in info:
        output += f"**History:** {info['history']}\n\n"
    
    if "products_we_carry" in info:
        output += "**Products We Carry:**\n"
        for product, desc in info["products_we_carry"].items():
            output += f"• **{product}**: {desc}\n"
        output += "\n"
    
    if "unique_features" in info:
        output += f"**Unique Features:** {info['unique_features']}\n\n"
    
    output += "💡 Contact us via IndiaMART (www.indiamart.com/plywoodstudio) for current availability and pricing."
    
    return output

def _format_door_info(name: str, info: dict) -> str:
    """Format door information"""
    output = f"**{name}**\n\n"
    output += f"{info['description']}\n\n"
    
    if "construction" in info:
        output += f"**Construction:** {info['construction']}\n\n"
    
    if "advantages" in info:
        output += f"**Advantages:** {info['advantages']}\n\n"
    
    if "sizes" in info:
        output += f"**Sizes:** {info['sizes']}\n\n"
    
    if "brands_we_carry" in info:
        output += f"**Brands:** {info['brands_we_carry']}\n\n"
    
    output += "💡 Visit our Goshamahal showroom or contact via IndiaMART for more details."
    
    return output
