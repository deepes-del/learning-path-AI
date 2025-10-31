"""
Main application file for Learning Path AI.
Initializes FastAPI app and includes routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from app.api import routes

# Initialize FastAPI app with increased timeout settings
app = FastAPI(
    title="Learning Path AI",
    description="AI-powered learning path generator with course structure, YouTube recommendations, and quizzes",
    version="1.0.0",
    timeout=90  # Increase timeout to 90 seconds
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routes
app.include_router(routes.router)

# Initialize Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get("/")
async def root():
    """
    Root endpoint for health check.
    
    Returns:
        dict: Simple health check response
    """
    return {"message": "Learning Path AI is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=90)