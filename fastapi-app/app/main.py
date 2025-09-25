from fastapi import FastAPI
from app.api.v1 import items
from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title="FastAPI on AWS")


app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)


app.include_router(items.router, prefix="/api/v1/items", tags=["items"])


@app.get("/health")
async def health():
    return {"status": "ok"}