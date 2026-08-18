from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from core.db import db_engine, Base
from api.router import router as finops_router
from core.exceptions import ExpenseException

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()

app = FastAPI(lifespan=lifespan)

async def exc_handler(request: Request, exc: ExpenseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

app.add_exception_handler(ExpenseException, exc_handler)

app.include_router(finops_router)

@app.get("/")
def test():
    return {"status": "success", "message": "connected successfully to financial copilot"}
