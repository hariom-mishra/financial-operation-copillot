import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from core.db import db_engine, Base
from api.router import router as finops_router
from core.exceptions import ExpenseException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await db_engine.dispose()

app = FastAPI(lifespan=lifespan)

# Use middleware so exceptions from Depends() are also caught
@app.middleware("http")
async def expense_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ExpenseException as e:
        logger.error(f"ExpenseException: {e.message}", exc_info=True)
        return JSONResponse(
            status_code=e.status_code,
            content={"message": e.message},
        )
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"message": f"Internal server error: {str(e)}"},
        )

app.include_router(finops_router)

@app.get("/")
def test():
    return {"status": "success", "message": "connected successfully to financial copilot"}
