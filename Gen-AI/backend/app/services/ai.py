import openai
from typing import List, Dict, Any
from ..core.config import settings

openai.api_key = settings.OPENAI_API_KEY

class AIService:
    @staticmethod
    async def get_travel_suggestions(
        destination: str,
        interests: List[str],
        budget: float,
        duration: int
    ) -> Dict[str, Any]:
        """
        Get AI-powered travel suggestions based on user preferences.
        """
        try:
            prompt = f"""As a travel expert, provide personalized suggestions for a trip to {destination}.
            Trip Duration: {duration} days
            Budget: ${budget}
            Interests: {', '.join(interests)}

            Please provide:
            1. Best time to visit
            2. Must-visit attractions
            3. Local cuisine recommendations
            4. Off-the-beaten-path experiences
            5. Budget allocation tips
            """

            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert travel advisor with deep knowledge of destinations worldwide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return {
                "suggestions": response.choices[0].message.content,
                "destination": destination,
                "success": True
            }

        except Exception as e:
            print(f"Error getting travel suggestions: {e}")
            return {
                "suggestions": "Unable to generate travel suggestions at this time.",
                "destination": destination,
                "success": False
            }

    @staticmethod
    async def generate_itinerary(
        destination: str,
        duration: int,
        activities: List[str],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a personalized travel itinerary using AI.
        """
        try:
            prompt = f"""Create a detailed {duration}-day itinerary for {destination}.
            Preferred Activities: {', '.join(activities)}
            Preferences:
            - Pace: {preferences.get('pace', 'moderate')}
            - Budget Level: {preferences.get('budget_level', 'medium')}
            - Dining Style: {preferences.get('dining', 'mixed')}

            For each day, include:
            1. Morning activities
            2. Afternoon activities
            3. Evening activities/dining
            4. Estimated costs
            5. Travel tips
            """

            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert travel planner who creates detailed, personalized itineraries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )

            return {
                "itinerary": response.choices[0].message.content,
                "destination": destination,
                "duration": duration,
                "success": True
            }

        except Exception as e:
            print(f"Error generating itinerary: {e}")
            return {
                "itinerary": "Unable to generate itinerary at this time.",
                "destination": destination,
                "duration": duration,
                "success": False
            }

    @staticmethod
    async def get_local_insights(
        destination: str,
        topics: List[str]
    ) -> Dict[str, Any]:
        """
        Get AI-generated local insights about a destination.
        """
        try:
            prompt = f"""Provide detailed local insights about {destination} covering:
            Topics of Interest: {', '.join(topics)}

            Please include:
            1. Cultural customs and etiquette
            2. Local transportation tips
            3. Safety information
            4. Best local experiences
            5. Common phrases in local language
            """

            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a local expert with deep knowledge about destinations and their cultural nuances."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            return {
                "insights": response.choices[0].message.content,
                "destination": destination,
                "success": True
            }

        except Exception as e:
            print(f"Error getting local insights: {e}")
            return {
                "insights": "Unable to generate local insights at this time.",
                "destination": destination,
                "success": False
            }
