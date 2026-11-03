"""NLP engine: text cleaning, model training and prediction.

Idea (for viva): every intent has example sentences. We turn sentences into
numbers with TF-IDF and teach a Logistic Regression classifier which intent
a new sentence belongs to. If the classifier is not confident, the bot
says it does not know instead of guessing.
"""
import json
import os
import random
import re

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import FeatureUnion, Pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

CONFIDENCE_THRESHOLD = 0.30
FALLBACK_REPLIES = [
    "Sorry, I didn't understand that. Try asking about admissions, fees, courses, hostel, placements or contact details.",
    "I'm not sure about that one. I can help with admissions, fees, courses, hostel, placements, library and transport.",
]


def clean_text(text: str) -> str:
    """Lowercase, remove punctuation and extra spaces."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_intents(path: str = INTENTS_PATH) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_pipeline() -> Pipeline:
    # Word n-grams capture meaning; character n-grams tolerate spelling mistakes.
    features = FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), sublinear_tf=True)),
    ])
    return Pipeline([
        ("tfidf", features),
        ("clf", LogisticRegression(C=20, max_iter=2000)),
    ])


def get_training_data(data: dict):
    texts, labels = [], []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            texts.append(clean_text(pattern))
            labels.append(intent["tag"])
    return texts, labels


def train_and_save():
    data = load_intents()
    texts, labels = get_training_data(data)
    model = build_pipeline()
    model.fit(texts, labels)
    joblib.dump(model, MODEL_PATH)
    return model, texts, labels


class ChatBot:
    def __init__(self):
        self.data = load_intents()
        self.responses = {i["tag"]: i["responses"] for i in self.data["intents"]}
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
        else:
            self.model, _, _ = train_and_save()

    def predict(self, message: str):
        """Return (tag, confidence) for a message."""
        cleaned = clean_text(message)
        if not cleaned:
            return None, 0.0
        probs = self.model.predict_proba([cleaned])[0]
        best = probs.argmax()
        return self.model.classes_[best], float(probs[best])

    def reply(self, message: str) -> dict:
        tag, confidence = self.predict(message)
        if tag is None or confidence < CONFIDENCE_THRESHOLD:
            return {"reply": random.choice(FALLBACK_REPLIES), "intent": "fallback", "confidence": round(confidence, 2)}
        return {"reply": random.choice(self.responses[tag]), "intent": tag, "confidence": round(confidence, 2)}
