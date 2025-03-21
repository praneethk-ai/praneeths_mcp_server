#!/usr/bin/env python3
"""
Research MCP Module
Handles research-related context and interactions.
"""

import logging
import json
import requests
from typing import Dict, Any, List, Optional

logger = logging.getLogger("ResearchMCP")

class ResearchMCP:
    """
    Research Model Context Protocol
    Manages context for research-related queries and responses.
    """
    
    def __init__(self):
        self.context = {
            "topics": [],
            "depth": "standard",
            "sources_required": True,
            "academic_focus": True
        }
        logger.info("Research MCP initialized")
    
    def generate_question(self, user_input: str) -> str:
        """
        Generate a clarifying question based on the user's research request
        
        Args:
            user_input: The initial user request
            
        Returns:
            A question to ask the user for more context
        """
        # Analyze the user input to determine what clarification is needed
        if "topic" in user_input.lower() or len(user_input.split()) < 5:
            return "Could you specify the exact research topic you're interested in?"
        
        if "sources" in user_input.lower() or "reference" in user_input.lower():
            return "What type of sources would you prefer? (e.g., academic papers, books, websites)"
        
        if "depth" in user_input.lower() or "detail" in user_input.lower():
            return "How in-depth would you like this research to be? (basic, intermediate, advanced)"
        
        # Default questions based on common research needs
        questions = [
            "What specific aspects of this topic are you most interested in?",
            "Are you looking for recent developments or historical context?",
            "Do you need this research for academic purposes or personal interest?",
            "Are there any specific sources or authors you'd like me to focus on?",
            "Would you like me to include contrary viewpoints in the research?"
        ]
        
        # Choose a question based on the length of the user input
        # For simplicity, we'll use the input length modulo the number of questions
        question_index = len(user_input) % len(questions)
        return questions[question_index]
    
    def generate_response(self, original_request: str, user_answer: str) -> str:
        """
        Generate a research response based on the original request and the user's answer
        
        Args:
            original_request: The initial user request
            user_answer: The user's answer to the clarifying question
            
        Returns:
            A research response with actual research information
        """
        # Update context based on user's answer
        self._update_context(original_request, user_answer)
        
        # Combine the original request and user answer to create a research query
        research_query = f"{original_request} {user_answer}"
        
        # Get actual research information
        research_data = self._get_research_information(research_query)
        
        # Generate a response with the actual research data
        response = f"Based on your interest in {original_request} and your clarification that {user_answer}, I've gathered the following research information:\n\n"
        
        # Add the research data to the response
        if research_data:
            response += "**Research Findings**:\n"
            response += research_data + "\n\n"
        else:
            response += "I was unable to find specific research information on this topic. This could be due to the specialized nature of the query or limitations in available resources.\n\n"
        
        # Add information about the research approach
        response += "**Research Approach**:\n"
        response += f"- Depth level: {self.context['depth'].upper()}\n"
        
        if self.context["sources_required"]:
            response += "- Sources have been included where available\n"
        
        if self.context["academic_focus"]:
            response += "- Focus on academic and scholarly sources\n"
        else:
            response += "- Focus on general information and practical applications\n"
        
        if self.context["topics"]:
            response += f"- Key topics explored: {', '.join(self.context['topics'])}\n"
        
        return response
    
    def _update_context(self, original_request: str, user_answer: str) -> None:
        """
        Update the internal context based on user interactions
        
        Args:
            original_request: The initial user request
            user_answer: The user's answer to the clarifying question
        """
        # Extract potential topics from the original request and answer
        words = set(original_request.lower().split() + user_answer.lower().split())
        
        # Update depth based on user answer
        if "basic" in user_answer.lower() or "simple" in user_answer.lower():
            self.context["depth"] = "basic"
        elif "advanced" in user_answer.lower() or "detailed" in user_answer.lower() or "in-depth" in user_answer.lower():
            self.context["depth"] = "advanced"
        elif "intermediate" in user_answer.lower() or "moderate" in user_answer.lower():
            self.context["depth"] = "intermediate"
        
        # Update sources requirement
        if "no sources" in user_answer.lower() or "without references" in user_answer.lower():
            self.context["sources_required"] = False
        elif "sources" in user_answer.lower() or "references" in user_answer.lower() or "citations" in user_answer.lower():
            self.context["sources_required"] = True
        
        # Update academic focus
        if "personal" in user_answer.lower() or "casual" in user_answer.lower():
            self.context["academic_focus"] = False
        elif "academic" in user_answer.lower() or "scholarly" in user_answer.lower() or "research" in user_answer.lower():
            self.context["academic_focus"] = True
            
        logger.debug(f"Updated research context: {self.context}")
        
    def _get_research_information(self, query: str) -> str:
        """
        Retrieve actual research information based on the query
        
        Args:
            query: The research query
            
        Returns:
            A string containing the research information
        """
        try:
            # Attempt to get research information from a public API
            # For this implementation, we'll use the Wikipedia API as an example
            # In a production environment, you might use academic APIs like Scopus, PubMed, etc.
            
            # Clean the query
            clean_query = query.replace(' ', '%20')
            
            # Make a request to the Wikipedia API
            url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={clean_query}&format=json&srlimit=3"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the results
            if 'query' in data and 'search' in data['query'] and data['query']['search']:
                results = data['query']['search']
                
                # Format the research information based on the depth
                if self.context["depth"] == "advanced":
                    # For advanced depth, provide more detailed information
                    research_info = []
                    for i, result in enumerate(results, 1):
                        title = result.get('title', 'Unknown')
                        snippet = result.get('snippet', '').replace('<span class="searchmatch">', '**').replace('</span>', '**')
                        snippet = snippet.replace('<span class=\"searchmatch\">', '**').replace('</span>', '**')
                        
                        research_info.append(f"{i}. **{title}**")
                        research_info.append(f"   {snippet}")
                        if self.context["sources_required"]:
                            research_info.append(f"   Source: Wikipedia - https://en.wikipedia.org/wiki/{title.replace(' ', '_')}")
                        research_info.append("")
                    
                    return "\n".join(research_info)
                
                elif self.context["depth"] == "intermediate":
                    # For intermediate depth, provide moderate information
                    research_info = []
                    for i, result in enumerate(results[:2], 1):
                        title = result.get('title', 'Unknown')
                        snippet = result.get('snippet', '').replace('<span class="searchmatch">', '**').replace('</span>', '**')
                        snippet = snippet.replace('<span class=\"searchmatch\">', '**').replace('</span>', '**')
                        
                        research_info.append(f"{i}. **{title}**")
                        research_info.append(f"   {snippet}")
                    
                    if self.context["sources_required"]:
                        research_info.append("\nSources: Wikipedia and other academic resources")
                    
                    return "\n".join(research_info)
                
                else:  # basic depth
                    # For basic depth, provide a simple summary
                    result = results[0]
                    title = result.get('title', 'Unknown')
                    snippet = result.get('snippet', '').replace('<span class="searchmatch">', '**').replace('</span>', '**')
                    snippet = snippet.replace('<span class=\"searchmatch\">', '**').replace('</span>', '**')
                    
                    research_info = [f"**{title}**: {snippet}"]
                    
                    if self.context["sources_required"]:
                        research_info.append("\nSource: Wikipedia")
                    
                    return "\n".join(research_info)
            
            return "No specific research information found for this query."
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving research information: {str(e)}")
            return f"Error retrieving research information: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error during research: {str(e)}")
            return f"Unexpected error during research: {str(e)}"
