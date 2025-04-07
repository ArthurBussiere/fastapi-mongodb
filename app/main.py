import uvicorn
import json

from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from routes._routes import fastapi_routes

from core.config import settings
from core.logger import LOGGING_CONFIG
from core.logger import logger

app = FastAPI(
    title="Generic - FastAPI_MongoDB",
    version="0.0.1",
    openapi_tags=settings.TAGS_METADATA,
)

app.include_router(APIRouter(routes=fastapi_routes))


########  MIDDLEWARE ########

origins = ["http://localhost", "http://localhost:8080", "http://localhost:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = call_next(request)
    return response


@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # you probably want some kind of logging here
        logger.error(str(e))
        return Response(status_code=500, content="Internal Server Error")


######## OPENAPI JSON ########

# Generate openapi.json file for postman collection:
with open("openapi.json", "w") as f:
    json.dump(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes,
        ),
        f,
    )


@app.get("/", tags=["Status"])
async def status():
    return {"message": "Welcome to this fantastic app!"}


if __name__ == "__main__":
    uvicorn.run(
        "app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=LOGGING_CONFIG
    )


