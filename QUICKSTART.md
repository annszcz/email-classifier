# ⚡ Quick Start Guide - 5 Minut do Działającej Aplikacji!

## 🚀 Najszybsza Droga

### Windows
```bash
# 1. Uruchom skrypt (jeden klik!)
start.bat
```

### Linux/Mac
```bash
# 1. Nadaj uprawnienia
chmod +x start.sh

# 2. Uruchom skrypt
./start.sh
```

To wszystko! Aplikacja otworzy się w przeglądarce.

---

## 🔧 Jeśli Wolisz Ręcznie

### Krok 1: Instalacja (2 minuty)
```bash
# Utwórz środowisko wirtualne
python -m venv venv

# Aktywuj (Windows)
venv\Scripts\activate

# Aktywuj (Linux/Mac)
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt
```

### Krok 2: Konfiguracja (1 minuta)
```bash
# Skopiuj przykładowy config
cp .env.example .env

# Edytuj .env (opcjonalne - działa bez Azure)
# Jeśli masz Azure OpenAI:
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_KEY=your-key-here
```

### Krok 3: Uruchomienie (1 minuta)
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
python -m http.server 8080
```

### Krok 4: Otwórz Przeglądarkę
```
http://localhost:8080
```

---

## ✅ Weryfikacja

Sprawdź czy wszystko działa:

1. **Backend API**
   - Otwórz: http://localhost:8000/docs
   - Powinieneś zobaczyć Swagger UI

2. **Frontend**
   - Otwórz: http://localhost:8080
   - Powinieneś zobaczyć piękny gradient UI

3. **Test Klasyfikacji**
   - Wpisz przykładowy email
   - Kliknij "Klasyfikuj"
   - Powinieneś dostać wynik w <1 sekundę

---

## 🆘 Problemy?

### Port już zajęty
```bash
# Backend na innym porcie
uvicorn backend.main:app --port 8001

# Frontend na innym porcie
python -m http.server 8081
```

### Brak Azure OpenAI
**Nie ma problemu!** Aplikacja działa z fallback classifierem opartym na regułach.

### Błędy importu
```bash
# Zainstaluj ponownie
pip install --upgrade -r requirements.txt
```

### Python nie znaleziony
- **Windows**: Zainstaluj Python 3.9+ z python.org
- **Linux**: `sudo apt install python3 python3-pip`
- **Mac**: `brew install python`

---

## 🎯 Co Dalej?

1. **Przetestuj aplikację**
   - Użyj przykładowych e-maili
   - Sprawdź metryki
   - Zobacz historię klasyfikacji

2. **Skonfiguruj Azure OpenAI** (opcjonalnie)
   - Zobacz: `docs/ai_foundry_setup.md`
   - Zajmuje ~15 minut
   - Daje 95%+ accuracy

3. **Przygotuj prezentację**
   - Zobacz: `docs/presentation_notes.md`
   - Kompletny scenariusz demo
   - Tips & tricks

---

## 📚 Dodatkowe Zasoby

- **README.md** - Pełna dokumentacja
- **docs/ai_foundry_setup.md** - Azure setup krok po kroku
- **docs/presentation_notes.md** - Notatki do prezentacji
- **API Docs** - http://localhost:8000/docs

---

## 🎉 Gotowe!

Twoja aplikacja działa! Teraz możesz:
- ✅ Klasyfikować e-maile
- ✅ Pokazać demo na prezentacji
- ✅ Rozbudowywać projekt

**Powodzenia! 🚀**
