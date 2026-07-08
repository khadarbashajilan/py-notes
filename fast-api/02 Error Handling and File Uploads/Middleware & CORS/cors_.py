from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def logs_(request: Request, call_next):
    method = request.method
    url = request.url.path  # .path gives just "/hello" instead of the full URL

    print(f"Incoming request: {method} {url}")

    response = await call_next(request)

    print(f"Response status code: {response.status_code}")

    return response

@app.get("/hello")
async def upload_details():
    return {"message": "Success"}
