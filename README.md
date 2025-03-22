# Model Context Protocol (MCP) Server 🚀

## Overview 📚

![image](https://github.com/user-attachments/assets/7ca5775a-5c02-4695-b4bc-8b45103f5168)


The Model Context Protocol (MCP) Server is a versatile, modular server designed to handle multiple specialized context-aware tasks. Currently, this implementation includes MCPs for research and web scraping functionalities, making it an ideal foundation for projects requiring automated research or real-time web data extraction.

## Purpose & Motivation 🎯
In today's world, real-time data and reliable research are foundational to informed decision-making. This project provides a centralized, extensible platform to easily integrate specialized functionalities like:

- **Automated Research**: Quickly obtain summarized research findings tailored to recent developments and historical context.
- **Web Scraping**: Seamlessly scrape and process web data into structured, meaningful information.

The MCP Server offers flexibility, clarity, and expandability, allowing developers and researchers to integrate and scale additional MCP modules as per evolving project requirements.

## Features & Functionality ⚙️

### Modular Design 🔗
- Easy integration of new MCP modules.
- Each MCP module functions independently yet integrates smoothly within the central server.

### Specialized MCP Modules 🌐
- **ResearchMCP**: Provides real-time insights and summarized content related to the user's specified research queries. Incorporates a structured approach to verify and present findings from credible sources.
- **WebscrapingMCP**: Automates web data collection, extracting structured content quickly and effectively from specified websites.

### Logging & Debugging 📋
- Built-in comprehensive logging capabilities to track system events, debug effectively, and monitor MCP interactions.

### User-Friendly Interaction 🤖
- Interactive prompts in the terminal interface for switching MCP modes dynamically.
- Clear, detailed responses to user requests, enhancing usability and readability.

## Technical Stack 🛠️
- **Python**: Core implementation and logic.
- **Argparse**: Simplified command-line argument handling.
- **Logging**: For detailed logs and debugging information.
- **JSON**: Structured data handling and communication.

## Installation & Setup ⚡️
Follow these easy steps to set up the MCP server locally:

1. Clone the repository:
```bash
git clone https://github.com/praneethk-ai/praneeths_mcp_server.git
cd MCP_Server
```

2. Set up a Python virtual environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python server.py
```

## Usage 🎮

Upon launching, the MCP Server initializes available protocols. You can dynamically select the MCP you wish to use:

- Switch to **Research MCP**:
```bash
RESEARCH
```

- Switch to **Webscraping MCP**:
```bash
WEBSCRAPING
```

- To exit:
```bash
exit
```

### Commands

- `switch`: Change to a different MCP
- `exit`: Exit the server

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


```
### Project Structure 
```

MCP_Server
│
├── mcp_research.py      # Research MCP Implementation
├── mcp_webscraping.py   # Webscraping MCP Implementation
├── mcp_server.py        # Core MCP Server
├── server.py            # Server execution script
├── requirements.txt     # Dependencies list
└── README.md            # Project documentation
```

Future Scope 🌟

This project aims to continually grow by adding additional specialized MCP modules such as:

AI-Driven Analysis
Real-Time Data Processing
Natural Language Generation
Sentiment and Trend Analysis
The modular nature encourages innovation and integration of novel functionalities.

Contributing 🤝

Contributions, enhancements, or feature requests are warmly welcomed! Please open an issue or pull request to start collaborating.

License 📝

This project is licensed under the MIT License — see the LICENSE file for details.
```
