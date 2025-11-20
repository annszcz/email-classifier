"""
Email Classification API
========================
FastAPI backend for email classification system using Azure OpenAI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict
import json
import os
from datetime import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Email Classifier API",
    description="AI-powered email classification system",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class EmailInput(BaseModel):
    """Email input model for classification"""
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    sender: Optional[EmailStr] = Field(None, description="Sender email address")

class ClassificationResult(BaseModel):
    """Classification result model"""
    label: str = Field(..., description="Predicted department label")
    confidence: float = Field(..., description="Confidence score (0-1)")
    timestamp: str = Field(..., description="Classification timestamp")
    email_preview: Dict = Field(..., description="Email preview")

class TrainingData(BaseModel):
    """Training data model"""
    emails: List[Dict]
    total_count: int
    labels: List[str]

class ModelMetrics(BaseModel):
    """Model performance metrics"""
    accuracy: float
    f1_score: float
    precision: float
    recall: float
    total_predictions: int

# Load training data
DATA_PATH = Path(__file__).parent.parent / "data" / "training_emails.json"

def load_training_data() -> List[Dict]:
    """Load training data from JSON file"""
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading training data: {e}")
        return []

# Department labels
DEPARTMENTS = ["IT", "Księgowość", "Obsługa Klienta", "Sprzedaż"]

# Store classification history
classification_history = []

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Email Classification API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/classify", response_model=ClassificationResult)
async def classify_email(email: EmailInput):
    """
    Classify an email to the appropriate department
    
    Args:
        email: Email input with subject, body, and optional sender
        
    Returns:
        Classification result with label and confidence
    """
    try:
        # Import classifier here to avoid circular imports
        from classifier import EmailClassifier
        
        classifier = EmailClassifier()
        result = classifier.classify(email.dict())
        
        # Store in history
        classification_history.append({
            **result,
            "timestamp": datetime.now().isoformat()
        })
        
        return ClassificationResult(
            label=result["label"],
            confidence=result["confidence"],
            timestamp=datetime.now().isoformat(),
            email_preview={
                "subject": email.subject[:50] + "..." if len(email.subject) > 50 else email.subject,
                "body": email.body[:100] + "..." if len(email.body) > 100 else email.body
            }
        )
        
    except Exception as e:
        logger.error(f"Classification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/training-data", response_model=TrainingData)
async def get_training_data():
    """Get training data statistics"""
    try:
        data = load_training_data()
        labels = list(set([email["label"] for email in data]))
        
        return TrainingData(
            emails=data,
            total_count=len(data),
            labels=sorted(labels)
        )
    except Exception as e:
        logger.error(f"Error getting training data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/departments")
async def get_departments():
    """Get list of available departments"""
    return {
        "departments": DEPARTMENTS,
        "total": len(DEPARTMENTS)
    }

@app.get("/history")
async def get_classification_history(limit: int = 10):
    """Get recent classification history"""
    return {
        "history": classification_history[-limit:],
        "total": len(classification_history)
    }

@app.get("/metrics", response_model=ModelMetrics)
async def get_model_metrics():
    """Get model performance metrics"""
    try:
        from classifier import EmailClassifier

        classifier = EmailClassifier()
        metrics = classifier.evaluate()
        
        return ModelMetrics(**metrics)
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/history")
async def clear_history():
    """Clear classification history"""
    global classification_history
    classification_history = []
    return {"message": "History cleared", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
