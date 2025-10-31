"""
Service for interacting with Google Gemini API.
Handles generation of learning path content.
"""

import os
import google.generativeai as genai
from typing import Dict, List, Any
import logging
import json
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
def configure_gemini():
    """
    Configure the Gemini API client.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    genai.configure(api_key=api_key)

async def generate_learning_path_content(topic: str) -> Dict[str, Any]:
    """
    Generate learning path content for a given topic using Gemini.
    
    Args:
        topic (str): The topic to generate content for
        
    Returns:
        Dict[str, Any]: Generated content including modules, YouTube recommendations, and quiz questions
    """
    try:
        configure_gemini()
        
        # Use a working model from the list we saw earlier
        # Let's try gemini-1.5-flash which should be stable and faster
        model_name = "gemini-1.5-flash"
        logger.info(f"Using model: {model_name}")
        model = genai.GenerativeModel(model_name)
        
        # Prepare the prompt with more detailed instructions
        prompt = f"""
        You are an expert educational content creator. Generate a comprehensive learning path for "{topic}".
        
        Return ONLY a valid JSON object with EXACTLY the following structure and nothing else:
        
        {{
            "modules": [
                {{
                    "title": "Module Title",
                    "subtopics": ["Subtopic 1", "Subtopic 2", "Subtopic 3", "Subtopic 4", "Subtopic 5"]
                }}
            ],
            "youtube_recommendations": [
                {{
                    "title": "Video Title",
                    "url": "https://youtube.com/watch?v=example",
                    "keywords": ["keyword1", "keyword2", "keyword3"]
                }}
            ],
            "quiz_questions": [
                {{
                    "question": "Quiz Question?",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer": "Option A"
                }}
            ]
        }}
        
        Requirements:
        1. Provide EXACTLY 5 modules with progressive difficulty
        2. Each module should have EXACTLY 5 detailed subtopics
        3. Provide EXACTLY 5 high-quality YouTube recommendations with real educational channels
        4. Provide EXACTLY 10 quiz questions with 4 options each
        5. Ensure all content is directly relevant to "{topic}"
        6. Make subtopics specific and actionable
        7. YouTube recommendations should be from reputable educational channels
        8. Quiz questions should test understanding of key concepts
        9. DO NOT include any explanatory text, only the JSON object
        10. DO NOT use markdown formatting or code blocks
        
        Example for "Python Programming":
        {{
            "modules": [
                {{
                    "title": "Python Basics",
                    "subtopics": ["Variables and Data Types", "Operators", "Control Flow", "Functions", "Data Structures"]
                }},
                {{
                    "title": "Object-Oriented Programming",
                    "subtopics": ["Classes and Objects", "Inheritance", "Polymorphism", "Encapsulation", "Abstraction"]
                }}
            ],
            "youtube_recommendations": [
                {{
                    "title": "Python Tutorial for Beginners",
                    "url": "https://youtube.com/watch?v=example1",
                    "keywords": ["python", "beginner", "tutorial"]
                }}
            ],
            "quiz_questions": [
                {{
                    "question": "What is Python?",
                    "options": ["A programming language", "A snake", "A computer", "An IDE"],
                    "correct_answer": "A programming language"
                }}
            ]
        }}
        """
        
        # Generate content with a longer timeout
        response = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: model.generate_content(prompt)
            ), 
            timeout=90.0
        )
        
        # Parse the response
        try:
            # Try to parse as JSON
            content = json.loads(response.text)
        except json.JSONDecodeError:
            # If that fails, try to extract JSON from the response
            # This handles cases where Gemini includes explanatory text
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                content = json.loads(json_match.group())
            else:
                # If we can't parse JSON, create a default structure
                logger.warning("Could not parse JSON from Gemini response, creating default structure")
                content = {
                    "modules": [
                        {
                            "title": f"Introduction to {topic}",
                            "subtopics": [f"Basics of {topic}", f"Fundamentals of {topic}", f"Getting Started with {topic}", f"Core Concepts of {topic}", f"Overview of {topic}"]
                        },
                        {
                            "title": f"Intermediate {topic}",
                            "subtopics": [f"Advanced {topic} Concepts", f"{topic} Best Practices", f"Real-world {topic} Applications", f"{topic} Tools and Techniques", f"Problem Solving with {topic}"]
                        }
                    ],
                    "youtube_recommendations": [
                        {
                            "title": f"Learn {topic}",
                            "url": "https://youtube.com",
                            "keywords": [topic.lower(), "tutorial"]
                        }
                    ],
                    "quiz_questions": [
                        {
                            "question": f"What is {topic}?",
                            "options": ["A", "B", "C", "D"],
                            "correct_answer": "A"
                        }
                    ]
                }
        
        # Ensure we have the required number of items
        if "modules" not in content or len(content["modules"]) < 2:
            content["modules"] = [
                {
                    "title": f"Foundations of {topic}",
                    "subtopics": [f"Introduction to {topic}", f"Basic Principles", f"Core Components", f"Essential Tools", f"Getting Started"]
                },
                {
                    "title": f"Intermediate {topic}",
                    "subtopics": [f"Advanced Concepts", f"Practical Applications", f"Problem Solving", f"Best Practices", f"Real-world Examples"]
                },
                {
                    "title": f"Advanced {topic}",
                    "subtopics": [f"Expert Techniques", f"Optimization Strategies", f"Industry Applications", f"Cutting-edge Developments", f"Future Trends"]
                }
            ]
            
        if "youtube_recommendations" not in content or len(content["youtube_recommendations"]) < 3:
            content["youtube_recommendations"] = [
                {
                    "title": f"Complete {topic} Course for Beginners",
                    "url": "https://youtube.com/watch?v=beginner",
                    "keywords": [topic.lower(), "course", "beginner"]
                },
                {
                    "title": f"Advanced {topic} Tutorial",
                    "url": "https://youtube.com/watch?v=advanced",
                    "keywords": [topic.lower(), "tutorial", "advanced"]
                },
                {
                    "title": f"{topic} Projects and Examples",
                    "url": "https://youtube.com/watch?v=projects",
                    "keywords": [topic.lower(), "projects", "examples"]
                },
                {
                    "title": f"{topic} Tips and Tricks",
                    "url": "https://youtube.com/watch?v=tips",
                    "keywords": [topic.lower(), "tips", "tricks"]
                },
                {
                    "title": f"Mastering {topic}",
                    "url": "https://youtube.com/watch?v=master",
                    "keywords": [topic.lower(), "master", "expert"]
                }
            ]
            
        if "quiz_questions" not in content or len(content["quiz_questions"]) < 5:
            content["quiz_questions"] = [
                {
                    "question": f"What is the primary purpose of {topic}?",
                    "options": [f"To solve {topic}-related problems", "To create art", "To play games", "To browse the internet"],
                    "correct_answer": f"To solve {topic}-related problems"
                },
                {
                    "question": f"Which of these is a fundamental concept in {topic}?",
                    "options": ["Core principle 1", "Random concept", "Irrelevant topic", "Unrelated field"],
                    "correct_answer": "Core principle 1"
                },
                {
                    "question": f"What is an important skill in {topic}?",
                    "options": ["Key skill", "Unrelated ability", "Irrelevant knowledge", "Random talent"],
                    "correct_answer": "Key skill"
                },
                {
                    "question": f"What tool is commonly used in {topic}?",
                    "options": ["Essential tool", "Unrelated software", "Irrelevant application", "Random program"],
                    "correct_answer": "Essential tool"
                },
                {
                    "question": f"What is a benefit of learning {topic}?",
                    "options": ["Key benefit", "Unrelated advantage", "Irrelevant gain", "Random improvement"],
                    "correct_answer": "Key benefit"
                },
                {
                    "question": f"What is a common challenge in {topic}?",
                    "options": ["Typical difficulty", "Unrelated obstacle", "Irrelevant problem", "Random issue"],
                    "correct_answer": "Typical difficulty"
                },
                {
                    "question": f"What is an advanced technique in {topic}?",
                    "options": ["Expert method", "Basic approach", "Simple technique", "Elementary strategy"],
                    "correct_answer": "Expert method"
                },
                {
                    "question": f"What is a best practice in {topic}?",
                    "options": ["Recommended approach", "Outdated method", "Inefficient technique", "Poor strategy"],
                    "correct_answer": "Recommended approach"
                },
                {
                    "question": f"What is a real-world application of {topic}?",
                    "options": ["Practical use case", "Theoretical concept", "Academic exercise", "Hypothetical scenario"],
                    "correct_answer": "Practical use case"
                },
                {
                    "question": f"What is the future of {topic}?",
                    "options": ["Emerging trend", "Declining field", "Stagnant area", "Obsolete technology"],
                    "correct_answer": "Emerging trend"
                }
            ]
        
        return content
        
    except asyncio.TimeoutError:
        logger.error(f"Timeout while generating content for topic: {topic}")
        # Return a default structure in case of timeout
        return {
            "modules": [
                {
                    "title": f"Introduction to {topic}",
                    "subtopics": [f"Basics of {topic}", f"Fundamentals of {topic}", f"Getting Started with {topic}", f"Core Concepts of {topic}", f"Overview of {topic}"]
                },
                {
                    "title": f"Intermediate {topic}",
                    "subtopics": [f"Advanced {topic} Concepts", f"{topic} Best Practices", f"Real-world {topic} Applications", f"{topic} Tools and Techniques", f"Problem Solving with {topic}"]
                },
                {
                    "title": f"Advanced {topic}",
                    "subtopics": [f"Expert Techniques", f"Optimization Strategies", f"Industry Applications", f"Cutting-edge Developments", f"Future Trends"]
                }
            ],
            "youtube_recommendations": [
                {
                    "title": f"Complete {topic} Tutorial for Beginners",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "tutorial", "beginner"]
                },
                {
                    "title": f"Advanced {topic} Techniques",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "advanced", "techniques"]
                },
                {
                    "title": f"{topic} Projects and Examples",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "projects", "examples"]
                },
                {
                    "title": f"{topic} Tips and Tricks",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "tips", "tricks"]
                },
                {
                    "title": f"Mastering {topic}",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "master", "expert"]
                }
            ],
            "quiz_questions": [
                {
                    "question": f"What is {topic} primarily used for?",
                    "options": [f"To solve {topic}-related problems", "To create art", "To play games", "To browse the internet"],
                    "correct_answer": f"To solve {topic}-related problems"
                },
                {
                    "question": f"Which of these is a fundamental concept in {topic}?",
                    "options": ["Core principle 1", "Random concept", "Irrelevant topic", "Unrelated field"],
                    "correct_answer": "Core principle 1"
                },
                {
                    "question": f"What is an important skill in {topic}?",
                    "options": ["Key skill", "Unrelated ability", "Irrelevant knowledge", "Random talent"],
                    "correct_answer": "Key skill"
                },
                {
                    "question": f"What tool is commonly used in {topic}?",
                    "options": ["Essential tool", "Unrelated software", "Irrelevant application", "Random program"],
                    "correct_answer": "Essential tool"
                },
                {
                    "question": f"What is a benefit of learning {topic}?",
                    "options": ["Key benefit", "Unrelated advantage", "Irrelevant gain", "Random improvement"],
                    "correct_answer": "Key benefit"
                },
                {
                    "question": f"What is a common challenge in {topic}?",
                    "options": ["Typical difficulty", "Unrelated obstacle", "Irrelevant problem", "Random issue"],
                    "correct_answer": "Typical difficulty"
                },
                {
                    "question": f"What is an advanced technique in {topic}?",
                    "options": ["Expert method", "Basic approach", "Simple technique", "Elementary strategy"],
                    "correct_answer": "Expert method"
                },
                {
                    "question": f"What is a best practice in {topic}?",
                    "options": ["Recommended approach", "Outdated method", "Inefficient technique", "Poor strategy"],
                    "correct_answer": "Recommended approach"
                },
                {
                    "question": f"What is a real-world application of {topic}?",
                    "options": ["Practical use case", "Theoretical concept", "Academic exercise", "Hypothetical scenario"],
                    "correct_answer": "Practical use case"
                },
                {
                    "question": f"What is the future of {topic}?",
                    "options": ["Emerging trend", "Declining field", "Stagnant area", "Obsolete technology"],
                    "correct_answer": "Emerging trend"
                }
            ]
        }
    except Exception as e:
        logger.error(f"Error generating learning path content: {str(e)}")
        # Return a default structure in case of error
        return {
            "modules": [
                {
                    "title": f"Introduction to {topic}",
                    "subtopics": [f"Basics of {topic}", f"Fundamentals of {topic}", f"Getting Started with {topic}", f"Core Concepts of {topic}", f"Overview of {topic}"]
                },
                {
                    "title": f"Intermediate {topic}",
                    "subtopics": [f"Advanced {topic} Concepts", f"{topic} Best Practices", f"Real-world {topic} Applications", f"{topic} Tools and Techniques", f"Problem Solving with {topic}"]
                },
                {
                    "title": f"Advanced {topic}",
                    "subtopics": [f"Expert Techniques", f"Optimization Strategies", f"Industry Applications", f"Cutting-edge Developments", f"Future Trends"]
                }
            ],
            "youtube_recommendations": [
                {
                    "title": f"Complete {topic} Tutorial for Beginners",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "tutorial", "beginner"]
                },
                {
                    "title": f"Advanced {topic} Techniques",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "advanced", "techniques"]
                },
                {
                    "title": f"{topic} Projects and Examples",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "projects", "examples"]
                },
                {
                    "title": f"{topic} Tips and Tricks",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "tips", "tricks"]
                },
                {
                    "title": f"Mastering {topic}",
                    "url": "https://youtube.com",
                    "keywords": [topic.lower(), "master", "expert"]
                }
            ],
            "quiz_questions": [
                {
                    "question": f"What is {topic} primarily used for?",
                    "options": [f"To solve {topic}-related problems", "To create art", "To play games", "To browse the internet"],
                    "correct_answer": f"To solve {topic}-related problems"
                },
                {
                    "question": f"Which of these is a fundamental concept in {topic}?",
                    "options": ["Core principle 1", "Random concept", "Irrelevant topic", "Unrelated field"],
                    "correct_answer": "Core principle 1"
                },
                {
                    "question": f"What is an important skill in {topic}?",
                    "options": ["Key skill", "Unrelated ability", "Irrelevant knowledge", "Random talent"],
                    "correct_answer": "Key skill"
                },
                {
                    "question": f"What tool is commonly used in {topic}?",
                    "options": ["Essential tool", "Unrelated software", "Irrelevant application", "Random program"],
                    "correct_answer": "Essential tool"
                },
                {
                    "question": f"What is a benefit of learning {topic}?",
                    "options": ["Key benefit", "Unrelated advantage", "Irrelevant gain", "Random improvement"],
                    "correct_answer": "Key benefit"
                },
                {
                    "question": f"What is a common challenge in {topic}?",
                    "options": ["Typical difficulty", "Unrelated obstacle", "Irrelevant problem", "Random issue"],
                    "correct_answer": "Typical difficulty"
                },
                {
                    "question": f"What is an advanced technique in {topic}?",
                    "options": ["Expert method", "Basic approach", "Simple technique", "Elementary strategy"],
                    "correct_answer": "Expert method"
                },
                {
                    "question": f"What is a best practice in {topic}?",
                    "options": ["Recommended approach", "Outdated method", "Inefficient technique", "Poor strategy"],
                    "correct_answer": "Recommended approach"
                },
                {
                    "question": f"What is a real-world application of {topic}?",
                    "options": ["Practical use case", "Theoretical concept", "Academic exercise", "Hypothetical scenario"],
                    "correct_answer": "Practical use case"
                },
                {
                    "question": f"What is the future of {topic}?",
                    "options": ["Emerging trend", "Declining field", "Stagnant area", "Obsolete technology"],
                    "correct_answer": "Emerging trend"
                }
            ]
        }