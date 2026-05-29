import json
from groq import AsyncGroq
from ..config.settings import settings
from ..logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.groq_api_key)

class OrchestratorAgent:
    def __init__(self):
        self.name = "Master Orchestrator"
        self.instructions = """
        You are the Master Orchestrator of an AI Business Operations system.
        Your job is to:
        1. Receive user requests.
        2. Analyze intent.
        3. Create a plan involving specialized agents: Sales, Support, PM, Content.
        4. Delegate tasks to them.
        5. Synthesize their outputs into a final professional response.

        Output your plan in JSON format:
        {
            "intent": "...",
            "plan": [
                {"agent": "Sales", "task": "..."},
                {"agent": "PM", "task": "..."},
                {"agent": "Content", "task": "..."}
            ]
        }
        """

    async def analyze_and_plan(self, user_request: str):
        ExecutionLogger.log(self.name, "Analyzing request and planning workflow", user_request[:50] + "...")
        
        response = await client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": user_request}
            ],
            response_format={"type": "json_object"}
        )
        
        plan_data = json.loads(response.choices[0].message.content)
        ExecutionLogger.log(self.name, "Workflow plan finalized", f"{len(plan_data.get('plan', []))} steps identified")
        return plan_data

    async def synthesize(self, original_request: str, agent_outputs: list):
        ExecutionLogger.log(self.name, "Synthesizing final response from agent outputs")
        
        context = "\n".join([f"Agent {o['agent']}: {o['output']}" for o in agent_outputs])
        
        response = await client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": "You are the Master Orchestrator. Synthesize the following agent outputs into a final professional response for the user."},
                {"role": "user", "content": f"Original Request: {original_request}\n\nAgent Outputs:\n{context}"}
            ]
        )
        
        return response.choices[0].message.content
