"""
Cấu hình nội dung website do admin sửa (video hero, bảng hướng dẫn chọn size,
bảng định mức may đo). Mỗi cấu hình là một key + giá trị JSON tự do.
"""
import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.auth import get_current_admin
from app.database import get_db
from app.models.setting import SiteSetting

router = APIRouter(prefix="/api/settings", tags=["Settings"])

MAX_VALUE_BYTES = 256 * 1024   # JSON cấu hình vài chục dòng bảng là cùng


class SettingIn(BaseModel):
    value: Any


def _parse(raw: str | None) -> Any:
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw   # giá trị cũ lưu dạng chuỗi thuần vẫn đọc được


@router.get("/")
def list_settings(_db=Depends(get_db)) -> dict[str, Any]:
    """Công khai — frontend nạp một lần rồi dùng cho cả trang."""
    return {s.key: _parse(s.value) for s in SiteSetting.select()}


@router.get("/{key}")
def get_setting(key: str, _db=Depends(get_db)):
    setting = SiteSetting.get_or_none(SiteSetting.key == key)
    if setting is None:
        raise HTTPException(status_code=404, detail=f"Không có cấu hình '{key}'.")
    return {"key": setting.key, "value": _parse(setting.value)}


@router.put("/{key}", dependencies=[Depends(get_current_admin)])
def upsert_setting(key: str, data: SettingIn, _db=Depends(get_db)):
    raw = json.dumps(data.value, ensure_ascii=False)
    if len(raw.encode("utf-8")) > MAX_VALUE_BYTES:
        raise HTTPException(status_code=413, detail="Nội dung cấu hình quá lớn.")

    setting = SiteSetting.get_or_none(SiteSetting.key == key)
    if setting is None:
        setting = SiteSetting.create(key=key, value=raw)
    else:
        setting.value = raw
        setting.save()
    return {"key": setting.key, "value": _parse(setting.value)}
