from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.ticket_repository import TicketRepository
from app.repositories.execution_repository import ExecutionRepository
from app.repositories.customer_repository import CustomerRepository
from app.agents.stage1_agents.orchestrator import OrchestratorAgent
from app.models.conversation_model import Conversation
from app.models.message_model import Message

from app.agents.stage1_agents.sales_agent import SalesAgent
from app.agents.stage1_agents.support_agent import SupportAgent
from app.agents.stage1_agents.pm_agent import PMAgent
from app.agents.stage1_agents.content_agent import ContentAgent
from app.services.intelligence_service import IntelligenceService
import json

class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ticket_repo = TicketRepository(db)
        self.exec_repo = ExecutionRepository(db)
        self.cust_repo = CustomerRepository(db)
        self.orchestrator = OrchestratorAgent()
        # Initialize specialized agents
        self.agents = {
            "Sales": SalesAgent(),
            "Support": SupportAgent(),
            "PM": PMAgent(),
            "Content": ContentAgent()
        }

    async def process_chat(self, customer_id: int, message_content: str, channel: str = "web"):
        # 0. Analyze Sentiment
        sentiment_data = await IntelligenceService.analyze_sentiment(message_content)

        # 1. Create/Retrieve Conversation
        conversation = Conversation(customer_id=customer_id, channel=channel)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)

        # 2. Store user message with sentiment
        user_msg = Message(
            conversation_id=conversation.id, 
            sender_type="user", 
            content=message_content,
            sentiment=sentiment_data['sentiment'],
            sentiment_score=sentiment_data['score']
        )
        self.db.add(user_msg)
        await self.db.commit()

        # 3. Trigger Orchestrator for Planning with Channel Awareness
        plan_data = await self.orchestrator.analyze_and_plan(message_content, channel, self.exec_repo)

        # 4. Execute delegated tasks with REAL agents
        outputs = []
        for step in plan_data.get('plan', []):
            agent_name = step['agent']
            task_desc = step['task']
            reasoning = step.get('reasoning', "")
            step_num = step.get('step_number', 1)
            
            if agent_name in self.agents:
                agent = self.agents[agent_name]
                output = await agent.run(task_desc, repo=self.exec_repo)
                await self.exec_repo.log_action(
                    agent_name=agent_name,
                    action=f"Completed task: {task_desc[:50]}...",
                    status="success",
                    details=output[:100],
                    reasoning=reasoning,
                    step_number=step_num
                )
                outputs.append({"agent": agent_name, "output": output})
            else:
                outputs.append({"agent": agent_name, "output": f"Agent {agent_name} not found."})

        # 5. Yield Metadata first (as JSON string)
        metadata = {
            "conversation_id": conversation.id,
            "sentiment": sentiment_data['sentiment'],
            "sentiment_score": sentiment_data['score'],
            "strategic_reasoning": plan_data.get('strategic_reasoning', "")
        }
        yield json.dumps(metadata) + "|||"

        # 6. Stream final response and capture it
        full_response = ""
        async for token in self.orchestrator.synthesize(
            message_content, 
            outputs, 
            channel, 
            plan_data.get('channel_guidelines', ""),
            self.exec_repo
        ):
            full_response += token
            yield token

        # 7. Store AI response after stream complete
        ai_msg = Message(conversation_id=conversation.id, sender_type="ai", content=full_response)
        self.db.add(ai_msg)
        
        # 8. Update Lead Score (Async)
        customer = await self.cust_repo.get_by_id(customer_id)
        if customer:
            lead_data = await IntelligenceService.calculate_lead_score(
                {"name": customer.name, "company": customer.company},
                [{"role": "user", "content": message_content}]
            )
            customer.lead_score = lead_data['score']
            customer.lead_status = lead_data['status']
            self.db.add(customer)

        await self.db.commit()
