
# 📦 Pull Request: Add Real-time Customer-facing Agent with FastAPI WebSocket

## ✨ Summary

This pull request introduces a new FastAPI server that integrates a **WebSocket endpoint** to serve a real-time, word-by-word streamed response from a customer-facing agent. It also enhances the agent’s prompts, introduces schemas, and includes a static HTML file for client testing. CORS is configured to allow broad client compatibility.

---

## 🔥 Features Added

✅ **FastAPI App Initialization**

* Creates a new FastAPI application instance.
* Adds CORS middleware to allow all origins, headers, and methods (for easy cross-origin testing and deployment).

✅ **WebSocket Endpoint (`/ws`)**

* Accepts WebSocket connections at `/ws`.
* On receiving a message, it:

  * Instantiates the customer-facing agent using `create_customer_facing_agent()`.
  * Invokes the agent with the client’s message as input.
  * Splits the agent’s output text word-by-word.
  * Streams each word to the client with a 0.1-second delay to simulate real-time typing.

✅ **Static HTML Serving (`/`)**

* Serves a static HTML file (`static/index.html`) at the root endpoint `/` for easy front-end testing.

✅ **Enhanced Agent Prompts**

* The agent now uses improved prompt templates for richer, more context-aware responses, making conversations more natural and helpful.

✅ **Schemas**

* Added schemas to define and validate the input and output structure between the client and the agent.

✅ **Error Handling**

* Catches and returns any runtime errors to the client over WebSocket.

---

## 🛠️ Technical Details

* **Dependencies**:

  * `FastAPI`: Web framework.
  * `uvicorn`: ASGI server for running FastAPI.
  * `asyncio.sleep`: To simulate typing delay.
  * `os`: To locate the static file directory.

* **Agent Integration**:

  * Uses `create_customer_facing_agent()` from the `app` module.
  * The agent expects a validated input dictionary (based on the new schema) and returns a dictionary with an `output` field.
  * Enhanced prompt design yields richer, more context-aware responses.

---

## 🗂️ Directory Structure

```
Itinera.Agentic/src/
│
├── api.py          # Contains the FastAPI app and WebSocket endpoint.
├── static/
│   └── index.html  # A static HTML file served at the root endpoint.
├── schema/
    └── classes.py     # Contains input/output schemas for validating agent communication.
```

---

## 🚀 How to Run

1️⃣ **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```


2️⃣ **Install dependencies** (assuming Python 3.8+):

```bash
pip install -r requirements.txt
```

3️⃣ **Run the server**:

```bash
python -m api.py
```

**Open your browser** at `http://127.0.0.1:8000` to load the static HTML client.


---

## 📌 Notes

* The agent logic is delegated to `create_customer_facing_agent()`, which is implemented in the `app` module.
* Schemas are  located in a separate module  `schema.classes.py`, which uses Pydantic.
* CORS is configured to allow all origins. For production, tighten these settings as needed.
* Error messages are sent over WebSocket as plain text starting with `Error: ...`.
