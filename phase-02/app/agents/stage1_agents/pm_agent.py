from groq import AsyncGroq
from ...config.settings import settings
from ...logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class PMAgent:
    def __init__(self):
        self.name = "Project Manager Agent"
        self.instructions = """
        You are a Project Manager Agent. Your goal is task decomposition, timeline generation, and workflow planning.
        You take high-level goals and break them down into actionable steps.
        Provide clear, numbered implementation roadmaps with estimated timelines.
        """

    async def run(self, input_text: str, context: dict = None, repo=None):
        await ExecutionLogger.log(self.name, "Planning workflow/roadmap", input_text[:50] + "...", repo)
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": input_text}
            ]
        )
        result = response.choices[0].message.content
        await ExecutionLogger.log(self.name, "Roadmap generated", None, repo)
        return result
