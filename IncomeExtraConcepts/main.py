from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from routers.income_router import router as income_router
from routers.expense_attachment_router import router as attachment_router


@asynccontextmanager
async def lifespan(app : FastAPI):
    print("Income Management API is running")

    yield

    print("Income Management API is shutting down...")

app = FastAPI(
    title="Income Management API",
    description="API for managing income, expenses and cash in hand",
    version="1.0.0",
    lifespan = lifespan
)

@app.middleware("http")
async def add_custom_header(request:Request,call_next):
    response = await call_next(request)
    response.headers["X-App-Name"] ="Income Management API"

    return response

app.include_router(income_router)
app.include_router(attachment_router)


@app.get("/")
def home():
    return {
        "message": "Income Management API is running"
    }