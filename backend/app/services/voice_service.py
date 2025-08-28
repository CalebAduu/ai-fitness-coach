import logging
import tempfile
import os
from typing import Optional, Dict, Any
import openai
from ..config import settings

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript.strip()
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    async def extract_onboarding_data(self, transcript: str) -> Dict[str, Any]:
        """
        Extract structured onboarding data from voice transcript using GPT-4.
        """
        try:
            prompt = f"""
            Extract user onboarding information from this voice transcript. 
            Return ONLY a JSON object with the following structure:
            {{
                "name": "user's name",
                "age": number,
                "sex": "male/female/other",
                "height_cm": number,
                "weight_kg": number,
                "fitness_level": "beginner/intermediate/advanced",
                "goals": ["goal1", "goal2"],
                "medical_conditions": ["condition1", "condition2"],
                "allergies": ["allergy1", "allergy2"],
                "days_per_week": number,
                "injuries": ["injury1", "injury2"],
                "equipment": ["equipment1", "equipment2"]
            }}
            
            Transcript: "{transcript}"
            
            If any information is missing or unclear, use reasonable defaults:
            - fitness_level: "beginner"
            - days_per_week: 3
            - goals: ["general fitness"]
            - equipment: ["bodyweight"]
            - medical_conditions, allergies, injuries: []
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured data from voice transcripts."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1
            )
            
            # Parse the JSON response
            import json
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from the response (in case it's wrapped in markdown)
            if content.startswith("```json"):
                content = content[7:-3]  # Remove ```json and ```
            elif content.startswith("```"):
                content = content[3:-3]  # Remove ``` and ```
            
            data = json.loads(content)
            return data
            
        except Exception as e:
            logger.error(f"Error extracting onboarding data: {str(e)}")
            raise Exception(f"Failed to extract onboarding data: {str(e)}")
    
    async def process_voice_onboarding(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Complete voice onboarding process: transcribe + extract data.
        """
        try:
            # Step 1: Transcribe audio to text
            transcript = await self.transcribe_audio(audio_file_path)
            logger.info(f"Transcribed text: {transcript}")
            
            # Step 2: Extract structured data
            onboarding_data = await self.extract_onboarding_data(transcript)
            logger.info(f"Extracted onboarding data: {onboarding_data}")
            
            return {
                "transcript": transcript,
                "onboarding_data": onboarding_data,
                "confidence": "high"  # Could be enhanced with confidence scoring
            }
            
        except Exception as e:
            logger.error(f"Error in voice onboarding: {str(e)}")
            raise Exception(f"Voice onboarding failed: {str(e)}")
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate that the uploaded file is a supported audio format.
        """
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in allowed_extensions
