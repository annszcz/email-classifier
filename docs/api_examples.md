# 🔌 API Usage Examples

## Podstawowe Użycie

### Python

```python
import requests
import json

# Endpoint
API_URL = "http://localhost:8000"

# Przykładowy e-mail do klasyfikacji
email = {
    "subject": "Problem z serwerem",
    "body": "Serwer produkcyjny nie odpowiada. Proszę o pilną interwencję.",
    "sender": "admin@firma.pl"
}

# Wyślij zapytanie
response = requests.post(
    f"{API_URL}/classify",
    json=email
)

# Pobierz wynik
result = response.json()
print(f"Dział: {result['label']}")
print(f"Pewność: {result['confidence'] * 100}%")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

async function classifyEmail() {
    const email = {
        subject: "Pytanie o fakturę",
        body: "Czy mogę prosić o przesłanie faktury VAT?",
        sender: "klient@email.com"
    };

    try {
        const response = await axios.post(
            'http://localhost:8000/classify',
            email
        );

        console.log(`Dział: ${response.data.label}`);
        console.log(`Pewność: ${response.data.confidence * 100}%`);
    } catch (error) {
        console.error('Błąd:', error.message);
    }
}

classifyEmail();
```

### cURL

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Reklamacja produktu",
    "body": "Produkt ma wadę i chciałbym go zwrócić",
    "sender": "klient@example.com"
  }'
```

---

## Wszystkie Endpointy

### 1. Klasyfikacja E-maila

**POST** `/classify`

**Request:**
```json
{
  "subject": "string",
  "body": "string",
  "sender": "string (optional)"
}
```

**Response:**
```json
{
  "label": "IT",
  "confidence": 0.92,
  "timestamp": "2024-11-20T10:30:00",
  "email_preview": {
    "subject": "Problem z serwerem",
    "body": "Serwer produkcyjny nie odpowiada..."
  }
}
```

**Python Example:**
```python
result = requests.post(f"{API_URL}/classify", json={
    "subject": "Błąd logowania",
    "body": "Nie mogę się zalogować do systemu"
}).json()
```

---

### 2. Metryki Modelu

**GET** `/metrics`

**Response:**
```json
{
  "accuracy": 0.95,
  "f1_score": 0.94,
  "precision": 0.95,
  "recall": 0.93,
  "total_predictions": 20
}
```

**Python Example:**
```python
metrics = requests.get(f"{API_URL}/metrics").json()
print(f"Accuracy: {metrics['accuracy'] * 100}%")
```

---

### 3. Dane Treningowe

**GET** `/training-data`

**Response:**
```json
{
  "emails": [...],
  "total_count": 20,
  "labels": ["IT", "Księgowość", "Obsługa Klienta", "Sprzedaż"]
}
```

**Python Example:**
```python
data = requests.get(f"{API_URL}/training-data").json()
print(f"Total emails: {data['total_count']}")
print(f"Labels: {data['labels']}")
```

---

### 4. Lista Działów

**GET** `/departments`

**Response:**
```json
{
  "departments": ["IT", "Księgowość", "Obsługa Klienta", "Sprzedaż"],
  "total": 4
}
```

**Python Example:**
```python
depts = requests.get(f"{API_URL}/departments").json()
print(f"Dostępne działy: {', '.join(depts['departments'])}")
```

---

### 5. Historia Klasyfikacji

**GET** `/history?limit=10`

**Response:**
```json
{
  "history": [
    {
      "label": "IT",
      "confidence": 0.92,
      "timestamp": "2024-11-20T10:30:00",
      "subject": "Problem z serwerem"
    }
  ],
  "total": 10
}
```

**Python Example:**
```python
history = requests.get(f"{API_URL}/history?limit=5").json()
for item in history['history']:
    print(f"{item['timestamp']}: {item['label']} ({item['confidence']})")
```

---

### 6. Czyszczenie Historii

**DELETE** `/history`

**Response:**
```json
{
  "message": "History cleared",
  "status": "success"
}
```

**Python Example:**
```python
response = requests.delete(f"{API_URL}/history")
print(response.json()['message'])
```

---

### 7. Health Check

**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-20T10:30:00"
}
```

**Python Example:**
```python
health = requests.get(f"{API_URL}/health").json()
print(f"Status: {health['status']}")
```

---

## Zaawansowane Przykłady

### Batch Classification

```python
import requests
import json

def classify_batch(emails):
    """Klasyfikuj wiele e-maili"""
    results = []
    
    for email in emails:
        response = requests.post(
            "http://localhost:8000/classify",
            json=email
        )
        results.append(response.json())
    
    return results

# Przykład użycia
emails = [
    {"subject": "Błąd systemu", "body": "System nie działa"},
    {"subject": "Faktura", "body": "Proszę o fakturę VAT"},
    {"subject": "Reklamacja", "body": "Chcę zwrócić produkt"}
]

results = classify_batch(emails)
for i, result in enumerate(results):
    print(f"Email {i+1}: {result['label']} ({result['confidence']*100:.1f}%)")
```

### Error Handling

```python
import requests
from requests.exceptions import RequestException

def safe_classify(email):
    """Klasyfikacja z obsługą błędów"""
    try:
        response = requests.post(
            "http://localhost:8000/classify",
            json=email,
            timeout=5  # 5 sekund timeout
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        print("Błąd: Przekroczono czas oczekiwania")
        return None
        
    except requests.exceptions.ConnectionError:
        print("Błąd: Nie można połączyć z API")
        return None
        
    except requests.exceptions.HTTPError as e:
        print(f"Błąd HTTP: {e}")
        return None
        
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return None

# Użycie
result = safe_classify({
    "subject": "Test",
    "body": "Test email"
})

if result:
    print(f"Wynik: {result['label']}")
else:
    print("Klasyfikacja nie powiodła się")
```

### Async Classification (Python)

```python
import asyncio
import aiohttp

async def classify_async(session, email):
    """Asynchroniczna klasyfikacja"""
    async with session.post(
        'http://localhost:8000/classify',
        json=email
    ) as response:
        return await response.json()

async def classify_many_async(emails):
    """Klasyfikuj wiele e-maili równolegle"""
    async with aiohttp.ClientSession() as session:
        tasks = [classify_async(session, email) for email in emails]
        results = await asyncio.gather(*tasks)
        return results

# Użycie
emails = [
    {"subject": f"Email {i}", "body": f"Treść {i}"}
    for i in range(10)
]

results = asyncio.run(classify_many_async(emails))
print(f"Sklasyfikowano {len(results)} e-maili")
```

### Integration with Email Client

```python
import imaplib
import email
from email.header import decode_header
import requests

def process_unread_emails():
    """Przetwórz nieprzeczytane e-maile z Gmail"""
    
    # Połącz z Gmail
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("your-email@gmail.com", "your-password")
    mail.select("inbox")
    
    # Znajdź nieprzeczytane
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    
    for email_id in email_ids:
        # Pobierz e-mail
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])
        
        # Dekoduj temat
        subject = decode_header(msg["Subject"])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode()
        
        # Pobierz treść
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        
        # Klasyfikuj
        result = requests.post(
            "http://localhost:8000/classify",
            json={
                "subject": subject,
                "body": body[:1000],  # Pierwsze 1000 znaków
                "sender": msg["From"]
            }
        ).json()
        
        print(f"Email: {subject}")
        print(f"Dział: {result['label']}")
        print(f"Pewność: {result['confidence']*100:.1f}%")
        print("-" * 50)
    
    mail.close()
    mail.logout()

# Użycie
# process_unread_emails()
```

---

## Rate Limiting

Domyślnie brak limitów w local deployment. W produkcji rozważ:

```python
from time import sleep

def classify_with_rate_limit(emails, max_per_second=10):
    """Klasyfikacja z rate limiting"""
    results = []
    delay = 1.0 / max_per_second
    
    for email in emails:
        result = requests.post(
            "http://localhost:8000/classify",
            json=email
        ).json()
        results.append(result)
        sleep(delay)
    
    return results
```

---

## Testing API

```python
import pytest
import requests

API_URL = "http://localhost:8000"

def test_classify_endpoint():
    """Test klasyfikacji"""
    response = requests.post(
        f"{API_URL}/classify",
        json={
            "subject": "Test",
            "body": "Test body"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "confidence" in data

def test_metrics_endpoint():
    """Test metryk"""
    response = requests.get(f"{API_URL}/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "accuracy" in data
    assert "f1_score" in data

def test_invalid_email():
    """Test nieprawidłowego e-maila"""
    response = requests.post(
        f"{API_URL}/classify",
        json={"invalid": "data"}
    )
    assert response.status_code == 422  # Validation error

# Run tests
# pytest examples/api_examples.py
```

---

## Performance Monitoring

```python
import requests
import time
import statistics

def benchmark_api(n_requests=100):
    """Benchmark API performance"""
    
    email = {
        "subject": "Test email",
        "body": "This is a test email body"
    }
    
    times = []
    
    for i in range(n_requests):
        start = time.time()
        response = requests.post(
            "http://localhost:8000/classify",
            json=email
        )
        elapsed = time.time() - start
        times.append(elapsed)
        
        if (i + 1) % 10 == 0:
            print(f"Processed {i + 1}/{n_requests}")
    
    print(f"\nResults for {n_requests} requests:")
    print(f"Mean: {statistics.mean(times)*1000:.2f}ms")
    print(f"Median: {statistics.median(times)*1000:.2f}ms")
    print(f"Min: {min(times)*1000:.2f}ms")
    print(f"Max: {max(times)*1000:.2f}ms")
    print(f"Stdev: {statistics.stdev(times)*1000:.2f}ms")

# Run benchmark
# benchmark_api(100)
```

---

## Next Steps

1. Przeczytaj **README.md** dla pełnej dokumentacji
2. Zobacz **docs/ai_foundry_setup.md** dla Azure integration
3. Eksperymentuj z przykładami!

Happy coding! 🚀
