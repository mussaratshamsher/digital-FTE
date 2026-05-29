import asyncio
import os
from dotenv import load_dotenv
from app.services.intelligence_service import IntelligenceService

async def test_intelligence():
    load_dotenv(override=True)
    
    # Test Sentiment Analysis
    text = "I am very frustrated with the slow delivery of my order!"
    print(f"\nTesting Sentiment Analysis with: {text}")
    sentiment = await IntelligenceService.analyze_sentiment(text)
    print(f"Result: {sentiment}")

    # Test Lead Scoring
    customer_data = {"name": "Tech Corp", "company": "Tech Solutions Inc"}
    interactions = [{"role": "user", "content": "We are looking for a bulk purchase of 500 AI servers."}]
    print(f"\nTesting Lead Scoring for: {customer_data['name']}")
    lead_score = await IntelligenceService.calculate_lead_score(customer_data, interactions)
    print(f"Result: {lead_score}")

if __name__ == "__main__":
    asyncio.run(test_intelligence())
