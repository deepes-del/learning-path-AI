"""
Service for custom application metrics.
Extends the default Prometheus metrics with application-specific metrics.
"""

from prometheus_client import Counter, Histogram, Gauge
import time

# Custom metrics
learning_paths_generated = Counter(
    "learning_paths_generated_total",
    "Total number of learning paths generated",
    ["topic"]
)

youtube_recommendations_requested = Counter(
    "youtube_recommendations_requested_total",
    "Total number of YouTube recommendations requested"
)

quiz_questions_generated = Counter(
    "quiz_questions_generated_total",
    "Total number of quiz questions generated",
    ["topic"]
)

generation_duration = Histogram(
    "learning_path_generation_duration_seconds",
    "Time spent generating learning paths",
    ["topic"]
)

active_requests = Gauge(
    "active_learning_path_requests",
    "Number of active learning path generation requests"
)

def track_learning_path_generation(topic: str, func):
    """
    Decorator to track learning path generation metrics.
    
    Args:
        topic (str): The topic for which the learning path is being generated
        func (callable): The function to decorate
        
    Returns:
        callable: The decorated function
    """
    async def wrapper(*args, **kwargs):
        # Increment active requests
        active_requests.inc()
        
        # Record start time
        start_time = time.time()
        
        try:
            # Execute the function
            result = await func(*args, **kwargs)
            
            # Update counters
            learning_paths_generated.labels(topic=topic).inc()
            quiz_questions_generated.labels(topic=topic).inc()
            
            return result
        finally:
            # Decrement active requests
            active_requests.dec()
            
            # Record duration
            duration = time.time() - start_time
            generation_duration.labels(topic=topic).observe(duration)
    
    return wrapper