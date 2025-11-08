"""
Test LangChain RAG Integration
Tests the complete pipeline with RAG system
"""
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def test_rag_integration():
    """Test end-to-end pipeline with RAG system"""
    from cli_interface import run_pipeline
    
    print("=" * 80)
    print("🧪 Testing LangChain RAG Integration")
    print("=" * 80)
    
    test_cases = [
        # Product queries (should use RAG)
        {
            "query": "What is marine plywood and where is it used?",
            "expected_keywords": ["waterproof", "marine", "exterior", "moisture"],
            "system": "RAG"
        },
        {
            "query": "Tell me about Centuryply Club Prime",
            "expected_keywords": ["centuryply", "club prime", "bwp", "virokill"],
            "system": "RAG"
        },
        {
            "query": "What types of doors do you have?",
            "expected_keywords": ["flush", "door", "greenply", "7ft", "panel"],
            "system": "RAG"
        },
        
        # Specifications (might trigger web search)
        {
            "query": "What are the specifications of 18mm commercial plywood?",
            "expected_keywords": ["18mm", "plywood", "thickness", "specification"],
            "system": "Web/RAG"
        },
        
        # Business info (should use RAG or fallback)
        {
            "query": "Where is Plywood Studio located?",
            "expected_keywords": ["goshamahal", "hyderabad", "location", "500012"],
            "system": "RAG/Fallback"
        },
        
        # Greeting (should use fallback)
        {
            "query": "Hello, how can you help me?",
            "expected_keywords": ["plywood studio", "welcome", "assist", "help"],
            "system": "Fallback"
        }
    ]
    
    results = []
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}/{len(test_cases)}: {test['query']}")
        print(f"Expected System: {test['system']}")
        print("-" * 80)
        
        try:
            response = run_pipeline(test["query"])
            
            # Check if response contains expected keywords
            response_lower = response.lower()
            found_keywords = [kw for kw in test["expected_keywords"] if kw in response_lower]
            keyword_coverage = len(found_keywords) / len(test["expected_keywords"])
            
            # Quality checks
            is_long_enough = len(response) > 100
            not_error = "error" not in response_lower[:50]
            has_content = keyword_coverage > 0.3
            
            passed = is_long_enough and not_error and has_content
            
            print(f"✅ Response Length: {len(response)} chars")
            print(f"✅ Keyword Coverage: {len(found_keywords)}/{len(test['expected_keywords'])} ({keyword_coverage:.0%})")
            print(f"✅ Found Keywords: {', '.join(found_keywords)}")
            print(f"\n📝 Response Preview:\n{response[:300]}...")
            print(f"\n{'✅ PASS' if passed else '❌ FAIL'}")
            
            results.append({
                "test": test["query"],
                "passed": passed,
                "length": len(response),
                "keyword_coverage": keyword_coverage
            })
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            results.append({
                "test": test["query"],
                "passed": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    passed_tests = sum(1 for r in results if r.get("passed", False))
    total_tests = len(results)
    
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result.get("passed") else "❌ FAIL"
        test_name = result["test"][:60]
        print(f"{status} - Test {i}: {test_name}")
        if "error" in result:
            print(f"   Error: {result['error']}")
    
    print(f"\n🎯 Overall: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests:.0%})")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! LangChain RAG integration is working perfectly!")
    elif passed_tests > total_tests * 0.7:
        print("\n✅ Most tests passed. System is functional.")
    else:
        print("\n⚠️ Some tests failed. Check the logs above for details.")
    
    return results

if __name__ == "__main__":
    print("🚀 Starting LangChain RAG Integration Tests...\n")
    
    try:
        results = test_rag_integration()
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
