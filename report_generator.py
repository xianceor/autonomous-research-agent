"""
Report Generator — converts structured research data into a formatted Markdown report.
"""

import os
import json
from datetime import datetime
from typing import Union


REPORT_TEMPLATE = """\
---
title: "{title}"
date: "{date}"
author: "Autonomous Research Agent (LangChain + Claude)"
---

# {title}

---

## 📋 Cover Page

| | |
|---|---|
| **Report Title** | {title} |
| **Generated On** | {date} |
| **Prepared By** | Autonomous Research Agent |
| **Powered By** | LangChain · Anthropic Claude · Tavily · Wikipedia |
| **Version** | 1.0 |

---

## 1. Introduction

{introduction}

---

## 2. Key Findings

{key_findings}

---

## 3. Challenges

{challenges}

---

## 4. Future Scope

{future_scope}

---

## 5. Statistics & Data Points

{statistics}

---

## 6. Conclusion

{conclusion}

---

## 7. Sources & References

{sources}

---

*Report generated automatically by the Autonomous Research Agent.*  
*Tools used: Web Search (Tavily), Wikipedia, LangChain ReAct Agent, Anthropic Claude.*
"""


def _format_list(items, emoji="•") -> str:
    """Format a list of strings as markdown bullet points."""
    if not items:
        return "_No data available._"
    if isinstance(items, str):
        return items
    result = []
    for item in items:
        if isinstance(item, dict):
            # Handle dict items gracefully
            title = item.get("title") or item.get("name") or item.get("finding") or ""
            detail = item.get("detail") or item.get("description") or item.get("content") or ""
            if title and detail:
                result.append(f"**{emoji} {title}**\n{detail}")
            elif title:
                result.append(f"{emoji} {title}")
            else:
                result.append(f"{emoji} {json.dumps(item)}")
        else:
            result.append(f"{emoji} {item}")
    return "\n\n".join(result)


def _format_sources(sources) -> str:
    """Format sources as a numbered markdown list."""
    if not sources:
        return "_Sources gathered via web search and Wikipedia during agent execution._"
    if isinstance(sources, str):
        return sources
    result = []
    for i, src in enumerate(sources, 1):
        if isinstance(src, dict):
            url = src.get("url") or src.get("link") or src.get("source") or ""
            title = src.get("title") or src.get("name") or url
            result.append(f"{i}. [{title}]({url})" if url else f"{i}. {title}")
        else:
            result.append(f"{i}. {src}")
    return "\n".join(result)


def generate_report(data: dict, output_dir: str = "outputs") -> str:
    """
    Generate a Markdown report from structured research data.
    Returns the path to the generated .md file.
    """
    os.makedirs(output_dir, exist_ok=True)

    topic = data.get("topic", "Research Report")
    date = data.get("generated_at", datetime.now().strftime("%B %d, %Y"))
    title = f"Research Report: {topic}"

    report_content = REPORT_TEMPLATE.format(
        title=title,
        date=date,
        introduction=data.get("introduction", "_Not available._"),
        key_findings=_format_list(data.get("key_findings", []), "✅"),
        challenges=_format_list(data.get("challenges", []), "⚠️"),
        future_scope=_format_list(data.get("future_scope", []), "🚀"),
        statistics=_format_list(data.get("statistics", []), "📊"),
        conclusion=data.get("conclusion", "_Not available._"),
        sources=_format_sources(data.get("sources", [])),
    )

    slug = topic.lower().replace(" ", "_")[:40]
    report_path = os.path.join(output_dir, f"{slug}_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return report_path


if __name__ == "__main__":
    # Quick test with sample data
    sample = {
        "topic": "Impact of AI in Healthcare",
        "generated_at": "March 24, 2025",
        "introduction": "Artificial Intelligence is rapidly transforming healthcare...",
        "key_findings": [
            "AI diagnostics achieve 94% accuracy in detecting early-stage cancers",
            "Drug discovery timelines reduced from 12 years to under 4 years using AI",
            "Predictive analytics prevent 30% of hospital readmissions",
        ],
        "challenges": [
            "Data privacy and HIPAA compliance remain major barriers",
            "Lack of interpretability (black-box AI) reduces clinician trust",
            "Unequal access to AI tools across healthcare systems",
        ],
        "future_scope": [
            "Personalized medicine driven by genomic AI models",
            "AI-powered surgical robots with sub-millimeter precision",
            "Mental health AI companions scaling care globally",
        ],
        "statistics": [
            "Global AI in healthcare market: $45.2B by 2026",
            "96% of healthcare executives plan AI investment in next 3 years",
        ],
        "conclusion": "AI in healthcare represents a paradigm shift...",
        "sources": [
            {"title": "WHO Digital Health Report", "url": "https://who.int"},
            {"title": "Nature Medicine AI Study 2024", "url": "https://nature.com"},
        ],
    }
    path = generate_report(sample, "outputs")
    print(f"Sample report: {path}")
