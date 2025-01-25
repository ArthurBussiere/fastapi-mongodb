from fastapi import APIRouter, FastAPI


from app.server.routes._routes import fastapi_routes


app = FastAPI()
app.include_router(APIRouter(routes=fastapi_routes))


@app.get('/', tags=['Root'])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}


