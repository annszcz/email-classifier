# 📁 Struktura Projektu Email Classifier

## Przegląd Plików

```
email-classifier/
│
├── 📄 README.md                    # Główna dokumentacja projektu
├── 📄 QUICKSTART.md                # Szybki start (5 minut do działania!)
├── 📄 requirements.txt             # Zależności Python
├── 📄 .env.example                 # Przykładowa konfiguracja Azure
├── 📄 .gitignore                   # Git ignore file
├── 🚀 start.bat                    # Skrypt startowy (Windows)
├── 🚀 start.sh                     # Skrypt startowy (Linux/Mac)
│
├── 📂 backend/                     # Backend API
│   ├── __init__.py
│   ├── main.py                     # FastAPI application + endpoints
│   └── classifier.py               # Email classifier logic
│
├── 📂 frontend/                    # Frontend UI
│   └── index.html                  # React single-page application
│
├── 📂 data/                        # Dane treningowe
│   └── training_emails.json       # 20 przykładowych e-maili
│
├── 📂 tests/                       # Testy jednostkowe
│   ├── __init__.py
│   └── test_classifier.py         # Testy dla classifiera
│
└── 📂 docs/                        # Dokumentacja
    ├── ai_foundry_setup.md         # Setup Azure AI Foundry
    ├── api_examples.md             # Przykłady użycia API
    ├── presentation_notes.md       # Notatki do prezentacji
    └── troubleshooting.md          # Rozwiązywanie problemów
```

## Opis Kluczowych Plików

### Backend (`backend/`)

#### `main.py` (400 linii)
**Odpowiedzialność:**
- FastAPI application setup
- REST API endpoints
- CORS configuration
- Request/response models
- Error handling

**Kluczowe endpointy:**
- `POST /classify` - Klasyfikacja e-maila
- `GET /metrics` - Metryki modelu
- `GET /training-data` - Dane treningowe
- `GET /history` - Historia klasyfikacji
- `GET /health` - Health check

**Technologie:**
- FastAPI 0.109.0
- Pydantic models
- Uvicorn ASGI server

---

#### `classifier.py` (350 linii)
**Odpowiedzialność:**
- Logika klasyfikacji e-maili
- Integracja z Azure OpenAI
- Few-shot learning prompts
- Fallback rule-based classifier
- Evaluation metrics

**Główne metody:**
- `classify()` - Klasyfikuj pojedynczy e-mail
- `batch_classify()` - Klasyfikuj wiele e-maili
- `evaluate()` - Oblicz metryki (accuracy, F1, etc.)
- `_fallback_classify()` - Backup classifier

**Technologie:**
- Azure OpenAI SDK
- scikit-learn (metrics)
- Few-shot prompting

---

### Frontend (`frontend/`)

#### `index.html` (600 linii)
**Odpowiedzialność:**
- React UI w jednym pliku
- Formularz klasyfikacji
- Wyświetlanie wyników
- Statystyki i metryki
- Historia klasyfikacji

**Komponenty:**
- Email input form
- Result display card
- Metrics dashboard
- Department badges
- History timeline
- Example emails

**Technologie:**
- React 18
- Babel standalone
- Font Awesome icons
- CSS3 animations

**Style:**
- Gradient backgrounds
- Smooth animations
- Responsive design
- Modern UI/UX

---

### Data (`data/`)

#### `training_emails.json` (150 linii)
**Format:**
```json
{
  "email_id": 1,
  "subject": "string",
  "body": "string",
  "sender": "email",
  "label": "IT|Księgowość|Obsługa Klienta|Sprzedaż"
}
```

**Zawartość:**
- 20 przykładowych e-maili
- 4 kategorie (5 per kategoria)
- Realistyczne scenariusze
- Polski język

---

### Tests (`tests/`)

#### `test_classifier.py` (200 linii)
**Pokrycie:**
- Inicjalizacja classifiera
- Klasyfikacja różnych typów e-maili
- Batch classification
- Metryki ewaluacji
- Fallback classifier
- Training data validation

**Framework:**
- pytest
- pytest fixtures
- Assertions

**Uruchomienie:**
```bash
pytest tests/ -v
```

---

### Documentation (`docs/`)

#### `ai_foundry_setup.md` (500+ linii)
**Zawiera:**
- Krok po kroku setup Azure
- Tworzenie resource
- Deploy model GPT-4o-mini
- Pobieranie credentials
- Fine-tuning (opcjonalnie)
- Monitoring i costs
- Security best practices

---

#### `api_examples.md` (400+ linii)
**Zawiera:**
- Przykłady w Python
- Przykłady w JavaScript
- cURL commands
- Batch processing
- Async operations
- Error handling
- Integration examples

---

#### `presentation_notes.md` (600+ linii)
**Zawiera:**
- Struktura prezentacji (14 slajdów)
- Szczegółowe notatki do każdego slajdu
- Scenariusz demo
- Timing (15-20 minut)
- Do's and Don'ts
- Backup plan
- Checklist przed prezentacją

---

#### `troubleshooting.md` (500+ linii)
**Zawiera:**
- Problemy z instalacją
- Problemy z backend
- Problemy z Azure OpenAI
- Problemy z frontend
- Debugging tips
- Common error messages
- Przydatne komendy

---

## Pliki Konfiguracyjne

### `requirements.txt`
```
fastapi==0.109.0           # Web framework
uvicorn[standard]==0.27.0  # ASGI server
openai==1.12.0             # Azure OpenAI SDK
scikit-learn==1.4.0        # Metrics
pydantic==2.5.3            # Data validation
pytest==7.4.3              # Testing
```

### `.env.example`
```
AZURE_OPENAI_ENDPOINT=https://...
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

---

## Skrypty Startowe

### `start.bat` (Windows)
**Funkcje:**
- Tworzy venv jeśli nie istnieje
- Instaluje zależności
- Kopiuje .env.example jeśli brak .env
- Uruchamia backend (port 8000)
- Uruchamia frontend (port 8080)
- Otwiera przeglądarkę

### `start.sh` (Linux/Mac)
**Funkcje:**
- Identyczne jak start.bat
- Dodatkowo: cleanup on exit
- SIGINT/SIGTERM handling

---

## Statystyki Projektu

```
Całkowite linie kodu:     ~2,500
  - Backend Python:       ~800
  - Frontend HTML/JS:     ~600
  - Tests:                ~200
  - Documentation:        ~1,500

Pliki:                    ~20

Technologie:              10+
  - Python 3.11
  - FastAPI
  - React 18
  - Azure OpenAI
  - scikit-learn
  - pytest
  - HTML5/CSS3
  - JavaScript ES6+
```

---

## Zależności Zewnętrzne

### Python Packages
- ✅ fastapi - REST API framework
- ✅ uvicorn - ASGI server
- ✅ openai - Azure OpenAI client
- ✅ scikit-learn - ML metrics
- ✅ pydantic - Data validation
- ✅ pytest - Testing

### JavaScript Libraries (CDN)
- ✅ React 18 - UI framework
- ✅ ReactDOM 18 - DOM rendering
- ✅ Babel - JSX transpiling
- ✅ Font Awesome 6.4 - Icons

### Azure Services
- ✅ Azure OpenAI - GPT-4o-mini
- ⭕ Azure App Service (optional)
- ⭕ Application Insights (optional)
- ⭕ Key Vault (optional)

---

## Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                    User Interface                    │
│              (React SPA - index.html)                │
│  • Input form                                        │
│  • Results display                                   │
│  • Metrics dashboard                                 │
└─────────────┬───────────────────────────────────────┘
              │ HTTP POST
              ▼
┌─────────────────────────────────────────────────────┐
│                   FastAPI Backend                    │
│                   (main.py)                          │
│  • Endpoint routing                                  │
│  • Request validation                                │
│  • Response formatting                               │
└─────────────┬───────────────────────────────────────┘
              │ function call
              ▼
┌─────────────────────────────────────────────────────┐
│                Email Classifier                      │
│                (classifier.py)                       │
│  • Few-shot prompt creation                          │
│  • Azure OpenAI API call                             │
│  • Fallback rule-based logic                         │
└─────────────┬───────────────────────────────────────┘
              │ API request
              ▼
┌─────────────────────────────────────────────────────┐
│              Azure OpenAI Service                    │
│                (GPT-4o-mini)                         │
│  • Model inference                                   │
│  • Text generation                                   │
│  • Classification result                             │
└─────────────┬───────────────────────────────────────┘
              │ response
              ▼
┌─────────────────────────────────────────────────────┐
│                  Classification Result               │
│  • Label: IT/Księgowość/Obsługa/Sprzedaż           │
│  • Confidence: 0-1                                   │
│  • Timestamp                                         │
└─────────────────────────────────────────────────────┘
```

---

## Development Workflow

```
1. Development
   ├── Write code
   ├── Run tests (pytest)
   ├── Test locally (uvicorn)
   └── Debug (logging)

2. Documentation
   ├── Update README
   ├── Document API
   ├── Write examples
   └── Update troubleshooting

3. Testing
   ├── Unit tests (pytest)
   ├── Integration tests (manual)
   ├── Performance tests (benchmark)
   └── End-to-end (UI testing)

4. Deployment
   ├── Local (start.sh/bat)
   ├── Docker (optional)
   ├── Azure App Service (optional)
   └── Monitoring (Application Insights)
```

---

## Next Steps

### Immediate (Po prezentacji)
1. ✅ Przejrzyj kod
2. ✅ Uruchom aplikację
3. ✅ Przetestuj funkcjonalność
4. ✅ Przygotuj prezentację

### Short-term (1-2 tygodnie)
1. ⭕ Skonfiguruj Azure OpenAI
2. ⭕ Dodaj więcej danych treningowych
3. ⭕ Zaimplementuj cache
4. ⭕ Dodaj rate limiting

### Long-term (1-3 miesiące)
1. ⭕ Fine-tune model
2. ⭕ Multi-label classification
3. ⭕ Integracja z Gmail/Outlook
4. ⭕ Analytics dashboard
5. ⭕ Auto-response generation

---

## Resources

### Documentation
- 📖 README.md - Start here!
- 📖 QUICKSTART.md - 5-minute setup
- 📖 docs/ - Comprehensive guides

### Code
- 💻 backend/ - Python backend
- 🎨 frontend/ - React UI
- 🧪 tests/ - Unit tests

### External Links
- [Azure OpenAI Docs](https://learn.microsoft.com/azure/ai-services/openai/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)

---

**Gotowy do startu? Otwórz QUICKSTART.md! 🚀**
