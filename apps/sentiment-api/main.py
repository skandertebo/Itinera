import sys

try:
    import numpy
    print(f"NumPy version: {numpy.__version__}")
except ImportError as e:
    print("Error: NumPy is not installed. Please run: pip install numpy")
    sys.exit(1)

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(
    title="Sentiment Analysis API",
    description="A REST API for sentiment analysis using transformers",
    version="1.0.0"
)

def clean_text(text):
    """Clean and preprocess the text"""
    if isinstance(text, str):
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    return ""

# Initialize the sentiment analysis model
try:
    # Try to load the fine-tuned model first
    try:
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="fine_tuned_model",
            device=0 if torch.cuda.is_available() else -1
        )
        print("Loaded fine-tuned model successfully")
    except Exception as e:
        print(f"Could not load fine-tuned model: {e}")
        print("Falling back to pre-trained model")
        sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            device=0 if torch.cuda.is_available() else -1
        )
except Exception as e:
    print(f"Error loading model: {e}")
    sentiment_analyzer = None

class TextInput(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    score: float

@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API"}

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(input_data: TextInput):
    if not sentiment_analyzer:
        raise HTTPException(status_code=500, detail="Model not loaded properly")
    
    try:
        # Clean the input text
        cleaned_text = clean_text(input_data.text)
        
        # Analyze sentiment
        result = sentiment_analyzer(cleaned_text)[0]
        
        # Map the labels to more meaningful terms
        sentiment_map = {
            "LABEL_0": "POSITIVE",
            "LABEL_1": "NEGATIVE",
            "POSITIVE": "POSITIVE",
            "NEGATIVE": "NEGATIVE"
        }
        
        # Get the sentiment and score
        sentiment = sentiment_map.get(result['label'], result['label'])
        score = float(result['score'])
        
        # If the text contains negative words, adjust the sentiment
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'poor', 'worst']
        if any(word in cleaned_text for word in negative_words):
            if sentiment == "POSITIVE" and score < 0.7:  # Only adjust if confidence is not very high
                sentiment = "NEGATIVE"
                score = 1 - score  # Invert the score
        
        return SentimentResponse(
            text=input_data.text,
            sentiment=sentiment,
            score=score
        )
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 