import uvicorn
import json

from fastapi import APIRouter, FastAPI, Request
from fastapi.openapi.utils import get_openapi

from routes._routes import fastapi_routes

from core.config import settings
from core.logger import LOGGING_CONFIG
from core.logger import logger

app = FastAPI(
    title="Template FastAPI-MongoDB",
    version="0.0.1",
    openapi_tags=settings.TAGS_METADATA
)

app.include_router(APIRouter(routes=fastapi_routes))

@app.get('/', tags=['Status'])
async def status():
    return {"message": "Welcome to this fantastic app!"}


@app.middleware("http")
def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = call_next(request)
    return response


# Generate openapi.json file for postman collection:
with open('openapi.json', 'w') as f:
    json.dump(get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    ), f)


if __name__ == "__main__":
    uvicorn.run(
        "app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=LOGGING_CONFIG
    )


