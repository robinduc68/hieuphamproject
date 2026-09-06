"""
Upload ảnh dùng chung — phục vụ trình soạn thảo nội dung trong trang admin
(chèn ảnh vào mô tả sản phẩm). Ảnh không gắn với sản phẩm nào nên không tạo
bản ghi ProductImage, chỉ trả về URL để nhúng vào HTML.
"""
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.auth import get_current_admin
from app.storage import upload_content_file

router = APIRouter(prefix="/api/uploads", tags=["Uploads"])

MAX_BYTES     = 10 * 1024 * 1024   # 10MB, khớp với giới hạn ghi trên form admin
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml"}

MAX_VIDEO_BYTES     = 200 * 1024 * 1024   # video nền trang chủ
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/ogg", "video/quicktime"}


@router.post("/image", status_code=201, dependencies=[Depends(get_current_admin)])
def upload_content_image(file: UploadFile = File(...)):
    content_type = file.content_type or "image/jpeg"
    if content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Định dạng ảnh không được hỗ trợ.")

    file_bytes = file.file.read()
    if len(file_bytes) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Ảnh vượt quá 10MB.")

    url = upload_content_file(file_bytes, file.filename or "image.jpg", content_type)
    return {"url": url}


@router.post("/video", status_code=201, dependencies=[Depends(get_current_admin)])
def upload_video(file: UploadFile = File(...)):
    """Video nền trang chủ. Đọc theo từng khối để file lớn không ngốn RAM."""
    content_type = file.content_type or "video/mp4"
    if content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Định dạng video không được hỗ trợ (dùng MP4 hoặc WEBM).",
        )

    chunks, total = [], 0
    while chunk := file.file.read(1024 * 1024):
        total += len(chunk)
        if total > MAX_VIDEO_BYTES:
            raise HTTPException(status_code=413, detail="Video vượt quá 200MB.")
        chunks.append(chunk)

    url = upload_content_file(b"".join(chunks), file.filename or "hero.mp4", content_type)
    return {"url": url}
