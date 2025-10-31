"""
YouTube service for searching and retrieving real YouTube videos
to enhance learning path recommendations.
"""

import os
import requests
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_youtube_videos(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for YouTube videos using the YouTube Data API.
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        List[Dict[str, Any]]: List of video information
    """
    api_key = os.environ.get("YOUTUBE_API_KEY")
    
    if not api_key:
        logger.warning("YOUTUBE_API_KEY not found in environment variables")
        return []
    
    # YouTube Data API endpoint
    search_url = "https://www.googleapis.com/youtube/v3/search"
    
    # Parameters for the search
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': max_results,
        'key': api_key,
        'videoDuration': 'medium',  # Prefer medium-length videos for tutorials
        'order': 'relevance'  # Order by relevance
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            videos = []
            
            for item in data.get('items', [])[:max_results]:
                video_info = {
                    'title': item['snippet']['title'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'description': item['snippet']['description'][:200] + "..." if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'channel': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt'],
                    'thumbnails': item['snippet']['thumbnails']
                }
                videos.append(video_info)
            
            logger.info(f"Found {len(videos)} YouTube videos for query: {query}")
            return videos
        else:
            logger.error(f"YouTube API error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return []

def enhance_learning_path_with_youtube(topic: str, learning_path: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enhance a learning path with real YouTube videos based on the topic and modules.
    
    Args:
        topic (str): The main topic of the learning path
        learning_path (Dict[str, Any]): The generated learning path
        
    Returns:
        Dict[str, Any]: Enhanced learning path with real YouTube recommendations
    """
    # Get the existing YouTube recommendations from the learning path
    existing_recommendations = learning_path.get('youtube_recommendations', [])
    
    # Create a set of keywords to avoid duplicates
    searched_keywords = set()
    enhanced_recommendations = []
    
    # Search for videos based on the main topic with better queries
    topic_queries = [
        f"{topic} complete tutorial",
        f"{topic} course for beginners",
        f"{topic} fundamentals"
    ]
    
    for query in topic_queries[:2]:  # Limit to 2 queries to avoid too many API calls
        topic_videos = search_youtube_videos(query, 2)
        for video in topic_videos:
            # Create more descriptive keywords
            keywords = [topic.lower(), query.split()[-1], 'tutorial']
            enhanced_recommendations.append({
                'title': video['title'],
                'url': video['url'],
                'keywords': keywords
            })
    
    # Search for videos based on module titles and subtopics
    modules = learning_path.get('modules', [])
    for module in modules[:3]:  # Limit to first 3 modules to avoid too many API calls
        module_title = module.get('title', '')
        if module_title and module_title not in searched_keywords:
            # Create better search queries for modules
            module_queries = [
                f"{module_title} explained",
                f"{module_title} tutorial {topic}",
                f"{topic} {module_title}"
            ]
            
            for query in module_queries[:1]:  # Limit to 1 query per module
                videos = search_youtube_videos(query, 1)
                for video in videos:
                    enhanced_recommendations.append({
                        'title': video['title'],
                        'url': video['url'],
                        'keywords': [topic.lower(), module_title.lower(), 'module']
                    })
                searched_keywords.add(module_title)
        
        # Search for videos based on subtopics
        subtopics = module.get('subtopics', [])
        for subtopic in subtopics[:2]:  # Limit to first 2 subtopics
            if subtopic and subtopic not in searched_keywords:
                # Create better search queries for subtopics
                subtopic_queries = [
                    f"{subtopic} {topic} tutorial",
                    f"{topic} {subtopic} explained"
                ]
                
                for query in subtopic_queries[:1]:  # Limit to 1 query per subtopic
                    videos = search_youtube_videos(query, 1)
                    for video in videos:
                        enhanced_recommendations.append({
                            'title': video['title'],
                            'url': video['url'],
                            'keywords': [topic.lower(), subtopic.lower(), 'concept']
                        })
                    searched_keywords.add(subtopic)
    
    # Ensure we have at least 5 recommendations by adding more if needed
    if len(enhanced_recommendations) < 5:
        # Search for general topic videos to fill in
        additional_videos = search_youtube_videos(f"{topic} advanced tutorial", 5 - len(enhanced_recommendations))
        for video in additional_videos:
            enhanced_recommendations.append({
                'title': video['title'],
                'url': video['url'],
                'keywords': [topic.lower(), 'advanced', 'tutorial']
            })
    
    # Deduplicate recommendations based on URL
    unique_recommendations = []
    seen_urls = set()
    
    for rec in enhanced_recommendations:
        if rec['url'] not in seen_urls:
            unique_recommendations.append(rec)
            seen_urls.add(rec['url'])
    
    # Limit to 5 recommendations
    final_recommendations = unique_recommendations[:5]
    
    # If we found real videos, replace the generated ones; otherwise keep the generated ones
    if final_recommendations:
        learning_path['youtube_recommendations'] = final_recommendations
        logger.info(f"Enhanced learning path with {len(final_recommendations)} real YouTube videos")
    else:
        logger.warning("Could not find real YouTube videos, keeping generated recommendations")
    
    return learning_path

# Example usage
if __name__ == "__main__":
    # Test the YouTube search function
    print("Testing YouTube search for 'Machine Learning':")
    videos = search_youtube_videos("Machine Learning", 3)
    
    for i, video in enumerate(videos, 1):
        print(f"\n{i}. {video['title']}")
        print(f"   Channel: {video['channel']}")
        print(f"   URL: {video['url']}")
        print(f"   Description: {video['description']}")