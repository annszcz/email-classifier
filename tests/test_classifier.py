"""
Unit tests for Email Classifier
"""

import pytest
import json
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from classifier import EmailClassifier

class TestEmailClassifier:
    """Test suite for EmailClassifier"""
    
    @pytest.fixture
    def classifier(self):
        """Create classifier instance"""
        return EmailClassifier()
    
    @pytest.fixture
    def sample_emails(self):
        """Sample emails for testing"""
        return [
            {
                "subject": "Błąd 500 na serwerze",
                "body": "Serwer produkcyjny przestał odpowiadać. Błąd Internal Server Error.",
                "expected": "IT"
            },
            {
                "subject": "Pytanie o fakturę",
                "body": "Czy mogę prosić o przesłanie faktury VAT za listopad?",
                "expected": "Księgowość"
            },
            {
                "subject": "Reklamacja produktu",
                "body": "Chciałbym zgłosić reklamację. Produkt ma wadę i nie działa.",
                "expected": "Obsługa Klienta"
            },
            {
                "subject": "Oferta współpracy",
                "body": "Jesteśmy zainteresowani długoterminową współpracą biznesową.",
                "expected": "Sprzedaż"
            }
        ]
    
    def test_classifier_initialization(self, classifier):
        """Test if classifier initializes correctly"""
        assert classifier is not None
        assert len(classifier.departments) == 4
        assert "IT" in classifier.departments
        assert "Księgowość" in classifier.departments
    
    def test_training_data_loads(self, classifier):
        """Test if training data loads"""
        assert classifier.training_data is not None
        assert len(classifier.training_data) > 0
        assert isinstance(classifier.training_data, list)
    
    def test_classify_it_email(self, classifier):
        """Test classification of IT email"""
        email = {
            "subject": "Problem z VPN",
            "body": "Nie mogę się połączyć z VPN firmowym. Connection timeout."
        }
        result = classifier.classify(email)
        
        assert result is not None
        assert "label" in result
        assert "confidence" in result
        assert result["label"] in classifier.departments
        assert 0 <= result["confidence"] <= 1
    
    def test_classify_accounting_email(self, classifier):
        """Test classification of accounting email"""
        email = {
            "subject": "Faktura korygująca",
            "body": "Proszę o wystawienie faktury korygującej. Kwota VAT jest nieprawidłowa."
        }
        result = classifier.classify(email)
        
        assert result["label"] in classifier.departments
        assert result["confidence"] > 0
    
    def test_classify_customer_service_email(self, classifier):
        """Test classification of customer service email"""
        email = {
            "subject": "Zwrot towaru",
            "body": "Chciałbym zwrócić produkt i otrzymać zwrot pieniędzy."
        }
        result = classifier.classify(email)
        
        assert result["label"] in classifier.departments
        assert result["confidence"] > 0
    
    def test_classify_sales_email(self, classifier):
        """Test classification of sales email"""
        email = {
            "subject": "Zapytanie ofertowe",
            "body": "Interesuje mnie Państwa oferta. Proszę o przesłanie cennika."
        }
        result = classifier.classify(email)
        
        assert result["label"] in classifier.departments
        assert result["confidence"] > 0
    
    def test_batch_classify(self, classifier, sample_emails):
        """Test batch classification"""
        results = classifier.batch_classify(sample_emails)
        
        assert len(results) == len(sample_emails)
        for result in results:
            assert "label" in result
            assert "confidence" in result
            assert result["label"] in classifier.departments
    
    def test_evaluate_metrics(self, classifier):
        """Test evaluation metrics"""
        metrics = classifier.evaluate()
        
        assert metrics is not None
        assert "accuracy" in metrics
        assert "f1_score" in metrics
        assert "precision" in metrics
        assert "recall" in metrics
        assert "total_predictions" in metrics
        
        # Check if metrics are in valid range
        assert 0 <= metrics["accuracy"] <= 1
        assert 0 <= metrics["f1_score"] <= 1
        assert 0 <= metrics["precision"] <= 1
        assert 0 <= metrics["recall"] <= 1
    
    def test_fallback_classifier(self, classifier):
        """Test fallback rule-based classifier"""
        # Temporarily disable Azure client to test fallback
        original_client = classifier.client
        classifier.client = None
        
        email = {
            "subject": "Awaria systemu",
            "body": "System nie działa, błąd przy logowaniu"
        }
        result = classifier._fallback_classify(email)
        
        assert result is not None
        assert result["label"] in classifier.departments
        assert result["method"] == "rule-based"
        
        # Restore client
        classifier.client = original_client
    
    def test_empty_email(self, classifier):
        """Test classification with minimal content"""
        email = {
            "subject": "Test",
            "body": "Test"
        }
        result = classifier.classify(email)
        
        assert result is not None
        assert result["label"] in classifier.departments
    
    def test_long_email(self, classifier):
        """Test classification with long content"""
        email = {
            "subject": "Bardzo długi temat " * 20,
            "body": "Bardzo długa treść e-maila " * 100
        }
        result = classifier.classify(email)
        
        assert result is not None
        assert result["label"] in classifier.departments


class TestTrainingData:
    """Test suite for training data"""
    
    @pytest.fixture
    def training_data_path(self):
        """Path to training data"""
        return Path(__file__).parent.parent / "data" / "training_emails.json"
    
    def test_training_data_exists(self, training_data_path):
        """Test if training data file exists"""
        assert training_data_path.exists()
    
    def test_training_data_format(self, training_data_path):
        """Test if training data has correct format"""
        with open(training_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Check first item structure
        item = data[0]
        assert "email_id" in item
        assert "subject" in item
        assert "body" in item
        assert "label" in item
        assert "sender" in item
    
    def test_all_labels_present(self, training_data_path):
        """Test if all department labels are present in training data"""
        with open(training_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        labels = set(item["label"] for item in data)
        expected_labels = {"IT", "Księgowość", "Obsługa Klienta", "Sprzedaż"}
        
        assert labels == expected_labels
    
    def test_balanced_distribution(self, training_data_path):
        """Test if training data is reasonably balanced"""
        with open(training_data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        label_counts = {}
        for item in data:
            label = item["label"]
            label_counts[label] = label_counts.get(label, 0) + 1
        
        # Check if each label has at least 3 examples
        for label, count in label_counts.items():
            assert count >= 3, f"Label '{label}' has only {count} examples"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
