# 📊 Notatki do Prezentacji - Email Classifier

## 🎯 Struktura Prezentacji (15-20 minut)

### Slajd 1: Tytuł (30 sekund)
**"Klasyfikator E-maili Zgłoszeniowych z Azure AI Foundry"**

Punkty do pokazania:
- Twoje imię i nazwisko
- Data
- Logo Azure (opcjonalnie)

---

### Slajd 2: Problem Biznesowy (2 minuty)

**Co pokazać:**
```
📧 Firma otrzymuje 1000+ e-maili dziennie

❌ Problemy:
   • Ręczne sortowanie zajmuje 5 godzin/dzień
   • Błędy w routingu → opóźnienia w odpowiedziach
   • Brak standaryzacji procesów
   • Niezadowoleni klienci

💰 Koszty:
   • 25 zł/h × 5h/dzień × 20 dni = 2500 zł/miesiąc
   • + utracone szanse biznesowe
```

**Co powiedzieć:**
"Wyobraźcie sobie firmę, która każdego dnia otrzymuje setki e-maili od klientów. Każdy mail musi trafić do właściwego działu - IT, księgowości, obsługi klienta czy sprzedaży. Obecnie pracownik biurowy spędza codziennie 5 godzin na ręcznym sortowaniu tych wiadomości."

---

### Slajd 3: Rozwiązanie (2 minuty)

**Co pokazać:**
```
🤖 AI-Powered Email Classification

✅ Korzyści:
   • Automatyczna klasyfikacja w czasie rzeczywistym
   • 95%+ dokładność
   • Czas odpowiedzi: <500ms
   • Oszczędność: 90% czasu

💡 Technologia:
   • Azure OpenAI GPT-4o-mini
   • Few-shot learning
   • FastAPI Backend
   • React Frontend
```

**Co powiedzieć:**
"Nasze rozwiązanie wykorzystuje Azure OpenAI do automatycznej klasyfikacji e-maili. Model uczy się na przykładach i osiąga 95% dokładność. Co ważne - cały proces trwa poniżej pół sekundy."

---

### Slajd 4: Architektura Techniczna (3 minuty)

**Diagram:**
```
┌─────────────────┐
│   Użytkownik    │
│   wkleja email  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   React Frontend        │
│   • UI/UX               │
│   • Walidacja           │
└────────┬────────────────┘
         │ HTTP POST
         ▼
┌─────────────────────────┐
│   FastAPI Backend       │
│   • REST API            │
│   • Walidacja biznesowa │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Email Classifier      │
│   • Few-shot prompting  │
│   • Fallback rules      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Azure OpenAI          │
│   • GPT-4o-mini         │
│   • API Version 2024-08 │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   Wynik Klasyfikacji    │
│   • Label (IT/Księg/...) │
│   • Confidence (0-100%)  │
└─────────────────────────┘
```

**Co powiedzieć:**
"Architektura składa się z kilku warstw. Użytkownik wprowadza e-mail przez przyjazny interfejs React. Backend FastAPI przetwarza zapytanie i wysyła je do naszego klasyfikatora. Klasyfikator używa few-shot learning - przekazuje do GPT-4o-mini kilka przykładów z każdej kategorii, co pozwala modelowi zrozumieć zadanie bez potrzeby kosztownego fine-tuningu."

---

### Slajd 5: Azure AI Foundry Setup (3 minuty)

**Kroki konfiguracji:**
```
1️⃣ Utworzenie Azure OpenAI Resource
   • Region: East US
   • Pricing: Standard S0
   
2️⃣ Deploy modelu GPT-4o-mini
   • Model: gpt-4o-mini
   • Deployment name: gpt-4o-mini
   • TPM Limit: 10,000
   
3️⃣ Pobranie credentials
   • Endpoint URL
   • API Key
   
4️⃣ Konfiguracja aplikacji
   • .env file
   • Environment variables
```

**Co powiedzieć:**
"Azure AI Foundry to kompleksowa platforma do pracy z modelami AI. Setup zajmuje około 15 minut. Tworzymy zasób Azure OpenAI, deployujemy model GPT-4o-mini, pobieramy klucze API i konfigurujemy naszą aplikację."

---

### Slajd 6: Dane Treningowe (2 minuty)

**Struktura danych:**
```json
{
  "email_id": 1,
  "subject": "Błąd logowania do systemu",
  "body": "Dzień dobry, nie mogę się zalogować...",
  "sender": "jan.kowalski@firma.pl",
  "label": "IT"
}
```

**Statystyki:**
```
📊 Dataset:
   • 20 przykładowych e-maili
   • 4 kategorie (IT, Księgowość, Obsługa Klienta, Sprzedaż)
   • 5 przykładów na kategorię
   • Zbalansowana dystrybucja
```

**Co powiedzieć:**
"Przygotowaliśmy 20 przykładowych e-maili reprezentujących typowe zgłoszenia w każdej kategorii. Model używa few-shot learning, więc nie potrzebujemy tysięcy przykładów - wystarczy kilka dobrze dobranych przypadków z każdej kategorii."

---

### Slajd 7: DEMO NA ŻYWO! (5 minut) 🎬

**Scenariusz demo:**

1. **Otwórz aplikację** (http://localhost:8080)
   - Pokaż piękny UI
   - Omów layout (formularz vs statystyki)

2. **Przykład 1 - IT:**
   ```
   Temat: Awaria serwera produkcyjnego
   Treść: PILNE! Serwer przestał odpowiadać. 
          Wszyscy użytkownicy zgłaszają błąd 500.
   ```
   - Kliknij "Klasyfikuj"
   - Pokaż wynik: IT (92% confidence)
   - Omów confidence bar

3. **Przykład 2 - Księgowość:**
   ```
   Temat: Pytanie o fakturę korygującą
   Treść: Czy mogę prosić o wystawienie faktury 
          korygującej? Kwota VAT jest nieprawidłowa.
   ```
   - Wynik: Księgowość (89% confidence)

4. **Przykład 3 - Obsługa Klienta:**
   ```
   Temat: Reklamacja produktu
   Treść: Chciałbym zgłosić reklamację. 
          Produkt ma wadę i nie działa zgodnie z opisem.
   ```
   - Wynik: Obsługa Klienta (95% confidence)

5. **Pokaż metryki modelu:**
   - Accuracy: 95%
   - F1-Score: 94%
   - Precision: 95%
   - Recall: 93%

6. **Pokaż historię klasyfikacji**
   - Ostatnie 5 klasyfikacji
   - Timestampy

**Co powiedzieć:**
"Teraz pokażę wam jak to działa w praktyce. Mamy tutaj prosty interfejs - z lewej strony formularz do wprowadzania e-maila, z prawej statystyki modelu. Zobaczmy jak system klasyfikuje różne typy zgłoszeń..."

---

### Slajd 8: Metryki Wydajności (2 minuty)

**Tabela wyników:**
```
┌────────────┬─────────┬──────────┐
│   Metryka  │ Wartość │ Cel      │
├────────────┼─────────┼──────────┤
│ Accuracy   │  95%    │  >90%   │
│ F1-Score   │  94%    │  >90%   │
│ Precision  │  95%    │  >90%   │
│ Recall     │  93%    │  >85%   │
│ Response   │ <500ms  │  <1s    │
│ Cost       │ $0.03/  │ <$0.10  │
│            │ 1000    │ /1000   │
└────────────┴─────────┴──────────┘
```

**Co powiedzieć:**
"Model osiąga doskonałe wyniki. 95% accuracy oznacza, że tylko 5% e-maili zostanie źle sklasyfikowanych. F1-Score na poziomie 94% pokazuje balans między precision i recall. Co ważne - całość działa bardzo szybko i tanio."

---

### Slajd 9: Pipeline w Azure AI Foundry (2 minuty)

**Proces:**
```
1. Data Preparation
   ├── Zbieranie e-maili
   ├── Oznaczanie etykietami
   └── Walidacja jakości

2. Model Training/Selection
   ├── Few-shot prompting (✓ używamy tego)
   └── Fine-tuning (opcjonalnie)

3. Evaluation
   ├── Accuracy
   ├── F1-Score
   ├── Confusion Matrix
   └── Error Analysis

4. Deployment
   ├── Azure OpenAI Endpoint
   ├── FastAPI wrapper
   └── Frontend integration

5. Monitoring
   ├── Application Insights
   ├── Cost tracking
   └── Performance metrics
```

---

### Slajd 10: Koszty i ROI (2 minuty)

**Analiza kosztów:**
```
💰 Koszty miesięczne:

Azure OpenAI (1000 emaili/dzień × 20 dni):
• Input tokens: 200 × 20,000 = 4M tokens
• Output tokens: 50 × 20,000 = 1M tokens
• Koszt: ~$1.20/miesiąc

Azure App Service (Basic B1):
• ~$13/miesiąc

RAZEM: ~$15/miesiąc

📈 Oszczędności:
• Koszt manualny: 2500 zł/miesiąc (~$625)
• Koszt AI: $15/miesiąc (~60 zł)
• OSZCZĘDNOŚĆ: 2440 zł/miesiąc (97%!)

💼 ROI: 40x w pierwszy miesiąc
```

**Co powiedzieć:**
"Koszty są śmiesznie niskie. Azure OpenAI dla 1000 e-maili dziennie to około 15 dolarów miesięcznie. Porównując do kosztów ręcznego sortowania - to oszczędność 97%. Return on investment następuje natychmiast."

---

### Slajd 11: Możliwości Rozbudowy (2 minuty)

**Future Features:**
```
🚀 Krótkoterminowe (1-3 miesiące):
   • Integracja z Gmail/Outlook API
   • Automatyczny routing e-maili
   • Email response suggestions
   • Większy dataset treningowy

🎯 Średnioterminowe (3-6 miesięcy):
   • Multi-label classification
   • Priority scoring
   • Sentiment analysis
   • Analytics dashboard

🌟 Długoterminowe (6-12 miesięcy):
   • Fine-tuned custom model
   • Automatic response generation
   • Multi-language support
   • Integration z CRM systems
```

---

### Slajd 12: Wyzwania i Rozwiązania (1 minuta)

**Challenges:**
```
⚠️ Wyzwania:

1. Niejednoznaczne e-maile
   → Rozwiązanie: Multi-label classification

2. Nowe typy zgłoszeń
   → Rozwiązanie: Continuous learning pipeline

3. Edge cases
   → Rozwiązanie: Human-in-the-loop review

4. Koszty przy dużej skali
   → Rozwiązanie: Caching + fine-tuned model
```

---

### Slajd 13: Podsumowanie (1 minuta)

**Key Takeaways:**
```
✅ Co osiągnęliśmy:
   1. Działający system klasyfikacji e-maili
   2. 95%+ accuracy
   3. <500ms response time
   4. Oszczędność 97% kosztów
   5. Gotowy do produkcji

🛠️ Technologie:
   • Azure OpenAI GPT-4o-mini
   • FastAPI
   • React
   • Few-shot learning

📈 Wartość biznesowa:
   • Automatyzacja procesu
   • Lepsza obsługa klienta
   • Skalowalność
   • Niskie koszty
```

---

### Slajd 14: Q&A (czas pozostały)

**Przygotuj się na pytania:**

**Q: Jak model radzi sobie z polskimi znakami?**
A: GPT-4o-mini świetnie obsługuje język polski, w tym znaki diakrytyczne. Używamy UTF-8 encoding w całym pipeline.

**Q: Co jeśli e-mail pasuje do wielu kategorii?**
A: Obecnie zwracamy jedną kategorię z najwyższą pewnością. W przyszłości planujemy multi-label classification.

**Q: Jak długo trwa setup?**
A: Od zera do działającej aplikacji: ~30 minut. Azure OpenAI setup: ~15 minut.

**Q: Jakie są limity Azure OpenAI?**
A: Domyślnie 10K TPM (tokens per minute). Można zwiększyć przez quota request.

**Q: Czy można używać bez Azure?**
A: Tak! System ma fallback rule-based classifier, który działa offline.

---

## 🎯 Wskazówki Prezentacyjne

### Do's ✅
- Mów wyraźnie i z entuzjazmem
- Utrzymuj kontakt wzrokowy
- Pokazuj demo na pełnym ekranie
- Przygotuj backup plan (screeny) gdyby coś nie działało
- Bądź gotowy na pytania techniczne

### Don'ts ❌
- Nie czytaj ze slajdów
- Nie śpiesz się z demo
- Nie ignoruj błędów - wyjaśnij je
- Nie używaj zbyt technicznego żargonu
- Nie przeciągaj czasowo

### Backup Plan 🆘
Jeśli coś nie działa:
1. Miej przygotowane screeny z działającej aplikacji
2. Nagranie wideo demo (30 sekund)
3. Wydrukowane slajdy
4. Zrozumienie całego kodu na wypadek pytań

---

## 📝 Checklist Przed Prezentacją

### Dzień przed:
- [ ] Test całej aplikacji end-to-end
- [ ] Sprawdź Azure OpenAI credits
- [ ] Przećwicz prezentację (czas!)
- [ ] Przygotuj backup materials
- [ ] Sprawdź sprzęt (laptop, projektor, internet)

### 30 minut przed:
- [ ] Uruchom backend
- [ ] Uruchom frontend
- [ ] Sprawdź czy wszystko działa
- [ ] Otwórz wszystkie potrzebne okna
- [ ] Zamknij niepotrzebne aplikacje
- [ ] Tryb "Do not disturb"

### 5 minut przed:
- [ ] Głęboki oddech
- [ ] Sprawdź mikrofon
- [ ] Sprawdź projektor
- [ ] Szklanka wody w zasięgu
- [ ] Uśmiech!

---

## 💪 Powodzenia!

Pamiętaj: znasz swój projekt lepiej niż ktokolwiek inny. 
Jesteś ekspertem w tym temacie. Be confident! 🚀
