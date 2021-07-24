from fastapi import FastAPI 
from routes.user import user

app = FastAPI(
    title="My firts API with fastAPI",
    version= "0.1",
    description= "API where a CRUD is practiced with mysql database.",
    openapi_tags=[{
        "name": "Users",
        "description": "CRUD users"
    }]
)



app.include_router(user)
