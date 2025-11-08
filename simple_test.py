"""
Simple test for LangChain RAG integration (Windows-compatible)
"""
import logging
logging.basicConfig(level=logging.WARNING)  # Reduce noise

from cli_interface import run_pipeline

print("\n" + "=" * 60)
print("LANGCHAIN RAG INTEGRATION TEST")
print("=" * 60)

test_queries = [
    "What is marine plywood?",
    "Tell me about Centuryply",
    "What doors do you have?",
]

for i, query in enumerate(test_queries, 1):
    print(f"\n[Test {i}] Query: {query}")
    print("-" * 60)
    response = run_pipeline(query)
    print(f"Response: {response[:200]}...")
    print(f"Length: {len(response)} characters")
    print(f"Status: {'PASS' if len(response) > 100 else 'FAIL'}")

print("\n" + "=" * 60)
print("TESTS COMPLETE")
print("=" * 60)
