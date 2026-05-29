import json
from groq import AsyncGroq
from ...config.settings import settings
from ...logs.execution_logger import ExecutionLogger

client = AsyncGroq(api_key=settings.GROQ_API_KEY)

class OrchestratorAgent:
    def __init__(self):
        self.name = "Master Orchestrator"
        self.instructions = """
        You are the Master Orchestrator of an AI Business Operations system.
        Your goal is to act as an autonomous employee who handles requests from different channels.

        CHANNELS & STYLE:
        - Email: Formal, detailed, include greeting/signature.
        - WhatsApp: Concise, conversational, under 300 chars.
        - Web Form: Semi-formal, helpful, structured.

        WORKFLOW:
        1. Receive request and channel info.
        2. Analyze intent and create a step-by-step plan involving specialized agents: 
           - Sales: Lead qualification, budget, pricing.
           - Support: Issues, technical questions, tickets.
           - PM: Planning, tasks, timelines.
           - Content: Writing emails, proposals, marketing.
        3. Output the plan in JSON format only.

        JSON FORMAT:
        {
            "intent": "Brief description",
            "strategic_reasoning": "High-level strategy for this request",
            "channel_guidelines": "Specific style instructions for this response",
            "plan": [
                {
                    "step_number": 1,
                    "agent": "Sales", 
                    "task": "detailed instruction",
                    "reasoning": "Why this agent is being used for this specific step"
                }
            ]
        }
        """

    async def analyze_and_plan(self, user_request: str, channel: str = "web", repo=None):
        await ExecutionLogger.log(self.name, f"Analyzing request from {channel}", user_request[:50] + "...", repo)
        
        prompt = f"Channel: {channel}\nRequest: {user_request}"
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        plan_data = json.loads(response.choices[0].message.content)
        await ExecutionLogger.log(self.name, "Workflow plan finalized", f"{len(plan_data.get('plan', []))} steps identified", repo)
        return plan_data

    async def synthesize(self, original_request: str, agent_outputs: list, channel: str, guidelines: str, repo=None):
        await ExecutionLogger.log(self.name, "Synthesizing final response (streaming)", f"Channel: {channel}", repo)
        
        context = "\n".join([f"Agent {o['agent']}: {o['output']}" for o in agent_outputs])
        
        system_prompt = f"""
        You are the Master Orchestrator. Synthesize the agent outputs into a final response.
        STRICT CHANNEL RULES:
        - Channel: {channel}
        - Guidelines: {guidelines}
        
        Ensure the output strictly follows the channel style requirements.
        """
        
        response = await client.chat.completions.create(
            model=settings.MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Original Request: {original_request}\n\nAgent Context:\n{context}"}
            ],
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
