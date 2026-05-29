from groq import AsyncGroq
from ..config.settings import settings
from ..tools.crm_tools import CRMTools
from ..tools.knowledge_tools import KnowledgeTools
from ..logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.groq_api_key)

class SupportAgent:
    def __init__(self):
        self.name = "Support Agent"
        self.instructions = """
        You are a Support Agent for a business operations platform.
        Your goal is to handle customer inquiries, solve technical issues, and manage support tickets.
        Use the knowledge base to answer questions and CRM tools to manage tickets.
        Be polite, professional, and helpful.
        If an issue is too complex, escalate it to the Orchestrator.
        """

    async def run(self, input_text: str, context: dict = None):
        ExecutionLogger.log(self.name, "Processing support request", input_text[:50] + "...")
        
        # Simple implementation for Stage 1
        # In a real app, this would use tool calling via OpenAI
        response = await client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        ExecutionLogger.log(self.name, "Generated response", "Length: " + str(len(result)))
        return result
