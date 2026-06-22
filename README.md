# HUY VO – Fullstack Clone

> **Vietnam's Sustainable Luxury House** – Clone hoàn chỉnh với Vue 3 Frontend + FastAPI Backend + PostgreSQL

---

## 📁 Cấu trúc dự án

```
huy-vo-fullstack/
├── docker-compose.yml          ← Orchestrate toàn bộ services
├── .env.example                ← Copy → .env rồi điền giá trị
│
├── backend/                    ← FastAPI + Peewee + PostgreSQL
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py             ← FastAPI app, CORS, routers, static files
│       ├── config.py           ← Settings qua pydantic-settings
│       ├── database.py         ← Peewee PostgresqlDatabase instance
│       ├── auth.py             ← JWT, bcrypt, FastAPI dependencies
│       ├── seed.py             ← Seed data (14 sản phẩm, 4 collections, admin)
│       ├── models/
│       │   ├── base.py         ← BaseModel với timestamps
│       │   ├── product.py      ← Category, Product, ProductImage, ProductSize
│       │   ├── collection.py   ← Collection
│       │   ├── user.py         ← User
│       │   └── order.py        ← Order, OrderItem, Newsletter
│       ├── schemas/            ← Pydantic v2 schemas (request/response)
│       │   ├── product.py
│       │   ├── collection.py
│       │   ├── user.py
│       │   └── order.py
│       ├── routers/            ← FastAPI routers
│       │   ├── products.py     ← CRUD sản phẩm + upload ảnh
│       │   ├── collections.py
│       │   ├── users.py        ← Register, Login, Me
│       │   └── orders.py       ← Đặt hàng + Newsletter
│       └── migrations/
│           ├── runner.py       ← Migration runner tự viết (upgrade/downgrade/status)
│           └── 0001_initial.py ← Tạo toàn bộ bảng + triggers updated_at
│
└── frontend/                   ← Vue 3 + Vite + Pinia + Axios
    ├── Dockerfile              ← Build → Nginx serve
    ├── nginx.conf              ← SPA routing + proxy /api → backend
    ├── src/
    │   ├── main.js             ← App entry, Router, Pinia
    │   ├── App.vue             ← Root layout
    │   ├── api/                ← Axios API clients
    │   │   ├── client.js       ← Base axios instance + JWT interceptor
    │   │   ├── products.js
    │   │   ├── collections.js
    │   │   ├── orders.js
    │   │   └── users.js
    │   ├── composables/        ← Reusable async state hooks
    │   │   ├── useProducts.js  ← useProducts, useProduct, useNewArrivals, useFeaturedProducts
    │   │   └── useCollections.js
    │   ├── stores/             ← Pinia stores
    │   │   ├── auth.js         ← Login, register, logout, JWT persist
    │   │   └── cart.js         ← Cart CRUD, localStorage persist
    │   ├── components/
    │   │   ├── layout/
    │   │   │   ├── TopBanner.vue
    │   │   │   ├── AppHeader.vue   ← Sticky nav + MegaMenu + Cart count
    │   │   │   ├── MegaMenu.vue
    │   │   │   └── AppFooter.vue
    │   │   ├── home/
    │   │   │   ├── HeroSection.vue
    │   │   │   ├── ModernHeritage.vue
    │   │   │   ├── NewArrivals.vue      ← Gọi API /products/new-arrivals
    │   │   │   ├── QuoteSection.vue
    │   │   │   ├── FeaturedCarousel.vue ← Gọi API /products/featured
    │   │   │   ├── IconicProducts.vue
    │   │   │   ├── CollectionsGrid.vue  ← Gọi API /collections
    │   │   │   └── NewsletterBanner.vue ← POST /newsletter/subscribe
    │   │   └── ui/
    │   │       ├── ProductCard.vue      ← Quick-add, size select, hover
    │   │       └── CartDrawer.vue       ← Slide-in, real cart items
    │   └── views/
    │       ├── HomeView.vue
    │       ├── ShopView.vue        ← Danh sách + filter + search + phân trang
    │       ├── ProductDetailView.vue ← Gallery, sizes, accordion, related
    │       └── CheckoutView.vue    ← Form + POST /orders/
```

---

## 🚀 Chạy với Docker (khuyến nghị)

```bash
# 1. Clone project
git clone <repo-url> && cd huy-vo-fullstack

# 2. Tạo file .env từ template
cp .env.example .env
# (Tuỳ chỉnh mật khẩu nếu cần)

# 3. Khởi động toàn bộ stack
docker compose up -d

# 4. Xem logs
docker compose logs -f backend

# 5. Truy cập
#   Frontend : http://localhost:3000
#   API docs  : http://localhost:8000/api/docs
#   pgAdmin   : docker compose --profile dev up -d pgadmin
#               → http://localhost:5050  (admin@huyvo.com / admin)
```

Khi `backend` khởi động, nó tự động:
1. Chạy migration `0001_initial` → tạo toàn bộ bảng
2. Chạy seed → insert 14 sản phẩm, 4 collections, 1 admin user

---

## 💻 Chạy local (dev mode)

### Backend

```bash
cd backend

# Tạo virtualenv
python -m venv .venv && source .venv/bin/activate

# Cài dependencies
pip install -r requirements.txt

# Tạo .env (hoặc export tay)
cp ../.env.example .env
# Sửa DATABASE_URL trỏ vào PostgreSQL local

# Chạy migration
python -m app.migrations.runner upgrade

# Seed data
python -m app.seed

# Chạy server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev    # → http://localhost:5173
```

Vite proxy đã được cấu hình sẵn: `/api` → `http://localhost:8000`

---

## 🔑 Migration CLI

```bash
# Chạy tất cả migrations còn pending
python -m app.migrations.runner upgrade

# Chạy đến migration cụ thể
python -m app.migrations.runner upgrade 0001_initial

# Revert 1 migration gần nhất
python -m app.migrations.runner downgrade

# Revert 2 migrations
python -m app.migrations.runner downgrade 2

# Xem trạng thái
python -m app.migrations.runner status
```

### Thêm migration mới

```bash
# Tạo file mới theo quy tắc đặt tên:
touch backend/app/migrations/0002_add_product_stock.py
```

```python
# backend/app/migrations/0002_add_product_stock.py
def upgrade(db):
    db.execute_sql("ALTER TABLE products ADD COLUMN stock INT NOT NULL DEFAULT 0")

def downgrade(db):
    db.execute_sql("ALTER TABLE products DROP COLUMN stock")
```

---

## 📡 API Endpoints

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| GET | `/api/health` | Health check |
| GET | `/api/products/` | Danh sách sản phẩm (page, per_page, category, search, is_new, is_featured) |
| GET | `/api/products/new-arrivals` | Sản phẩm mới |
| GET | `/api/products/featured` | Sản phẩm nổi bật |
| GET | `/api/products/{slug}` | Chi tiết sản phẩm |
| POST | `/api/products/` | Tạo sản phẩm *(admin)* |
| PUT | `/api/products/{id}` | Cập nhật *(admin)* |
| DELETE | `/api/products/{id}` | Soft delete *(admin)* |
| POST | `/api/products/{id}/images` | Upload ảnh *(admin)* |
| GET | `/api/categories/` | Danh sách danh mục |
| GET | `/api/collections/` | Danh sách bộ sưu tập |
| POST | `/api/users/register` | Đăng ký |
| POST | `/api/users/login` | Đăng nhập → JWT |
| GET | `/api/users/me` | Thông tin cá nhân *(auth)* |
| POST | `/api/orders/` | Đặt hàng |
| GET | `/api/orders/my-orders` | Đơn hàng của tôi *(auth)* |
| PATCH | `/api/orders/{id}/status` | Cập nhật trạng thái *(admin)* |
| POST | `/api/newsletter/subscribe` | Đăng ký nhận tin |

Swagger UI đầy đủ: **http://localhost:8000/api/docs**

---

## 🛠 Design System

| Token | Giá trị |
|-------|---------|
| `--cream` | `#f5f0e8` |
| `--charcoal` | `#1a1a18` |
| `--gold` | `#b8972a` |
| `--gold-light` | `#d4af37` |
| `--warm-white` | `#faf8f4` |
| `--font-display` | Cormorant Garamond |
| `--font-body` | Montserrat |

---

## 👤 Tài khoản mặc định

| Role | Email | Mật khẩu |
|------|-------|----------|
| Admin | `admin@huyvo.com` | `Admin@123` |

---

## 🌐 Deploy lên VPS (Ubuntu 24.04)

### Yêu cầu
- VPS Ubuntu 24.04
- Domain trỏ về IP VPS (DNS A record)
- Repo đã push lên GitHub

### Lần đầu deploy

**1. SSH vào VPS**
```bash
ssh root@IP_VPS
```

**2. Cập nhật hệ thống**
```bash
apt update && apt upgrade -y
reboot
# SSH lại sau 30 giây
```

**3. Cài Docker**
```bash
curl -fsSL https://get.docker.com | sh
```

**4. Cài Nginx + Certbot**
```bash
apt install nginx certbot python3-certbot-nginx -y
```

**5. Clone repo**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git /var/www/hahoatsilk
cd /var/www/hahoatsilk
```

**6. Tạo file .env**
```bash
cp .env.production.example .env
nano .env
```
Tạo password và secret key:
```bash
python3 -c "import secrets; print(secrets.token_hex(16))"  # POSTGRES_PASSWORD
python3 -c "import secrets; print(secrets.token_hex(32))"  # SECRET_KEY
```
Điền vào `.env`: `POSTGRES_PASSWORD`, `DATABASE_URL`, `SECRET_KEY`, `ALLOWED_ORIGINS`, `APP_ENV=production`, `DEBUG=false`

**7. Cài Nginx config tạm (HTTP)**
```bash
cp /var/www/hahoatsilk/nginx-vps-temp.conf /etc/nginx/sites-available/hahoatsilk
ln -s /etc/nginx/sites-available/hahoatsilk /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx
```

**8. Trỏ DNS về IP VPS** (Cloudflare)

Thêm 3 A record, Proxy status = **DNS only**:
| Name | Content |
|------|---------|
| `@` | IP VPS |
| `www` | IP VPS |
| `admin` | IP VPS |

**9. Cài SSL**
```bash
certbot --nginx -d hahoatsilk.com -d www.hahoatsilk.com -d admin.hahoatsilk.com
```

**10. Deploy app**
```bash
bash deploy.sh
```

---

### Các lần deploy tiếp theo

Push code lên GitHub rồi chạy trên VPS:
```bash
cd /var/www/hahoatsilk && bash deploy.sh
```

---

### Kiểm tra logs
```bash
docker compose logs -f backend     # log backend
docker compose logs -f frontend    # log frontend
docker compose ps                  # trạng thái containers
```

---

## 📦 Tech Stack

| Layer | Công nghệ |
|-------|-----------|
| Frontend | Vue 3, Vue Router 4, Pinia, Axios, Vite |
| Backend | FastAPI, Peewee ORM, Pydantic v2, python-jose, passlib |
| Database | PostgreSQL 16 |
| Web server | Nginx 1.25 (Alpine) |
| Container | Docker + Docker Compose |
