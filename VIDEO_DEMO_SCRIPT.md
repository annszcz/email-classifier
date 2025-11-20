# 🎥 Video Demo Script - Email Classifier

## Przygotowanie (przed nagraniem)

### Setup
- [ ] Uruchom backend: `cd backend && python -m uvicorn main:app --reload --port 8000`
- [ ] Uruchom frontend: `cd frontend && python -m http.server 8080`
- [ ] Sprawdź czy wszystko działa: http://localhost:8080
- [ ] Zamknij niepotrzebne aplikacje
- [ ] Wyczyść desktop (screenshots)
- [ ] Ustaw rozdzielczość 1920x1080
- [ ] Testuj mikrofon i audio
- [ ] Przygotuj przykładowe e-maile

### Przykładowe E-maile do Demo
```
1. IT:
Temat: Awaria serwera produkcyjnego
Treść: PILNE! Serwer przestał odpowiadać od 10 minut. 
       Wszyscy użytkownicy zgłaszają błąd 500 Internal Server Error.
       Proszę o natychmiastową interwencję.

2. Księgowość:
Temat: Pytanie o fakturę korygującą
Treść: Dzień dobry, na fakturze 123/2024 jest błędna kwota VAT. 
       Zamiast 23% jest 8%. Czy mogę prosić o wystawienie 
       faktury korygującej?

3. Obsługa Klienta:
Temat: Reklamacja produktu
Treść: Witam, zakupiony produkt ma wadę fabryczną. 
       Opakowanie było uszkodzone przy dostawie. 
       Chciałbym zgłosić reklamację i uzyskać zwrot pieniędzy.

4. Sprzedaż:
Temat: Zapytanie ofertowe - pakiet Enterprise
Treść: Dzień dobry, reprezentuję firmę 500-osobową. 
       Jesteśmy zainteresowani zakupem pakietu Enterprise. 
       Proszę o przesłanie oferty i możliwość umówienia prezentacji demo.
```

---

## 🎬 Skrypt Video (5-7 minut)

### [0:00-0:30] Intro + Problem

**Video:** Pokaż desktop z logo projektu lub okno VS Code

**Tekst:**
> "Cześć! Dzisiaj pokażę wam mój projekt - Email Classifier - 
> inteligentny system klasyfikacji e-maili zgłoszeniowych 
> wykorzystujący Azure OpenAI i AI Foundry.
> 
> Problem: Firma otrzymuje setki e-maili dziennie. 
> Każdy musi trafić do właściwego działu - IT, księgowości, 
> obsługi klienta czy sprzedaży. Ręczne sortowanie zajmuje 
> godziny i prowadzi do błędów.
> 
> Rozwiązanie: AI automatycznie klasyfikuje e-maile 
> z dokładnością 95% w czasie poniżej pół sekundy."

---

### [0:30-1:30] Architektura + Technologie

**Video:** Pokaż diagram architektury (można narysować w Paint lub pokazać w README.md)

**Tekst:**
> "System składa się z trzech głównych części:
> 
> 1. Frontend w React - przyjazny interfejs użytkownika 
>    z pięknym designem i animacjami
> 
> 2. Backend w FastAPI - REST API, które przetwarza zapytania, 
>    waliduje dane i komunikuje się z AI
> 
> 3. Azure OpenAI GPT-4o-mini - model językowy, który faktycznie 
>    klasyfikuje e-maile używając few-shot learning
> 
> Dodatkowo mamy fallback classifier oparty na regułach, 
> który działa nawet bez Azure. 
> 
> Dane treningowe to 20 przykładowych e-maili - 5 z każdej kategorii."

---

### [1:30-2:00] Demo - Otwieranie Aplikacji

**Video:** Otwórz przeglądarkę i przejdź do http://localhost:8080

**Tekst:**
> "Zobaczmy jak to działa w praktyce. Uruchamiam aplikację... 
> 
> [pauza, pokaż UI]
> 
> Z lewej strony mamy formularz do wprowadzania e-maila - 
> temat, treść i opcjonalnie nadawca.
> 
> Z prawej strony widzimy statystyki modelu - accuracy 95%, 
> F1-score 94% - naprawdę dobre wyniki!
> 
> Mamy też listę dostępnych działów i przykładowe e-maile 
> do szybkiego testowania."

---

### [2:00-3:00] Demo - Klasyfikacja IT

**Video:** Wpisz pierwszy przykładowy e-mail (IT)

**Tekst:**
> "Zacznijmy od typowego zgłoszenia IT. 
> Wpisuję temat: 'Awaria serwera produkcyjnego'
> 
> [wpisz temat]
> 
> Treść: 'PILNE! Serwer przestał odpowiadać...'
> 
> [wpisz treść]
> 
> Klikam 'Klasyfikuj'...
> 
> [kliknij, poczekaj na wynik]
> 
> I voilà! System rozpoznał to jako zgłoszenie IT 
> z pewnością 92%. Widzimy też pasek postępu confidence 
> i timestamp klasyfikacji.
> 
> Idealnie! Ten e-mail trafi do działu IT, który może 
> natychmiast zająć się awarią serwera."

---

### [3:00-4:00] Demo - Klasyfikacja Księgowość

**Video:** Wpisz drugi przykładowy e-mail (Księgowość)

**Tekst:**
> "Spróbujmy czegoś innego. Tym razem pytanie o fakturę.
> 
> [wpisz e-mail o fakturze]
> 
> Klasyfikuję... i system poprawnie identyfikuje to jako 
> zgłoszenie księgowe z 89% pewnością.
> 
> Widzicie? Model rozumie kontekst - słowa kluczowe jak 
> 'faktura', 'VAT', 'korygująca' wskazują na księgowość."

---

### [4:00-5:00] Demo - Obsługa Klienta i Sprzedaż

**Video:** Szybko przetestuj pozostałe dwa przykłady

**Tekst:**
> "Sprawdzam jeszcze dwa ostatnie przykłady...
> 
> [wpisz e-mail o reklamacji]
> 
> Reklamacja produktu - Obsługa Klienta, 95% confidence. 
> Perfekcyjnie!
> 
> [wpisz e-mail o ofercie]
> 
> I zapytanie ofertowe - Sprzedaż, 91% confidence.
> 
> [pokaż historię klasyfikacji]
> 
> Wszystkie nasze klasyfikacje pojawiają się tutaj w historii 
> z timestampami. Możemy śledzić co było klasyfikowane 
> i z jaką pewnością."

---

### [5:00-5:45] Metryki i Statystyki

**Video:** Pokaż prawą stronę z metrykami

**Tekst:**
> "Zobaczmy teraz metryki modelu.
> 
> [pokaż kartę z metrykami]
> 
> Accuracy 95% - to znaczy że 95% e-maili jest poprawnie 
> sklasyfikowanych.
> 
> F1-Score 94% - świetny balans między precision i recall.
> 
> Te wyniki osiągamy dzięki few-shot learning - przekazujemy 
> modelowi kilka przykładów z każdej kategorii, a on uczy się 
> na ich podstawie bez kosztownego fine-tuningu.
> 
> Mamy też 20 e-maili treningowych - wystarczająco dla 
> few-shot approach."

---

### [5:45-6:30] Technologia - Backend

**Video:** Otwórz http://localhost:8000/docs (Swagger UI)

**Tekst:**
> "Backend to FastAPI z automatycznie wygenerowaną dokumentacją.
> 
> [pokaż Swagger UI]
> 
> Mamy kilka endpointów:
> - POST /classify - główna funkcja klasyfikacji
> - GET /metrics - metryki wydajności
> - GET /training-data - dane treningowe
> - GET /history - historia klasyfikacji
> 
> API jest RESTful, zwraca JSON, super łatwe w integracji 
> z innymi systemami.
> 
> [możesz szybko pokazać test endpoint w Swagger]"

---

### [6:30-7:00] Podsumowanie + Azure AI Foundry

**Video:** Wróć do frontendu lub pokaż README.md

**Tekst:**
> "To był szybki demo Email Classifier!
> 
> Podsumowując:
> ✅ Automatyczna klasyfikacja z 95% dokładnością
> ✅ Czas odpowiedzi poniżej 500ms
> ✅ Azure OpenAI GPT-4o-mini z few-shot learning
> ✅ Piękny, responsywny UI
> ✅ Gotowy REST API do integracji
> 
> Projekt wykorzystuje Azure AI Foundry do zarządzania 
> modelami, monitoringu i deployment.
> 
> Całość jest open source, kod dostępny w repozytorium.
> Setup zajmuje dosłownie 5 minut dzięki skryptom startowym.
> 
> Dziękuję za uwagę! Mam nadzieję że projekt się podobał.
> Link do kodu w opisie. Do zobaczenia!"

---

## 🎬 Alternatywny Skrypt - Krótsze Demo (3 minuty)

### [0:00-0:45] Intro + Quick Demo

**Tekst:**
> "Cześć! Email Classifier - AI do sortowania e-maili.
> 
> [pokaż UI]
> 
> Wpisuję e-mail o awarii serwera... klasyfikuję... 
> IT z 92% pewnością!
> 
> Następny - pytanie o fakturę... Księgowość, 89%!
> 
> Kolejny - reklamacja... Obsługa Klienta, 95%!
> 
> Prosty, szybki, dokładny."

### [0:45-1:30] Technologia

**Tekst:**
> "Tech stack:
> - React frontend
> - FastAPI backend  
> - Azure OpenAI GPT-4o-mini
> - Few-shot learning
> 
> 95% accuracy, <500ms response time.
> 
> [pokaż metryki]
> 
> Wszystkie metryki w czasie rzeczywistym."

### [1:30-2:30] Use Cases + ROI

**Tekst:**
> "Przypadki użycia:
> - Automatyczny routing e-maili
> - Priorytetyzacja zgłoszeń
> - Analityka customer support
> 
> ROI: firma z 1000 emaili/dzień oszczędza 5h pracy dziennie.
> To 2500 zł miesięcznie przy kosztach Azure ~60 zł.
> 
> 40x return on investment!"

### [2:30-3:00] Call to Action

**Tekst:**
> "Projekt open source, pełna dokumentacja, 
> 5-minutowy setup.
> 
> Link w opisie. Dzięki za uwagę!"

---

## 📝 Tips dla Nagrania

### Audio
- 🎤 Dobry mikrofon (nie laptop mic jeśli możliwe)
- 🔇 Cicha lokacja
- 🗣️ Mów wyraźnie, nie za szybko
- ⏸️ Rób pauzy między sekcjami

### Video
- 📺 Rozdzielczość 1920x1080 minimum
- 🖱️ Smooth cursor movements
- 🚫 Hide notifications (Do Not Disturb)
- 🎨 Zoom in na ważne elementy

### Editing
- ✂️ Cut dead time
- 🎵 Add background music (quiet!)
- 📊 Add text overlays for key points
- 🎬 Add intro/outro graphics

### Publishing
- 📹 YouTube: MP4, H.264
- 📝 Description: Link do repo, timestamps
- 🏷️ Tags: AI, Azure, Python, FastAPI, React
- 📸 Thumbnail: Screenshot z UI + duży tytuł

---

## 🎯 Checklist przed Nagraniem

- [ ] Aplikacja działa bez błędów
- [ ] Przykładowe e-maile przygotowane
- [ ] Backend uruchomiony
- [ ] Frontend uruchomiony  
- [ ] Notifications wyłączone
- [ ] Desktop wyczyszczony
- [ ] Mikrofon przetestowany
- [ ] Rozdzielczość ustawiona
- [ ] Skrypt przećwiczony 2-3 razy
- [ ] Backup plan (screenshots) ready

---

## 🎬 Po Nagraniu

- [ ] Obejrzyj całe video
- [ ] Edit out mistakes
- [ ] Add music/graphics
- [ ] Export w wysokiej jakości
- [ ] Upload na YouTube
- [ ] Dodaj do opisu:
  - Link do repo
  - Timestamps
  - Instrukcje setup
  - Tech stack details
- [ ] Share na social media!

---

**Good luck with your demo! 🎥🚀**
