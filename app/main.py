import uvicorn
from app.core.logger import LOGGING_CONFIG

if __name__ == "__main__":
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=LOGGING_CONFIG
    )
