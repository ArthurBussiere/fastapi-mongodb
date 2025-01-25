from fastapi import APIRouter, FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes._routes import fastapi_routes
import json

app = FastAPI(
    title="Template FastAPI-MongoDB",
    version="0.0.1"
)
app.include_router(APIRouter(routes=fastapi_routes))


@app.get('/', tags=['Root'])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


with open('openapi.json', 'w') as f:
    json.dump(get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    ), f)