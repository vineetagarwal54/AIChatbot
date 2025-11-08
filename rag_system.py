"""
LangChain RAG System for Plywood Studio
Uses vector embeddings and retrieval for intelligent product information
"""
import logging
from typing import List, Optional
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Updated import
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate  # Updated import
from langchain_core.documents import Document  # Fixed import
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import OPENAI_API_KEY, TEMPERATURE, MAX_TOKENS

# Initialize components
embeddings = None
vectorstore = None
qa_chain = None

def initialize_rag_system():
    """Initialize the RAG system with product knowledge"""
    global embeddings, vectorstore, qa_chain
    
    if not OPENAI_API_KEY:
        logging.warning("OpenAI API key not found. RAG system disabled.")
        return False
    
    try:
        # Initialize embeddings
        embeddings = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model="text-embedding-3-small"  # Cost-effective embedding model
        )
        
        # Load product knowledge
        documents = _load_product_documents()
        
        # Create vector store
        vectorstore = FAISS.from_documents(documents, embeddings)
        
        # Initialize LLM
        llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
        
        # Create retriever
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}  # Retrieve top 4 most relevant documents
        )
        
        # Create custom prompt using LCEL (LangChain Expression Language)
        prompt_template = """You are an expert assistant for Plywood Studio, a premium plywood, doors, and laminate supplier in Hyderabad, India.

BUSINESS CONTEXT:
- Company: Plywood Studio (established 2022)
- Location: Goshamahal, Hyderabad-500012, Telangana
- Products: Premium plywood, wooden doors, laminate sheets, door hardware
- Brands: Centuryply (Club Prime, Bond 710), Sainik MR Plywood, Greenply
- Contact: www.indiamart.com/plywoodstudio

Use the following product information to answer the customer's question accurately and helpfully:

{context}

CUSTOMER QUESTION: {question}

INSTRUCTIONS:
- Provide detailed, accurate, and helpful information
- If the context doesn't contain specific details, provide general guidance based on your knowledge
- Always mention how to contact us (IndiaMART or visit Goshamahal showroom) for pricing and availability
- Be professional yet friendly
- Focus on practical advice for customers

Your response:"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        # Create RAG chain using LCEL
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        qa_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        logging.info("✅ LangChain RAG system initialized successfully")
        return True
        
    except Exception as e:
        logging.error(f"Failed to initialize RAG system: {e}")
        return False

def _load_product_documents() -> List[Document]:
    """Load all product knowledge as LangChain documents"""
    from knowledge_base import (
        PLYWOOD_KNOWLEDGE, BRAND_KNOWLEDGE, DOOR_KNOWLEDGE, 
        LAMINATE_KNOWLEDGE, TECHNICAL_SPECS
    )
    
    documents = []
    
    # Add plywood knowledge
    for product_type, info in PLYWOOD_KNOWLEDGE.items():
        content = f"""Product: {product_type.replace('_', ' ').title()}

Description: {info['description']}

Features:
{chr(10).join('- ' + feature for feature in info.get('features', []))}

Applications: {info.get('applications', 'N/A')}

Brands Available: {info.get('brands_we_carry', 'Various brands')}

{info.get('difference_from_regular', '')}
"""
        documents.append(Document(
            page_content=content,
            metadata={"type": "plywood", "product": product_type}
        ))
    
    # Add brand knowledge
    for brand, info in BRAND_KNOWLEDGE.items():
        products_text = "\n".join(
            f"- {name}: {desc}" 
            for name, desc in info.get('products_we_carry', {}).items()
        )
        
        content = f"""Brand: {brand.title()}

Description: {info['description']}

History: {info.get('history', 'N/A')}

Products We Carry:
{products_text}

Unique Features: {info.get('unique_features', 'N/A')}

Warranty: {info.get('warranty', 'Available')}
"""
        documents.append(Document(
            page_content=content,
            metadata={"type": "brand", "brand": brand}
        ))
    
    # Add door knowledge
    for door_type, info in DOOR_KNOWLEDGE.items():
        content = f"""Product: {door_type.replace('_', ' ').title()}

Description: {info['description']}

Construction: {info.get('construction', 'N/A')}

Advantages: {info.get('advantages', 'N/A')}

Applications: {info.get('applications', 'N/A')}

Sizes Available: {info.get('sizes', 'Standard and custom sizes')}

Brands: {info.get('brands_we_carry', 'Various brands')}
"""
        documents.append(Document(
            page_content=content,
            metadata={"type": "door", "product": door_type}
        ))
    
    # Add laminate knowledge
    content = f"""Product: Decorative Laminates

{LAMINATE_KNOWLEDGE['description']}

Types Available:
{chr(10).join(f"- {name}: {desc}" for name, desc in LAMINATE_KNOWLEDGE['types'].items())}

Applications: {LAMINATE_KNOWLEDGE['applications']}

Thickness Options: {LAMINATE_KNOWLEDGE['thickness_options']}

Brands: {LAMINATE_KNOWLEDGE['brands_we_carry']}
"""
    documents.append(Document(
        page_content=content,
        metadata={"type": "laminate"}
    ))
    
    # Add technical specifications
    thickness_info = TECHNICAL_SPECS['plywood_thickness']
    apps_text = "\n".join(
        f"- {size}: {app}"
        for size, app in thickness_info['applications'].items()
    )
    
    content = f"""Technical Specifications: Plywood Thickness

Common Sizes: {', '.join(thickness_info['common_sizes'])}

Applications by Thickness:
{apps_text}

Plywood Grades:
{chr(10).join(f"- {grade}: {desc}" for grade, desc in TECHNICAL_SPECS['plywood_grades'].items())}
"""
    documents.append(Document(
        page_content=content,
        metadata={"type": "technical"}
    ))
    
    # Add business information
    business_doc = Document(
        page_content="""Plywood Studio - Business Information

Company: Plywood Studio
Type: Partnership Firm
Established: 2022
Location: 5-5-983, 5-5-982/1, Goshamahal, Hyderabad-500012, Telangana, India

Contact Information:
- Website: www.indiamart.com/plywoodstudio
- Platform: IndiaMART (5-star verified supplier)
- GST Number: 36ABCFP0708R1ZW

Business Details:
- Annual Turnover: 5-25 Cr
- Employees: Up to 10 people
- Business Type: Wholesale Trader
- Rating: 5.0 stars on IndiaMART

Specialties:
- Authorized dealer for premium brands (Centuryply, Sainik, Greenply)
- Wide variety of plywood grades and thicknesses
- Quality wooden doors (flush, panel, laminate)
- Decorative laminate sheets
- Expert knowledge of wood products
- GST registered and IndiaMART verified

How to Contact:
- Visit our showroom at Goshamahal, Hyderabad
- Contact through IndiaMART for quotes and availability
- Partner: Shubham Agarwal
""",
        metadata={"type": "business"}
    )
    documents.append(business_doc)
    
    logging.info(f"Loaded {len(documents)} product documents into RAG system")
    return documents

def query_rag(question: str, chat_history: Optional[List] = None) -> dict:
    """
    Query the RAG system with a question
    Returns: {"answer": str, "source_documents": List[Document]}
    """
    global qa_chain
    
    if not qa_chain:
        # Try to initialize
        if not initialize_rag_system():
            return {
                "answer": "RAG system not available. Using fallback response.",
                "source_documents": []
            }
    
    try:
        # Invoke the LCEL chain
        answer = qa_chain.invoke(question)
        
        # Get source documents
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        source_docs = retriever.invoke(question)
        
        logging.info(f"RAG query successful, found {len(source_docs)} sources")
        return {
            "answer": answer,
            "source_documents": source_docs
        }
    except Exception as e:
        logging.error(f"RAG query failed: {e}")
        return {
            "answer": f"Error querying RAG system: {str(e)}",
            "source_documents": []
        }

def add_documents(documents: List[Document]):
    """Add new documents to the vector store"""
    global vectorstore
    
    if vectorstore:
        vectorstore.add_documents(documents)
        logging.info(f"Added {len(documents)} new documents to RAG system")
    else:
        logging.warning("Vector store not initialized")

def search_similar(query: str, k: int = 4) -> List[Document]:
    """Search for similar documents without generating answer"""
    if not vectorstore:
        return []
    
    try:
        docs = vectorstore.similarity_search(query, k=k)
        return docs
    except Exception as e:
        logging.error(f"Similarity search failed: {e}")
        return []

# Auto-initialize on import (if API key available)
if OPENAI_API_KEY:
    initialize_rag_system()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🤖 Testing LangChain RAG System")
    print("=" * 80)
    
    if initialize_rag_system():
        test_questions = [
            "What is marine plywood and what are its features?",
            "Tell me about Centuryply Club Prime",
            "What's the difference between MR and BWP plywood?",
            "What types of doors do you offer?"
        ]
        
        for q in test_questions:
            print(f"\n❓ Question: {q}")
            print("-" * 80)
            result = query_rag(q)
            print(f"🤖 Answer: {result['answer'][:300]}...")
            print(f"📚 Sources: {len(result.get('source_documents', []))} documents")
    else:
        print("❌ Failed to initialize RAG system")
