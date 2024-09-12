import uvicorn
from app.server import app

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD_ON_CHANGE,
        workers=2,
    )