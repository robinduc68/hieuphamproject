# HUY VO Clone – Vue 3 + Vite

Clone giao diện trang web [huy-vo.com](https://huy-vo.com) sử dụng **Vue 3**, **Vue Router**, và **Vite**.

## Cấu trúc thư mục

```
huy-vo-clone/
├── index.html                      # Entry HTML
├── package.json
├── vite.config.js
└── src/
    ├── main.js                     # App entry, router setup
    ├── App.vue                     # Root layout (Banner + Header + RouterView + Footer)
    ├── assets/
    │   └── base.css                # Design tokens, reset, global utilities
    ├── data/                       # Static data (thay bằng API thật khi cần)
    │   ├── navigation.js           # Nav links, mega-menu, footer links
    │   ├── products.js             # New arrivals, featured products
    │   └── collections.js         # Collections data
    ├── components/
    │   ├── layout/
    │   │   ├── TopBanner.vue       # Marquee thông báo phía trên
    │   │   ├── AppHeader.vue       # Sticky header: logo, nav, search, cart
    │   │   ├── MegaMenu.vue        # Dropdown mega menu khi hover Shop
    │   │   └── AppFooter.vue       # Footer: links, newsletter, copyright
    │   ├── home/
    │   │   ├── HeroSection.vue     # Hero fullscreen với animation
    │   │   ├── ModernHeritage.vue  # Section Modern Heritage 2 cột
    │   │   ├── NewArrivals.vue     # Lưới sản phẩm mới + tab filter
    │   │   ├── QuoteSection.vue    # Quote thương hiệu
    │   │   ├── FeaturedCarousel.vue# Carousel sản phẩm nổi bật (auto-play, drag)
    │   │   ├── IconicProducts.vue  # Sản phẩm biểu tượng + mosaic grid
    │   │   ├── CollectionsGrid.vue # Grid bộ sưu tập 2×2
    │   │   └── NewsletterBanner.vue# Form đăng ký email
    │   └── ui/
    │       ├── ProductCard.vue     # Card sản phẩm tái sử dụng (quick-add, size chips)
    │       └── CartDrawer.vue      # Slide-in giỏ hàng
    └── views/
        └── HomeView.vue            # Trang chủ – ghép các section lại
```

## Cài đặt & chạy

```bash
# 1. Di chuyển vào thư mục
cd huy-vo-clone

# 2. Cài dependencies
npm install

# 3. Chạy development server
npm run dev

# 4. Build production
npm run build

# 5. Preview bản build
npm run preview
```

## Tính năng đã implement

| Section | Chi tiết |
|---|---|
| **TopBanner** | Marquee thông báo loop vô hạn |
| **AppHeader** | Sticky, scroll-shadow, mega menu hover, search bar collapsible, cart drawer |
| **MegaMenu** | 4 cột danh mục + editorial panel, transition mượt |
| **CartDrawer** | Teleport, overlay blur, slide animation |
| **HeroSection** | Fullscreen, staggered animation, atmospheric gradient + noise texture |
| **ModernHeritage** | 2-column layout, 4-card grid với hover scale |
| **NewArrivals** | Tab filter (Tất cả / Áo Dài / Bà Ba), ProductCard grid, toast notification |
| **ProductCard** | Quick-add overlay, size selection, hover effects |
| **QuoteSection** | Background text watermark, gold ornaments |
| **FeaturedCarousel** | Auto-play 4.5s, drag-to-navigate, dot + arrow controls |
| **IconicProducts** | Stats row, mosaic tile grid với span-tall |
| **CollectionsGrid** | 2×2 grid, tall card span 2 rows, hover animations |
| **NewsletterBanner** | Form validation, checkbox consent, success state |
| **AppFooter** | 5-column layout, social links, newsletter inline |

## Mở rộng (gợi ý)

- Kết nối **WooCommerce REST API** để lấy sản phẩm thật
- Thêm **Pinia** store để quản lý giỏ hàng
- Thêm **i18n** (vue-i18n) cho đa ngôn ngữ VI/EN
- Thêm **IntersectionObserver** để trigger scroll animations
- Tích hợp **Stripe / VNPAY** cho thanh toán

## Design System

| Token | Giá trị |
|---|---|
| `--cream` | `#f5f0e8` |
| `--charcoal` | `#1a1a18` |
| `--gold` | `#b8972a` |
| `--gold-light` | `#d4af37` |
| `--warm-white` | `#faf8f4` |
| `--font-display` | Cormorant Garamond |
| `--font-body` | Montserrat |
