"""
API routes for the Learning Path AI application.
Contains endpoints for generating learning paths and exposing metrics.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from app.schemas.learning_path import LearningPathRequest, LearningPathResponse
from app.services import supabase_service, gemini_service
from app.services.youtube_service import enhance_learning_path_with_youtube
from app.services.metrics_service import (
    learning_paths_generated,
    youtube_recommendations_requested,
    quiz_questions_generated,
    generation_duration,
    active_requests
)
import time

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=LearningPathResponse)
async def generate_learning_path(request: LearningPathRequest):
    """
    Generate a learning path for a given topic.
    
    Args:
        request (LearningPathRequest): Request containing the topic
        
    Returns:
        LearningPathResponse: Generated learning path with modules, YouTube recommendations, and quizzes
    """
    # Increment active requests
    active_requests.inc()
    
    # Record start time
    start_time = time.time()
    
    try:
        # Generate content using Gemini
        generated_content = await gemini_service.generate_learning_path_content(request.topic)
        
        # Create a learning path object with the generated content
        learning_path = {
            "topic": request.topic,
            "modules": generated_content["modules"],
            "youtube_recommendations": generated_content.get("youtube_recommendations", []),
            "quiz_questions": generated_content.get("quiz_questions", [])
        }
        
        # Enhance with real YouTube videos
        enhanced_learning_path = enhance_learning_path_with_youtube(request.topic, learning_path)
        
        # Update metrics
        learning_paths_generated.labels(topic=request.topic).inc()
        youtube_recommendations_requested.inc(len(enhanced_learning_path.get("youtube_recommendations", [])))
        quiz_questions_generated.labels(topic=request.topic).inc(len(enhanced_learning_path.get("quiz_questions", [])))
        
        # Store in Supabase
        stored_path = supabase_service.insert_learning_path(
            topic=request.topic,
            modules=enhanced_learning_path["modules"],
            youtube_recommendations=enhanced_learning_path.get("youtube_recommendations", []),
            quiz_questions=enhanced_learning_path.get("quiz_questions", []),
            user_id=getattr(request, "user_id", None)
        )
        
        # Return the generated content
        return LearningPathResponse(
            id=stored_path["id"],
            topic=request.topic,
            modules=enhanced_learning_path["modules"],
            youtube_recommendations=enhanced_learning_path["youtube_recommendations"],
            quiz_questions=enhanced_learning_path["quiz_questions"]
        )
    except Exception as e:
        logger.error(f"Error generating learning path: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Decrement active requests
        active_requests.dec()
        
        # Record duration
        duration = time.time() - start_time
        generation_duration.labels(topic=request.topic).observe(duration)

@router.get("/learning-path/{path_id}", response_model=LearningPathResponse)
async def get_learning_path(path_id: str):
    """
    Retrieve a learning path by ID.
    
    Args:
        path_id (str): The ID of the learning path to retrieve
        
    Returns:
        LearningPathResponse: The requested learning path
    """
    try:
        # Retrieve from Supabase
        stored_path = supabase_service.get_learning_path(path_id)
        
        # Return the learning path
        return LearningPathResponse(
            id=stored_path["id"],
            topic=stored_path["topic"],
            modules=stored_path["modules"],
            youtube_recommendations=stored_path.get("youtube_recommendations", []),
            quiz_questions=stored_path.get("quiz_questions", [])
        )
    except Exception as e:
        logger.error(f"Error retrieving learning path: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"}