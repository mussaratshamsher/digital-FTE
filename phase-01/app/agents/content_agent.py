from groq import AsyncGroq
from ..config.settings import settings
from ..tools.communication_tools import CommunicationTools
from ..logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.groq_api_key)

class ContentAgent:
    def __init__(self):
        self.name = "Content Agent"
        self.instructions = """
        You are a Content Agent. Your goal is to draft professional emails, proposals, and business communications.
        Ensure a professional tone and clear structure.
        Use communication tools to send messages when requested.
        """

    async def run(self, input_text: str, context: dict = None):
        ExecutionLogger.log(self.name, "Drafting content", input_text[:50] + "...")
        
        response = await client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        ExecutionLogger.log(self.name, "Draft complete")
        return result
