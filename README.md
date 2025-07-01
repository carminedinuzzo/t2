# Clone CDN

Prototype project for a personal AI clone that runs on a local machine with a GPU and exposes a web interface. The repository is organized into two parts:

- **local_ai_node**: handles audio/video processing, runs a local LLM with `llama-cpp-python`, stores interactions, and exposes a FastAPI server.
- **web_server**: Flask application that communicates with the local node via a secure tunnel and provides a simple HTML interface protected by login.

## Requirements

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running

1. Start the local node:
   ```bash
   python -m clone_cdn.local_ai_node.main
   ```
2. Set login credentials for the web server:
   ```bash
   export ADMIN_USERNAME=admin
   export ADMIN_PASSWORD=secret
   export FLASK_SECRET_KEY=change-me
   ```
3. In another terminal, start the web server:
   ```bash
   python -m clone_cdn.web_server.app
   ```

Both servers can be exposed through a tunnel as needed (see `tunnel/ngrok.yml`).
