import uvicorn
from fastapi import FastAPI

from application.api.routers.auth.register import router as register_router
from application.api.routers.auth.login import router as login_router
from application.api.health import router as health_router

app = FastAPI(
    title="FinMind AI",
    description="Private Financial Analisys System",
    version="1.0.0"
)

app.include_router(register_router)
app.include_router(login_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run("application.main:app", host="0.0.0.0", port=8081)