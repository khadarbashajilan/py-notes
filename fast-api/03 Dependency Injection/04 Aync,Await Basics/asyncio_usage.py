"""
Async/Await Basics
This module illustrates the use of asyncio for handling asynchronous operations and concurrent tasks in FastAPI.
"""

import asyncio
from fastapi import FastAPI

app = FastAPI()

# Mock async functions simulating slow I/O (DB or API calls)
async def fetch_users():
    await asyncio.sleep(1)  # Simulates 1 second network delay
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

async def fetch_revenue():
    await asyncio.sleep(1)
    return {"total": 5000, "currency": "USD"}

async def fetch_traffic():
    await asyncio.sleep(1)
    return {"visitors": 1200, "pageviews": 3400}

@app.get("/dashboard")
async def get_dashboard():
    # 1. Fire off all 3 tasks at the exact same time
    users, revenue, traffic = await asyncio.gather(
        fetch_users(),
        fetch_revenue(),
        fetch_traffic()
    )
    
    # 2. Combine the results
    return {
        "status": "success",
        "data": {
            "users": users,
            "revenue": revenue,
            "traffic": traffic
        }
    }
