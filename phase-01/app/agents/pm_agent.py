from groq import AsyncGroq
from ..config.settings import settings
from ..logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.groq_api_key)

class PMAgent:
    def __init__(self):
        self.name = "Project Manager Agent"
        self.instructions = """
        You are a Project Manager Agent. Your goal is task decomposition, timeline generation, and workflow planning.
        You take high-level goals and break them down into actionable steps.
        Provide clear, numbered implementation roadmaps with estimated timelines.
        """

    async def run(self, input_text: str, context: dict = None):
        ExecutionLogger.log(self.name, "Planning workflow/roadmap", input_text[:50] + "...")
        
        response = await client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        ExecutionLogger.log(self.name, "Roadmap generated")
        return result
