# Praneeth's Model Context Protocol (MCP) Server

A Python-based MCP server that manages multiple context protocols for different types of tasks. This implementation includes two specialized MCPs:

1. **Research MCP**: Handles research-related queries with appropriate context management
2. **Webscraping MCP**: Manages web scraping requests with relevant context adaptation

## Features

- Interactive command-line interface
- Dynamic context management for each MCP type
- Question-first approach that asks clarifying questions before providing responses
- Ability to switch between different MCPs
- Contextual memory within each MCP session

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the server with:

```bash
python server.py
```

You can also specify an initial MCP to use:

```bash
python server.py --mcp research
```

### Commands

- `switch`: Change to a different MCP
- `exit`: Exit the server

## Example Interactions

### Research MCP

```
[RESEARCH MCP] Enter your request: I need information about quantum computing

[RESEARCH MCP]: What specific aspects of this topic are you most interested in?
Your answer: I'm interested in quantum algorithms and their applications

[RESEARCH MCP RESPONSE]: Based on your interest in I need information about quantum computing and your clarification that I'm interested in quantum algorithms and their applications, I've analyzed the available information and found that:

1. This topic has several important aspects worth exploring.
2. Recent developments have changed how experts view this field.

Relevant sources include recent publications by leading researchers and established textbooks in the field.
```

### Webscraping MCP

```
[WEBSCRAPING MCP] Enter your request: I want to scrape product data from an e-commerce site

[WEBSCRAPING MCP]: What specific website or URL would you like to scrape data from?
Your answer: https://example.com/products

[WEBSCRAPING MCP RESPONSE]: Based on your request to scrape data from https://example.com/products here's how we can approach this:

1. **Web Scraping Approach**:
   - We can use the Requests library with BeautifulSoup for parsing the HTML content.

2. **Data Extraction**:
   - We'll extract the main content based on common HTML patterns and selectors.

3. **Output Format**:
   - The scraped data will be provided in JSON format, which is easily parseable and can be used in various applications.

**Important Considerations**:
- Always check the website's robots.txt file and terms of service before scraping.
- Implement rate limiting to avoid overloading the server.
- Consider using an API if one is available instead of scraping.
```

## Extending the System

You can extend this system by:

1. Adding new MCP types in separate modules
2. Implementing the required methods (`generate_question` and `generate_response`)
3. Registering the new MCP in the `MCPServer` initialization

## License

This project is available for personal use.

## Author

Praneeth
