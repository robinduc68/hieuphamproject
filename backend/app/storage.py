"""
Storage abstraction – Cloudflare R2 hoặc local disk.
Dùng `upload_file()` để upload ảnh, trả về public URL.
Tự động chọn backend dựa vào R2_* env vars:
  - Có đủ credentials → Cloudflare R2
  - Thiếu credentials  → local ./media (phù hợp để dev)
"""
from __future__ import annotations

import os
import uuid
from pathlib import Path

from app.config import get_settings

settings = get_settings()


def _r2_client():
    import boto3
    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.r2_access_key_id,
        aws_secret_access_key=settings.r2_secret_access_key,
        region_name="auto",
    )


def upload_file(file_bytes: bytes, original_filename: str, product_id: int,
                content_type: str = "image/jpeg") -> str:
    """
    Upload ảnh sản phẩm, trả về public URL.
    Key trên R2: products/{product_id}/{uuid}_{filename}
    """
    ext      = Path(original_filename).suffix.lower() or ".jpg"
    uid      = uuid.uuid4().hex[:8]
    filename = f"{uid}_{Path(original_filename).stem[:40]}{ext}"
    key      = f"products/{product_id}/{filename}"

    if settings.use_r2:
        client = _r2_client()
        client.put_object(
            Bucket=settings.r2_bucket_name,
            Key=key,
            Body=file_bytes,
            ContentType=content_type,
        )
        base = settings.r2_public_url.rstrip("/")
        return f"{base}/{key}"
    else:
        # Fallback: local disk
        save_dir = Path(settings.media_dir) / "products" / str(product_id)
        save_dir.mkdir(parents=True, exist_ok=True)
        (save_dir / filename).write_bytes(file_bytes)
        return f"/media/products/{product_id}/{filename}"


def delete_file(url: str) -> None:
    """Xóa file khỏi R2 (hoặc local). url là public URL đã lưu trong DB."""
    if not url:
        return

    if settings.use_r2 and settings.r2_public_url and url.startswith(settings.r2_public_url):
        base = settings.r2_public_url.rstrip("/")
        key  = url[len(base):].lstrip("/")
        try:
            _r2_client().delete_object(Bucket=settings.r2_bucket_name, Key=key)
        except Exception:
            pass
    elif url.startswith("/media/"):
        local_path = Path(settings.media_dir) / url[len("/media/"):].lstrip("/")
        try:
            local_path.unlink(missing_ok=True)
        except Exception:
            pass
