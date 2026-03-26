import requests
import json
import os
from aiapi import ApiKeys

class ChatApp:
    def __init__(self):
        self.ai_models = ["ChatGPT", "Gemini", "Grok", "DeepSeek"]
        self.current_ai_index = 0 
        self.current_ai = self.ai_models[self.current_ai_index]
        
        # İlk konuyu işle
        title = self.get_topic_from_file()
        if title:
            prompt = self.prepare_prompt(title)
            if prompt:
                response = self.get_ai_response(prompt)
                if response:
                    self.save_story(response)
        
        # İkinci konuyu işle
        self.process_next_topic()

    def get_topic_from_file(self):
        """konu.txt'den ilk konuyu oku"""
        try:
            with open("konu.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith('1:'):
                        title = line.split('"')[1].strip()
                        print(f"\n📖 Başlık okundu: {title}")
                        return title
        except FileNotFoundError:
            print("⚠️ konu.txt bulunamadı!")
        return None

    def prepare_prompt(self, title):
        """Promptu hazırla ve başlıkla birleştir"""
        try:
            with open("promt1.txt", "r", encoding="utf-8") as f:
                prompt_template = f.read().strip()
                complete_prompt = prompt_template.replace('"konuburayagelcek"', f'"{title}"')
                print("\n📝 Prompt hazırlandı")
                return complete_prompt
        except FileNotFoundError:
            print("⚠️ promt1.txt bulunamadı!")
        return None

    def get_ai_response(self, prompt):
        """AI'den yanıt al"""
        print("\n🚀 AI'ya gönderiliyor...")
        max_attempts = len(self.ai_models)
        attempts = 0
        
        while attempts < max_attempts:
            try:
                endpoint, headers, data = self.prepare_request(prompt)
                if not endpoint:
                    print(f"⚠️ {self.current_ai} API bulunamadı!")
                    self.change_ai()
                    attempts += 1
                    continue

                response = requests.post(endpoint, headers=headers, data=data)
                if response.status_code == 200:
                    ai_response = self.extract_response(response.json())
                    if ai_response:
                        print(f"✅ {self.current_ai} yanıt verdi!")
                        return ai_response
                else:
                    print(f"⚠️ {self.current_ai} Hata: {response.status_code}")
                    self.change_ai()
                    attempts += 1
                    
            except Exception as e:
                print(f"🚨 Bağlantı hatası: {str(e)}")
                self.change_ai()
                attempts += 1
        
        print("❌ Hiçbir AI'ya bağlanılamadı!")
        return None

    def save_story(self, story_text):
        """Hikayeyi dosyaya kaydet"""
        try:
            # Klasör oluştur
            save_dir = os.path.join("download", "1")
            os.makedirs(save_dir, exist_ok=True)
            
            # Dosyaya kaydet
            save_path = os.path.join(save_dir, "hikaye.txt")
            with open(save_path, "w", encoding="utf-8") as f:
                # Başlık ve etiketleri temizle
                if "**Giriş:" in story_text:
                    story_text = story_text[story_text.find("**Giriş:"):]
                f.write(story_text)
            
            print(f"💾 Hikaye kaydedildi: {save_path}")
            return True
        except Exception as e:
            print(f"⚠️ Kayıt hatası: {str(e)}")
            return False

    def change_ai(self):
        """Diğer AI'ya geç"""
        self.current_ai_index = (self.current_ai_index + 1) % len(self.ai_models)
        self.current_ai = self.ai_models[self.current_ai_index]
        print(f"🔄 Yeni AI: {self.current_ai}")

    def prepare_request(self, user_message):
        """API isteğini hazırla"""
        api = ApiKeys.get_api_details(self.current_ai)
        if not api:
            return None, None, None

        key = api["api_key"]
        endpoint = api["endpoint"]
        
        headers = {"Content-Type": "application/json"}
        if self.current_ai in ["ChatGPT", "Grok", "DeepSeek"]:
            headers["Authorization"] = f"Bearer {key}"
        elif self.current_ai == "Gemini":
            endpoint += f"?key={key}"

        if self.current_ai == "ChatGPT":
            data = json.dumps({"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": user_message}]})
        elif self.current_ai == "Grok":
            data = json.dumps({"model": "xai-grok", "messages": [{"role": "user", "content": user_message}]})
        elif self.current_ai == "DeepSeek":
            data = json.dumps({"model": "deepseek-chat", "messages": [{"role": "user", "content": user_message}]})
        elif self.current_ai == "Gemini":
            data = json.dumps({"contents": [{"parts": [{"text": user_message}]}]})
        else:
            return None, None, None

        return endpoint, headers, data

    def extract_response(self, response_json):
        """API yanıtından metni çıkar"""
        try:
            if self.current_ai == "ChatGPT":
                return response_json["choices"][0]["message"]["content"]
            elif self.current_ai == "Grok":
                return response_json["choices"][0]["message"]["content"]
            elif self.current_ai == "DeepSeek":
                return response_json["choices"][0]["message"]["content"]
            elif self.current_ai == "Gemini":
                return response_json["candidates"][0]["content"]["parts"][0]["text"]
        except:
            return None

    def get_next_topic(self):
        """konu.txt'den 2. konuyu oku"""
        try:
            with open("konu.txt", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith('2:'):
                        title = line.split('"')[1].strip()
                        print(f"\n📖 2. Başlık okundu: {title}")
                        return title
            print("⚠️ 2. konu bulunamadı!")
        except FileNotFoundError:
            print("⚠️ konu.txt bulunamadı!")
        return None

    def process_next_topic(self):
        """2. konuyu işle"""
        title = self.get_next_topic()
        if title:
            print(f"\n📌 İşlenecek konu: {title}")
            prompt = self.prepare_prompt(title)
            
            if prompt:
                print("\n📝 Prompt hazırlanıyor...")
                complete_prompt = prompt.replace('"konuburayagelcek"', f'"{title}"')
                print("\n🚀 AI'ya gönderiliyor...")
                
                response = self.get_ai_response(complete_prompt)
                if response:
                    # Yeni klasör oluştur (2 numaralı)
                    save_dir = os.path.join("download", "2")
                    os.makedirs(save_dir, exist_ok=True)
                    save_path = os.path.join(save_dir, "hikaye.txt")
                    
                    with open(save_path, "w", encoding="utf-8") as f:
                        if "**Giriş:" in response:
                            response = response[response.find("**Giriş:"):]
                        f.write(response)
                    print(f"💾 2. hikaye kaydedildi: {save_path}")

if __name__ == "__main__":
    app = ChatApp()