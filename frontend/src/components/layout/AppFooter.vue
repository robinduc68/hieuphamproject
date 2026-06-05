<template>
  <footer class="app-footer">
    <div class="footer-wrap">
      <!-- Top row: Logo + tagline + CTA -->
      <div class="footer-top">
        <div class="footer-brand">
          <div class="footer-logo">
            <svg viewBox="0 0 48 48" fill="none" class="footer-badge">
              <circle cx="24" cy="24" r="22" stroke="white" stroke-width="1.2"/>
              <text x="24" y="31" text-anchor="middle" font-family="Great Vibes, cursive" font-size="22" fill="white">H</text>
            </svg>
            <div class="footer-logo-text">
              <span class="footer-brand-script">Hà Hoạt</span>
              <span class="footer-brand-sub">Silk</span>
            </div>
          </div>
          <p class="footer-tagline">
            <em>Lụa tơ tằm NhaXá cao cấp</em>
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

.footer-badge { width: 40px; height: 40px; }

.footer-logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1;
}

.footer-brand-script {
  font-family: var(--font-script);
  font-size: 34px;
  color: white;
  line-height: 1.0;
}

.footer-brand-sub {
  font-family: var(--font-display);
  font-size: 11px;
  font-style: italic;
  color: rgba(255,255,255,0.75);
  letter-spacing: 3px;
  text-align: right;
}

.footer-tagline {
  font-family: var(--font-script);
  font-size: 30px;
  color: rgba(255,255,255,0.95);
  font-style: normal;
}

/* CTA button */
.footer-cta {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  border: 1.5px solid rgba(255,255,255,0.75);
  border-radius: 40px;
  padding: 13px 32px;
  font-size: 13px;
  font-weight: 500;
  color: white;
  transition: all var(--transition);
  white-space: nowrap;
}
.footer-cta:hover {
  background: rgba(255,255,255,0.1);
  border-color: white;
}
.footer-cta svg { width: 20px; height: 10px; }

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
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  color: rgba(255,255,255,0.55);
  margin-bottom: 18px;
  text-transform: uppercase;
}

.contact-line {
  font-size: 13px;
  color: rgba(255,255,255,0.85);
  line-height: 2;
}

.footer-col ul { list-style: none; }
.footer-col li { margin-bottom: 12px; }
.footer-col a {
  font-size: 13px;
  color: rgba(255,255,255,0.85);
  transition: color var(--transition);
}
.footer-col a:hover { color: white; }

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
