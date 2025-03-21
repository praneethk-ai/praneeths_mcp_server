#!/usr/bin/env python3
"""

Praneeth's MCP Server
A Model Context Protocol server that manages multiple context protocols.
"""

import argparse
import json
import logging
import random
import sys
from typing import Dict, Any, List, Optional

from mcp_research import ResearchMCP
from enhanced_webscraping_mcp import WebscrapingMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("PraneethMCP")

class MCPServer:
    """Main MCP Server that manages multiple context protocols"""
    
    def __init__(self):
        self.mcps = {
            "research": ResearchMCP(),
            "webscraping": WebscrapingMCP()
        }
        self.current_mcp = None
        logger.info("Praneeth's MCP Server initialized with protocols: %s", list(self.mcps.keys()))
    
    def list_available_mcps(self) -> List[str]:
        """Return a list of available MCPs"""
        return list(self.mcps.keys())
    
    def set_current_mcp(self, mcp_name: str) -> bool:
        """Set the current active MCP"""
        if mcp_name in self.mcps:
            self.current_mcp = mcp_name
            logger.info(f"Switched to {mcp_name} MCP")
            return True
        else:
            logger.error(f"MCP '{mcp_name}' not found")
            return False
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process a user request through the current MCP"""
        if not self.current_mcp:
            return {
                "status": "error",
                "message": "No MCP selected. Please select an MCP first.",
                "available_mcps": self.list_available_mcps()
            }
        
        try:
            # Get the appropriate MCP handler
            mcp_handler = self.mcps[self.current_mcp]
            
            # First, get the question from the MCP
            question = mcp_handler.generate_question(user_input)
            
            # Display the question to the user
            print(f"\n[{self.current_mcp.upper()} MCP]: {question}")
            
            # Wait for user's answer
            answer = input("Your answer: ")
            
            # Process the answer and generate a response
            response = mcp_handler.generate_response(user_input, answer)
            
            return {
                "status": "success",
                "mcp": self.current_mcp,
                "question": question,
                "response": response
            }
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "status": "error",
                "message": f"Error processing request: {str(e)}"
            }

def main():
    """Main entry point for the MCP server"""
    parser = argparse.ArgumentParser(description="Praneeth's MCP Server")
    parser.add_argument('--mcp', type=str, help='Initial MCP to use')
    parser.add_argument('--random', action='store_true', help='Randomly select an MCP')
    args = parser.parse_args()
    
    server = MCPServer()
    print(f"Welcome to Praneeth's MCP Server!")
    print(f"Available MCPs: {', '.join(server.list_available_mcps())}")
    
    # Set initial MCP if provided or randomly select one
    if args.random:
        random_mcp = random.choice(server.list_available_mcps())
        server.set_current_mcp(random_mcp)
        print(f"Randomly selected: {random_mcp.upper()} MCP")
    elif args.mcp:
        if not server.set_current_mcp(args.mcp):
            print(f"Invalid MCP: {args.mcp}")
            print(f"Available MCPs: {', '.join(server.list_available_mcps())}")
    
    # Main interaction loop
    while True:
        try:
            # If no MCP is selected, prompt to select one
            if not server.current_mcp:
                mcp_choice = input("\nSelect an MCP (research/webscraping): ").strip().lower()
                if mcp_choice in server.mcps:
                    server.set_current_mcp(mcp_choice)
                    print(f"Switched to {mcp_choice.upper()} MCP")
                else:
                    print(f"Invalid choice. Available MCPs: {', '.join(server.list_available_mcps())}")
                continue
            
            # Get user input for the current MCP
            user_input = input(f"\n[{server.current_mcp.upper()} MCP] Enter your request (or 'switch' to change MCP, 'exit' to quit): ")
            
            if user_input.lower() == 'exit':
                print("Exiting Praneeth's MCP Server. Goodbye!")
                break
            
            if user_input.lower() == 'switch':
                server.current_mcp = None
                continue
            
            # Process the request
            result = server.process_request(user_input)
            
            if result["status"] == "success":
                print(f"\n[{result['mcp'].upper()} MCP RESPONSE]: {result['response']}")
            else:
                print(f"\nError: {result['message']}")
        
        except KeyboardInterrupt:
            print("\nExiting Praneeth's MCP Server. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
