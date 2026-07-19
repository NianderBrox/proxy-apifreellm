from contextlib import asynccontextmanager

from fastapi import FastAPI

from .client import client
from .openai.router import router
from .openai.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await client.close()


app = FastAPI(
    title="ApiFreeLLM OpenAI Proxy",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(router)