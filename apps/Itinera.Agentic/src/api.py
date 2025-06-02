from asyncio import sleep
import os
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app import create_customer_facing_agent



app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        lg_agent = create_customer_facing_agent()
        async for message in websocket.iter_text():
            try:
                customer_response = lg_agent.invoke({"input": message})
                output: str = customer_response['output']
        
                for word in output.split(' '):
                  await websocket.send_text(word)
                  await sleep(0.1)
            except Exception as e:
                await websocket.send_text(f"Error: {e}")
    except Exception as e:
        await websocket.send_text(f"Error: {e}")


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