# Autonomous Research Agent (LangChain)

## Overview
This project implements an AI-powered Autonomous Research Agent using LangChain. The agent accepts a topic as input, retrieves information from multiple sources, analyzes the data, and generates a structured research report.

The system follows the ReAct (Reasoning and Acting) paradigm, enabling it to iteratively gather and refine information before producing a final output.

## Architecture

User Input (Topic)
       │
       ▼
ReAct Agent (LangChain)
       │
  ┌────┴────────────────────┐
  │                         │
  ▼                         ▼
Web Search              Wikipedia
(Tavily)                (Knowledge)
  │                         │
  └────────┬────────────────┘
           │
           ▼
Content Analyzer (LLM)
           │
           ▼
Structured JSON Data
           │
           ▼
Report Generator
           │
           ▼
Markdown Report

## Tools Used

- Tavily Web Search: Retrieves real-time information, statistics, and case studies  
- Wikipedia: Provides background knowledge and foundational information  
- LLM Analyzer: Extracts and synthesizes key insights from collected data  

## Setup and Installation

1. Clone the Repository
git clone https://github.com/yourusername/autonomous-research-agent.git
cd autonomous-research-agent

2. Install Dependencies
pip install -r requirements.txt

3. Configure API Keys
cp .env.example .env

Add the following keys in `.env`:
ANTHROPIC_API_KEY=your_key_here  
TAVILY_API_KEY=your_key_here  

## Usage

Run with default topic:
python agent.py

Run with custom topic:
python agent.py "Impact of AI in Healthcare"

## Project Structure

autonomous-research-agent/
├── agent.py
├── report_generator.py
├── requirements.txt
├── .env.example
├── README.md
└── outputs/
    ├── *_research.json
    └── *_report.md

## Output Format

Each generated report includes:
- Cover Page  
- Introduction  
- Key Findings  
- Challenges  
- Future Scope  
- Statistics and Data Points  
- Conclusion  
- Sources and References  

## Sample Outputs

- Impact of AI in Healthcare  
- Role of Technology in Combating Climate Change  

## ReAct Agent Workflow

- Thought: Determines next step  
- Action: Uses a tool  
- Observation: Processes output  
- Repeat until sufficient data  
- Final Answer: Structured research output  

## Configuration

- model: claude-3-5-sonnet-20241022  
- max_iterations: 12  
- max_results: 5  
- temperature: 0.3  

## Dependencies

- langchain  
- langchain-anthropic  
- langchain-community  
- tavily-python  
- wikipedia  
- python-dotenv  

## Conclusion

This project demonstrates how autonomous AI agents can perform end-to-end research by integrating web search, knowledge retrieval, and reasoning capabilities to generate structured reports.

Autonomous Research Agent
