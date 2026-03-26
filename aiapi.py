class ApiKeys:
    _api_details = {
        "ChatGPT": {
            "api_key": "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",
            "endpoint": "https://api.openai.com/v1/chat/completions",
            "website": "https://openai.com"
        },
        "Gemini": {
            "api_key": "AIzaSyBIEZUZzIjWkESXgzX6wOZiMugGf_YhMPU",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
            "website": "https://ai.google.dev"
        },
        "SerpAPI": {
            "api_key": "18de205d32340c42991578433a1caa2adf56ef83b5e61f71bed0bcf668b851a6",
            "endpoint": "https://serpapi.com/search",
            "website": "https://serpapi.com"
        },
        "Pexels": {
            "api_key": "Qv0gUKLAVGuG8PgLog8evvnDYGbwObppIJOAK2XAfUuefhoOXSbuJN0F",
            "endpoint": "https://api.pexels.com/v1/",
            "website": "https://www.pexels.com/api/"
        },
        "Pixabay": {
            "api_key": "49596689-91f99a2eba0386a3c524e3c4e",
            "endpoint": "https://pixabay.com/api/",
            "website": "https://pixabay.com/api/docs/"
        }
    }

    @classmethod
    def get_api_details(cls, ai_name):
        """AI modelinin API detaylarını döndürür"""
        return cls._api_details.get(ai_name)
