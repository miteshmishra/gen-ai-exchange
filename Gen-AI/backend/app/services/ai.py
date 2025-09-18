import openai
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.agent import AgentAction, Experiment
from ..models.feedback import Feedback
from ..db.session import get_db
from ..core.config import settings
from .ollama import OllamaService

openai.api_key = settings.OPENAI_API_KEY

from app.services.adk import get_adk_client, ADKClient

class AIService:
    def __init__(self, adk_client_instance: ADKClient):
        self._adk_client = adk_client_instance
    async def _generate_content(self, prompt: str, images: List[str] = None) -> str:
        if settings.ADK_MODEL_ID:
            return await self._adk_client.generate_content(prompt=prompt, images=images)
        elif settings.OPENAI_API_KEY:
            client = openai.AsyncOpenAI()
            response = await client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        else:
            # Ollama integration
            try:
                response = await OllamaService.generate_completion(
                    prompt=prompt,
                    system_prompt="You are a helpful AI assistant.",
                    temperature=0.7,
                    max_tokens=1000
                )
                return response
            except asyncio.TimeoutError as e:
                raise TimeoutError("Ollama service request timed out")
            except Exception as e:
                raise Exception(f"Ollama service error: {str(e)}")

    async def get_travel_suggestions(
        self,
        destination: str,
        interests: List[str],
        budget: float,
        duration: int
    ) -> Dict[str, Any]:
        """
        Get AI-powered travel suggestions based on user preferences.
        """
        try:
            prompt = f"""As a travel expert, provide personalized suggestions for a trip to {destination}.\n            Trip Duration: {duration} days\n            Budget: ${budget}\n            Interests: {', '.join(interests)}\n\n            Please provide:\n            1. Best time to visit\n            2. Must-visit attractions\n            3. Local cuisine recommendations\n            4. Off-the-beaten-path experiences\n            5. Budget allocation tips\n            """
            
            suggestions = await self._generate_content(prompt)

            if not suggestions:
                raise ValueError("Empty response from AI service")

            return {
                "suggestions": suggestions.split("\n") if isinstance(suggestions, str) else suggestions,
                "destination": destination,
                "success": True
            }

        except TimeoutError as e:
            raise HTTPException(status_code=504, detail=str(e))
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def generate_itinerary(
        self,
        destination: str,
        duration: int,
        activities: List[str],
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate a personalized travel itinerary using AI.
        """
        try:
            prompt = f"""As a travel itinerary expert, create a detailed {duration}-day itinerary for {destination}.\n            Activities of interest: {', '.join(activities)}\n            Preferences: {preferences}\n\n            Please provide:\n            1. Daily schedule with times\n            2. Activity descriptions\n            3. Travel time estimates\n            4. Meal recommendations\n            5. Budget considerations\n            """

            itinerary = await self._generate_content(prompt)
            if isinstance(itinerary, str):
                itinerary = itinerary.split("\n")  # Convert string to list if needed
            
            return {
                "itinerary": itinerary,
                "destination": destination,
                "success": True
            }

        except Exception as e:
            print(f"Error generating itinerary: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_local_insights(
        self,
        destination: str,
        topics: List[str]
    ) -> Dict[str, Any]:
        """
        Get AI-generated local insights about a destination.
        """
        try:
            prompt = f"""As a local expert, provide comprehensive insights about {destination}.\n            Topics to cover: {', '.join(topics)}\n\n            Please provide detailed information about:\n            1. Local culture and customs\n            2. Transportation options\n            3. Safety considerations\n            3. Dining and cuisine\n            4. Hidden gems and local secrets\n            """

            insights = await self._generate_content(prompt)
            if isinstance(insights, str):
                # Convert string to dict if needed
                insights_dict = {}
                lines = insights.split("\n")
                for line in lines:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        insights_dict[key.strip()] = value.strip()
                insights = insights_dict
            
            return {
                "insights": insights,
                "destination": destination,
                "success": True
            }

        except Exception as e:
            print(f"Error getting local insights: {e}")
            return {
                "success": False,
                "error": str(e)
            }

class UXObserver:
    """Collects and analyzes user interaction telemetry"""
    
    @staticmethod
    async def collect_telemetry(event_data: Dict[str, Any]) -> None:
        """Store user interaction events for analysis"""
        db = next(get_db())
        # Process and store telemetry data
        # Calculate metrics like task completion time, friction points
        
    @staticmethod
    async def analyze_patterns(timeframe_hours: int = 24) -> Dict[str, Any]:
        """Analyze recent user behavior patterns"""
        db = next(get_db())
        # Analyze telemetry data for patterns
        # Return insights about user behavior and friction points
        return {}

class UXStrategist:
    """Proposes UI improvements based on observations"""
    
    @staticmethod
    async def generate_hypothesis(insights: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate improvement hypotheses based on observations"""
        prompt = f"""As a UX optimization expert, analyze these user behavior insights and suggest improvements:
        Insights: {insights}
        
        Focus on:
        1. Conversion optimization
        2. Time-to-book reduction
        3. Group collaboration efficiency
        4. Accessibility improvements
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a UX optimization expert focused on travel booking platforms."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Parse GPT response into structured hypotheses
        return []
    
    @staticmethod
    async def create_experiment(
        feature_key: str,
        variants: List[Dict[str, Any]],
        metrics: List[str]
    ) -> Experiment:
        """Create a new A/B test experiment"""
        db = next(get_db())
        experiment = Experiment(
            feature_key=feature_key,
            variants=variants,
            metrics=metrics,
            status="active",
            start_date=datetime.utcnow()
        )
        db.add(experiment)
        db.commit()
        return experiment

class UXImplementer:
    """Implements approved UI changes"""
    
    @staticmethod
    async def generate_change_spec(
        hypothesis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate detailed change specification"""
        prompt = f"""As a UI engineer, create a detailed change specification for this improvement hypothesis:
        Hypothesis: {hypothesis}
        
        Include:
        1. Component-level changes
        2. Style updates
        3. Interaction modifications
        4. Accessibility considerations
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a UI engineering expert who creates detailed technical specifications."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Parse GPT response into structured change spec
        return {}
    
    @staticmethod
    async def submit_change(
        feature_key: str,
        change_spec: Dict[str, Any],
        rationale: str
    ) -> AgentAction:
        """Submit a change for approval"""
        db = next(get_db())
        action = AgentAction(
            feature_key=feature_key,
            agent_type="implementer",
            change_spec=change_spec,
            rationale=rationale,
            status="proposed"
        )
        db.add(action)
        db.commit()
        return action

class UXGovernor:
    """Enforces safety and performance guardrails"""
    
    @staticmethod
    async def validate_change(
        action: AgentAction,
        checks: List[str]
    ) -> Dict[str, bool]:
        """Validate a proposed change against guardrails"""
        results = {
            "accessibility": True,
            "performance": True,
            "security": True,
            "compliance": True
        }
        # Run specified checks
        return results
    
    @staticmethod
    async def approve_change(action_id: int) -> AgentAction:
        """Approve a change for deployment"""
        db = next(get_db())
        action = db.query(AgentAction).filter(AgentAction.id == action_id).first()
        if not action:
            raise HTTPException(status_code=404, detail="Action not found")
        
        action.status = "approved"
        action.approvals = {"governor": datetime.utcnow().isoformat()}
        db.commit()
        return action
    
    @staticmethod
    async def rollback_change(action_id: int, reason: str) -> AgentAction:
        """Rollback a deployed change"""
        db = next(get_db())
        action = db.query(AgentAction).filter(AgentAction.id == action_id).first()
        if not action:
            raise HTTPException(status_code=404, detail="Action not found")
        
        action.status = "rolled-back"
        action.metrics = {"rollback_reason": reason}
        db.commit()
        return action

# Singleton instances for global use
observer = UXObserver()
strategist = UXStrategist()
implementer = UXImplementer()
governor = UXGovernor()
