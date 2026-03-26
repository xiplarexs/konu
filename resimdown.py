import os
import time
from PIL import Image
from resimayar import search_serpapi, search_pexels, search_pixabay, download_image

def get_topic(index):
    """konu.txt'den verilen indeksteki konuyu al"""
    try:
        with open("konu.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Boş satırları atla
                if not line:
                    continue
                    
                # İndeks kontrolü
                if line.startswith(f'{index}:'):
                    title = line.split('"')[1].strip()
                    print(f"\n📖 {index}. konu: {title}")
                    return title + " 4K wallpaper"
    except FileNotFoundError:
        print("⚠️ konu.txt bulunamadı!")
    return None

def is_valid_image(image_path):
    """Görüntü boyut kontrolü"""
    try:
        img = Image.open(image_path)
        width, height = img.size
        size_kb = os.path.getsize(image_path) / 1024

        if width >= 1000 and height >= 1000 and size_kb >= 100:
            print(f"✅ Geçerli: {width}x{height}, {size_kb:.1f}KB")
            return True
            
        print(f"❌ Geçersiz: {width}x{height}, {size_kb:.1f}KB")
        return False
        
    except Exception as e:
        print(f"⚠️ Görüntü hatası: {str(e)}")
        return False

def create_directory(index):
    """İndeks için klasör oluştur"""
    save_dir = os.path.join("download", str(index))
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
            print(f"📁 Yeni klasör oluşturuldu: {save_dir}")
        except Exception as e:
            print(f"⚠️ Klasör oluşturma hatası: {str(e)}")
            return None
    return save_dir

def get_unique_filename(save_dir, base_name):
    """Benzersiz dosya adı oluştur"""
    name, ext = os.path.splitext(base_name)
    counter = 1
    
    # Temel dosya adı
    filename = f"{name}{ext}"
    
    # Eğer dosya varsa yeni isim oluştur
    while os.path.exists(os.path.join(save_dir, filename)):
        filename = f"{name}_{counter}{ext}"
        counter += 1
        
    return filename

def process_topic(topic, index):
    """Konuya ait görselleri indir"""
    if not topic:
        return False

    # Önce ana download klasörü kontrol et
    if not os.path.exists("download"):
        try:
            os.makedirs("download")
            print("📁 Ana download klasörü oluşturuldu")
        except Exception as e:
            print(f"⚠️ Ana klasör oluşturma hatası: {str(e)}")
            return False

    # Konu klasörünü oluştur
    save_dir = create_directory(index)
    if not save_dir:
        return False
    
    sources = [
        ("SerpAPI", search_serpapi),
        ("Pexels", search_pexels),
        ("Pixabay", search_pixabay)
    ]
    
    successful = 0
    required = 5
    
    for source_name, search_func in sources:
        if successful >= required:
            break
            
        print(f"\n🔍 {source_name}'den aranıyor...")
        urls = search_func(topic)
        
        if not urls:
            print(f"⚠️ {source_name}'de görüntü bulunamadı")
            continue
        
        for i, url in enumerate(urls[:5], 1):
            if successful >= required:
                break
                
            # Benzersiz dosya adı al
            base_filename = f"{source_name.lower()}_{i}.jpg"
            filename = get_unique_filename(save_dir, base_filename)
            save_path = os.path.join(save_dir, filename)
            
            print(f"\n⬇️ İndiriliyor: {filename}")
            if download_image(url, save_path) and is_valid_image(save_path):
                successful += 1
                print(f"✅ {filename} başarıyla indirildi")
            else:
                print(f"❌ {filename} indirilemedi veya geçersiz")

    print(f"\n✨ {successful} görüntü başarıyla indirildi")
    return successful > 0

def main():
    """Ana program döngüsü"""
    index = 1
    
    while True:  # Sonsuz döngü
        topic = get_topic(index)
        if not topic:  # Konu bulunamadıysa sonlan 
            print("\n🏁 Tüm konular tamamlandı!")
            break
            
        print(f"\n🎯 {index}. konu işleniyor: {topic}")
        
        if process_topic(topic, index):
            print(f"✅ {index}. konu tamamlandı")
        else:
            print(f"❌ {index}. konu başarısız oldu")
            
        # API limit koruması
        print("\n⏳ 5 saniye bekleniyor...")
        time.sleep(5)
        
        index += 1

if __name__ == "__main__":
    main()