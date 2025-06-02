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

# Initialize the sentiment analysis model
try:
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
        result = sentiment_analyzer(input_data.text)[0]
        return SentimentResponse(
            text=input_data.text,
            sentiment=result['label'],
            score=float(result['score'])
        )
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 