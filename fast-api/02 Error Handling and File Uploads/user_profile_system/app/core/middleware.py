from fastapi import Request

async def logs_(request:Request, call_next):
    method=request.method
    url=request.url.path

    print(f"Incoming request: {method}{url}")

    response = await call_next(request)

    print(f"Request status code: {response.status_code}")

    return response

