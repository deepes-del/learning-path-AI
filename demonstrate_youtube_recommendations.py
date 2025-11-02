"""
Demonstration script to show how YouTube recommendations work in the Learning Path AI application.
"""

import requests
import json
from typing import Dict, Any

def demonstrate_youtube_recommendations():
    """
    Demonstrate the YouTube recommendations feature with detailed analysis.
    """
    print("=" * 80)
    print("LEARNING PATH AI - YOUTUBE RECOMMENDATIONS DEMONSTRATION")
    print("=" * 80)
    
    # Test topics
    topics = ["React.js", "Machine Learning"]
    
    for topic in topics:
        print(f"\n\n🔍 GENERATING LEARNING PATH FOR: {topic.upper()}")
        print("-" * 60)
        
        # Call the generate endpoint
        url = "http://localhost:8000/generate"
        payload = {"topic": topic}
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract YouTube recommendations
                youtube_recommendations = data.get('youtube_recommendations', [])
                
                print(f"\n📺 YOUTUBE RECOMMENDATIONS ({len(youtube_recommendations)} videos found):")
                print("-" * 40)
                
                for i, rec in enumerate(youtube_recommendations, 1):
                    print(f"\n{i}. 🎬 {rec.get('title', 'N/A')}")
                    print(f"   🔗 URL: {rec.get('url', 'N/A')}")
                    keywords = rec.get('keywords', [])
                    if keywords:
                        print(f"   🏷️  Keywords: {', '.join(keywords)}")
                    
                # Show modules for context
                modules = data.get('modules', [])
                print(f"\n📚 LEARNING MODULES ({len(modules)} modules):")
                print("-" * 40)
                
                for i, module in enumerate(modules, 1):
                    print(f"\n{i}. {module.get('title', 'N/A')}")
                    subtopics = module.get('subtopics', [])
                    for j, subtopic in enumerate(subtopics[:3], 1):  # Show first 3 subtopics
                        print(f"   • {subtopic}")
                    if len(subtopics) > 3:
                        print(f"   ... and {len(subtopics) - 3} more subtopics")
                        
                # Show quiz questions
                quiz_questions = data.get('quiz_questions', [])
                print(f"\n❓ QUIZ QUESTIONS ({len(quiz_questions)} questions):")
                print("-" * 40)
                
                for i, question in enumerate(quiz_questions[:2], 1):  # Show first 2 questions
                    print(f"\n{i}. {question.get('question', 'N/A')}")
                    options = question.get('options', [])
                    print(f"   Options: {', '.join(options)}")
                    print(f"   Correct: {question.get('correct_answer', 'N/A')}")
                    
                if len(quiz_questions) > 2:
                    print(f"\n   ... and {len(quiz_questions) - 2} more questions")
                    
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Error generating learning path: {e}")

def analyze_recommendation_quality():
    """
    Analyze the quality of YouTube recommendations.
    """
    print("\n\n" + "=" * 80)
    print("QUALITY ANALYSIS OF YOUTUBE RECOMMENDATIONS")
    print("=" * 80)
    
    print("""
✅ STRENGTHS OF CURRENT APPROACH:
   • Relevant keywords are generated for each topic
   • Titles are descriptive and topic-specific
   • URLs follow standard YouTube format
   • Recommendations cover different aspects (beginner, advanced, projects)

💡 ENHANCEMENT OPPORTUNITIES:
   • Integrate with YouTube Data API for real video search
   • Add video duration and view count information
   • Include channel reputation metrics
   • Filter by upload date for recent content
   • Add video thumbnail previews

🔧 TECHNICAL IMPROVEMENTS:
   • Cache search results to reduce API calls
   • Implement fallback to mock data when API unavailable
   • Add user ratings and review integration
   • Personalize recommendations based on user history
   • Include playlist recommendations for comprehensive learning

📈 BENEFITS FOR LEARNERS:
   • Curated, high-quality video content
   • Diverse learning resources
   • Practical examples and tutorials
   • Supplemental learning materials
   • Multiple perspectives on the same topic
    """)

if __name__ == "__main__":
    demonstrate_youtube_recommendations()
    analyze_recommendation_quality()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\n📋 To test with your own topics:")
    print("   1. Modify the 'topics' list in this script")
    print("   2. Run: python demonstrate_youtube_recommendations.py")
    print("\n🔗 Access the API directly:")
    print("   POST http://localhost:8000/generate")
    print("   Body: {\"topic\": \"Your Topic Here\"}")