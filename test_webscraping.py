#!/usr/bin/env python3
"""
Test script for the enhanced webscraping MCP
"""

import logging
from enhanced_webscraping_mcp import WebscrapingMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def test_webscraping():
    """Test the webscraping MCP with a real website"""
    print("\n=== Testing Enhanced Webscraping MCP ===\n")
    
    # Initialize the MCP
    mcp = WebscrapingMCP()
    print("Webscraping MCP initialized")
    
    # Test URLs to scrape
    test_urls = [
        "https://news.ycombinator.com",
        "https://www.python.org",
        "https://en.wikipedia.org/wiki/Artificial_intelligence"
    ]
    
    for url in test_urls:
        print(f"\n--- Testing URL: {url} ---\n")
        
        # Generate a question
        request = f"I want to scrape data from {url} and extract titles, descriptions, and links"
        question = mcp.generate_question(request)
        print(f"Question: {question}")
        
        # Simulate user answer
        answer = f"I want the data in JSON format from {url}"
        print(f"Answer: {answer}")
        
        # Generate response with actual scraping
        print("\nGenerating response with actual web scraping...\n")
        response = mcp.generate_response(request, answer)
        
        # Print the response
        print("Response:")
        print("-" * 80)
        print(response)
        print("-" * 80)
        print("\n")

if __name__ == "__main__":
    test_webscraping()
