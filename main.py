from fastapi import FastAPI
import uvicorn
from app.routers import user, auth
from core.config import settings
app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(user.router)
app.include_router(auth.router)

if __name__ == "__main__":

    uvicorn.run(app, host="localhost", port=8000, reload=True)
