import os
import requests
from aiapi import ApiKeys
import datetime

def log(message):
    """Log messages to a file."""
    log_file = r"D:\x\x1\baslik\log.txt"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {message}\n")

def search_serpapi(query):
    """Search videos using SerpAPI"""
    try:
        api_key = ApiKeys.get_api_details("SerpAPI").get("api_key")
        if not api_key:
            log("SerpAPI key not found!")
            return []
        
        params = {
            "engine": "google_videos",
            "q": query,
            "api_key": api_key,
            "num": 5
        }
        
        response = requests.get("https://serpapi.com/search", params=params, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        return [vid.get("link", "") for vid in results.get("video_results", [])]
    except Exception as e:
        log(f"SerpAPI search error: {e}")
        return []

def search_pexels(query):
    """Search videos using Pexels API"""
    try:
        api_key = ApiKeys.get_api_details("Pexels").get("api_key")
        if not api_key:
            log("Pexels API key not found!")
            return []
        
        headers = {"Authorization": api_key}
        response = requests.get(
            f"https://api.pexels.com/videos/search?query={query}&per_page=5", 
            headers=headers, 
            timeout=30
        )
        response.raise_for_status()
        
        results = response.json()
        return [vid["video_files"][0]["link"] for vid in results.get("videos", []) if vid["duration"] >= 5]
    except Exception as e:
        log(f"Pexels search error: {e}")
        return []

def search_pixabay(query):
    """Search videos using Pixabay API"""
    try:
        api_key = ApiKeys.get_api_details("Pixabay").get("api_key")
        if not api_key:
            log("Pixabay API key not found!")
            return []
        
        response = requests.get(
            f"https://pixabay.com/api/videos/?key={api_key}&q={query}&video_type=film&per_page=5", 
            timeout=30
        )
        response.raise_for_status()
        
        results = response.json()
        return [vid["videos"]["large"]["url"] for vid in results.get("hits", []) if vid["duration"] >= 5]
    except Exception as e:
        log(f"Pixabay search error: {e}")
        return []

def download_video(url, save_path):
    """Download a video file"""
    try:
        response = requests.get(url, timeout=60, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                file.write(chunk)

        log(f"✓ Downloaded: {save_path}")
        return True
    except Exception as e:
        log(f"Download error for {url}: {e}")
        return False
