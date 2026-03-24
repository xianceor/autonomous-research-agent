"""
Autonomous Research Agent using LangChain + Anthropic Claude
Assignment 2 — AI Research Agent
"""

import os
import json
import datetime
from typing import Optional
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

from report_generator import generate_report

load_dotenv()


# ─────────────────────────────────────────────
# 1. LLM
# ─────────────────────────────────────────────
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
    temperature=0.3,
    max_tokens=4096,
)


# ─────────────────────────────────────────────
# 2. Tools
# ─────────────────────────────────────────────

# Tool 1 — Web Search (Tavily)
web_search_tool = TavilySearchResults(
    max_results=5,
    tavily_api_key=os.getenv("TAVILY_API_KEY"),
    description=(
        "Search the internet for current, up-to-date information about any topic. "
        "Use this for recent news, statistics, case studies, and real-world examples. "
        "Input should be a focused search query."
    ),
)

# Tool 2 — Wikipedia Knowledge Tool
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=3000),
    description=(
        "Query Wikipedia for factual background knowledge, definitions, historical context, "
        "and established academic information. Best for foundational knowledge about a topic."
    ),
)

# Tool 3 — Deep Analysis (LLM-powered summarizer)
def analyze_and_summarize(text: str) -> str:
    """Use the LLM to analyze and extract key insights from raw text."""
    prompt = f"""You are a research analyst. Analyze the following text and extract:
1. Key facts and statistics
2. Important trends
3. Notable challenges
4. Future implications

Text:
{text}

Provide a structured, insightful analysis."""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

analysis_tool = Tool(
    name="analyze_content",
    func=analyze_and_summarize,
    description=(
        "Analyzes and summarizes raw text content to extract key insights, trends, "
        "challenges, and future implications. Use this after gathering information to "
        "distill it into structured findings."
    ),
)

tools = [web_search_tool, wikipedia_tool, analysis_tool]


# ─────────────────────────────────────────────
# 3. ReAct Agent Prompt
# ─────────────────────────────────────────────
REACT_PROMPT = PromptTemplate.from_template("""
You are an expert autonomous research agent. Your task is to thoroughly research a topic 
and gather comprehensive information to generate a detailed, structured report.

You have access to the following tools:
{tools}

Use the following format STRICTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Guidelines:
- Search the web at least 2-3 times with different queries to get diverse information
- Use Wikipedia to get foundational/background knowledge
- Use the analyze_content tool to synthesize information you've gathered
- Gather information on: overview, current applications, challenges, future scope, key statistics
- Be thorough — the final answer should be a comprehensive JSON with all research findings

Begin!

Question: Research the topic "{input}" comprehensively. Gather:
1. An introduction/overview
2. Key findings and applications (at least 5)
3. Major challenges (at least 3)
4. Future scope and trends (at least 3)
5. Relevant statistics and data points
6. Key takeaways for the conclusion

Return a detailed JSON object with keys: 
topic, introduction, key_findings, challenges, future_scope, statistics, conclusion, sources

{agent_scratchpad}
""")


# ─────────────────────────────────────────────
# 4. Build Agent
# ─────────────────────────────────────────────
agent = create_react_agent(llm, tools, REACT_PROMPT)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=12,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
)


# ─────────────────────────────────────────────
# 5. Main Research Function
# ─────────────────────────────────────────────
def research_topic(topic: str, output_dir: str = "outputs") -> str:
    """
    Run the research agent on a topic and generate a PDF/Markdown report.
    Returns the path to the generated report.
    """
    print(f"\n{'='*60}")
    print(f"  🔍 AUTONOMOUS RESEARCH AGENT")
    print(f"  Topic: {topic}")
    print(f"{'='*60}\n")

    # Run agent
    result = agent_executor.invoke({"input": topic})
    raw_output = result["output"]

    # Try to parse JSON from agent output
    research_data = {}
    try:
        # Find JSON in output
        start = raw_output.find("{")
        end = raw_output.rfind("}") + 1
        if start != -1 and end > start:
            research_data = json.loads(raw_output[start:end])
        else:
            raise ValueError("No JSON found")
    except Exception:
        # Fallback: ask LLM to structure the output
        print("\n⚠️  Structuring output with LLM fallback...")
        structure_prompt = f"""Convert this research output into a valid JSON object with these exact keys:
topic, introduction, key_findings (list), challenges (list), future_scope (list), 
statistics (list), conclusion, sources (list).

Research output:
{raw_output}

Return ONLY valid JSON, no markdown, no explanation."""
        response = llm.invoke([HumanMessage(content=structure_prompt)])
        try:
            text = response.content
            start = text.find("{")
            end = text.rfind("}") + 1
            research_data = json.loads(text[start:end])
        except Exception as e:
            print(f"Structuring failed: {e}")
            research_data = {
                "topic": topic,
                "introduction": raw_output[:500],
                "key_findings": ["See full output"],
                "challenges": [],
                "future_scope": [],
                "statistics": [],
                "conclusion": raw_output[-300:],
                "sources": [],
            }

    research_data["topic"] = research_data.get("topic", topic)
    research_data["generated_at"] = datetime.datetime.now().strftime("%B %d, %Y")

    # Save raw JSON
    os.makedirs(output_dir, exist_ok=True)
    slug = topic.lower().replace(" ", "_")[:40]
    json_path = os.path.join(output_dir, f"{slug}_research.json")
    with open(json_path, "w") as f:
        json.dump(research_data, f, indent=2)
    print(f"\n✅ Raw research saved: {json_path}")

    # Generate report
    report_path = generate_report(research_data, output_dir)
    print(f"✅ Report generated: {report_path}")

    return report_path


# ─────────────────────────────────────────────
# 6. Entry Point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Impact of AI in Healthcare"
    report_path = research_topic(topic)
    print(f"\n🎉 Done! Report: {report_path}")
