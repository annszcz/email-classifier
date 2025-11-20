# 🔧 Troubleshooting Guide

## Problemy z Instalacją

### Problem: `python` nie jest rozpoznawany jako polecenie

**Objawy:**
```
'python' is not recognized as an internal or external command
```

**Rozwiązanie:**
```bash
# Windows - sprawdź czy Python jest w PATH
# Lub użyj:
py -m venv venv
py -m pip install -r requirements.txt

# Linux/Mac - użyj python3
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

---

### Problem: Błędy podczas instalacji pakietów

**Objawy:**
```
ERROR: Could not build wheels for ...
```

**Rozwiązanie:**
```bash
# Aktualizuj pip
python -m pip install --upgrade pip

# Instaluj build tools (Windows)
pip install wheel setuptools

# Lub instaluj bez binary
pip install --no-binary :all: package-name

# Jeśli nadal nie działa, instaluj po kolei:
pip install fastapi
pip install uvicorn
pip install openai
pip install scikit-learn
pip install numpy
```

---

## Problemy z Backend

### Problem: Port 8000 już zajęty

**Objawy:**
```
ERROR: [Errno 98] Address already in use
```

**Rozwiązanie:**

**Windows:**
```bash
# Znajdź proces
netstat -ano | findstr :8000

# Zabij proces (zamień PID na właściwy)
taskkill /PID <PID> /F

# Lub użyj innego portu
uvicorn backend.main:app --port 8001
```

**Linux/Mac:**
```bash
# Znajdź proces
lsof -i :8000

# Zabij proces
kill -9 <PID>

# Lub użyj innego portu
uvicorn backend.main:app --port 8001
```

---

### Problem: ModuleNotFoundError: No module named 'backend'

**Objawy:**
```
ModuleNotFoundError: No module named 'backend'
```

**Rozwiązanie:**
```bash
# Upewnij się że jesteś w głównym katalogu projektu
cd email-classifier

# Uruchom z flagą -m
python -m uvicorn backend.main:app --reload

# Lub dodaj PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"  # Linux/Mac
set PYTHONPATH=%PYTHONPATH%;%CD%          # Windows
```

---

### Problem: ImportError podczas importu classifier

**Objawy:**
```
ImportError: cannot import name 'EmailClassifier' from 'backend.classifier'
```

**Rozwiązanie:**
```bash
# Sprawdź czy wszystkie pliki są w miejscu
ls backend/
# Powinno pokazać: __init__.py, main.py, classifier.py

# Upewnij się że __init__.py nie jest pusty
cat backend/__init__.py

# Reinstaluj zależności
pip install -r requirements.txt --force-reinstall
```

---

## Problemy z Azure OpenAI

### Problem: Authentication failed

**Objawy:**
```
AuthenticationError: Incorrect API key provided
```

**Rozwiązanie:**
1. Sprawdź klucz w Azure Portal:
   - Przejdź do Resource → Keys and Endpoint
   - Skopiuj KEY 1 (nie KEY 2)

2. Sprawdź .env:
```bash
cat .env
# Powinno zawierać:
# AZURE_OPENAI_API_KEY=twój-klucz-bez-spacji
```

3. Zrestartuj backend po zmianie .env

---

### Problem: Resource not found

**Objawy:**
```
ResourceNotFoundError: The API deployment for this resource does not exist
```

**Rozwiązanie:**
1. Sprawdź deployment name w Azure Portal:
   - Resource → Model deployments
   - Skopiuj dokładną nazwę (case-sensitive!)

2. Zaktualizuj .env:
```bash
AZURE_OPENAI_DEPLOYMENT=twoja-dokladna-nazwa
```

3. Upewnij się że endpoint jest poprawny:
```bash
# Format: https://resource-name.openai.azure.com/
# NIE: https://resource-name.openai.azure.com/openai/...
```

---

### Problem: Rate limit exceeded

**Objawy:**
```
RateLimitError: Rate limit reached for requests
```

**Rozwiązanie:**
1. Sprawdź limity w Azure Portal:
   - Resource → Quotas
   - Zobacz TPM (Tokens per Minute)

2. Zwiększ limity:
   - Kliknij "Request quota increase"
   - Poczekaj na approval (~1-2 dni)

3. Tymczasowo:
   - Zmniejsz częstotliwość requestów
   - Dodaj retry logic z exponential backoff

---

### Problem: Region not available

**Objawy:**
```
This model is not available in your region
```

**Rozwiązanie:**
1. Sprawdź dostępność regionu:
   https://learn.microsoft.com/azure/ai-services/openai/concepts/models

2. Utwórz nowy resource w dostępnym regionie:
   - East US
   - West Europe
   - Sweden Central

---

## Problemy z Frontend

### Problem: Cannot connect to backend

**Objawy:**
W konsoli przeglądarki:
```
Failed to fetch
Network Error
CORS error
```

**Rozwiązanie:**

1. Sprawdź czy backend działa:
```bash
curl http://localhost:8000/health
```

2. Sprawdź CORS w backend/main.py:
```python
# Powinno być:
allow_origins=["*"]  # Lub ["http://localhost:8080"]
```

3. Sprawdź URL w frontend:
```javascript
// W index.html, zmień jeśli potrzeba:
const API_URL = 'http://localhost:8000';
```

4. Wyłącz cache w przeglądarce:
   - Chrome: Ctrl+Shift+R
   - Firefox: Ctrl+F5

---

### Problem: Blank page after opening

**Objawy:**
Pusta strona, brak błędów

**Rozwiązanie:**

1. Otwórz Developer Tools (F12)
2. Sprawdź Console dla błędów JavaScript
3. Upewnij się że wszystkie CDN są dostępne:
```html
<!-- Sprawdź te linki w przeglądarce: -->
https://unpkg.com/react@18/umd/react.production.min.js
https://unpkg.com/react-dom@18/umd/react-dom.production.min.js
```

4. Spróbuj innej przeglądarki

---

## Problemy z Danymi

### Problem: Training data not loading

**Objawy:**
```
Error loading training data
```

**Rozwiązanie:**

1. Sprawdź czy plik istnieje:
```bash
ls data/training_emails.json
```

2. Sprawdź format JSON:
```bash
python -m json.tool data/training_emails.json
```

3. Sprawdź encoding:
```bash
file data/training_emails.json
# Powinno być: UTF-8 Unicode text
```

---

### Problem: Poor classification accuracy

**Objawy:**
Model klasyfikuje wszystko jako jedną kategorię lub losowo

**Rozwiązanie:**

1. Jeśli używasz fallback classifier:
   - To normalne - accuracy ~70-80%
   - Skonfiguruj Azure OpenAI dla lepszych wyników

2. Jeśli używasz Azure OpenAI:
   - Sprawdź few-shot examples w classifier.py
   - Upewnij się że temperature=0.1 (nie wyższa)
   - Dodaj więcej przykładów treningowych

3. Sprawdź dane wejściowe:
   - Czy e-mail ma wystarczająco treści?
   - Czy język jest polski?

---

## Problemy z Testami

### Problem: Tests failing

**Objawy:**
```bash
pytest tests/
# Multiple failures
```

**Rozwiązanie:**

1. Upewnij się że backend nie działa podczas testów:
```bash
# Zatrzymaj uvicorn przed testami
```

2. Sprawdź czy masz dane treningowe:
```bash
ls data/training_emails.json
```

3. Uruchom testy pojedynczo:
```bash
pytest tests/test_classifier.py::TestEmailClassifier::test_classifier_initialization -v
```

4. Sprawdź czy wszystkie zależności są zainstalowane:
```bash
pip list | grep pytest
```

---

## Problemy z Performance

### Problem: Slow response times (>2s)

**Możliwe przyczyny i rozwiązania:**

1. **Azure OpenAI throttling**
   - Sprawdź rate limits
   - Zwiększ quota

2. **Slow network**
   - Sprawdź ping do Azure endpoint:
```bash
ping your-resource.openai.azure.com
```

3. **Large prompts**
   - Ogranicz długość body do 1000 znaków
   - Nie wysyłaj attachments

4. **Cold start**
   - Pierwsze zapytanie zawsze wolniejsze
   - Drugi i kolejne: <500ms

---

## Problemy z Deployment

### Problem: Azure App Service errors

**Objawy:**
```
Application Error
```

**Rozwiązanie:**

1. Sprawdź logi:
```bash
az webapp log tail --name email-classifier --resource-group email-classifier-rg
```

2. Sprawdź environment variables:
```bash
az webapp config appsettings list --name email-classifier --resource-group email-classifier-rg
```

3. Sprawdź Python version:
```bash
# W portal.azure.com:
App Service → Configuration → General settings
# Python version: 3.11
```

---

## Debugging Tips

### Enable Debug Logging

```python
# W backend/main.py, na początku:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Environment Variables

```python
# W classifier.py:
import os
print("Endpoint:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("Has API Key:", bool(os.getenv("AZURE_OPENAI_API_KEY")))
```

### Test Azure Connection

```python
# test_azure.py
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-08-01-preview"
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Test"}],
        max_tokens=10
    )
    print("✅ Azure OpenAI działa!")
    print(response.choices[0].message.content)
except Exception as e:
    print("❌ Błąd:", e)
```

---

## Uzyskiwanie Pomocy

Jeśli żaden z powyższych rozwiązań nie pomaga:

1. **Sprawdź logi:**
```bash
# Backend logs
cat backend.log

# System logs (Linux)
journalctl -u email-classifier

# Azure logs
az webapp log tail --name email-classifier
```

2. **Zbierz informacje:**
   - Wersja Python: `python --version`
   - System: `uname -a` (Linux/Mac) lub `ver` (Windows)
   - Zainstalowane pakiety: `pip list`
   - Pełen stack trace błędu

3. **Kontakt:**
   - GitHub Issues (jeśli projekt jest na GitHub)
   - Azure Support (dla problemów z Azure)
   - Dokumentacja: `docs/`

---

## Checklist Diagnostyczny

Przed zgłoszeniem problemu, sprawdź:

- [ ] Python 3.9+ zainstalowany
- [ ] Wszystkie zależności zainstalowane (`pip list`)
- [ ] .env skonfigurowany (jeśli używasz Azure)
- [ ] Backend działa (`curl http://localhost:8000/health`)
- [ ] Frontend dostępny (`http://localhost:8080`)
- [ ] Brak błędów w konsoli przeglądarki (F12)
- [ ] Porty 8000 i 8080 wolne
- [ ] Firewall nie blokuje
- [ ] Restart całej aplikacji wykonany

---

## Common Error Messages

```
"Email classification failed"
→ Sprawdź Azure OpenAI credentials lub użyj fallback

"Connection refused"
→ Backend nie działa, uruchom uvicorn

"404 Not Found"
→ Sprawdź URL, backend endpoint, czy plik istnieje

"422 Unprocessable Entity"
→ Nieprawidłowy format danych, sprawdź JSON

"500 Internal Server Error"
→ Błąd w backendzie, sprawdź logi
```

---

## Przydatne Komendy

```bash
# Sprawdź czy backend działa
curl http://localhost:8000/health

# Test klasyfikacji
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"subject":"Test","body":"Test"}'

# Zobacz API docs
open http://localhost:8000/docs

# Sprawdź logi w czasie rzeczywistym
tail -f backend.log

# Restart wszystkiego
# Windows:
taskkill /F /IM python.exe
start.bat

# Linux/Mac:
killall python
./start.sh
```

---

Pamiętaj: większość problemów można rozwiązać przez:
1. Restart aplikacji
2. Reinstalację zależności
3. Sprawdzenie logów

Good luck! 🍀
