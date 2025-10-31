"""
Pydantic models for learning path generation requests and responses.
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import datetime

class LearningPathRequest(BaseModel):
    """
    Request model for generating a learning path.
    """
    topic: str
    user_id: Optional[str] = None

class Module(BaseModel):
    """
    Represents a module in the learning path.
    """
    title: str
    subtopics: List[str]

class YouTubeRecommendation(BaseModel):
    """
    Represents a YouTube recommendation.
    """
    title: str
    url: str
    keywords: List[str]

class QuizQuestion(BaseModel):
    """
    Represents a quiz question.
    """
    question: str
    options: List[str]
    correct_answer: str

class LearningPathResponse(BaseModel):
    """
    Response model for generated learning path.
    """
    id: str
    topic: str
    modules: List[Module]
    youtube_recommendations: List[YouTubeRecommendation]
    quiz_questions: List[QuizQuestion]