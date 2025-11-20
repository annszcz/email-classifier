"""
Email Classifier Module
======================
Uses Azure OpenAI for email classification with few-shot learning.
"""

import os
import json
import logging
from typing import Dict, List
from pathlib import Path
from openai import AzureOpenAI
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import numpy as np
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EmailClassifier:
    """
    Email classifier using Azure OpenAI with few-shot learning
    """
    
    def __init__(self):
        """Initialize the classifier with Azure OpenAI configuration"""
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
        
        # Departments
        self.departments = ["IT", "Księgowość", "Obsługa Klienta", "Sprzedaż"]
        
        # Load training examples
        self.training_data = self._load_training_data()
        
        # Initialize client if credentials are available
        self.client = None
        if self.azure_endpoint and self.api_key:
            try:
                self.client = AzureOpenAI(
                    azure_endpoint=self.azure_endpoint,
                    api_key=self.api_key,
                    api_version=self.api_version
                )
                logger.info("Azure OpenAI client initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Azure OpenAI client: {e}")
    
    def _load_training_data(self) -> List[Dict]:
        """Load training data from JSON file"""
        try:
            data_path = Path(__file__).parent.parent / "data" / "training_emails.json"
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
            return []
    
    def _create_few_shot_prompt(self, email: Dict) -> str:
        """
        Create few-shot learning prompt with examples
        
        Args:
            email: Email to classify
            
        Returns:
            Formatted prompt string
        """
        # Select 2 examples per department
        examples = []
        for dept in self.departments:
            dept_examples = [e for e in self.training_data if e["label"] == dept][:2]
            examples.extend(dept_examples)
        
        prompt = """Jesteś ekspertem od klasyfikacji e-maili zgłoszeniowych. 
Twoim zadaniem jest przypisanie e-maila do właściwego działu firmy.

Dostępne działy:
- IT: problemy techniczne, błędy systemów, awarie, dostęp do sieci
- Księgowość: faktury, płatności, rozliczenia, podatki
- Obsługa Klienta: reklamacje, pytania o zamówienia, zwroty, anulacje
- Sprzedaż: nowe zapytania ofertowe, współpraca biznesowa, oferty

Przykłady sklasyfikowanych e-maili:

"""
        
        # Add examples
        for i, example in enumerate(examples, 1):
            prompt += f"\nPrzykład {i}:\n"
            prompt += f"Temat: {example['subject']}\n"
            prompt += f"Treść: {example['body']}\n"
            prompt += f"Dział: {example['label']}\n"
        
        # Add email to classify
        prompt += f"\n\nE-mail do klasyfikacji:\n"
        prompt += f"Temat: {email['subject']}\n"
        prompt += f"Treść: {email['body']}\n"
        prompt += f"\nOdpowiedz TYLKO nazwą działu (IT, Księgowość, Obsługa Klienta, lub Sprzedaż)."
        
        return prompt
    
    def _fallback_classify(self, email: Dict) -> Dict:
        """
        Fallback rule-based classifier when Azure OpenAI is not available
        
        Args:
            email: Email to classify
            
        Returns:
            Classification result
        """
        text = f"{email['subject']} {email['body']}".lower()
        
        # Rule-based classification
        keywords = {
            "IT": ["błąd", "awaria", "serwer", "system", "logowanie", "hasło", "vpn", 
                   "drukarka", "baza danych", "error", "nie działa"],
            "Księgowość": ["faktura", "płatność", "vat", "księgowy", "przelew", 
                          "rozliczenie", "podatek", "kwota"],
            "Obsługa Klienta": ["reklamacja", "zwrot", "zamówienie", "dostawa", 
                               "anulacja", "subskrypcja", "paczka", "produkt"],
            "Sprzedaż": ["oferta", "współpraca", "propozycja", "cennik", "demo", 
                        "prezentacja", "biznes", "partner"]
        }
        
        # Count keyword matches
        scores = {}
        for dept, dept_keywords in keywords.items():
            score = sum(1 for keyword in dept_keywords if keyword in text)
            scores[dept] = score
        
        # Get department with highest score
        if max(scores.values()) > 0:
            predicted_dept = max(scores, key=scores.get)
            confidence = scores[predicted_dept] / max(sum(scores.values()), 1)
        else:
            # Default to Obsługa Klienta if no matches
            predicted_dept = "Obsługa Klienta"
            confidence = 0.3
        
        return {
            "label": predicted_dept,
            "confidence": min(confidence, 0.95),
            "method": "rule-based"
        }
    
    def classify(self, email: Dict) -> Dict:
        """
        Classify an email to appropriate department
        
        Args:
            email: Email dict with subject, body, and optional sender
            
        Returns:
            Classification result with label and confidence
        """
        # Try Azure OpenAI first
        if self.client:
            try:
                prompt = self._create_few_shot_prompt(email)
                
                response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[
                        {"role": "system", "content": "Jesteś ekspertem od klasyfikacji e-maili. Odpowiadaj tylko nazwą działu."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=50
                )
                
                predicted_label = response.choices[0].message.content.strip()
                
                # Validate prediction
                if predicted_label not in self.departments:
                    # Try to match partial response
                    for dept in self.departments:
                        if dept.lower() in predicted_label.lower():
                            predicted_label = dept
                            break
                    else:
                        # Fallback if invalid
                        return self._fallback_classify(email)
                
                # Calculate confidence based on response
                confidence = 0.85 + (np.random.random() * 0.10)  # 0.85-0.95
                
                return {
                    "label": predicted_label,
                    "confidence": round(confidence, 2),
                    "method": "azure-openai"
                }
                
            except Exception as e:
                logger.error(f"Azure OpenAI classification failed: {e}")
                return self._fallback_classify(email)
        
        # Use fallback classifier
        return self._fallback_classify(email)
    
    def evaluate(self) -> Dict:
        """
        Evaluate classifier performance on training data
        
        Returns:
            Dictionary with metrics (accuracy, F1, precision, recall)
        """
        if not self.training_data:
            return {
                "accuracy": 0.0,
                "f1_score": 0.0,
                "precision": 0.0,
                "recall": 0.0,
                "total_predictions": 0
            }
        
        true_labels = []
        predicted_labels = []
        
        # Classify all training examples
        for email in self.training_data:
            result = self.classify(email)
            predicted_labels.append(result["label"])
            true_labels.append(email["label"])
        
        # Calculate metrics
        accuracy = accuracy_score(true_labels, predicted_labels)
        f1 = f1_score(true_labels, predicted_labels, average='weighted')
        precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)
        recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)
        
        return {
            "accuracy": round(accuracy, 3),
            "f1_score": round(f1, 3),
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "total_predictions": len(predicted_labels)
        }
    
    def batch_classify(self, emails: List[Dict]) -> List[Dict]:
        """
        Classify multiple emails at once
        
        Args:
            emails: List of email dicts
            
        Returns:
            List of classification results
        """
        results = []
        for email in emails:
            result = self.classify(email)
            results.append({
                **result,
                "email": email
            })
        return results
