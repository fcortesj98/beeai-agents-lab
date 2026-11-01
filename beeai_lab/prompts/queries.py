"""Sample user inputs used by the examples. Override them with ``--query``."""

from textwrap import dedent

# Section 2
BUSINESS_IDEA_QUERY = (
    "Help me brainstorm a unique business idea for a food delivery service that doesn't exist yet."
)

# Section 3
PROJECT_EVALUATION_TEMPLATE = """
You are a senior data scientist evaluating a machine learning project proposal.

Project Details:
- Project Name: {{project_name}}
- Business Problem: {{business_problem}}
- Available Data: {{data_description}}
- Timeline: {{timeline}}
- Success Metrics: {{success_metrics}}

Please provide:
1. Feasibility assessment (1-10 scale)
2. Key technical challenges
3. Recommended approach
4. Risk mitigation strategies
5. Expected outcomes

Be specific and actionable in your recommendations.
"""

PROJECT_SCENARIOS: list[dict[str, str]] = [
    {
        "project_name": "Smart Inventory Optimization",
        "business_problem": "Reduce inventory costs while maintaining 95% product availability",
        "data_description": "2 years of sales data, supplier lead times, seasonal patterns, 500K records",
        "timeline": "3 months development, 1 month testing",
        "success_metrics": "15% cost reduction, maintain 95% availability, <2% forecast error",
    },
    {
        "project_name": "Fraud Detection System",
        "business_problem": "Detect fraudulent transactions in real-time with minimal false positives",
        "data_description": "1M transaction records, user behavior data, device fingerprints",
        "timeline": "6 months development, 2 months validation",
        "success_metrics": "95% fraud detection rate, <1% false positive rate, <100ms response time",
    },
]

# Section 4
BUSINESS_PLAN_QUERY = (
    "Create a business plan for a mobile app that helps people find and book "
    "unique local experiences in their city."
)

# Sections 5-10 (same query on purpose, to compare agent capabilities)
CYBERSECURITY_QUERY = dedent(
    """\
    Analyze the cybersecurity risks of quantum computing for financial institutions.
    What are the main threats, timeline for concern, and recommended preparation strategies?"""
)

# Section 11
MATH_QUERIES: list[str] = [
    "What is 15 + 27?",
    "Calculate 144 divided by 12",
    "I need to know what 8 times 9 equals",
    "What's (10 + 5) * 3 - 7?",
]

# Section 12
TRAVEL_QUERY = dedent(
    """\
    I'm planning a 2-week cultural immersion trip to Japan (Tokyo and Osaka) as a first-time visitor.
    I want to experience traditional culture, visit historical sites, and interact with locals.
    I speak only English and want to be respectful of Japanese customs.
    What should I know about the destination, weather expectations, and language/cultural tips?"""
)
