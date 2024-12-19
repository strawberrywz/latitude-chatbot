from fastapi import FastAPI
from routers import chat, feedback
from config import settings

app = FastAPI(title="Langflow API Wrapper", 
              description="FastAPI wrapper for Langflow API", 
              debug=settings.DEBUG)

app.include_router(chat.router, tags=["chat"])
app.include_router(feedback.router, tags=["feedback"])

def start():
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        reload_dirs=["routers", "config.py", "main.py"]
    )

if __name__ == "__main__":
    start()