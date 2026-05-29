import asyncio
import os
from dotenv import load_dotenv
from app.agents.stage1_agents.orchestrator import OrchestratorAgent
from app.config.settings import settings

async def test_orchestrator():
    load_dotenv(override=True)
    orchestrator = OrchestratorAgent()
    request = "I want to buy 100 laptops for my company. Can you help me with a quote and a delivery plan?"
    print(f"Testing Orchestrator with request: {request}")
    try:
        plan = await orchestrator.analyze_and_plan(request)
        print("Plan generated:")
        print(plan)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
