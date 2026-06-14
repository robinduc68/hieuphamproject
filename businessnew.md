# HUY VO – Chuẩn hoá DB & API Design

> Review và thiết kế lại dựa trên UI thực tế đã xây dựng.  
> Phần **❌ Sai hiện tại** → **✅ Chuẩn** ghi rõ từng lý do.

---

## PHẦN 1 – CÁC LỖI DESIGN HIỆN TẠI

### DB Issues

| # | Bảng / Field | Vấn đề | Mức độ |
|---|---|---|---|
| 1 | `order_items.product_id` | `ON DELETE RESTRICT` — nếu admin xoá sản phẩm sẽ **block** vì còn order_items trỏ tới. Phải là `SET NULL` | 🔴 Nghiêm trọng |
| 2 | `order_items` | Không có cột `product_name` lưu snapshot. Khi sản phẩm bị đổi tên hoặc xoá → **mất dữ liệu lịch sử đơn hàng** | 🔴 Nghiêm trọng |
| 3 | `orders` | Thiếu `payment_method`, `payment_status` — không biết khách trả tiền chưa, trả kiểu gì | 🔴 Nghiêm trọng |
| 4 | `orders` | Thiếu `shipping_fee`, `discount_amount` — `total` đang là tổng sản phẩm thuần, không tính phí ship | 🟠 Quan trọng |
| 5 | `orders` | Địa chỉ VN thiếu `district` (quận/huyện) và `ward` (phường/xã) | 🟠 Quan trọng |
| 6 | `product_sizes` | Không có `sort_order` — size hiển thị theo thứ tự insert, không kiểm soát được (S M L hay 32 34 36) | 🟠 Quan trọng |
| 7 | `product_images` | Có cả `is_primary` lẫn `sort_order`, hai field này **redundant** — `sort_order = 0` đã là ảnh chính | 🟡 Nhỏ |
| 8 | `products` | Thiếu `compare_at_price` — không thể hiện giá gốc khi sale (luxury brand hay có promo) | 🟡 Nhỏ |
| 9 | `users` | `address` là text tự do gắn thẳng vào user — địa chỉ giao hàng thuộc về order, không thuộc user | 🟡 Nhỏ |
| 10 | `ShopView.vue` | Hardcode category slug (`ao-dai`, `phap-phuc`, `dam-lua`, `khan-lua`) **không khớp** với DB đang seed (`modern-heritage`, `womenswear`) — UI và DB **hoàn toàn lệch nhau** | 🔴 Nghiêm trọng |

### API Issues

| # | Endpoint | Vấn đề | Mức độ |
|---|---|---|---|
| 1 | `PUT /api/users/me/password` | Dùng **query params** cho password → password lộ trong server log, browser history, proxy log | 🔴 Nghiêm trọng |
| 2 | `GET /api/products/{slug}` | Detect số → query by ID là **hack**, bỏ qua `is_active`. Admin cần endpoint riêng | 🟠 Quan trọng |
| 3 | `GET /api/orders/my-orders` | **Không có pagination** — user có 1000 đơn thì trả về 1000 record một lúc | 🟠 Quan trọng |
| 4 | `DELETE /newsletter/unsubscribe/{email}` | Email trong URL path → bị encode kỳ lạ, server log lộ email. Nên dùng body/query | 🟡 Nhỏ |
| 5 | `POST /api/products` | Tự động tạo 1 row `product_images` với URL placeholder giả → rác trong DB | 🟡 Nhỏ |
| 6 | Admin routes trộn lẫn với public routes | `POST /api/products` (admin) và `GET /api/products` (public) cùng prefix — khó maintain, khó phân quyền rõ ràng | 🟡 Nhỏ |

---

## PHẦN 2 – DATABASE DESIGN CHUẨN

Tất cả bảng kế thừa 3 cột chung: `id` (PK auto-increment), `created_at`, `updated_at`.

---

### 2.1 `users`

| Column          | Type         | Constraint       | Ghi chú                                   |
|-----------------|--------------|------------------|-------------------------------------------|
| id              | integer      | PK               |                                           |
| email           | varchar(255) | UNIQUE, NOT NULL |                                           |
| hashed_password | varchar(255) | NOT NULL         | bcrypt hash                               |
| full_name       | varchar(255) | nullable         |                                           |
| phone           | varchar(30)  | nullable         |                                           |
| is_active       | boolean      | default true     | false = tài khoản bị khoá                |
| is_admin        | boolean      | default false    |                                           |
| created_at      | timestamp    |                  |                                           |
| updated_at      | timestamp    |                  |                                           |

> ❌ **Bỏ** `address` ra khỏi users — địa chỉ giao hàng thuộc về từng đơn hàng, không phải user.

---

### 2.2 `categories`

Danh mục cấp 1: Áo Dài, Pháp Phục, Đầm Lụa, Khăn Lụa, v.v. — **phải khớp với ShopView.vue**.

| Column      | Type         | Constraint       | Ghi chú                      |
|-------------|--------------|------------------|------------------------------|
| id          | integer      | PK               |                              |
| name        | varchar(120) | NOT NULL         | VD: "Áo Dài"                |
| slug        | varchar(120) | UNIQUE, NOT NULL | VD: "ao-dai"                |
| description | text         | nullable         |                              |
| image_url   | varchar(500) | nullable         |                              |
| is_active   | boolean      | default true     |                              |
| sort_order  | integer      | default 0        |                              |
| created_at  | timestamp    |                  |                              |
| updated_at  | timestamp    |                  |                              |

---

### 2.3 `subcategories`

Danh mục cấp 2: Khăn lụa vẽ tay, Khăn lụa loang tia, v.v.

| Column      | Type         | Constraint              | Ghi chú                        |
|-------------|--------------|-------------------------|--------------------------------|
| id          | integer      | PK                      |                                |
| category_id | integer      | FK → categories(id)     | CASCADE on delete              |
| name        | varchar(120) | NOT NULL                |                                |
| slug        | varchar(120) | UNIQUE, NOT NULL        |                                |
| description | text         | nullable                |                                |
| image_url   | varchar(500) | nullable                |                                |
| is_active   | boolean      | default true            |                                |
| sort_order  | integer      | default 0               |                                |
| created_at  | timestamp    |                         |                                |
| updated_at  | timestamp    |                         |                                |

---

### 2.4 `products`

| Column            | Type           | Constraint              | Ghi chú                                             |
|-------------------|----------------|-------------------------|-----------------------------------------------------|
| id                | integer        | PK                      |                                                     |
| name              | varchar(255)   | NOT NULL                |                                                     |
| slug              | varchar(255)   | UNIQUE, NOT NULL        |                                                     |
| price             | decimal(14,0)  | NOT NULL                | Giá bán hiện tại (VNĐ)                             |
| compare_at_price  | decimal(14,0)  | nullable                | ✅ **Mới** — giá gốc trước khi sale, hiển thị gạch ngang |
| description       | text           | nullable                |                                                     |
| fabric            | text           | nullable                | Chất liệu vải                                      |
| care_instructions | text           | nullable                | Hướng dẫn bảo quản                                |
| shipping_info     | text           | nullable                |                                                     |
| category_id       | integer        | FK → categories(id)     | SET NULL on delete                                 |
| subcategory_id    | integer        | FK → subcategories(id)  | SET NULL on delete, nullable                        |
| collection_id     | integer        | FK → collections(id)    | SET NULL on delete, nullable                        |
| primary_color     | varchar(20)    | nullable                | HEX cho UI placeholder                             |
| is_new            | boolean        | default false           | Badge "Mới"                                        |
| is_active         | boolean        | default true            | false = soft delete                                |
| is_featured       | boolean        | default false           | Hiển thị section nổi bật                          |
| sort_order        | integer        | default 0               |                                                     |
| created_at        | timestamp      |                         |                                                     |
| updated_at        | timestamp      |                         |                                                     |

---

### 2.5 `product_images`

| Column     | Type         | Constraint           | Ghi chú                                                        |
|------------|--------------|----------------------|----------------------------------------------------------------|
| id         | integer      | PK                   |                                                                |
| product_id | integer      | FK → products(id)    | CASCADE on delete                                              |
| url        | varchar(500) | NOT NULL             | `/media/products/{id}/filename.jpg`                           |
| alt_text   | varchar(255) | nullable             |                                                                |
| sort_order | integer      | default 0            | ✅ **0 = ảnh chính** — bỏ `is_primary` vì redundant với sort_order=0 |
| created_at | timestamp    |                      |                                                                |
| updated_at | timestamp    |                      |                                                                |

> ❌ **Bỏ** `is_primary` — dùng `ORDER BY sort_order ASC LIMIT 1` để lấy ảnh chính.

---

### 2.6 `product_sizes`

| Column       | Type        | Constraint           | Ghi chú                                                   |
|--------------|-------------|----------------------|-----------------------------------------------------------|
| id           | integer     | PK                   |                                                           |
| product_id   | integer     | FK → products(id)    | CASCADE on delete                                         |
| size         | varchar(20) | NOT NULL             | "S", "M", "L", "XL" hoặc "32", "34", "36"              |
| is_available | boolean     | default true         | false = hết hàng                                         |
| sort_order   | integer     | default 0            | ✅ **Mới** — kiểm soát thứ tự hiển thị S→M→L→XL          |
| created_at   | timestamp   |                      |                                                           |
| updated_at   | timestamp   |                      |                                                           |

---

### 2.7 `collections`

| Column       | Type         | Constraint       | Ghi chú                                     |
|--------------|--------------|------------------|---------------------------------------------|
| id           | integer      | PK               |                                             |
| name         | varchar(180) | NOT NULL         |                                             |
| slug         | varchar(180) | UNIQUE, NOT NULL |                                             |
| subtitle     | varchar(255) | nullable         |                                             |
| description  | text         | nullable         |                                             |
| cover_url    | varchar(500) | nullable         |                                             |
| gradient     | varchar(255) | nullable         | CSS gradient cho banner                    |
| accent_color | varchar(20)  | nullable         | HEX màu nhấn                               |
| is_active    | boolean      | default true     |                                             |
| sort_order   | integer      | default 0        |                                             |
| created_at   | timestamp    |                  |                                             |
| updated_at   | timestamp    |                  |                                             |

---

### 2.8 `orders`

| Column           | Type           | Constraint           | Ghi chú                                                            |
|------------------|----------------|----------------------|--------------------------------------------------------------------|
| id               | integer        | PK                   |                                                                    |
| user_id          | integer        | FK → users(id)       | SET NULL on delete; null = khách vãng lai                         |
| email            | varchar(255)   | NOT NULL             |                                                                    |
| full_name        | varchar(200)   | NOT NULL             |                                                                    |
| phone            | varchar(20)    | NOT NULL             |                                                                    |
| address          | text           | NOT NULL             | Số nhà, tên đường                                                 |
| ward             | varchar(100)   | nullable             | ✅ **Mới** — Phường/Xã                                             |
| district         | varchar(100)   | nullable             | ✅ **Mới** — Quận/Huyện                                            |
| city             | varchar(100)   | NOT NULL             | Tỉnh/Thành phố                                                    |
| country          | varchar(100)   | default "Vietnam"    |                                                                    |
| note             | text           | nullable             |                                                                    |
| subtotal         | decimal(16,0)  | NOT NULL             | ✅ **Đổi tên từ `total`** — tổng tiền sản phẩm trước ship/giảm giá |
| shipping_fee     | decimal(16,0)  | default 0            | ✅ **Mới** — phí vận chuyển                                        |
| discount_code    | varchar(50)    | nullable             | ✅ **Mới** — mã giảm giá đã áp dụng                               |
| discount_amount  | decimal(16,0)  | default 0            | ✅ **Mới** — số tiền được giảm                                     |
| grand_total      | decimal(16,0)  | NOT NULL             | ✅ **Mới** — `subtotal + shipping_fee - discount_amount` (số tiền thực thu) |
| payment_method   | varchar(30)    | default "cod"        | ✅ **Mới** — `cod`, `bank_transfer`, `vnpay`, `momo`              |
| payment_status   | varchar(20)    | default "unpaid"     | ✅ **Mới** — `unpaid`, `paid`, `refunded`                         |
| status           | varchar(20)    | default "pending"    | Trạng thái xử lý đơn (xem bên dưới)                              |
| tracking_code    | varchar(100)   | nullable             |                                                                    |
| created_at       | timestamp      |                      |                                                                    |
| updated_at       | timestamp      |                      |                                                                    |

**Vòng đời `status` (trạng thái xử lý):**
```
pending → confirmed → processing → shipped → delivered
                                ↘ cancelled → (refunded nếu đã thanh toán)
```

**Vòng đời `payment_status`:**
```
unpaid → paid
paid   → refunded
```

| payment_method | Ý nghĩa          |
|----------------|------------------|
| cod            | Trả tiền khi nhận |
| bank_transfer  | Chuyển khoản      |
| vnpay          | Cổng VNPay        |
| momo           | Ví MoMo           |

---

### 2.9 `order_items`

| Column       | Type           | Constraint           | Ghi chú                                                           |
|--------------|----------------|----------------------|-------------------------------------------------------------------|
| id           | integer        | PK                   |                                                                   |
| order_id     | integer        | FK → orders(id)      | CASCADE on delete                                                 |
| product_id   | integer        | FK → products(id)    | ✅ **SET NULL** on delete (❌ hiện đang RESTRICT — sai)            |
| product_name | varchar(255)   | NOT NULL             | ✅ **Mới** — snapshot tên sản phẩm lúc đặt hàng                   |
| size         | varchar(20)    | NOT NULL             | Snapshot size                                                     |
| quantity     | integer        | NOT NULL, default 1  |                                                                   |
| unit_price   | decimal(14,0)  | NOT NULL             | ✅ **Đổi tên từ `price`** — giá đơn vị lúc đặt hàng (snapshot)   |
| created_at   | timestamp      |                      |                                                                   |
| updated_at   | timestamp      |                      |                                                                   |

---

### 2.10 `newsletter_subscriptions`

| Column    | Type         | Constraint       | Ghi chú               |
|-----------|--------------|------------------|-----------------------|
| id        | integer      | PK               |                       |
| email     | varchar(255) | UNIQUE, NOT NULL |                       |
| full_name | varchar(255) | nullable         |                       |
| is_active | boolean      | default true     | false = unsubscribed  |
| created_at| timestamp    |                  |                       |
| updated_at| timestamp    |                  |                       |

---

### Sơ đồ quan hệ

```
categories (1) ──────────────< (n) subcategories
categories (1) ──────────────< (n) products
subcategories (1) ───────────< (n) products
collections (1) ─────────────< (n) products
products (1) ────────────────< (n) product_images
products (1) ────────────────< (n) product_sizes
users (1) ───────────────────< (n) orders
orders (1) ──────────────────< (n) order_items
order_items (n) >────────────── (1) products  [SET NULL on delete]
```

---

## PHẦN 3 – API DESIGN CHUẨN

**Base URL:** `/api`  
**Auth:** `Authorization: Bearer <jwt_token>`

**Ký hiệu:**
- 🔓 Public
- 🔐 User đăng nhập
- 🛡️ Admin (`is_admin = true`)

---

### 3.1 Auth — `/api/auth`

| Method | Path        | Auth | Request Body                              | Response        | Ghi chú                                     |
|--------|-------------|------|-------------------------------------------|-----------------|---------------------------------------------|
| POST   | `/register` | 🔓   | `email, password, full_name?, phone?`     | `token + user`  | 409 nếu email đã tồn tại                   |
| POST   | `/login`    | 🔓   | `email, password`                         | `token + user`  | 401 nếu sai, 403 nếu bị khoá               |

> ✅ Tách khỏi `/api/users` để rõ ràng hơn về mục đích.

---

### 3.2 Users (cá nhân) — `/api/users`

| Method | Path             | Auth | Request Body                        | Ghi chú                                                          |
|--------|------------------|------|-------------------------------------|------------------------------------------------------------------|
| GET    | `/me`            | 🔐   | —                                   | Lấy thông tin tài khoản đang đăng nhập                          |
| PUT    | `/me`            | 🔐   | `full_name?, phone?`                | Cập nhật thông tin cá nhân                                       |
| POST   | `/me/password`   | 🔐   | `old_password, new_password` (body) | ✅ **Body thay vì query params** — tránh lộ password trong log   |
| GET    | `/me/orders`     | 🔐   | —                                   | ✅ **Chuyển đây** thay vì `/orders/my-orders` — đúng REST hơn. Query: `page, per_page` |

---

### 3.3 Categories — `/api/categories`

| Method | Path                       | Auth | Ghi chú                                                      |
|--------|----------------------------|------|--------------------------------------------------------------|
| GET    | `/`                        | 🔓   | Danh sách tất cả categories kèm subcategories. `?active_only=true` |
| GET    | `/{slug}`                  | 🔓   | Chi tiết 1 category                                          |
| POST   | `/`                        | 🛡️   | Tạo category. Body: `name, slug, description?, sort_order?` |
| PUT    | `/{id}`                    | 🛡️   | Cập nhật category                                            |
| DELETE | `/{id}`                    | 🛡️   | Xoá cứng (hard delete)                                       |
| POST   | `/{id}/subcategories`      | 🛡️   | Tạo subcategory trong category                               |

### SubCategories — `/api/subcategories`

| Method | Path    | Auth | Ghi chú             |
|--------|---------|------|---------------------|
| PUT    | `/{id}` | 🛡️   | Cập nhật subcategory |
| DELETE | `/{id}` | 🛡️   | Xoá cứng             |

---

### 3.4 Products — `/api/products`

**Public (storefront):**

| Method | Path             | Auth | Ghi chú                                                                                        |
|--------|------------------|------|------------------------------------------------------------------------------------------------|
| GET    | `/`              | 🔓   | Danh sách sản phẩm active, có phân trang. Query: `page, per_page, category, category_id, search, is_new, is_featured` |
| GET    | `/new-arrivals`  | 🔓   | Sản phẩm mới. Query: `limit`                                                                   |
| GET    | `/featured`      | 🔓   | Sản phẩm nổi bật. Query: `limit`                                                               |
| GET    | `/{slug}`        | 🔓   | Chi tiết sản phẩm theo **slug** (chỉ slug, không phải ID)                                     |

**Admin (quản lý):**

| Method | Path                            | Auth | Ghi chú                                                       |
|--------|--------------------------------|------|---------------------------------------------------------------|
| GET    | `/api/admin/products`           | 🛡️   | ✅ Danh sách admin — hiện cả inactive, có search/filter       |
| GET    | `/api/admin/products/{id}`      | 🛡️   | ✅ Lấy sản phẩm theo numeric ID (dùng khi edit)               |
| POST   | `/api/products`                 | 🛡️   | Tạo sản phẩm. ❌ Bỏ auto-tạo placeholder image               |
| PUT    | `/api/products/{id}`            | 🛡️   | Cập nhật thông tin sản phẩm                                   |
| DELETE | `/api/products/{id}`            | 🛡️   | Soft delete (`is_active = false`)                             |
| POST   | `/api/products/{id}/images`     | 🛡️   | Upload ảnh (multipart, field `file`)                          |
| PUT    | `/api/products/{id}/images/{img_id}` | 🛡️ | Cập nhật `sort_order`, `alt_text`                         |
| DELETE | `/api/products/{id}/images/{img_id}` | 🛡️ | Xoá ảnh                                                   |
| POST   | `/api/products/{id}/sizes`      | 🛡️   | Thêm size. Body: `size, is_available?, sort_order?`           |
| PUT    | `/api/products/{id}/sizes/{size_id}` | 🛡️ | Cập nhật size (`size, is_available, sort_order`)          |
| DELETE | `/api/products/{id}/sizes/{size_id}` | 🛡️ | Xoá size                                                  |

---

### 3.5 Collections — `/api/collections`

| Method | Path    | Auth | Ghi chú                          |
|--------|---------|------|----------------------------------|
| GET    | `/`     | 🔓   | Danh sách active, theo sort_order |
| GET    | `/{slug}` | 🔓 | Chi tiết                          |
| POST   | `/`     | 🛡️   | Tạo mới                           |
| PUT    | `/{id}` | 🛡️   | Cập nhật                          |
| DELETE | `/{id}` | 🛡️   | Soft delete                       |

---

### 3.6 Orders — `/api/orders`

| Method | Path            | Auth | Request Body / Query                                                 | Ghi chú                                               |
|--------|-----------------|------|----------------------------------------------------------------------|-------------------------------------------------------|
| POST   | `/`             | 🔓🔐  | `email, full_name, phone, address, ward?, district?, city, country?, note?, payment_method?, items[]` | Tạo đơn. Hệ thống tự tính `subtotal`, `grand_total`. Validate size còn hàng. |
| GET    | `/`             | 🛡️   | `?page, per_page, status, payment_status`                            | (Admin) Tất cả đơn hàng                              |
| GET    | `/{id}`         | 🔐🛡️  | —                                                                    | Chi tiết đơn. User chỉ xem đơn của mình              |
| PATCH  | `/{id}/status`  | 🛡️   | `status, tracking_code?`                                             | (Admin) Cập nhật trạng thái xử lý                    |
| PATCH  | `/{id}/payment` | 🛡️   | `payment_status`                                                     | ✅ **Mới** (Admin) Cập nhật trạng thái thanh toán     |

---

### 3.7 Newsletter — `/api/newsletter`

| Method | Path           | Auth | Ghi chú                                                                  |
|--------|----------------|------|--------------------------------------------------------------------------|
| POST   | `/subscribe`   | 🔓   | Body: `email, full_name?`. Reactivate nếu đã tồn tại và inactive        |
| POST   | `/unsubscribe` | 🔓   | ✅ Body: `email` — thay vì email trong URL path để tránh log lộ email    |

---

### 3.8 Admin — `/api/admin`

| Method | Path               | Auth | Ghi chú                                                                              |
|--------|--------------------|------|--------------------------------------------------------------------------------------|
| GET    | `/stats`           | 🛡️   | Thống kê: `total_orders, revenue (chỉ đơn delivered/paid), total_products, total_users` |
| GET    | `/products`        | 🛡️   | Danh sách sản phẩm gồm cả inactive. Query: `page, per_page, search, category_id, is_active` |
| GET    | `/products/{id}`   | 🛡️   | Chi tiết sản phẩm theo numeric ID (dùng khi edit trên admin panel)                  |
| GET    | `/users`           | 🛡️   | Danh sách users. Query: `page, per_page, search, is_admin`                           |
| PUT    | `/users/{id}`      | 🛡️   | Cập nhật user: `full_name, email, phone, is_admin, is_active, password?`             |
| DELETE | `/users/{id}`      | 🛡️   | Soft delete (`is_active = false`). Không thể tự xoá mình                            |

---

### 3.9 Health

| Method | Path      | Auth | Ghi chú                                    |
|--------|-----------|------|--------------------------------------------|
| GET    | `/health` | 🔓   | Kiểm tra server + DB. Trả về version, status |

---

## PHẦN 4 – DANH SÁCH VIỆC CẦN LÀM ĐỂ ĐẠT CHUẨN

### Ưu tiên cao (🔴 phải sửa):

- [ ] **Fix `order_items.product_id`** từ `RESTRICT` → `SET NULL` on delete
- [ ] **Thêm cột `product_name`** vào `order_items` và snapshot khi tạo đơn
- [ ] **Thêm `payment_method`, `payment_status`** vào `orders`
- [ ] **Đổi tên `total` → `subtotal`**, thêm `grand_total`, `shipping_fee`, `discount_amount` vào `orders`
- [ ] **Fix `PUT /me/password`** từ query params → body
- [ ] **Đồng bộ category slugs** giữa ShopView.vue và DB seed (hiện tại hoàn toàn lệch nhau)

### Ưu tiên vừa (🟠 nên sửa):

- [ ] Thêm `district`, `ward` vào `orders`
- [ ] Thêm `sort_order` vào `product_sizes`
- [ ] Thêm `compare_at_price` vào `products`
- [ ] Thêm pagination cho `GET /api/users/me/orders`
- [ ] Tạo `/api/admin/products/{id}` thay thế hack detect-số trong `GET /products/{slug}`

### Ưu tiên thấp (🟡 cải thiện):

- [ ] Bỏ `is_primary` trong `product_images`, dùng `sort_order = 0`
- [ ] Bỏ auto-tạo placeholder image khi tạo sản phẩm mới
- [ ] Đổi `DELETE /newsletter/unsubscribe/{email}` → `POST /newsletter/unsubscribe` với body
- [ ] Thêm `PATCH /api/orders/{id}/payment` để admin đánh dấu đã thu tiền
- [ ] Xoá `address` khỏi `users` table (địa chỉ chỉ thuộc orders)
