from fastapi import FastAPI
from app.api.v1 import items
from app.api.Frontent import index
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse



app = FastAPI(title="FastAPI on AWS")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(items.router, prefix="/api/v1", tags=["items"])

app.include_router(index.router, prefix="/index", tags=["Frontend"])


@app.get("/health")
async def health():
    return {"status": "ok"}