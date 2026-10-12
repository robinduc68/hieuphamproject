"""
Tích hợp VietQR — hai chiều:

  1. Hệ thống  →  VietQR : lấy token rồi tạo mã QR động cho từng đơn hàng.
  2. VietQR    →  Hệ thống: khi tiền về, VietQR gọi /api/bank/api/transaction-sync
                            (xem app/routers/payments.py).

Tài liệu: https://api.vietqr.vn/vi/api-vietqr-callback
Sandbox : https://dev.vietqr.org   |  Production: https://api.vietqr.org

Thiếu cấu hình (xem VIETQR_* trong .env) thì mọi hàm ở đây raise VietQRError,
web tự quay về hình thức chuyển khoản thủ công chứ không vỡ trang.
"""
from __future__ import annotations

import base64
import logging
import time
import unicodedata
from decimal import Decimal

import httpx

from app.config import get_settings

log = logging.getLogger(__name__)
settings = get_settings()

# Token VietQR sống 300s, xin lại trước khi hết hạn 30s cho chắc
_TOKEN_SAFETY_SECONDS = 30
_token_cache: dict = {"value": None, "expires_at": 0.0}

TIMEOUT = httpx.Timeout(15.0)


class VietQRError(RuntimeError):
    """Gọi VietQR thất bại — caller tự quyết định fallback."""


def _require_config() -> None:
    if not settings.vietqr_enabled:
        raise VietQRError(
            "Chưa cấu hình VietQR. Cần VIETQR_USERNAME, VIETQR_PASSWORD, "
            "VIETQR_BANK_CODE, VIETQR_BANK_ACCOUNT, VIETQR_ACCOUNT_NAME trong .env"
        )


def _url(path: str) -> str:
    return f"{settings.vietqr_base_url.rstrip('/')}{path}"


def get_token(force: bool = False) -> str:
    """access_token của VietQR, có cache theo expires_in."""
    _require_config()
    now = time.time()
    if not force and _token_cache["value"] and now < _token_cache["expires_at"]:
        return _token_cache["value"]

    basic = base64.b64encode(
        f"{settings.vietqr_username}:{settings.vietqr_password}".encode()
    ).decode()

    try:
        r = httpx.post(
            _url("/vqr/api/token_generate"),
            headers={"Authorization": f"Basic {basic}", "Content-Type": "application/json"},
            json={},
            timeout=TIMEOUT,
        )
    except httpx.HTTPError as e:
        raise VietQRError(f"Không gọi được API token của VietQR: {e}") from e

    if r.status_code != 200:
        raise VietQRError(f"VietQR từ chối cấp token ({r.status_code}): {r.text[:200]}")

    data = r.json()
    token = data.get("access_token")
    if not token:
        raise VietQRError(f"Phản hồi token thiếu access_token: {data}")

    _token_cache["value"] = token
    _token_cache["expires_at"] = now + max(int(data.get("expires_in", 300)) - _TOKEN_SAFETY_SECONDS, 30)
    return token


def strip_accents(text: str) -> str:
    """'LÊ VĂN TUẤN' → 'LE VAN TUAN' — VietQR không nhận dấu tiếng Việt."""
    nfkd = unicodedata.normalize("NFD", text or "")
    plain = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    return plain.replace("Đ", "D").replace("đ", "d")


def generate_qr(*, order_code: str, amount: Decimal | int, note: str = "") -> dict:
    """
    Tạo QR động cho một đơn hàng.

    order_code dùng cho cả orderId (tối đa 13 ký tự) lẫn content (tối đa 23) —
    để lúc tiền về đối chiếu được ngay về đơn nào.
    """
    _require_config()
    token = get_token()

    payload = {
        "bankCode":     settings.vietqr_bank_code,
        "bankAccount":  settings.vietqr_bank_account,
        "userBankName": strip_accents(settings.vietqr_account_name).upper(),
        "content":      order_code[:23],
        "qrType":       0,                     # QR động: gắn số tiền + orderId
        "amount":       int(Decimal(str(amount))),
        "orderId":      order_code[:13],
        "transType":    "C",                   # tiền vào
    }
    if note:
        payload["note"] = note[:100]

    try:
        r = httpx.post(
            _url("/vqr/api/qr/generate-customer"),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
            timeout=TIMEOUT,
        )
    except httpx.HTTPError as e:
        raise VietQRError(f"Không gọi được API tạo QR: {e}") from e

    # Token hết hạn sớm → xin lại một lần rồi thử lại
    if r.status_code == 401:
        token = get_token(force=True)
        r = httpx.post(
            _url("/vqr/api/qr/generate-customer"),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json=payload,
            timeout=TIMEOUT,
        )

    if r.status_code != 200:
        raise VietQRError(f"VietQR không tạo được QR ({r.status_code}): {r.text[:300]}")

    data = r.json()
    if not data.get("qrCode"):
        raise VietQRError(f"Phản hồi tạo QR thiếu qrCode: {data}")
    return data
