# Clone CDN

Prototype project for a personal AI clone that runs on a local machine with a GPU and exposes a simple web interface. The repository is organized into two main parts:

- **local_ai_node**: handles audio/video processing, runs a local LLM with `llama-cpp-python`, stores interactions, and exposes a FastAPI server.
- **web_server**: Flask application that communicates with the local node via a secure tunnel and provides a basic HTML interface.

See `requirements.txt` for Python dependencies.
