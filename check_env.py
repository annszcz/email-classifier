import os
from dotenv import load_dotenv

load_dotenv()

print("🔍 Sprawdzam zmienne środowiskowe:\n")

vars_to_check = [
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY", 
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_DEPLOYMENT"
]

for var in vars_to_check:
    value = os.getenv(var)
    if value:
        # Ukryj API key
        if "KEY" in var:
            print(f"✅ {var}: {'*' * 20}")
        else:
            print(f"✅ {var}: {value}")
    else:
        print(f"❌ {var}: BRAK!")

print("\n📁 Lokalizacja .env:", os.path.abspath(".env"))
print("📂 Aktualny katalog:", os.getcwd())