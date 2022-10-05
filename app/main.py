from fastapi import FastAPI

from app.config import settings
from app.routes import posts, users, auth, voting


print(settings.DB_HOST)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(voting.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
