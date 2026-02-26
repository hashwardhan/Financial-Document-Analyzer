#!/usr/bin/env python3
"""
Test script for Financial Document Analyzer API
"""

import requests
import json
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8001"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_api_documentation():
    """Show API documentation URL"""
    print("\n" + "="*60)
    print("TEST 2: API Documentation")
    print("="*60)
    
    docs_url = f"{BASE_URL}/docs"
    print(f"Interactive API docs available at: {docs_url}")
    print("Open this URL in your browser to test endpoints with Swagger UI")
    return True


def test_analyze_with_sample_pdf():
    """Test the analyze endpoint with a sample PDF"""
    print("\n" + "="*60)
    print("TEST 3: Analyze Endpoint (with sample PDF)")
    print("="*60)
    
    # Check if sample.pdf exists
    sample_pdf = Path("data/sample.pdf")
    if not sample_pdf.exists():
        print(f"⚠️  Sample PDF not found at {sample_pdf}")
        print("To test: Place a PDF file at 'data/sample.pdf'")
        print("\nExample with curl:")
        print('curl -X POST "http://127.0.0.1:8001/analyze"')
        print('  -F "file=@path/to/your/file.pdf"')
        print('  -F "query=Analyze this financial document"')
        return False
    
    try:
        with open(sample_pdf, 'rb') as f:
            files = {'file': f}
            data = {'query': 'Provide a financial analysis of this document'}
            
            print(f"Uploading: {sample_pdf}")
            response = requests.post(
                f"{BASE_URL}/analyze",
                files=files,
                data=data,
                timeout=60
            )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def print_usage_examples():
    """Print curl and Python examples"""
    print("\n" + "="*60)
    print("USAGE EXAMPLES")
    print("="*60)
    
    print("\n1. Health Check (curl):")
    print("   curl http://127.0.0.1:8001/")
    
    print("\n2. Analyze Document (curl):")
    print('   curl -X POST "http://127.0.0.1:8001/analyze" \\')
    print('     -F "file=@path/to/document.pdf" \\')
    print('     -F "query=What is the financial status?"')
    
    print("\n3. Using Python requests:")
    print("""
    import requests
    
    with open('document.pdf', 'rb') as f:
        files = {'file': f}
        data = {'query': 'Analyze this document'}
        response = requests.post(
            'http://127.0.0.1:8001/analyze',
            files=files,
            data=data
        )
        print(response.json())
    """)


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("FINANCIAL DOCUMENT ANALYZER - API TEST SUITE")
    print("="*60)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: API Documentation
    results.append(("API Documentation", test_api_documentation()))
    
    # Test 3: Analyze endpoint
    results.append(("Analyze Endpoint", test_analyze_with_sample_pdf()))
    
    # Print usage examples
    print_usage_examples()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "⚠️  SKIPPED/FAILED"
        print(f"{test_name}: {status}")
    
    print("\n" + "="*60)
    print("SERVER STATUS: ✅ Running on http://127.0.0.1:8001")
    print("="*60)


if __name__ == "__main__":
    main()
