# 🏭 Azure AI Foundry - Kompletny Przewodnik

## Czym jest Azure AI Foundry?

Azure AI Foundry to zintegrowana platforma do budowania, trenowania i wdrażania modeli AI. Oferuje:

- **AI Studio** - środowisko wizualne do pracy z modelami
- **Model Catalog** - dostęp do pre-trained models
- **Fine-tuning** - dostosowywanie modeli do własnych danych
- **Deployment** - wdrażanie modeli do produkcji
- **Monitoring** - śledzenie wydajności i kosztów

## 📋 Krok po Kroku: Setup w Azure Portal

### Faza 1: Przygotowanie Konta Azure

1. **Utwórz konto Azure** (jeśli nie masz)
   - Przejdź do https://portal.azure.com
   - Kliknij "Start free" lub zaloguj się
   - Potrzebujesz karty kredytowej (nie będzie obciążona bez zgody)

2. **Aktywuj kredyty studenckie** (jeśli jesteś studentem)
   - Azure for Students: $100 kredytów
   - Nie wymaga karty kredytowej
   - Link: https://azure.microsoft.com/free/students/

### Faza 2: Tworzenie Resource Group

```bash
# Opcja 1: Azure Portal
1. W Azure Portal kliknij "Resource groups"
2. Kliknij "+ Create"
3. Wypełnij:
   - Subscription: Twoja subskrypcja
   - Resource group name: email-classifier-rg
   - Region: East US
4. Kliknij "Review + create" → "Create"

# Opcja 2: Azure CLI
az group create \
  --name email-classifier-rg \
  --location eastus
```

### Faza 3: Azure OpenAI Service

#### 3.1 Tworzenie Zasobu

1. W Azure Portal, kliknij **"+ Create a resource"**
2. Wyszukaj **"Azure OpenAI"**
3. Kliknij **"Create"**

4. Wypełnij formularz:
```
Basics:
  Subscription: [Twoja subskrypcja]
  Resource group: email-classifier-rg
  Region: East US (sprawdź dostępność!)
  Name: email-classifier-openai
  Pricing tier: Standard S0

Networking:
  Network: All networks (dla developmentu)
  
Tags:
  Environment: Development
  Project: EmailClassifier
```

5. Kliknij **"Review + create"** → **"Create"**
6. Czekaj ~2-5 minut na deployment

#### 3.2 Sprawdzenie Dostępności Regionu

⚠️ **Ważne**: Nie wszystkie regiony mają Azure OpenAI!

Dostępne regiony (na listopad 2024):
- ✅ East US
- ✅ East US 2
- ✅ South Central US
- ✅ West Europe
- ✅ France Central
- ✅ Sweden Central

Sprawdź aktualną listę: https://learn.microsoft.com/azure/ai-services/openai/concepts/models#model-availability

### Faza 4: Deploy Model GPT-4o-mini

#### 4.1 W Azure Portal

1. Przejdź do swojego zasobu **email-classifier-openai**
2. W menu po lewej, kliknij **"Model deployments"**
3. Kliknij **"+ Create new deployment"**

4. Wypełnij:
```
Select a model: gpt-4o-mini
Model version: Latest (domyślnie)
Deployment name: gpt-4o-mini
Deployment type: Standard

Advanced options:
  Tokens per Minute Rate Limit: 10K (można zwiększyć później)
  Content filter: Default
```

5. Kliknij **"Create"**
6. Czekaj ~30 sekund na deployment

#### 4.2 Weryfikacja Deploymentu

```bash
# Test przez curl
curl -X POST "https://email-classifier-openai.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: YOUR_API_KEY" \
  -d '{
    "messages": [
      {"role": "user", "content": "Powiedz cześć"}
    ],
    "max_tokens": 50
  }'
```

### Faza 5: Pobranie Credentials

#### 5.1 Endpoint i Keys

1. W zasobie **email-classifier-openai**
2. Kliknij **"Keys and Endpoint"** w menu
3. Skopiuj:

```
Endpoint: 
https://email-classifier-openai.openai.azure.com/

KEY 1: 
[długi string znaków]

KEY 2: 
[drugi długi string - backup]
```

#### 5.2 Konfiguracja w Aplikacji

Utwórz plik `.env`:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://email-classifier-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=twój-key-1-tutaj
AZURE_OPENAI_API_VERSION=2024-08-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini

# App Config
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=INFO
```

## 🎓 Azure AI Foundry Studio

### Dostęp do AI Studio

1. Przejdź do https://ai.azure.com/
2. Zaloguj się tym samym kontem Azure
3. Wybierz swoją subskrypcję i resource group

### Funkcje AI Studio

#### 1. Playground

- **Chat Playground**: Testuj modele interaktywnie
- **Completions**: Testuj completion API
- **Embeddings**: Generuj embeddingi

```
Przejdź do: AI Studio → Playgrounds → Chat
1. Wybierz deployment: gpt-4o-mini
2. Wprowadź system prompt
3. Testuj zapytania
4. Zobacz przykłady JSON/Python
```

#### 2. Fine-tuning

##### Przygotowanie Danych

```python
# prepare_training_data.py
import json

def convert_to_jsonl():
    with open('data/training_emails.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open('fine_tune_data.jsonl', 'w', encoding='utf-8') as f:
        for item in data:
            example = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Klasyfikujesz e-maile do działów: IT, Księgowość, Obsługa Klienta, Sprzedaż"
                    },
                    {
                        "role": "user",
                        "content": f"Temat: {item['subject']}\nTreść: {item['body']}"
                    },
                    {
                        "role": "assistant",
                        "content": item['label']
                    }
                ]
            }
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

convert_to_jsonl()
```

##### Upload i Training

```bash
# 1. Upload pliku
az cognitiveservices account deployment create \
  --name email-classifier-openai \
  --resource-group email-classifier-rg \
  --deployment-name email-classifier-ft \
  --model-format OpenAI \
  --model-name gpt-4o-mini \
  --model-version "0301" \
  --sku-capacity 1 \
  --sku-name "Standard"

# 2. Start fine-tuning job
az ml job create --file fine-tune-job.yml
```

##### Lub przez AI Studio:

```
1. AI Studio → Fine-tuning → Create
2. Upload: fine_tune_data.jsonl
3. Validation: Opcjonalnie upload validation set
4. Base model: gpt-4o-mini
5. Hyperparameters:
   - Epochs: 3
   - Batch size: Auto
   - Learning rate: Auto
6. Start training
7. Monitor w "Jobs"
```

#### 3. Evaluation

AI Studio oferuje automatyczną ewaluację:

```
1. AI Studio → Evaluation → Create
2. Select model: Twój fine-tuned model
3. Upload test data
4. Choose metrics:
   - ✅ Accuracy
   - ✅ F1 Score
   - ✅ Precision
   - ✅ Recall
5. Run evaluation
6. View results
```

## 💰 Koszty i Limity

### Pricing GPT-4o-mini

**Pay-as-you-go:**
- Input: $0.00015 / 1K tokens (~$0.15 / 1M tokens)
- Output: $0.0006 / 1K tokens (~$0.60 / 1M tokens)

**Przykładowy koszt:**
- 1 email (200 tokens) → $0.00003
- 1000 emaili → $0.03
- 100,000 emaili → $3

### Rate Limits (Default)

```
Tokens per minute (TPM): 10,000
Requests per minute (RPM): 100

Możesz zwiększyć przez:
1. Azure Portal → Resource → Quotas
2. Request quota increase
3. Czekaj na approval (~1-2 dni)
```

### Monitoring Kosztów

```bash
# Azure CLI
az consumption usage list \
  --start-date 2024-11-01 \
  --end-date 2024-11-30 \
  --query "[?contains(instanceName, 'email-classifier')]"

# Lub w Azure Portal:
Cost Management + Billing → Cost Analysis
Filter by: Resource = email-classifier-openai
```

## 🔒 Bezpieczeństwo

### 1. Key Vault Integration

```bash
# Utwórz Key Vault
az keyvault create \
  --name email-classifier-kv \
  --resource-group email-classifier-rg \
  --location eastus

# Dodaj secret
az keyvault secret set \
  --vault-name email-classifier-kv \
  --name openai-api-key \
  --value "your-api-key"

# Pobierz w aplikacji
az keyvault secret show \
  --vault-name email-classifier-kv \
  --name openai-api-key \
  --query value -o tsv
```

### 2. Managed Identity

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(
    vault_url="https://email-classifier-kv.vault.azure.net/",
    credential=credential
)

api_key = client.get_secret("openai-api-key").value
```

### 3. Private Endpoints

```
Azure Portal → Resource → Networking
1. Disable public network access
2. Add private endpoint
3. Connect to VNet
```

## 📊 Monitoring i Logging

### Application Insights

```bash
# Utwórz App Insights
az monitor app-insights component create \
  --app email-classifier-insights \
  --location eastus \
  --resource-group email-classifier-rg \
  --application-type web

# Pobierz Instrumentation Key
az monitor app-insights component show \
  --app email-classifier-insights \
  --resource-group email-classifier-rg \
  --query instrumentationKey
```

### Integracja w Kodzie

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=your-key'
))

# Log events
logger.info('Email classified', extra={'label': 'IT', 'confidence': 0.95})
```

### Alerty

```
Azure Portal → email-classifier-insights → Alerts
1. Create alert rule
2. Condition: 
   - Metric: Failed Requests
   - Threshold: > 10 in 5 minutes
3. Action: Email notification
4. Save
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy Email Classifier

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Deploy to Azure
      uses: azure/webapps-deploy@v2
      with:
        app-name: email-classifier
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## 📖 Dokumentacja dla Prezentacji

### Slajdy do Pokazania

**Slajd 1: Problem**
- Firma otrzymuje 1000+ emaili dziennie
- Ręczne sortowanie zajmuje 5h/dzień
- Błędy w routingu → niezadowoleni klienci

**Slajd 2: Rozwiązanie**
- AI-powered klasyfikacja
- Azure OpenAI GPT-4o-mini
- Few-shot learning
- 95%+ accuracy

**Slajd 3: Architektura**
```
┌─────────────┐
│   Email     │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  FastAPI Backend    │
│  + Classifier       │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Azure OpenAI       │
│  GPT-4o-mini        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  IT/Księgowość/     │
│  Obsługa/Sprzedaż   │
└─────────────────────┘
```

**Slajd 4: Metryki**
- Accuracy: 95%
- F1-Score: 94%
- Response time: <500ms
- Cost: $0.03/1000 emails

**Slajd 5: Demo**
- Live klasyfikacja
- UI showcase
- Różne przykłady

## ❓ FAQ

**Q: Czy potrzebuję płatnej subskrypcji?**
A: Możesz użyć Azure for Students ($100 free) lub Free Trial.

**Q: Jak długo trwa setup?**
A: ~30 minut od zera do działającej aplikacji.

**Q: Co jeśli nie mam dostępu do Azure OpenAI?**
A: Aplikacja ma fallback classifier (rule-based).

**Q: Czy mogę użyć innych modeli?**
A: Tak! Zmień `AZURE_OPENAI_DEPLOYMENT` na np. `gpt-4`.

**Q: Jak zwiększyć limity?**
A: Azure Portal → Resource → Quotas → Request Increase.

## 🎯 Checklist przed Prezentacją

- [ ] Zainstalowane wszystkie dependencje
- [ ] Backend działa na localhost:8000
- [ ] Frontend działa na localhost:8080
- [ ] Azure OpenAI skonfigurowany (lub fallback ready)
- [ ] Przygotowane przykładowe emaile
- [ ] Screenshot metryk
- [ ] Backup prezentacji (gdyby coś nie działało)

---

**Good luck! 🚀**
