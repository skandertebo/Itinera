import os
from asyncio import sleep

from app import create_customer_facing_agent
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/predict')
async def predict(request: Request):
    data = await request.json()
    messages_history = data.get('messages_history')
    input = data.get('input')
    agent = create_customer_facing_agent(messages_history)
    customer_response = agent.invoke({"input": input})
    output: str = customer_response['output']
    return {'output': {
        "sender": "assistant",
        "content": output
    }}



# Serve the static HTML file
@app.get("/")
async def get():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "static", "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)