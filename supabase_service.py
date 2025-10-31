"""
Service for interacting with Supabase database.
Handles inserting and retrieving learning paths.
"""

import os
from typing import List, Dict, Any, Optional
from supabase import create_client, Client
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Supabase client
def get_supabase_client() -> Client:
    """
    Initialize and return Supabase client.
    
    Returns:
        Client: Supabase client instance
    """
    try:
        url: str = os.environ.get("SUPABASE_URL", "")
        key: str = os.environ.get("SUPABASE_KEY", "")
        return create_client(url, key)
    except Exception as e:
        logger.error(f"Error initializing Supabase client: {str(e)}")
        raise

def insert_learning_path(
    topic: str, 
    modules: List[Dict[str, Any]], 
    youtube_recommendations: Optional[List[Dict[str, Any]]] = None,
    quiz_questions: Optional[List[Dict[str, Any]]] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Insert a learning path into the Supabase database.
    
    Args:
        topic (str): The topic of the learning path
        modules (List[Dict[str, Any]]): The modules in the learning path
        youtube_recommendations (Optional[List[Dict[str, Any]]]): YouTube recommendations
        quiz_questions (Optional[List[Dict[str, Any]]]): Quiz questions
        user_id (Optional[str]): The ID of the user who generated the path
        
    Returns:
        Dict[str, Any]: The inserted record or a mock record if database is not available
    """
    try:
        supabase = get_supabase_client()
        
        # Prepare the data to insert
        data = {
            "topic": topic,
            "modules": modules,
            "youtube_recommendations": youtube_recommendations or [],
            "quiz_questions": quiz_questions or [],
            "user_id": user_id
        }
        
        # Insert the data
        response = supabase.table("learning_paths").insert(data).execute()
        
        if response.data:
            logger.info(f"Successfully inserted learning path for topic: {topic}")
            return response.data[0]
        else:
            # Return a mock response if insertion fails
            logger.warning("Failed to insert learning path, returning mock response")
            return {
                "id": "mock-id",
                "topic": topic,
                "modules": modules,
                "youtube_recommendations": youtube_recommendations or [],
                "quiz_questions": quiz_questions or [],
                "user_id": user_id,
                "created_at": "2025-01-01T00:00:00Z"
            }
            
    except Exception as e:
        # Return a mock response if there's an error
        logger.warning(f"Error inserting learning path, returning mock response: {str(e)}")
        return {
            "id": "mock-id",
            "topic": topic,
            "modules": modules,
            "youtube_recommendations": youtube_recommendations or [],
            "quiz_questions": quiz_questions or [],
            "user_id": user_id,
            "created_at": "2025-01-01T00:00:00Z"
        }

def get_learning_path(path_id: str) -> Dict[str, Any]:
    """
    Retrieve a learning path from the Supabase database.
    
    Args:
        path_id (str): The ID of the learning path to retrieve
        
    Returns:
        Dict[str, Any]: The retrieved learning path or a mock path if database is not available
    """
    try:
        supabase = get_supabase_client()
        
        # Retrieve the data
        response = supabase.table("learning_paths").select("*").eq("id", path_id).execute()
        
        if response.data:
            return response.data[0]
        else:
            # Return a mock response if not found
            logger.warning(f"Learning path with ID {path_id} not found, returning mock response")
            return {
                "id": path_id,
                "topic": "Mock Topic",
                "modules": [{"title": "Mock Module", "subtopics": ["Mock Subtopic"]}],
                "youtube_recommendations": [],
                "quiz_questions": [],
                "created_at": "2025-01-01T00:00:00Z"
            }
            
    except Exception as e:
        # Return a mock response if there's an error
        logger.warning(f"Error retrieving learning path, returning mock response: {str(e)}")
        return {
            "id": path_id,
            "topic": "Mock Topic",
            "modules": [{"title": "Mock Module", "subtopics": ["Mock Subtopic"]}],
            "youtube_recommendations": [],
            "quiz_questions": [],
            "created_at": "2025-01-01T00:00:00Z"
        }