"""
Thanh toán VietQR.

Hai nhóm endpoint:

  • /api/payments/...          → web khách gọi: xin mã QR, hỏi trạng thái đơn.
  • /api/bank/api/...          → VIETQR gọi ngược về hệ thống. Đây chính là
    "URL Kết Nối" khai báo trên cổng merchant của VietQR:
        token_generate    – VietQR đưa username/password (Basic) để lấy token
        transaction-sync  – VietQR bắn giao dịch về, kèm Bearer token ở trên

Định dạng request/response của 2 endpoint dưới bám theo tài liệu VietQR:
https://api.vietqr.vn/vi/api-vietqr-callback/api-transaction-sync
"""
from __future__ import annotations

import logging
import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from jose import JWTError, jwt
from pydantic import BaseModel
from peewee import DoesNotExist

from app.config import get_settings
from app.database import get_db
from app.models.order import Order
from app.services.vietqr import VietQRError, generate_qr

log = logging.getLogger(__name__)
settings = get_settings()

router      = APIRouter(prefix="/api/payments", tags=["Payments"])
bank_router = APIRouter(prefix="/api/bank/api",  tags=["VietQR callback"])

CALLBACK_TOKEN_TTL_SECONDS = 300
_CALLBACK_AUDIENCE = "vietqr-callback"

# Khách chuyển cọc 50% khi đặt, phần còn lại thu sau khi giao.
# Phải khớp dòng "Đặt cọc 50%" ở trang thanh toán (frontend CheckoutView.vue).
DEPOSIT_RATE = Decimal("0.5")


def deposit_of(order: Order) -> Decimal:
    """Số tiền cọc phải chuyển, làm tròn về đồng."""
    return (Decimal(str(order.grand_total)) * DEPOSIT_RATE).quantize(Decimal("1"))


# ══════════════════════════════════════════════════════════════════════════
# Web khách gọi
# ══════════════════════════════════════════════════════════════════════════
class QrOut(BaseModel):
    order_code:     str
    amount:         Decimal          # tổng đơn
    deposit_amount: Decimal          # số tiền QR yêu cầu chuyển (cọc 50%)
    qr_code:        Optional[str] = None
    qr_link:        Optional[str] = None
    bank_code:      Optional[str] = None
    bank_account:   Optional[str] = None
    account_name:   Optional[str] = None
    payment_status: str
    # Chưa bật VietQR thì web hiện hướng dẫn chuyển khoản tay bằng đúng số TK này
    available:      bool = True
    message:        Optional[str] = None


def _get_order(order_code: str) -> Order:
    order = Order.get_or_none(Order.order_code == order_code)
    if order is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")
    return order


@router.post("/vietqr/{order_code}", response_model=QrOut)
def create_qr(order_code: str, _db=Depends(get_db)):
    """Tạo (hoặc lấy lại) mã QR cho đơn. Gọi lại nhiều lần vẫn ra cùng một QR."""
    order = _get_order(order_code)

    if order.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Đơn hàng đã thanh toán đủ.")

    if order.qr_code:                       # đã tạo rồi → dùng lại
        return _qr_out(order)

    try:
        data = generate_qr(order_code=order.order_code, amount=deposit_of(order))
    except VietQRError as e:
        log.warning("[vietqr] tạo QR thất bại cho %s: %s", order.order_code, e)
        return QrOut(
            order_code=order.order_code,
            amount=Decimal(str(order.grand_total)),
            deposit_amount=deposit_of(order),
            bank_code=settings.vietqr_bank_code,
            bank_account=settings.vietqr_bank_account,
            account_name=settings.vietqr_account_name,
            payment_status=order.payment_status,
            available=False,
            message="Chưa tạo được mã QR tự động, vui lòng chuyển khoản theo thông tin bên dưới.",
        )

    order.qr_code           = data.get("qrCode")
    order.qr_link           = data.get("qrLink")
    order.qr_transaction_id = data.get("transactionId")
    order.save()
    return _qr_out(order)


@router.get("/status/{order_code}", response_model=QrOut)
def payment_status(order_code: str, _db=Depends(get_db)):
    """Web khách hỏi lại sau mỗi vài giây để biết tiền đã về chưa."""
    return _qr_out(_get_order(order_code))


def _qr_out(order: Order) -> QrOut:
    return QrOut(
        order_code=order.order_code,
        amount=Decimal(str(order.grand_total)),
        deposit_amount=deposit_of(order),
        qr_code=order.qr_code,
        qr_link=order.qr_link,
        bank_code=settings.vietqr_bank_code,
        bank_account=settings.vietqr_bank_account,
        account_name=settings.vietqr_account_name,
        payment_status=order.payment_status,
        available=bool(order.qr_code),
    )


# ══════════════════════════════════════════════════════════════════════════
# VietQR gọi ngược về
# ══════════════════════════════════════════════════════════════════════════
class TokenOut(BaseModel):
    access_token: str
    token_type:   str = "Bearer"
    expires_in:   int = CALLBACK_TOKEN_TTL_SECONDS


@bank_router.post("/token_generate", response_model=TokenOut)
def callback_token(request: Request):
    """
    VietQR gửi Basic auth (username/password mình khai báo trên cổng merchant)
    để đổi lấy token, rồi đính token đó vào mỗi lần bắn giao dịch về.
    """
    if not (settings.vietqr_callback_username and settings.vietqr_callback_password):
        raise HTTPException(status_code=503, detail="Chưa cấu hình tài khoản callback VietQR.")

    import base64
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("basic "):
        raise HTTPException(status_code=401, detail="Thiếu Basic authentication.")
    try:
        username, _, password = base64.b64decode(header[6:]).decode().partition(":")
    except Exception:
        raise HTTPException(status_code=401, detail="Basic authentication không hợp lệ.")

    # so sánh kiểu hằng thời gian, tránh dò mật khẩu qua thời gian phản hồi
    ok = secrets.compare_digest(username, settings.vietqr_callback_username) and \
         secrets.compare_digest(password, settings.vietqr_callback_password)
    if not ok:
        raise HTTPException(status_code=401, detail="Sai username hoặc password.")

    token = jwt.encode(
        {
            "aud": _CALLBACK_AUDIENCE,
            "sub": username,
            "exp": datetime.utcnow() + timedelta(seconds=CALLBACK_TOKEN_TTL_SECONDS),
        },
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return TokenOut(access_token=token)


class TransactionSyncIn(BaseModel):
    bankaccount:     str
    amount:          Decimal
    transType:       str
    content:         str
    transactionid:   str
    transactiontime: int
    referencenumber: str
    orderId:         Optional[str] = None
    terminalCode:    Optional[str] = None
    subTerminalCode: Optional[str] = None
    serviceCode:     Optional[str] = None
    urlLink:         Optional[str] = None
    sign:            Optional[str] = None


def _sync_error(reason: str, message: str):
    return {"error": True, "errorReason": reason, "toastMessage": message, "object": None}


@bank_router.post("/transaction-sync")
def transaction_sync(data: TransactionSyncIn, request: Request, _db=Depends(get_db)):
    """VietQR báo có tiền về → đánh dấu đơn đã thanh toán."""
    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        return _sync_error("UNAUTHORIZED", "Thiếu Bearer token.")
    try:
        jwt.decode(
            header[7:], settings.secret_key,
            algorithms=[settings.algorithm], audience=_CALLBACK_AUDIENCE,
        )
    except JWTError:
        return _sync_error("UNAUTHORIZED", "Token không hợp lệ hoặc đã hết hạn.")

    # Chỉ quan tâm tiền VÀO
    if (data.transType or "").upper() != "C":
        return {"error": False, "errorReason": None,
                "toastMessage": "Bỏ qua giao dịch tiền ra.",
                "object": {"reftransactionid": data.transactionid}}

    # orderId là chuẩn; nếu thiếu thì dò mã đơn trong nội dung chuyển khoản
    order = None
    if data.orderId:
        order = Order.get_or_none(Order.order_code == data.orderId.strip())
    if order is None and data.content:
        for word in data.content.replace("-", " ").replace(".", " ").split():
            order = Order.get_or_none(Order.order_code == word.strip())
            if order:
                break
    if order is None:
        log.warning("[vietqr] callback không khớp đơn nào: %s", data.model_dump())
        return _sync_error("ORDER_NOT_FOUND", "Không tìm thấy đơn hàng tương ứng.")

    # VietQR có thể gửi lại cùng một giao dịch → không cộng dồn, không ghi đè
    if order.payment_status == "paid" and order.payment_ref == data.transactionid:
        return {"error": False, "errorReason": None, "toastMessage": "Đã ghi nhận trước đó.",
                "object": {"reftransactionid": data.transactionid}}

    # Cộng dồn: khách có thể chuyển cọc trước rồi trả nốt sau
    received = Decimal(str(order.paid_amount or 0)) + Decimal(str(data.amount))
    total    = Decimal(str(order.grand_total))
    deposit  = deposit_of(order)

    order.paid_amount = received
    order.payment_ref = data.transactionid
    order.paid_at     = datetime.utcnow()

    if received >= total:
        order.payment_status = "paid"
        note = "Đã thanh toán đủ."
    elif received >= deposit:
        order.payment_status = "deposit_paid"
        note = "Đã nhận tiền cọc."
    else:
        # Chưa đủ cọc → vẫn để unpaid, người bán tự xử lý
        order.payment_status = "unpaid"
        note = "Ghi nhận giao dịch thiếu tiền cọc."
        log.warning("[vietqr] đơn %s nhận thiếu cọc: %s / %s",
                    order.order_code, received, deposit)

    if order.payment_status in ("paid", "deposit_paid") and order.status == "pending":
        order.status = "confirmed"
    order.save()
    log.info("[vietqr] đơn %s: %s (đã nhận %s / tổng %s)",
             order.order_code, order.payment_status, received, total)

    return {"error": False, "errorReason": None, "toastMessage": note,
            "object": {"reftransactionid": data.transactionid}}
