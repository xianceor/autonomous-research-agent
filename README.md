# 🤖 Autonomous Research Agent
### LangChain + Anthropic Claude | Assignment 2

An AI-powered agent that autonomously researches any topic, synthesizes information from multiple sources, and generates structured, professional research reports.

---

## 🏗️ Architecture

```
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
    Content Analyzer
    (LLM-powered tool)
           │
           ▼
  Structured JSON Data
           │
           ▼
    Report Generator
           │
           ▼
  📄 Markdown Report
```

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| **Tavily Web Search** | Real-time internet search for current data, statistics, case studies |
| **Wikipedia** | Background knowledge, definitions, historical context |
| **LLM Analyzer** | Synthesizes and extracts key insights from gathered information |

## 🚀 Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/autonomous-research-agent.git
cd autonomous-research-agent
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
```bash
cp .env.example .env
# Edit .env and add your API keys:
# ANTHROPIC_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here
```

**Get your API keys:**
- Anthropic: https://console.anthropic.com/
- Tavily (free tier available): https://tavily.com/

### 4. Run the Agent
```bash
# Default topic
python agent.py

# Custom topic
python agent.py "Quantum Computing Applications in Cryptography"
python agent.py "Impact of AI in Healthcare"
python agent.py "Future of Electric Vehicles"
```

## 📁 Project Structure

```
research-agent/
├── agent.py              # Main agent — ReAct agent, tools, orchestration
├── report_generator.py   # Converts research data → formatted Markdown report
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── outputs/              # Generated reports (auto-created)
    ├── *_research.json   # Raw structured research data
    └── *_report.md       # Final formatted report
```

## 📋 Output Format

Every generated report includes:

1. **Cover Page** — Title, date, tools used
2. **Introduction** — Overview and context of the topic
3. **Key Findings** — 5+ major insights with supporting evidence
4. **Challenges** — 3+ significant obstacles or limitations
5. **Future Scope** — Emerging trends and forward-looking analysis
6. **Statistics & Data Points** — Quantitative evidence
7. **Conclusion** — Summary and key takeaways
8. **Sources & References** — All sources used during research

## 📄 Sample Outputs

| Topic | Report |
|-------|--------|
| Impact of AI in Healthcare | [outputs/sample1_ai_healthcare_report.md](outputs/sample1_ai_healthcare_report.md) |
| Role of Technology in Combating Climate Change | [outputs/sample2_climate_tech_report.md](outputs/sample2_climate_tech_report.md) |

## 🧠 How the ReAct Agent Works

The agent uses **ReAct (Reasoning + Acting)** — a prompting strategy that interleaves:

1. **Thought** — The agent reasons about what to do next
2. **Action** — Selects and calls the appropriate tool
3. **Observation** — Receives and processes the tool's output
4. Repeats until sufficient information is gathered
5. **Final Answer** — Synthesizes all findings into structured JSON

This loop allows the agent to adaptively gather information, fill knowledge gaps, and produce comprehensive research across up to 12 iterations.

## ⚙️ Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `model` | `claude-3-5-sonnet-20241022` | Anthropic model to use |
| `max_iterations` | `12` | Maximum agent reasoning steps |
| `max_results` | `5` | Web search results per query |
| `temperature` | `0.3` | LLM creativity (lower = more factual) |

## 📦 Dependencies

- `langchain` — Agent framework and tool orchestration
- `langchain-anthropic` — Anthropic Claude integration
- `langchain-community` — Wikipedia and other community tools
- `tavily-python` — Web search API client
- `python-dotenv` — Environment variable management

---

*Built for Assignment 2 — Autonomous Research Agent | LangChain*
