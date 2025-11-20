"""
Email Classifier Backend
========================
"""

from .main import app
from .classifier import EmailClassifier

__version__ = "1.0.0"
__all__ = ["app", "EmailClassifier"]
