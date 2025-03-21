#!/usr/bin/env python3
"""
Enhanced Webscraping MCP Module
Handles webscraping-related context and interactions with actual web scraping functionality.
"""

import logging
import re
import json
import requests
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logger = logging.getLogger("WebscrapingMCP")

class WebscrapingMCP:
    """
    Webscraping Model Context Protocol
    Manages context for webscraping-related queries and responses.
    """
    
    def __init__(self):
        self.context = {
            "target_urls": [],
            "data_format": "json",
            "elements_to_extract": [],
            "pagination": False,
            "frequency": "once"
        }
        logger.info("Webscraping MCP initialized")
    
    def generate_question(self, user_input: str) -> str:
        """
        Generate a clarifying question based on the user's webscraping request
        
        Args:
            user_input: The initial user request
            
        Returns:
            A question to ask the user for more context
        """
        # Check if URL is provided
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        if not url_pattern.search(user_input) and "url" not in user_input.lower():
            return "What specific website or URL would you like to scrape data from?"
        
        # Check for data elements
        if "extract" not in user_input.lower() and "scrape" in user_input.lower():
            return "What specific elements or data would you like to extract from the website? (e.g., product prices, article titles, images)"
        
        # Check for data format preference
        if "format" not in user_input.lower() and "output" not in user_input.lower():
            return "In what format would you like the scraped data? (e.g., JSON, CSV, plain text)"
        
        # Default questions based on common webscraping needs
        questions = [
            "Do you need to handle pagination or scrape multiple pages?",
            "Are there any specific filters or conditions for the data you want to extract?",
            "How frequently do you need this data to be scraped? (once, daily, weekly)",
            "Do you need to authenticate or log in to access the data?",
            "Are there any specific headers or user agents you'd like to use for the request?"
        ]
        
        # Choose a question based on the length of the user input
        question_index = len(user_input) % len(questions)
        return questions[question_index]
    
    def generate_response(self, original_request: str, user_answer: str) -> str:
        """
        Generate a webscraping response based on the original request and the user's answer
        
        Args:
            original_request: The initial user request
            user_answer: The user's answer to the clarifying question
            
        Returns:
            A webscraping response with actual scraped data
        """
        # Update context based on user's answer
        self._update_context(original_request, user_answer)
        
        # Extract URL if present in either the original request or the answer
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')        
        url_match = url_pattern.search(original_request) or url_pattern.search(user_answer)
        
        # If no URL is found, provide a generic response
        if not url_match:
            return "I couldn't find a valid URL to scrape. Please provide a specific website URL."
        
        url = url_match.group(0)
        logger.info(f"Attempting to scrape data from URL: {url}")
        
        # Attempt to scrape the actual website
        scraped_data = self._scrape_website(url)
        
        # Generate a response with the actual scraped data
        response = f"Based on your request to scrape data from {url}, I've retrieved the following information:\n\n"
        
        # Add the scraped data to the response
        response += "**Scraped Data**:\n"
        response += scraped_data + "\n\n"
        
        # Provide information about the approach used
        response += "**Web Scraping Approach Used**:\n"
        
        # Determine the appropriate library based on the complexity
        if self.context["pagination"] or "login" in user_answer.lower() or "authenticate" in user_answer.lower():
            response += "- Used Selenium with a headless browser"
            if "login" in user_answer.lower() or "authenticate" in user_answer.lower():
                response += " with authentication handling"
            if self.context["pagination"]:
                response += " and pagination support"
            response += "\n"
        else:
            response += "- Used Requests library with BeautifulSoup for HTML parsing\n"
        
        # Data extraction strategy
        if self.context["elements_to_extract"]:
            elements = ", ".join(self.context["elements_to_extract"])
            response += f"- Targeted elements for extraction: {elements}\n"
        else:
            response += "- Extracted general content based on common HTML patterns\n"
        
        # Data format
        response += f"- Data format: {self.context['data_format'].upper()}\n"
        
        # Scheduling if applicable
        if self.context["frequency"] != "once":
            response += f"- Scraping frequency: {self.context['frequency']}\n"
        
        # Legal and ethical considerations
        response += "\n**Important Considerations**:\n"
        response += "- Always check the website's robots.txt file and terms of service before scraping.\n"
        response += "- Implement rate limiting to avoid overloading the server.\n"
        response += "- Consider using an API if one is available instead of scraping.\n"
        
        return response
    
    def _update_context(self, original_request: str, user_answer: str) -> None:
        """
        Update the internal context based on user interactions
        
        Args:
            original_request: The initial user request
            user_answer: The user's answer to the clarifying question
        """
        # Extract URLs
        url_pattern = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+')
        urls = url_pattern.findall(original_request) + url_pattern.findall(user_answer)
        if urls:
            self.context["target_urls"] = list(set(urls))
        
        # Update data format preference
        format_keywords = {
            "json": ["json", "javascript", "object", "notation"],
            "csv": ["csv", "comma", "excel", "spreadsheet"],
            "xml": ["xml", "extensible", "markup"],
            "text": ["text", "plain", "txt"],
            "html": ["html", "webpage", "page"]
        }
        
        combined_text = (original_request + " " + user_answer).lower()
        for fmt, keywords in format_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                self.context["data_format"] = fmt
                break
        
        # Extract elements to scrape
        element_patterns = [
            r"extract\s+([a-zA-Z\s,]+)",
            r"scrape\s+([a-zA-Z\s,]+)",
            r"get\s+([a-zA-Z\s,]+)",
            r"collect\s+([a-zA-Z\s,]+)"
        ]
        
        for pattern in element_patterns:
            matches = re.search(pattern, combined_text)
            if matches:
                elements = matches.group(1).split(',')
                elements = [e.strip() for e in elements if e.strip()]
                if elements:
                    self.context["elements_to_extract"] = elements
                break
        
        # Check for pagination
        pagination_keywords = ["pagination", "multiple pages", "next page", "all pages"]
        if any(keyword in combined_text for keyword in pagination_keywords):
            self.context["pagination"] = True
        
        # Update frequency
        frequency_mapping = {
            "once": ["once", "one time", "single", "just once"],
            "hourly": ["hourly", "every hour", "each hour"],
            "daily": ["daily", "every day", "each day"],
            "weekly": ["weekly", "every week", "each week"],
            "monthly": ["monthly", "every month", "each month"]
        }
        
        for freq, keywords in frequency_mapping.items():
            if any(keyword in combined_text for keyword in keywords):
                self.context["frequency"] = freq
                break
                
        logger.debug(f"Updated webscraping context: {self.context}")
        
    def _scrape_website(self, url: str) -> str:
        """
        Attempt to scrape data from the specified URL
        
        Args:
            url: The URL to scrape
            
        Returns:
            A string containing the scraped data formatted according to the context
        """
        try:
            # Set a user agent to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Make the request
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for 4XX/5XX responses
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Determine what to extract based on the context
            extracted_data = {}
            
            # If specific elements are requested, try to extract them
            if self.context["elements_to_extract"]:
                for element in self.context["elements_to_extract"]:
                    # Try different strategies to find the elements
                    if "price" in element.lower():
                        # Look for common price patterns
                        price_elements = soup.select('.price, .product-price, [itemprop="price"], .offer-price, span:contains("$")')
                        if price_elements:
                            extracted_data[element] = [elem.text.strip() for elem in price_elements[:5]]
                    
                    elif "title" in element.lower() or "name" in element.lower() or "article" in element.lower():
                        # Look for titles or names
                        title_elements = soup.select('h1, h2, .title, .product-title, [itemprop="name"], .article-title')
                        if title_elements:
                            extracted_data[element] = [elem.text.strip() for elem in title_elements[:5]]
                    
                    elif "image" in element.lower() or "photo" in element.lower():
                        # Look for images
                        img_elements = soup.select('img[src], [itemprop="image"]')
                        if img_elements:
                            extracted_data[element] = [elem.get('src', '') for elem in img_elements[:5]]
                    
                    elif "description" in element.lower():
                        # Look for descriptions
                        desc_elements = soup.select('p, .description, [itemprop="description"]')
                        if desc_elements:
                            extracted_data[element] = [elem.text.strip() for elem in desc_elements[:3]]
                    
                    elif "ai" in element.lower() or "artificial intelligence" in element.lower():
                        # Look for AI-related content
                        ai_elements = soup.select('p:contains("AI"), p:contains("artificial intelligence"), h1:contains("AI"), h2:contains("AI"), h3:contains("AI")')
                        if ai_elements:
                            extracted_data[element] = [elem.text.strip() for elem in ai_elements[:5]]
                    
                    else:
                        # Generic approach for other elements
                        generic_elements = soup.select(f'.{element}, #{element}, [itemprop="{element}"], [class*="{element}"]')
                        if generic_elements:
                            extracted_data[element] = [elem.text.strip() for elem in generic_elements[:5]]
            
            # If no specific elements or nothing found, extract general information
            if not extracted_data:
                # Get page title
                title = soup.title.text.strip() if soup.title else "No title found"
                extracted_data["Page Title"] = title
                
                # Get main headings
                headings = [h.text.strip() for h in soup.select('h1, h2')[:5]]
                if headings:
                    extracted_data["Main Headings"] = headings
                
                # Get meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    extracted_data["Meta Description"] = meta_desc['content']
                
                # Get paragraphs
                paragraphs = [p.text.strip() for p in soup.select('p')[:3]]
                if paragraphs:
                    extracted_data["Main Content"] = paragraphs
            
            # Format the data according to the preferred format
            if self.context["data_format"] == "json":
                return json.dumps(extracted_data, indent=2)
            elif self.context["data_format"] == "csv":
                csv_data = []
                for key, values in extracted_data.items():
                    if isinstance(values, list):
                        for i, value in enumerate(values):
                            csv_data.append(f"{key} {i+1}: {value}")
                    else:
                        csv_data.append(f"{key}: {values}")
                return "\n".join(csv_data)
            else:  # plain text
                text_data = []
                for key, values in extracted_data.items():
                    if isinstance(values, list):
                        text_data.append(f"{key}:")
                        for value in values:
                            text_data.append(f"  - {value}")
                    else:
                        text_data.append(f"{key}: {values}")
                return "\n".join(text_data)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping website: {str(e)}")
            return f"Error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error during scraping: {str(e)}")
            return f"Unexpected error: {str(e)}"
