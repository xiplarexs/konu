import os
import re
from videoayar import search_serpapi, search_pexels, search_pixabay, download_video, log

def get_search_queries(filename="baslik/baslik.txt"):
    """Extract search queries from title file"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.readlines()
            queries = [re.search(r'"(.*?)"', line) for line in content]
            queries = [match.group(1) + " 2K video" for match in queries if match]
            log(f"Total queries found: {len(queries)}")
            return queries
    except FileNotFoundError:
        log(f"ERROR: File {filename} not found!")
    except Exception as e:
        log(f"Error reading file: {e}")
    return []

def process_query(query):
    """Process each query: download videos from multiple sources"""
    output_dir = os.path.join("download", query.replace(" ", "_"))
    os.makedirs(output_dir, exist_ok=True)
    
    sources = [
        ("SerpAPI", search_serpapi),
        ("Pexels", search_pexels),
        ("Pixabay", search_pixabay)
    ]
    
    downloaded_count = 0
    max_videos = 5  # Maximum 5 videos
    
    for source_name, search_func in sources:
        if downloaded_count >= max_videos:
            break
        
        log(f"\nSearching videos from {source_name}...")
        video_urls = search_func(query)
        
        if not video_urls:
            log(f"No videos found from {source_name}")
            continue
        
        for i, url in enumerate(video_urls[:2], 1):  # Limit to 2 per source
            if downloaded_count >= max_videos:
                break
            
            if not url or not url.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
                continue
            
            filename = f"{source_name.lower()}_{i}.mp4"
            save_path = os.path.join(output_dir, filename)
            
            if download_video(url, save_path):
                log(f"✓ Downloaded: {filename}")
                downloaded_count += 1
            else:
                log(f"✗ Failed to download: {filename}")

def main():
    """Main function to loop through all queries"""
    queries = get_search_queries()
    if not queries:
        log("No search queries found. Exiting.")
        return
    
    for query in queries:
        process_query(query)
    
if __name__ == "__main__":
    main()