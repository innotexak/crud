from fastapi import FastAPI
from routers import posts

app = FastAPI(
    title="Post API", 
    summary="A sample application showing how to use FastAPI with MongoDB.",
)

# Include resource routers
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Post API"}