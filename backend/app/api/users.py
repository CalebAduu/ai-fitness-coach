from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
import logging
from uuid import UUID
import tempfile
import os

from ..models.user import UserProfileRequest, UserProfileResponse
from ..models.plan import WorkoutPlan, MealPlan
from ..database import get_supabase_client
from ..config import settings
from ..services.voice_service import VoiceService

logger = logging.getLogger(__name__)
router = APIRouter()
voice_service = VoiceService()

@router.post("/", response_model=UserProfileResponse)
async def create_user_profile(profile: UserProfileRequest):
    """
    Create a new user profile.
    """
    try:
        supabase = get_supabase_client()
        
        # For now, we'll create a profile without auth_user_id
        # In a real implementation, this would come from authentication
        profile_data = {
            "name": profile.name,
            "sex": profile.sex,
            "age": profile.age,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "fitness_level": profile.fitness_level,
            "goals": profile.goals,
            "medical_conditions": profile.medical_conditions,
            "allergies": profile.allergies,
            "days_per_week": profile.days_per_week,
            "injuries": profile.injuries,
            "equipment": profile.equipment
        }
        
        result = supabase.table("profiles").insert(profile_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create profile")
        
        created_profile = result.data[0]
        
        return UserProfileResponse(
            id=created_profile["id"],
            age=created_profile["age"],
            sex=created_profile["sex"],
            weight_kg=created_profile["weight_kg"],
            height_cm=created_profile["height_cm"],
            fitness_level=created_profile["fitness_level"],
            goals=created_profile["goals"],
            medical_conditions=created_profile["medical_conditions"],
            allergies=created_profile["allergies"],
            days_per_week=created_profile["days_per_week"],
            injuries=created_profile["injuries"],
            equipment=created_profile["equipment"]
        )
        
    except Exception as e:
        logger.error(f"Error creating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating profile: {str(e)}")

@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: str):
    """
    Get user profile by ID.
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("profiles").select("*").eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        profile = result.data[0]
        
        return UserProfileResponse(
            id=profile["id"],
            age=profile["age"],
            sex=profile["sex"],
            weight_kg=profile["weight_kg"],
            height_cm=profile["height_cm"],
            fitness_level=profile["fitness_level"],
            goals=profile["goals"],
            medical_conditions=profile["medical_conditions"],
            allergies=profile["allergies"],
            days_per_week=profile["days_per_week"],
            injuries=profile["injuries"],
            equipment=profile["equipment"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting profile: {str(e)}")

@router.put("/{user_id}", response_model=UserProfileResponse)
async def update_user_profile(user_id: str, profile: UserProfileRequest):
    """
    Update user profile.
    """
    try:
        supabase = get_supabase_client()
        
        profile_data = {
            "sex": profile.sex,
            "age": profile.age,
            "height_cm": profile.height_cm,
            "weight_kg": profile.weight_kg,
            "fitness_level": profile.fitness_level,
            "goals": profile.goals,
            "medical_conditions": profile.medical_conditions,
            "allergies": profile.allergies,
            "days_per_week": profile.days_per_week,
            "injuries": profile.injuries,
            "equipment": profile.equipment
        }
        
        result = supabase.table("profiles").update(profile_data).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        updated_profile = result.data[0]
        
        return UserProfileResponse(
            id=updated_profile["id"],
            age=updated_profile["age"],
            sex=updated_profile["sex"],
            weight_kg=updated_profile["weight_kg"],
            height_cm=updated_profile["height_cm"],
            fitness_level=updated_profile["fitness_level"],
            goals=updated_profile["goals"],
            medical_conditions=updated_profile["medical_conditions"],
            allergies=updated_profile["allergies"],
            days_per_week=updated_profile["days_per_week"],
            injuries=updated_profile["injuries"],
            equipment=updated_profile["equipment"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating profile: {str(e)}")

@router.delete("/{user_id}")
async def delete_user_profile(user_id: str):
    """
    Delete user profile.
    """
    try:
        supabase = get_supabase_client()
        
        result = supabase.table("profiles").delete().eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return {"message": "User profile deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting profile: {str(e)}")

@router.post("/{user_id}/onboarding")
async def complete_onboarding(user_id: str):
    """
    Mark user onboarding as complete.
    """
    try:
        supabase = get_supabase_client()
        
        # Update profile to mark onboarding as complete
        result = supabase.table("profiles").update({
            "onboarding_completed": True
        }).eq("id", user_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return {"message": "Onboarding completed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing onboarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completing onboarding: {str(e)}")

@router.post("/voice-onboarding")
async def voice_onboarding(audio_file: UploadFile = File(...)):
    """
    Process voice onboarding - transcribe audio and extract user profile data.
    """
    try:
        # Validate file type
        if not voice_service.validate_audio_file(audio_file.filename):
            raise HTTPException(
                status_code=400, 
                detail="Unsupported audio format. Please use MP3, WAV, M4A, OGG, or FLAC."
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[1]) as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process voice onboarding
            result = await voice_service.process_voice_onboarding(temp_file_path)
            
            return {
                "success": True,
                "transcript": result["transcript"],
                "onboarding_data": result["onboarding_data"],
                "confidence": result["confidence"],
                "message": "Voice onboarding processed successfully. Please review and confirm the extracted data."
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in voice onboarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Voice onboarding failed: {str(e)}")

@router.post("/voice-onboarding/confirm", response_model=UserProfileResponse)
async def confirm_voice_onboarding(onboarding_data: UserProfileRequest):
    """
    Confirm and create user profile from voice onboarding data.
    """
    try:
        supabase = get_supabase_client()
        
        profile_data = {
            "name": onboarding_data.name,
            "sex": onboarding_data.sex,
            "age": onboarding_data.age,
            "height_cm": onboarding_data.height_cm,
            "weight_kg": onboarding_data.weight_kg,
            "fitness_level": onboarding_data.fitness_level,
            "goals": onboarding_data.goals,
            "medical_conditions": onboarding_data.medical_conditions,
            "allergies": onboarding_data.allergies,
            "days_per_week": onboarding_data.days_per_week,
            "injuries": onboarding_data.injuries,
            "equipment": onboarding_data.equipment
        }
        
        result = supabase.table("profiles").insert(profile_data).execute()
        
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to create profile from voice data")
        
        created_profile = result.data[0]
        
        return UserProfileResponse(
            id=created_profile["id"],
            age=created_profile["age"],
            sex=created_profile["sex"],
            weight_kg=created_profile["weight_kg"],
            height_cm=created_profile["height_cm"],
            fitness_level=created_profile["fitness_level"],
            goals=created_profile["goals"],
            medical_conditions=created_profile["medical_conditions"],
            allergies=created_profile["allergies"],
            days_per_week=created_profile["days_per_week"],
            injuries=created_profile["injuries"],
            equipment=created_profile["equipment"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error confirming voice onboarding: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating profile from voice data: {str(e)}")
