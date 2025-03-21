#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Server
Manages multiple specialized MCPs and handles client requests.
"""

import logging
import argparse
import json
import sys
from typing import Dict, Any, List, Optional

# Import specialized MCPs
from mcp_research import ResearchMCP
from mcp_webscraping import WebscrapingMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("MCPServer")

class MCPServer:
    """
    Model Context Protocol Server
    Manages multiple specialized MCPs and routes user requests to the appropriate one.
    """
    
    def __init__(self, name: str = "Praneeth's MCP"):
        """
        Initialize the MCP server with specialized MCPs
        
        Args:
            name: The name of the MCP server
        """
        self.name = name
        self.mcps = {
            "research": ResearchMCP(),
            "webscraping": WebscrapingMCP()
        }
        logger.info(f"MCP Server '{name}' initialized with {len(self.mcps)} specialized MCPs")
    
    def process_request(self, user_request: str) -> str:
        """
        Process a user request by routing it to the appropriate MCP
        
        Args:
            user_request: The user's request
            
        Returns:
            A response to the user's request
        """
        # Determine which MCP to use based on the request content
        mcp_type = self._determine_mcp_type(user_request)
        logger.info(f"Request classified as '{mcp_type}' type")
        
        # Get the appropriate MCP
        mcp = self.mcps[mcp_type]
        
        # Generate a clarifying question
        question = mcp.generate_question(user_request)
        logger.info(f"Generated clarifying question: {question}")
        
        # In a real implementation, we would wait for the user's answer
        # For this example, we'll simulate a user answer
        print(f"Question: {question}")
        user_answer = input("Your answer: ")
        
        # Generate a response based on the original request and the user's answer
        response = mcp.generate_response(user_request, user_answer)
        logger.info("Generated response")
        
        return response
    
    def _determine_mcp_type(self, user_request: str) -> str:
        """
        Determine which specialized MCP should handle the user request
        
        Args:
            user_request: The user's request
            
        Returns:
            The type of MCP to use (e.g., "research", "webscraping")
        """
        user_request_lower = user_request.lower()
        
        # Check for webscraping-related keywords
        webscraping_keywords = ["scrape", "extract data", "website data", "html", "web page", "crawler"]
        if any(keyword in user_request_lower for keyword in webscraping_keywords):
            return "webscraping"
        
        # Default to research for all other requests
        return "research"

def main():
    """
    Main entry point for the MCP server
    """
    parser = argparse.ArgumentParser(description="Model Context Protocol Server")
    parser.add_argument("--name", type=str, default="Praneeth's MCP", help="Name of the MCP server")
    args = parser.parse_args()
    
    # Create the MCP server
    server = MCPServer(name=args.name)
    
    # Simple interactive loop
    print(f"Welcome to {server.name}!")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYour request: ")
        
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        try:
            response = server.process_request(user_input)
            print(f"\nResponse: {response}")
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            print(f"Sorry, an error occurred: {str(e)}")

if __name__ == "__main__":
    main()
