# 📧 Email Classifier - Azure AI Foundry Demo

Inteligentny system klasyfikacji e-maili zgłoszeniowych wykorzystujący Azure OpenAI i AI Foundry.

## 🎯 Opis Projektu

System automatycznie klasyfikuje przychodzące e-maile zgłoszeniowe do odpowiednich działów:
- **IT** - problemy techniczne, awarie, błędy systemów
- **Księgowość** - faktury, płatności, rozliczenia
- **Obsługa Klienta** - reklamacje, pytania o zamówienia, zwroty
- **Sprzedaż** - zapytania ofertowe, współpraca biznesowa

## ✨ Funkcjonalności

- ✅ Klasyfikacja e-maili w czasie rzeczywistym
- ✅ Few-shot learning z Azure OpenAI GPT-4o (lub GPT-4o-mini)
- ✅ Walidacja adresów email (Pydantic EmailStr)
- ✅ Metryki wydajności modelu (Accuracy, F1-Score, Precision, Recall)
- ✅ Piękny, responsywny interfejs użytkownika
- ✅ Historia klasyfikacji
- ✅ Przykładowe dane treningowe
- ✅ Fallback na klasyfikację regułową
- ✅ Automatyczne ładowanie zmiennych środowiskowych

## 🏗️ Architektura

```
email-classifier/
├── backend/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   └── classifier.py     # Classifier logic
├── frontend/
│   └── index.html        # React UI
├── data/
│   └── training_emails.json
├── docs/
│   └── ai_foundry_setup.md
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Szybki Start

### Wymagania

- Python 3.9+
- Azure OpenAI API (opcjonalne - aplikacja działa też bez Azure!)
- Przeglądarka internetowa

### Opcja 1: Automatyczne uruchomienie (Windows)

**Najszybszy sposób!** Użyj gotowego skryptu:

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/TWOJA-NAZWA/email-classifier.git
cd email-classifier

# 2. Uruchom aplikację
start.bat
```

Skrypt automatycznie:
- ✅ Utworzy środowisko wirtualne
- ✅ Zainstaluje wszystkie zależności
- ✅ Uruchomi backend i frontend
- ✅ Otworzy aplikację w przeglądarce

**Uwaga**: Jeśli nie masz Azure OpenAI, aplikacja będzie działać w trybie fallback (klasyfikacja regułowa).

### Opcja 2: Instalacja manualna

1. **Sklonuj repozytorium**
```bash
git clone https://github.com/TWOJA-NAZWA/email-classifier.git
cd email-classifier
```

2. **Utwórz wirtualne środowisko**
```bash
python -m venv venv
```

3. **Aktywuj środowisko**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Zainstaluj zależności**
```bash
pip install -r requirements.txt
```

5. **Skonfiguruj Azure OpenAI (opcjonalne)**
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env

# Edytuj plik .env i dodaj swoje klucze Azure
# Jeśli nie masz Azure OpenAI, pomiń ten krok - aplikacja będzie działać w trybie fallback
```

6. **Uruchom backend**
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

7. **Uruchom frontend** (w nowej karcie terminala)
```bash
cd frontend
python -m http.server 8080
```

8. **Otwórz przeglądarkę**
```
http://localhost:8080
```

### Opcja 3: Linux/Mac - automatyczne uruchomienie

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/TWOJA-NAZWA/email-classifier.git
cd email-classifier

# 2. Nadaj uprawnienia i uruchom
chmod +x start.sh
./start.sh
```

## 🎮 Jak używać aplikacji

Po uruchomieniu zobaczysz:

1. **Formularz klasyfikacji** (lewa strona):
   - Wpisz temat emaila
   - Wpisz treść emaila
   - Opcjonalnie: dodaj adres nadawcy (musi być poprawny email!)
   - Kliknij "Klasyfikuj"

2. **Przykładowe emaile** (pod formularzem):
   - Kliknij na przykład, aby automatycznie wypełnić formularz
   - Świetne do szybkiego testowania!

3. **Statystyki modelu** (prawa strona):
   - Metryki wydajności (Accuracy, F1-Score, itp.)
   - Lista dostępnych działów
   - Historia ostatnich klasyfikacji

4. **Wynik klasyfikacji**:
   - Nazwa działu (IT, Księgowość, Obsługa Klienta, Sprzedaż)
   - Poziom pewności (0-100%)
   - Timestamp klasyfikacji

### ✅ Test czy działa

Szybki test:
```bash
# W nowej karcie terminala
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"subject":"Awaria serwera","body":"Serwer nie odpowiada","sender":"admin@firma.pl"}'
```

Jeśli zobaczysz JSON z wynikiem - wszystko działa! 🎉

## 🔧 Konfiguracja Azure AI Foundry

### Krok 1: Utwórz Azure Resource

1. Zaloguj się do [Azure Portal](https://portal.azure.com)
2. Kliknij **"Create a resource"**
3. Wyszukaj **"Azure OpenAI"**
4. Kliknij **"Create"**

### Krok 2: Wypełnij szczegóły

```
Subscription: [Twoja subskrypcja]
Resource Group: email-classifier-rg
Region: East US (lub inny dostępny)
Name: email-classifier-openai
Pricing Tier: Standard S0
```

### Krok 3: Deploy Model

1. W Azure Portal, przejdź do swojego zasobu OpenAI
2. Kliknij **"Model deployments"** → **"Create new deployment"**
3. Wybierz model: **gpt-4o-mini**
4. Nadaj nazwę: **gpt-4o-mini**
5. Kliknij **"Create"**

### Krok 4: Pobierz klucze

1. W zasobie OpenAI, przejdź do **"Keys and Endpoint"**
2. Skopiuj:
   - **Endpoint** (np. https://your-resource.openai.azure.com/)
   - **Key 1** (Twój API key)

### Krok 5: Skonfiguruj aplikację

1. Skopiuj `.env.example` jako `.env`:
```bash
cp .env.example .env
```

2. Edytuj `.env`:
```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=twój-api-key
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

## 📊 Azure AI Foundry - Dodatkowe Opcje

### Fine-tuning (Opcjonalnie)

Jeśli chcesz wytrenować własny model:

1. **Przygotuj dane w formacie JSONL**
```python
# convert_data.py
import json

with open('data/training_emails.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('training_data.jsonl', 'w', encoding='utf-8') as f:
    for item in data:
        training_example = {
            "messages": [
                {"role": "system", "content": "Jesteś ekspertem od klasyfikacji e-maili."},
                {"role": "user", "content": f"Temat: {item['subject']}\nTreść: {item['body']}"},
                {"role": "assistant", "content": item['label']}
            ]
        }
        f.write(json.dumps(training_example, ensure_ascii=False) + '\n')
```

2. **Upload do Azure**
```bash
az openai fine-tune create \
  --resource-group email-classifier-rg \
  --name email-classifier-openai \
  --deployment-name email-classifier-ft \
  --training-file training_data.jsonl \
  --model gpt-4o-mini
```

3. **Użyj w aplikacji**
```bash
# W .env zmień:
AZURE_OPENAI_DEPLOYMENT=email-classifier-ft
```

### Content Safety

1. W Azure Portal, dodaj **Content Safety** resource
2. Skonfiguruj filtry:
   - Hate: Medium
   - Sexual: Medium
   - Violence: Medium
   - Self-harm: Medium

### Monitoring

1. W Azure Portal, włącz **Application Insights**
2. Konfiguruj alerty dla:
   - API call failures
   - High latency (>2s)
   - Token usage threshold

## 📈 Metryki Modelu

Model jest oceniany na podstawie:

- **Accuracy** - ogólna dokładność klasyfikacji
- **F1-Score** - harmonic mean precision i recall
- **Precision** - jakość pozytywnych predykcji
- **Recall** - pełność wykrywania klas

Endpoint: `GET /metrics`

## 🔌 API Endpoints

### Klasyfikacja E-maila
```http
POST /classify
Content-Type: application/json

{
  "subject": "Błąd logowania",
  "body": "Nie mogę się zalogować do systemu...",
  "sender": "user@email.com"
}
```

**Odpowiedź:**
```json
{
  "label": "IT",
  "confidence": 0.92,
  "timestamp": "2024-11-20T10:30:00",
  "email_preview": {
    "subject": "Błąd logowania",
    "body": "Nie mogę się zalogować do systemu..."
  }
}
```

### Metryki
```http
GET /metrics
```

**Odpowiedź:**
```json
{
  "accuracy": 0.95,
  "f1_score": 0.94,
  "precision": 0.95,
  "recall": 0.93,
  "total_predictions": 20
}
```

### Dane Treningowe
```http
GET /training-data
```

### Działy
```http
GET /departments
```

### Historia
```http
GET /history?limit=10
```

## 🎨 UI Features

- **Gradient Design** - Nowoczesny wygląd z gradientami
- **Animacje** - Płynne przejścia i efekty
- **Responsywność** - Działa na wszystkich urządzeniach
- **Real-time Updates** - Natychmiastowe wyniki
- **Przykłady** - Predefiniowane e-maile do testowania

## 🧪 Testowanie

### Test klasyfikacji
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Problem z serwerem",
    "body": "Serwer nie odpowiada od godziny"
  }'
```

### Test metryk
```bash
curl http://localhost:8000/metrics
```

## 📦 Deployment

### Docker (Opcjonalnie)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t email-classifier .
docker run -p 8000:8000 --env-file .env email-classifier
```

### Azure App Service

```bash
az webapp up \
  --name email-classifier \
  --resource-group email-classifier-rg \
  --runtime "PYTHON:3.11" \
  --sku B1
```

## 🔐 Bezpieczeństwo

- ✅ Nie commituj plików `.env`
- ✅ Używaj Azure Key Vault dla sekretów
- ✅ Włącz HTTPS w produkcji
- ✅ Ogranicz CORS do zaufanych domen
- ✅ Rotuj klucze API regularnie

## 📝 Notatki Implementacyjne

### Few-Shot Learning

System używa few-shot learning - przekazuje 2 przykłady z każdej kategorii do GPT-4o-mini, co pozwala na:
- Lepszą dokładność bez fine-tuningu
- Szybkie dostosowanie do nowych kategorii
- Niższe koszty niż pełny fine-tuning

### Fallback Classifier

Jeśli Azure OpenAI nie jest dostępny, system automatycznie przełącza się na klasyfikator regułowy oparty na słowach kluczowych.

## 🐛 Troubleshooting

### Backend nie startuje
```bash
# Sprawdź czy port 8000 jest wolny
netstat -ano | findstr :8000

# Użyj innego portu
uvicorn backend.main:app --port 8001
```

### Azure OpenAI błędy
```bash
# Sprawdź klucze
curl -H "api-key: YOUR_KEY" YOUR_ENDPOINT/openai/deployments?api-version=2024-08-01-preview

# Sprawdź limity
az cognitiveservices account list-usage
```

### Frontend nie łączy się z API
```bash
# Sprawdź CORS w backend/main.py
# Upewnij się że frontend działa na http://localhost:8080
```

## 📚 Dodatkowe Zasoby

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

## 👥 Autor

Projekt wykonany na potrzeby prezentacji Azure AI Foundry.

## 📄 Licencja

MIT License - możesz swobodnie używać w swoich projektach.

---

**Powodzenia z prezentacją! 🚀**
