# Sentiment Analysis API

A REST API for sentiment analysis using the DistilBERT model fine-tuned on the SST-2 dataset.

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /
- Returns a welcome message

### POST /analyze
- Analyzes the sentiment of the provided text
- Request body:
```json
{
    "text": "Your text here"
}
```
- Response:
```json
{
    "text": "Your text here",
    "sentiment": "POSITIVE/NEGATIVE",
    "score": 0.9876
}
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc` 