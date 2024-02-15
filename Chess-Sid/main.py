from fastapi import FastAPI, Request
from .asgi import application  # Replace `.asgi` with your Django ASGI module name

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Django & FastAPI!"}

@app.get("/django/{path}")
async def django_route(path: str, request: Request):
    response = await application(request.scope)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
