from fastapi import APIRouter, HTTPException, Depends
from peewee import DoesNotExist

from app.models.collection import Collection
from app.schemas.collection import CollectionOut, CollectionCreate, CollectionUpdate
from app.auth import get_current_admin
from app.database import get_db

router = APIRouter(prefix="/api/collections", tags=["Collections"])


@router.get("/", response_model=list[CollectionOut])
def list_collections(_db=Depends(get_db)):
    qs = (
        Collection.select()
        .where(Collection.is_active == True)
        .order_by(Collection.sort_order)
    )
    return [CollectionOut.model_validate(c, from_attributes=True) for c in qs]


@router.get("/{slug}", response_model=CollectionOut)
def get_collection(slug: str, _db=Depends(get_db)):
    try:
        col = Collection.get(Collection.slug == slug, Collection.is_active == True)
        return CollectionOut.model_validate(col, from_attributes=True)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Collection not found")


@router.post("/", response_model=CollectionOut, status_code=201,
             dependencies=[Depends(get_current_admin)])
def create_collection(data: CollectionCreate, _db=Depends(get_db)):
    col = Collection.create(**data.model_dump())
    return CollectionOut.model_validate(col, from_attributes=True)


@router.put("/{col_id}", response_model=CollectionOut,
            dependencies=[Depends(get_current_admin)])
def update_collection(col_id: int, data: CollectionUpdate, _db=Depends(get_db)):
    try:
        col = Collection.get_by_id(col_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Collection not found")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(col, field, val)
    col.save()
    return CollectionOut.model_validate(col, from_attributes=True)


@router.delete("/{col_id}", status_code=204,
               dependencies=[Depends(get_current_admin)])
def delete_collection(col_id: int, _db=Depends(get_db)):
    try:
        col = Collection.get_by_id(col_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Collection not found")
    col.is_active = False
    col.save()
