#!/usr/bin/env python3
"""
Demo script for Praneeth's MCP Server
This script demonstrates the MCP server with a random selection and predefined interactions
"""

import random
import time
from mcp_research import ResearchMCP
from mcp_webscraping import WebscrapingMCP

def print_with_delay(text, delay=0.5):
    """Print text with a delay to simulate typing"""
    print(text)
    time.sleep(delay)

def main():
    """Main demo function"""
    print_with_delay("Welcome to Praneeth's MCP Server Demo!")
    print_with_delay("This demo will show how the MCP server works with random selection.")
    print_with_delay("\nAvailable MCPs: research, webscraping")
    
    # Randomly select an MCP
    mcps = ["research", "webscraping"]
    selected_mcp = random.choice(mcps)
    print_with_delay(f"\nRandomly selected: {selected_mcp.upper()} MCP")
    
    # Initialize the selected MCP
    if selected_mcp == "research":
        mcp = ResearchMCP()
        demo_research_mcp(mcp)
    else:
        mcp = WebscrapingMCP()
        demo_webscraping_mcp(mcp)
    
    print_with_delay("\nDemo completed! You can run the full server with 'python server.py --random'")
    print_with_delay("Exiting Praneeth's MCP Server Demo. Goodbye!")

def demo_research_mcp(mcp):
    """Demonstrate the Research MCP"""
    print_with_delay("\n[RESEARCH MCP] Enter your request: artificial intelligence applications in healthcare")
    
    # Generate question
    question = mcp.generate_question("artificial intelligence applications in healthcare")
    print_with_delay(f"\n[RESEARCH MCP]: {question}")
    
    # Simulate user answer
    user_answer = "I'm interested in diagnostic tools and patient monitoring systems"
    print_with_delay(f"Your answer: {user_answer}")
    
    # Generate response
    response = mcp.generate_response("artificial intelligence applications in healthcare", user_answer)
    print_with_delay(f"\n[RESEARCH MCP RESPONSE]: {response}")

def demo_webscraping_mcp(mcp):
    """Demonstrate the Webscraping MCP"""
    print_with_delay("\n[WEBSCRAPING MCP] Enter your request: I need to extract product prices from an e-commerce site")
    
    # Generate question
    question = mcp.generate_question("I need to extract product prices from an e-commerce site")
    print_with_delay(f"\n[WEBSCRAPING MCP]: {question}")
    
    # Simulate user answer
    user_answer = "https://example.com/products"
    print_with_delay(f"Your answer: {user_answer}")
    
    # Generate response
    response = mcp.generate_response("I need to extract product prices from an e-commerce site", user_answer)
    print_with_delay(f"\n[WEBSCRAPING MCP RESPONSE]: {response}")

if __name__ == "__main__":
    main()
