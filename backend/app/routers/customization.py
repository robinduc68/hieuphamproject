from fastapi import APIRouter, HTTPException, Depends
from peewee import DoesNotExist, IntegrityError

from app.models.customization import CustomizationOption
from app.schemas.customization import (
    CustomizationOptionOut, CustomizationGroupOut,
    CustomizationOptionCreate, CustomizationOptionUpdate,
)
from app.auth import require
from app.database import get_db

router = APIRouter(prefix="/api/customization-options", tags=["Customization"])


def _to_out(opt: CustomizationOption) -> CustomizationOptionOut:
    return CustomizationOptionOut(
        id=opt.id,
        group_key=opt.group_key,
        group_label=opt.group_label,
        option_key=opt.option_key,
        option_label=opt.option_label,
        price_adjustment=opt.price_adjustment,
        sort_order=opt.sort_order,
        is_active=opt.is_active,
    )


# ── Public: grouped active options ────────────────────────────────────────
@router.get("/", response_model=list[CustomizationGroupOut])
def list_grouped(_db=Depends(get_db)):
    opts = list(
        CustomizationOption.select()
        .where(CustomizationOption.is_active == True)
        .order_by(CustomizationOption.group_key, CustomizationOption.sort_order)
    )
    groups: dict[str, CustomizationGroupOut] = {}
    for opt in opts:
        if opt.group_key not in groups:
            groups[opt.group_key] = CustomizationGroupOut(
                group_key=opt.group_key,
                group_label=opt.group_label,
                options=[],
            )
        groups[opt.group_key].options.append(_to_out(opt))
    return list(groups.values())


# ── Admin: all options (including inactive) ───────────────────────────────
@router.get("/all", response_model=list[CustomizationOptionOut],
            dependencies=[Depends(require("customization.view"))])
def list_all(_db=Depends(get_db)):
    opts = list(
        CustomizationOption.select()
        .order_by(CustomizationOption.group_key, CustomizationOption.sort_order)
    )
    return [_to_out(o) for o in opts]


@router.post("/", response_model=CustomizationOptionOut, status_code=201,
             dependencies=[Depends(require("customization.update"))])
def create_option(data: CustomizationOptionCreate, _db=Depends(get_db)):
    try:
        opt = CustomizationOption.create(**data.model_dump())
        return _to_out(opt)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Option key đã tồn tại trong nhóm này.")


@router.put("/{option_id}", response_model=CustomizationOptionOut,
            dependencies=[Depends(require("customization.update"))])
def update_option(option_id: int, data: CustomizationOptionUpdate, _db=Depends(get_db)):
    try:
        opt = CustomizationOption.get_by_id(option_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Option không tồn tại.")
    for field, val in data.model_dump(exclude_none=True).items():
        setattr(opt, field, val)
    opt.save()
    return _to_out(opt)


@router.delete("/{option_id}", status_code=204,
               dependencies=[Depends(require("customization.update"))])
def delete_option(option_id: int, _db=Depends(get_db)):
    try:
        opt = CustomizationOption.get_by_id(option_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Option không tồn tại.")
    opt.delete_instance()
