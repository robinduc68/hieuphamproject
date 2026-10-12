// Giới hạn dung lượng ảnh — phải khớp MAX_UPLOAD_SIZE_MB ở backend (.env).
// Chặn ngay tại trình duyệt để khỏi tải lên cả chục MB rồi mới bị từ chối.
export const MAX_IMAGE_MB = 10

/** Trả về chuỗi lỗi nếu ảnh quá nặng, null nếu hợp lệ. */
export function imageTooLarge(file) {
  const mb = file.size / 1048576
  return mb > MAX_IMAGE_MB
    ? `Ảnh "${file.name}" nặng ${mb.toFixed(1)}MB, vượt quá ${MAX_IMAGE_MB}MB. Vui lòng nén hoặc giảm kích thước ảnh.`
    : null
}
