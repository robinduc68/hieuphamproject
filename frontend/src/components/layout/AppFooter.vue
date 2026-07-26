<template>
  <footer class="app-footer">
    <div class="footer-wrap">
      <!-- Top row: Logo + tagline + CTA -->
      <div class="footer-top">
        <div class="footer-brand">
          <div class="footer-logo">
            <img src="/HHS LG (1) (2).png" alt="Hà Hoạt Silk" class="footer-logo-img" />
          </div>
          <p class="footer-tagline">
            <em>Lụa tơ tằm Nha Xá cao cấp</em>
          </p>
        </div>

        <RouterLink to="/cua-hang" class="footer-cta">
          Khám phá sản phẩm
          <svg viewBox="0 0 20 10" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M0 5h18M13 1l5 4-5 4"/>
          </svg>
        </RouterLink>
      </div>

      <div class="footer-divider" />

      <!-- Bottom columns -->
      <div class="footer-cols">
        <!-- Support -->
        <div class="footer-col">
          <h4 class="col-title">HỖ TRỢ KHÁCH HÀNG</h4>
          <p class="contact-line">(+84)08 66666 201</p>
          <p class="contact-line">hahoatsilk@gmail.com</p>
          <p class="contact-line">Làng nghề Nha Xá, Duy Tân, Ninh Bình</p>
        </div>

        <!-- Explore -->
        <div class="footer-col">
          <h4 class="col-title">KHÁM PHÁ</h4>
          <ul>
            <li><RouterLink to="/ve-chung-toi">Về chúng tôi</RouterLink></li>
            <li><RouterLink to="/cua-hang">Sản phẩm</RouterLink></li>
            <li><RouterLink to="/faq">Câu hỏi thường gặp</RouterLink></li>
            <li><RouterLink to="/tin-tuc">Tin tức</RouterLink></li>
          </ul>
        </div>

        <!-- Policy -->
        <div class="footer-col">
          <h4 class="col-title">CHÍNH SÁCH</h4>
          <ul>
            <li><RouterLink to="/chinh-sach-bao-mat">Chính sách bảo mật</RouterLink></li>
            <li><RouterLink to="/chinh-sach-doi-tra">Chính sách đổi trả</RouterLink></li>
            <li><RouterLink to="/chinh-sach-thanh-toan">Chính sách thanh toán</RouterLink></li>
            <li><RouterLink to="/chinh-sach-van-chuyen">Chính sách vận chuyển</RouterLink></li>
          </ul>
        </div>

        <!-- Social -->
        <div class="footer-col">
          <h4 class="col-title">THEO DÕI HÀ HOẠT SILK</h4>
          <div class="social-links">
            <a href="https://facebook.com" target="_blank" rel="noopener" aria-label="Facebook" class="social-btn">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>
              </svg>
            </a>
            <a href="https://tiktok.com" target="_blank" rel="noopener" aria-label="TikTok" class="social-btn">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.31 6.31 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.69a8.18 8.18 0 004.78 1.52V6.76a4.85 4.85 0 01-1.01-.07z"/>
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.app-footer {
  background: var(--brand-dark);
  width: 100%;
}

.footer-wrap {
  max-width: 1440px;
  margin: 0 auto;
  padding: 40px 64px 48px;
  color: white;
}

/* Top row */
.footer-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 24px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-logo-img {
  height: 88px;
  width: auto;
  object-fit: contain;
}

.footer-tagline {
  font-family: var(--font-script);
  font-size: 42px;
  color: #E8D5A8;
  font-style: normal;
}

/* CTA button */
.footer-cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  border: 1.5px solid #E8D5A8;
  border-radius: 40px;
  padding: 17px 38px;
  font-size: 19px;
  font-weight: 700;
  color: var(--brand-dark);
  background: #E8D5A8;
  transition: all var(--transition);
  white-space: nowrap;
}
.footer-cta:hover {
  background: #ECD3A2;
  border-color: #ECD3A2;
  transform: translateY(-2px);
}
.footer-cta svg { width: 22px; height: 11px; }

/* Divider */
.footer-divider {
  height: 1px;
  background: rgba(255,255,255,0.15);
  margin-bottom: 32px;
}

/* Columns */
.footer-cols {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr 1fr;
  gap: 32px;
}

.col-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 1.4px;
  color: rgba(255,255,255,0.6);
  margin-bottom: 20px;
  text-transform: uppercase;
}

.contact-line {
  font-size: 17px;
  color: rgba(255,255,255,0.85);
  line-height: 2;
}

.footer-col ul { list-style: none; }
.footer-col li { margin-bottom: 13px; }
.footer-col a {
  font-size: 17px;
  color: rgba(255,255,255,0.85);
  transition: color var(--transition);
}
.footer-col a:hover { color: #E8D5A8; }

/* Social */
.social-links { display: flex; gap: 10px; margin-top: 4px; }

.social-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.8);
  transition: all var(--transition);
}
.social-btn:hover {
  border-color: white;
  color: white;
  background: rgba(255,255,255,0.1);
}
.social-btn svg { width: 16px; height: 16px; }
</style>
