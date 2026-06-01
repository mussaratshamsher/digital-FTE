from groq import AsyncGroq
from ..config.settings import settings
import json

client = AsyncGroq(api_key=settings.GROQ_API_KEY)
# Use 8B for simple classification tasks to save tokens and latency
SMALL_MODEL = "llama-3.1-8b-instant"

class IntelligenceService:
    @staticmethod
    async def analyze_sentiment(text: str):
        prompt = f"""
        Analyze the sentiment of the following text. 
        Return a JSON object with 'sentiment' (one of: Positive, Neutral, Negative, Frustrated, Excited) 
        and 'score' (an integer from 0 to 100).
        
        SCORING RULE: 
        - 0 is extremely negative, angry, or frustrated.
        - 50 is neutral.
        - 100 is extremely positive, happy, or excited.

        Text: {text}
        """
        try:
            response = await client.chat.completions.create(
                model=SMALL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Sentiment Analysis Error: {e}")
            return {"sentiment": "Neutral", "score": 50}

    @staticmethod
    async def calculate_lead_score(customer_data: dict, interactions: list):
        prompt = f"""
        Evaluate this lead based on their profile and interaction history.
        Return a JSON object with 'score' (0-100) and 'status' (one of: cold, warm, hot, converted).

        Profile: {customer_data}
        Recent Interactions: {interactions}
        """
        try:
            response = await client.chat.completions.create(
                model=SMALL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Lead Scoring Error: {e}")
            return {"score": 10, "status": "cold"}

    @staticmethod
    async def generate_suggestions(last_message: str, history: str = ""):
        prompt = f"""
        Based on the current business conversation, suggest 3 short, professional "Next Step" actions the user might want to take.
        Suggestions should be concise (max 25 characters each).
        Return a JSON object with a 'suggestions' key containing a list of strings.

        History: {history}
        Last Message: {last_message}
        """
        try:
            response = await client.chat.completions.create(
                model=SMALL_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content).get('suggestions', [])
        except Exception as e:
            print(f"Suggestion Generation Error: {e}")
            return ["Tell me more", "Draft an email", "Create a plan"]

    @staticmethod
    async def generate_summary(history: str):
        prompt = f"""
        Provide a concise, one-sentence executive summary of the following business conversation.
        Focus on the main objective and current status.

        Conversation History:
        {history}
        """
        try:
            response = await client.chat.completions.create(
                model=SMALL_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Summary Generation Error: {e}")
            return "Ongoing business discussion."
