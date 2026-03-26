import os
import requests
from aiapi import ApiKeys

def download_image(url, save_path):
    """Download a single image with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except Exception as e:
        log(f"Download error for {url}: {e}")
        return False

def search_serpapi(query):
    """Google Images üzerinden kaliteli görsel arama"""
    try:
        api_key = ApiKeys.get_api_details("SerpAPI").get("api_key")
        if not api_key:
            print("⚠️ SerpAPI anahtarı bulunamadı!")
            return []
        
        # Ana konuyu al
        base_query = query.replace("4K wallpaper", "").strip()
        
        # Gelişmiş arama parametreleri
        params = {
            "engine": "google_images",
            "q": f"{base_query} (4K OR UHD OR HD) (wallpaper OR artwork OR concept art) -site:pinterest.*",
            "api_key": api_key,
            "num": 10,  # Daha fazla sonuç iste
            "ijn": "0",
            "tbs": "isz:l,iar:w,itp:photo,ic:specific,isc:red",  # Büyük, geniş, fotoğraf
            "safe": "active"
        }
        
        print(f"🔍 Google'da aranıyor: {params['q']}")
        response = requests.get(
            "https://serpapi.com/search", 
            params=params, 
            timeout=30
        )
        response.raise_for_status()
        
        results = response.json()
        images = []
        
        # Görsel sonuçlarını filtrele
        for img in results.get("images_results", []):
            original_url = img.get("original")
            if original_url and all(x not in original_url.lower() for x in ['pinterest', 'stock']):
                width = img.get("original_width", 0)
                height = img.get("original_height", 0)
                
                # Minimum 1000x1000 piksel
                if width >= 1000 and height >= 1000:
                    images.append(original_url)
                    if len(images) >= 5:
                        break

        print(f"📸 {len(images)} yüksek kaliteli görsel bulundu")
        return images
        
    except Exception as e:
        print(f"⚠️ Google görsel arama hatası: {str(e)}")
        return []

def search_pixabay(query):
    """Pixabay'den yüksek kaliteli görsel arama"""
    try:
        api_key = ApiKeys.get_api_details("Pixabay").get("api_key")
        if not api_key:
            print("⚠️ Pixabay API anahtarı bulunamadı!")
            return []
        
        # Ana konuyu al ve düzenle
        search_query = query.replace("4K wallpaper", "").strip()
        
        # API parametreleri
        params = {
            "key": api_key,
            "q": search_query,
            "image_type": "photo",
            "orientation": "horizontal",
            "min_width": 1920,
            "min_height": 1080,
            "per_page": 10,
            "safesearch": "true",
            "order": "latest"  # En yeni görseller
        }
        
        print(f"🔍 Pixabay'de aranıyor: {search_query}")
        response = requests.get(
            "https://pixabay.com/api/",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        
        results = response.json()
        images = []
        
        # Görselleri filtrele
        for img in results.get("hits", []):
            if img.get("imageWidth", 0) >= 1000 and img.get("imageHeight", 0) >= 1000:
                image_url = img.get("largeImageURL")  # Büyük boyutlu görsel URL'si
                if image_url and image_url not in images:
                    images.append(image_url)
                    if len(images) >= 5:
                        break
        
        print(f"📸 {len(images)} yüksek kaliteli görsel bulundu")
        return images
        
    except Exception as e:
        print(f"⚠️ Pixabay arama hatası: {str(e)}")
        return []

def search_pexels(query):
    """Pexels API ile gelişmiş görsel arama"""
    try:
        api_key = ApiKeys.get_api_details("Pexels").get("api_key")
        if not api_key:
            print("⚠️ Pexels API anahtarı bulunamadı!")
            return []
        
        # Ana konuyu al
        base_query = query.replace("4K wallpaper", "").strip()
        
        # Farklı arama terimleri
        search_queries = [
            f"{base_query} space concept art",  # Konsept sanat
            f"{base_query} digital illustration",  # Dijital çizim
            f"{base_query} astronomy",  # Astronomi
            f"{base_query} artistic",  # Sanatsal
            f"{base_query} high resolution"  # Yüksek çözünürlük
        ]
        
        headers = {"Authorization": api_key}
        all_photos = []
        
        # Her sorgu için arama yap
        for search_query in search_queries:
            print(f"🔎 Aranıyor: {search_query}")
            
            response = requests.get(
                f"https://api.pexels.com/v1/search",
                params={
                    "query": search_query,
                    "per_page": 2,  # Her sorgudan 2 görsel
                    "size": "large",  # Büyük boyut
                    "orientation": "landscape"  # Yatay
                },
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            for img in results.get("photos", []):
                # En yüksek kaliteli URL'yi al
                url = img["src"].get("original") or img["src"].get("large2x")
                if url and url not in all_photos:  # Tekrarları önle
                    all_photos.append(url)
                    
            if len(all_photos) >= 5:  # Yeterli görsel bulunduysa dur
                break
                
        print(f"📸 Toplam {len(all_photos)} benzersiz görsel bulundu")
        return all_photos[:5]  # En fazla 5 görsel döndür
        
    except Exception as e:
        print(f"⚠️ Pexels arama hatası: {str(e)}")
        return []