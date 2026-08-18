from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.db import db_engine, Base
from api.router import router as finops_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(finops_router)

@app.get("/")
def test():
    return {"status": "success", "message": "connected successfully to financial copilot"}
