from typing import List, Dict
from ..logs.execution_logger import ExecutionLogger

class KnowledgeTools:
    MOCK_KB = {
        "ai automation": "AI automation can reduce operational costs by up to 40% in the first year.",
        "pricing": "Our pricing starts at $5,000/month for the basic agent workforce package.",
        "onboarding": "Onboarding typically takes 2-4 weeks depending on system complexity.",
        "support": "We offer 24/7 technical support through our AI Support Agents."
    }

    @staticmethod
    async def search_knowledge_base(query: str) -> str:
        ExecutionLogger.log("Knowledge Base", f"Searching for: {query}")
        query = query.lower()
        for key, value in KnowledgeTools.MOCK_KB.items():
            if key in query:
                return value
        return "No specific information found. Please escalate to a human manager if necessary."
