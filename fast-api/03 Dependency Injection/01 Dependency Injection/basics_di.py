"""
Dependency Injection Basics
This module demonstrates the basic usage of dependency injection in FastAPI, focusing on common query parameters.
"""

from fastapi import FastAPI, Depends
from typing import Dict
app = FastAPI()

def CommonQueryParams(skip:int=0, limit:int=0, search:str=""):
    return {"skip": skip, "limit": limit, "search": search}

#or:
#class CommonQueryParams:
#    def __init__(self, skip:int = 0, limit:int = 0, search:str = ""):
#        self.skip = skip
#        self.limit = limit
#        self.search = search


@app.get("/itmes")
def get_items(params:Dict = Depends(CommonQueryParams)):
    return {
        "endpoint": "itmes",
        "skipping": params['skip'],
        "taking": params['limit'],
        "searching_for": params['search']
    }

@app.get("/users")
def get_users(params:Dict = Depends(CommonQueryParams)):
    return {
        "endpoint": "users",
        "skipping": params['skip'],
        "taking": params['limit'],
        "searching_for": params['search']
    }

@app.get("/posts")
def get_posts(params:Dict = Depends(CommonQueryParams)):
    return {
        "endpoint": "posts",
        "skipping": params['skip'],
        "taking": params['limit'],
        "searching_for": params['search']
    }
