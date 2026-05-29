from groq import AsyncGroq
from ...config.settings import settings
from ...tools.crm_tools import CRMTools
from ...logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class SalesAgent:
    def __init__(self):
        self.name = "Sales Agent"
        self.instructions = """
        You are a Sales Agent. Your goal is to qualify leads, analyze budgets, and recommend services.
        Use CRM tools to track lead progress. 
        Focus on value proposition and identifying business needs.
        Always provide a structured lead qualification report.
        """

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Analyzing lead/opportunity", input_text[:50] + "...", repo)
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        await ExecutionLogger.log(self.name, "Lead analysis complete", None, repo)
        return result
