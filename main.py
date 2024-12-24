from fastapi import FastAPI
import uvicorn
from app.routers import user, auth
from core.config import settings
app = FastAPI(title="API", version="0.1.0")

app.include_router(user.router)
app.include_router(auth.router)

# Configuración para Railway
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Usa el puerto asignado por Railway
    uvicorn.run(app, host="0.0.0.0", port=port)
