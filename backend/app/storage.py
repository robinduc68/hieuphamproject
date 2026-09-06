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


def upload_content_file(file_bytes: bytes, original_filename: str,
                        content_type: str = "image/jpeg") -> str:
    """
    Upload ảnh chèn trong nội dung (mô tả sản phẩm, bài viết…), trả về public URL.
    Key trên R2: content/{uuid}_{filename}
    """
    ext      = Path(original_filename).suffix.lower() or ".jpg"
    uid      = uuid.uuid4().hex[:8]
    filename = f"{uid}_{Path(original_filename).stem[:40]}{ext}"
    key      = f"content/{filename}"

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

    save_dir = Path(settings.media_dir) / "content"
    save_dir.mkdir(parents=True, exist_ok=True)
    (save_dir / filename).write_bytes(file_bytes)
    return f"/media/content/{filename}"


def _contrast_text_color(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return "#ffffff"
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    return "#1a1a18" if luminance > 0.6 else "#ffffff"


def _placeholder_svg(name: str, hex_color: str | None) -> bytes:
    color = hex_color or "#c9bba0"
    if not color.startswith("#"):
        color = f"#{color}"
    text_color = _contrast_text_color(color)
    initials = "".join(w[0] for w in name.split()[:2]).upper() or "?"
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="400" viewBox="0 0 300 400">'
        f'<rect width="300" height="400" fill="{color}"/>'
        f'<text x="150" y="210" font-family="Georgia, serif" font-size="72" fill="{text_color}" '
        f'text-anchor="middle" dominant-baseline="middle" opacity="0.85">{initials}</text>'
        "</svg>"
    )
    return svg.encode("utf-8")


def save_placeholder(product_slug: str, product_name: str, hex_color: str | None) -> str:
    """Sinh ảnh placeholder SVG thật (nền màu + chữ cái đầu) và lưu vào storage, trả về public URL."""
    svg_bytes = _placeholder_svg(product_name, hex_color)
    key = f"placeholder/{product_slug}.svg"

    if settings.use_r2:
        client = _r2_client()
        client.put_object(
            Bucket=settings.r2_bucket_name,
            Key=key,
            Body=svg_bytes,
            ContentType="image/svg+xml",
        )
        base = settings.r2_public_url.rstrip("/")
        return f"{base}/{key}"
    else:
        save_dir = Path(settings.media_dir) / "placeholder"
        save_dir.mkdir(parents=True, exist_ok=True)
        (save_dir / f"{product_slug}.svg").write_bytes(svg_bytes)
        return f"/media/placeholder/{product_slug}.svg"


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
