from fastapi import FastAPI

from app.routes import posts, users, auth, voting


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(voting.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
