"""Sample in-memory CRUD resource used to drive the front end.

Replace the in-process store with a real database when you need
persistence. The HTTP contract stays the same.
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["items"], prefix="/items")


class Item(BaseModel):
    id: int
    title: str
    done: bool = False
    created_at: str


class ItemIn(BaseModel):
    title: str
    done: bool = False


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# in-memory store (seeded so the UI has something to show)
_store: dict[int, Item] = {
    1: Item(id=1, title="Scaffold the project", done=True, created_at=_now()),
    2: Item(id=2, title="Wire up the React front end", done=True, created_at=_now()),
    3: Item(id=3, title="Add a real database", done=False, created_at=_now()),
}
_next_id = 4


@router.get("", response_model=list[Item])
def list_items() -> list[Item]:
    """Return all items, most recent first."""
    return sorted(_store.values(), key=lambda i: i.id, reverse=True)


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = _store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return item


@router.post("", response_model=Item, status_code=201)
def create_item(payload: ItemIn) -> Item:
    global _next_id
    item = Item(id=_next_id, title=payload.title, done=payload.done, created_at=_now())
    _store[item.id] = item
    _next_id += 1
    return item


@router.patch("/{item_id}", response_model=Item)
def update_item(item_id: int, payload: ItemIn) -> Item:
    item = _store.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    item.title = payload.title
    item.done = payload.done
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    if item_id not in _store:
        raise HTTPException(status_code=404, detail="item not found")
    del _store[item_id]
