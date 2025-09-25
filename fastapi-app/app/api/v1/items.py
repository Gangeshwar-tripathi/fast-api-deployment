from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List


router = APIRouter()


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None


# In-memory store for example. Replace with DB access.
ITEMS =ITEMS = {
    i: {
        "id": i,
        "name": f"Item {i}",
        "description": f"Description for item {i}"
    }
    for i in range(1, 10)
}

@router.get("/", response_model=List[Item])
async def list_items():
    return list(ITEMS.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    item = ITEMS.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: Item):
    if item.id in ITEMS:
        raise HTTPException(status_code=400, detail="ID exists")
    ITEMS[item.id] = item.dict()
    return item