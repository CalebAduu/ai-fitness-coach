import openai
import os
import json
import logging
from typing import Dict, List, Any, Optional

from app.config import settings
from app.models.user import UserProfileResponse
from app.models.plan import WorkoutPlan, MealPlan, PlanGenerationRequest, PlanAdaptationRequest
from app.models.feedback import FeedbackAnalysis, FeedbackSummary
from app.services.external_api_service import ExternalAPIService
from app.services.rag_service import RAGService
from app.models.external_apis import KnowledgeQuery, KnowledgeResponse

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.openai_api_key)
        self.rag_service = RAGService()
        self.external_api_service = ExternalAPIService()
        logger.info("AI Service initialized with RAG knowledge base and external APIs")

    async def generate_workout_plan(self, user_profile: UserProfileResponse, week: str) -> WorkoutPlan:
        """Generate personalized workout plan using AI, RAG knowledge, and external APIs"""
        try:
            # Build context from user profile
            context = self._build_user_context(user_profile)
            
            # Get RAG knowledge context
            rag_query = f"workout plan {user_profile.goals[0] if user_profile.goals else 'general fitness'} training principles"
            rag_context = self.rag_service.get_context(rag_query)
            
            # Get external API knowledge
            knowledge_query = KnowledgeQuery(
                query=f"workout plan for {user_profile.goals[0] if user_profile.goals else 'general fitness'}",
                sources=["exercise_db", "wger"],
                include_nutrition=False,
                include_exercises=True
            )
            
            knowledge_response = await self.external_api_service.get_comprehensive_knowledge(knowledge_query)
            
            # Create enhanced prompt with RAG and external data
            prompt = self._create_workout_prompt(user_profile, week, context, rag_context, knowledge_response)
            
            # Generate plan with OpenAI
            response = await self._call_openai(prompt, "workout_plan")
            
            # Parse and validate response
            workout_plan = self._parse_workout_plan(response, week)
            return workout_plan
            
        except Exception as e:
            logger.error(f"Error generating workout plan: {e}")
            # Return a basic fallback plan
            return self._create_fallback_workout_plan(user_profile, week)

    async def generate_meal_plan(self, user_profile: UserProfileResponse, week: str) -> MealPlan:
        """Generate personalized meal plan using AI, RAG knowledge, and external nutrition data"""
        try:
            # Build context from user profile
            context = self._build_user_context(user_profile)
            
            # Get RAG knowledge context
            rag_query = f"nutrition plan {user_profile.goals[0] if user_profile.goals else 'general health'} macronutrients meal timing"
            rag_context = self.rag_service.get_context(rag_query)
            
            # Get external nutrition knowledge
            knowledge_query = KnowledgeQuery(
                query=f"nutrition plan for {user_profile.goals[0] if user_profile.goals else 'general health'}",
                sources=["usda"],
                include_nutrition=True,
                include_exercises=False
            )
            
            knowledge_response = await self.external_api_service.get_comprehensive_knowledge(knowledge_query)
            
            # Create enhanced prompt with RAG and nutrition data
            prompt = self._create_meal_prompt(user_profile, week, context, rag_context, knowledge_response)
            
            # Generate plan with OpenAI
            response = await self._call_openai(prompt, "meal_plan")
            
            # Parse and validate response
            meal_plan = self._parse_meal_plan(response, week)
            return meal_plan
            
        except Exception as e:
            logger.error(f"Error generating meal plan: {e}")
            # Return a basic fallback plan
            return self._create_fallback_meal_plan(user_profile, week)

    async def adapt_plans(self, user_profile: UserProfileResponse, feedback_analysis: FeedbackAnalysis) -> Dict[str, Any]:
        """Adapt plans based on feedback analysis using RAG knowledge and external APIs"""
        try:
            # Get RAG knowledge context
            rag_query = f"exercise modifications {feedback_analysis.adaptation_reason} injury prevention technique"
            rag_context = self.rag_service.get_context(rag_query)
            
            # Get external API knowledge
            knowledge_query = KnowledgeQuery(
                query=f"exercise modifications for {feedback_analysis.adaptation_reason}",
                sources=["exercise_db", "wger"],
                include_nutrition=True,
                include_exercises=True
            )
            
            knowledge_response = await self.external_api_service.get_comprehensive_knowledge(knowledge_query)
            
            # Create adaptation prompt with RAG and external data
            prompt = self._create_adaptation_prompt(user_profile, feedback_analysis, rag_context, knowledge_response)
            
            # Generate adaptation with OpenAI
            response = await self._call_openai(prompt, "plan_adaptation")
            
            # Parse adaptation response
            adaptation = self._parse_adaptation_response(response)
            return adaptation
            
        except Exception as e:
            logger.error(f"Error adapting plans: {e}")
            return {"message": "Unable to adapt plans at this time"}

    async def analyze_feedback(self, feedback_summary: FeedbackSummary) -> FeedbackAnalysis:
        """Analyze feedback using AI and RAG knowledge"""
        try:
            # Get RAG knowledge context for feedback analysis
            rag_query = f"workout feedback analysis {feedback_summary.avg_difficulty} difficulty soreness recovery"
            rag_context = self.rag_service.get_context(rag_query)
            
            # Create analysis prompt with RAG context
            prompt = self._create_feedback_analysis_prompt(feedback_summary, rag_context)
            
            # Generate analysis with OpenAI
            response = await self._call_openai(prompt, "feedback_analysis")
            
            # Parse analysis response
            analysis = self._parse_feedback_analysis(response)
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing feedback: {e}")
            return FeedbackAnalysis(
                overall_trend="stable",
                adaptation_needed=False,
                adaptation_reason="Analysis unavailable",
                recommendations=["Continue with current plan"]
            )

    async def search_knowledge(self, query: str, sources: List[str] = None) -> KnowledgeResponse:
        """Search knowledge from multiple sources including RAG knowledge base"""
        if sources is None:
            sources = ["rag", "usda", "exercise_db", "wger"]
        
        # Get RAG knowledge if requested
        rag_results = []
        if "rag" in sources:
            rag_results = self.rag_service.search(query, top_k=5)
        
        # Get external API knowledge
        external_sources = [s for s in sources if s != "rag"]
        knowledge_query = KnowledgeQuery(
            query=query,
            sources=external_sources,
            include_nutrition=True,
            include_exercises=True
        )
        
        external_response = await self.external_api_service.get_comprehensive_knowledge(knowledge_query)
        
        # Combine RAG and external results
        combined_content = external_response.content
        
        if rag_results:
            rag_content = "\n\n".join([f"From {r['source']}: {r['content']}" for r in rag_results])
            combined_content = f"Knowledge Base Information:\n{rag_content}\n\nExternal API Information:\n{external_response.content}"
        
        return KnowledgeResponse(
            content=combined_content,
            sources_used=sources,
            query=query
        )
    
    def search_rag_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search only the RAG knowledge base"""
        return self.rag_service.search(query, top_k)
    
    def get_rag_context(self, query: str, max_length: int = 2000) -> str:
        """Get context from RAG knowledge base"""
        return self.rag_service.get_context(query, max_length)
    
    def add_rag_document(self, content: str, source: str, doc_type: str = "md") -> str:
        """Add a new document to the RAG knowledge base"""
        return self.rag_service.add_document(content, source, doc_type)
    
    def get_rag_statistics(self) -> Dict[str, Any]:
        """Get RAG knowledge base statistics"""
        return self.rag_service.get_statistics()

    def _build_user_context(self, user_profile: UserProfileResponse) -> str:
        """Build context string from user profile"""
        context_parts = [
            f"Age: {user_profile.age}",
            f"Sex: {user_profile.sex}",
            f"Height: {user_profile.height_cm}cm",
            f"Weight: {user_profile.weight_kg}kg",
            f"Goals: {', '.join(user_profile.goals)}",
            f"Days per week: {user_profile.days_per_week}"
        ]
        
        if user_profile.injuries:
            context_parts.append(f"Injuries: {', '.join(user_profile.injuries)}")
        if user_profile.equipment:
            context_parts.append(f"Equipment: {', '.join(user_profile.equipment)}")
        
        return "; ".join(context_parts)

    def _create_workout_prompt(self, user_profile: UserProfileResponse, week: str, 
                             context: str, rag_context: str, knowledge_response: KnowledgeResponse) -> str:
        """Create enhanced workout generation prompt with RAG knowledge"""
        prompt = f"""
        Generate a personalized workout plan for week {week}.
        
        User Context: {context}
        
        Training Principles and Guidelines:
        {rag_context}
        
        Available Exercise Data: {knowledge_response.content}
        
        Requirements:
        1. Create a {user_profile.days_per_week}-day workout plan
        2. Focus on user goals: {', '.join(user_profile.goals)}
        3. Consider injuries: {', '.join(user_profile.injuries) if user_profile.injuries else 'None'}
        4. Use available equipment: {', '.join(user_profile.equipment) if user_profile.equipment else 'Bodyweight'}
        5. Follow proper exercise progression and training principles
        6. Include warm-up and cool-down recommendations
        7. Apply injury prevention strategies
        
        Return the plan in this exact JSON format:
        {{
            "week": "{week}",
            "days": [
                {{
                    "day": 1,
                    "focus": "Muscle Group",
                    "exercises": [
                        {{
                            "name": "Exercise Name",
                            "sets": 3,
                            "reps": "8-10",
                            "rir": 2,
                            "notes": "Optional technique notes"
                        }}
                    ]
                }}
            ]
        }}
        """
        return prompt

    def _create_meal_prompt(self, user_profile: UserProfileResponse, week: str, 
                          context: str, rag_context: str, knowledge_response: KnowledgeResponse) -> str:
        """Create enhanced meal generation prompt with RAG knowledge"""
        # Calculate basic macros based on user profile
        bmr = self._calculate_bmr(user_profile)
        tdee = self._calculate_tdee(bmr, user_profile.goals)
        macros = self._calculate_macros(tdee, user_profile.goals)
        
        prompt = f"""
        Generate a personalized meal plan for week {week}.
        
        User Context: {context}
        
        Daily Targets:
        - Calories: {macros['calories']}
        - Protein: {macros['protein']}g
        - Carbs: {macros['carbs']}g
        - Fat: {macros['fat']}g
        
        Nutrition Principles and Guidelines:
        {rag_context}
        
        Available Nutrition Data: {knowledge_response.content}
        
        Requirements:
        1. Create 7 days of meals
        2. Meet daily macro targets
        3. Consider user preferences and restrictions
        4. Include variety and balance
        5. Follow proper meal timing principles
        6. Ensure adequate hydration recommendations
        
        Return the plan in this exact JSON format:
        {{
            "week": "{week}",
            "daily": [
                {{
                    "day": 1,
                    "targets": {{
                        "cal": {macros['calories']},
                        "protein_g": {macros['protein']},
                        "carb_g": {macros['carbs']},
                        "fat_g": {macros['fat']}
                    }},
                    "meals": [
                        {{
                            "name": "Breakfast",
                            "items": ["Food item 1", "Food item 2"],
                            "calories": 600,
                            "protein_g": 30,
                            "carb_g": 60,
                            "fat_g": 20
                        }}
                    ]
                }}
            ]
        }}
        """
        return prompt

    def _create_adaptation_prompt(self, user_profile: UserProfileResponse, 
                                feedback_analysis: FeedbackAnalysis, 
                                rag_context: str, knowledge_response: KnowledgeResponse) -> str:
        """Create plan adaptation prompt with RAG knowledge"""
        prompt = f"""
        Adapt the current workout and meal plans based on user feedback.
        
        User Context: {self._build_user_context(user_profile)}
        
        Feedback Analysis:
        - Overall Trend: {feedback_analysis.overall_trend}
        - Adaptation Needed: {feedback_analysis.adaptation_needed}
        - Reason: {feedback_analysis.adaptation_reason}
        - Recommendations: {', '.join(feedback_analysis.recommendations)}
        
        Training Principles and Safety Guidelines:
        {rag_context}
        
        Available Exercise and Nutrition Data: {knowledge_response.content}
        
        Provide specific adaptations for:
        1. Exercise modifications (if needed)
        2. Intensity adjustments
        3. Volume changes
        4. Nutrition adjustments (if needed)
        5. Recovery recommendations
        6. Injury prevention strategies
        
        Return adaptations in JSON format with specific changes to implement.
        """
        return prompt

    def _create_feedback_analysis_prompt(self, feedback_summary: FeedbackSummary, rag_context: str) -> str:
        """Create feedback analysis prompt with RAG knowledge"""
        prompt = f"""
        Analyze the following workout feedback and provide insights.
        
        Feedback Summary:
        - Average Difficulty: {feedback_summary.avg_difficulty}/10
        - Average Soreness: {feedback_summary.avg_soreness}/10
        - Pain Reports: {feedback_summary.pain_count}/{feedback_summary.total_workouts}
        - Average Enjoyment: {feedback_summary.avg_enjoyment}/5
        - Recent Feedback: {feedback_summary.recent_feedback}
        
        Training Principles and Recovery Guidelines:
        {rag_context}
        
        Analyze and provide:
        1. Overall trend assessment
        2. Whether adaptation is needed
        3. Specific adaptation reasons
        4. Recommendations for improvement
        5. Safety considerations
        
        Return analysis in structured format.
        """
        return prompt

    async def _call_openai(self, prompt: str, response_type: str) -> str:
        """Make OpenAI API call with error handling"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert fitness coach and nutritionist. Provide accurate, safe, and personalized advice."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            raise

    def _parse_workout_plan(self, response: str, week: str) -> WorkoutPlan:
        """Parse OpenAI response into WorkoutPlan"""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            data = json.loads(json_str)
            return WorkoutPlan(**data)
        except Exception as e:
            logger.error(f"Failed to parse workout plan: {e}")
            raise

    def _parse_meal_plan(self, response: str, week: str) -> MealPlan:
        """Parse OpenAI response into MealPlan"""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            json_str = response[json_start:json_end]
            
            data = json.loads(json_str)
            return MealPlan(**data)
        except Exception as e:
            logger.error(f"Failed to parse meal plan: {e}")
            raise

    def _parse_adaptation_response(self, response: str) -> Dict[str, Any]:
        """Parse adaptation response"""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"message": response}
        except Exception as e:
            logger.error(f"Failed to parse adaptation response: {e}")
            return {"message": response}

    def _parse_feedback_analysis(self, response: str) -> FeedbackAnalysis:
        """Parse feedback analysis response"""
        try:
            # Simple parsing for now - could be enhanced
            return FeedbackAnalysis(
                overall_trend="stable",
                adaptation_needed=False,
                adaptation_reason="Analysis completed",
                recommendations=[response]
            )
        except Exception as e:
            logger.error(f"Failed to parse feedback analysis: {e}")
            return FeedbackAnalysis(
                overall_trend="stable",
                adaptation_needed=False,
                adaptation_reason="Analysis failed",
                recommendations=["Continue with current plan"]
            )

    def _calculate_bmr(self, user_profile: UserProfileResponse) -> float:
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if user_profile.sex.lower() == "male":
            bmr = 10 * user_profile.weight_kg + 6.25 * user_profile.height_cm - 5 * user_profile.age + 5
        else:
            bmr = 10 * user_profile.weight_kg + 6.25 * user_profile.height_cm - 5 * user_profile.age - 161
        return bmr

    def _calculate_tdee(self, bmr: float, goals: List[str]) -> float:
        """Calculate Total Daily Energy Expenditure"""
        # Activity multiplier (assuming moderate activity)
        activity_multiplier = 1.55
        
        # Goal adjustments
        if any("lose" in goal.lower() or "weight" in goal.lower() for goal in goals):
            return bmr * activity_multiplier * 0.85  # 15% deficit
        elif any("gain" in goal.lower() or "muscle" in goal.lower() for goal in goals):
            return bmr * activity_multiplier * 1.1   # 10% surplus
        else:
            return bmr * activity_multiplier  # Maintenance

    def _calculate_macros(self, tdee: float, goals: List[str]) -> Dict[str, float]:
        """Calculate macronutrient targets"""
        if any("gain" in goal.lower() or "muscle" in goal.lower() for goal in goals):
            # Higher protein for muscle building
            protein_ratio = 0.25
            carb_ratio = 0.45
            fat_ratio = 0.30
        elif any("lose" in goal.lower() or "weight" in goal.lower() for goal in goals):
            # Higher protein for weight loss
            protein_ratio = 0.30
            carb_ratio = 0.35
            fat_ratio = 0.35
        else:
            # Balanced macros
            protein_ratio = 0.20
            carb_ratio = 0.50
            fat_ratio = 0.30
        
        return {
            "calories": round(tdee),
            "protein": round((tdee * protein_ratio) / 4),  # 4 cal/g protein
            "carbs": round((tdee * carb_ratio) / 4),       # 4 cal/g carbs
            "fat": round((tdee * fat_ratio) / 9)           # 9 cal/g fat
        }

    def _create_fallback_workout_plan(self, user_profile: UserProfileResponse, week: str) -> WorkoutPlan:
        """Create a basic fallback workout plan"""
        return WorkoutPlan(
            week=week,
            days=[
                {
                    "day": 1,
                    "focus": "Full Body",
                    "exercises": [
                        {"name": "Push-ups", "sets": 3, "reps": "8-12", "rir": 2},
                        {"name": "Squats", "sets": 3, "reps": "12-15", "rir": 2},
                        {"name": "Plank", "sets": 3, "reps": "30-60s", "rir": 0}
                    ]
                }
            ]
        )

    def _create_fallback_meal_plan(self, user_profile: UserProfileResponse, week: str) -> MealPlan:
        """Create a basic fallback meal plan"""
        return MealPlan(
            week=week,
            daily=[
                {
                    "day": 1,
                    "targets": {"cal": 2000, "protein_g": 150, "carb_g": 200, "fat_g": 70},
                    "meals": [
                        {
                            "name": "Breakfast",
                            "items": ["Oatmeal with berries", "Greek yogurt", "Nuts"],
                            "calories": 400,
                            "protein_g": 20,
                            "carb_g": 50,
                            "fat_g": 15
                        }
                    ]
                }
            ]
        )
