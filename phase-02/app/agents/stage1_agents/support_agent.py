from groq import AsyncGroq
from ...config.settings import settings
from ...tools.crm_tools import CRMTools
from ...tools.knowledge_tools import KnowledgeTools
from ...logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

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

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Processing support request", input_text[:50] + "...", repo)
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        await ExecutionLogger.log(self.name, "Generated support response", f"Length: {len(result)}", repo)
        return result
