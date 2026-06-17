<template>
  <div class="about-page">
    <div class="contact-box">
      <h2 class="contact-title">Liên hệ với Hà Hoạt Silk</h2>

      <div class="contact-cards">
        <!-- Zalo -->
        <a href="https://zalo.me/0866666201" target="_blank" class="contact-card">
          <div class="contact-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="48" height="48" rx="10" fill="#0068FF"/>
              <text x="24" y="34" text-anchor="middle"
                font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="#fff">Z</text>
            </svg>
          </div>
          <p class="card-name">Hà Hoạt Silk</p>
          <p class="card-sub">(08 66666 201)</p>
        </a>

        <!-- Messenger -->
        <a href="https://m.me/hahoatsilk" target="_blank" class="contact-card">
          <div class="contact-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <linearGradient id="msg-grad" x1="0" y1="48" x2="48" y2="0" gradientUnits="userSpaceOnUse">
                  <stop offset="0%" stop-color="#0099FF"/>
                  <stop offset="100%" stop-color="#A033FF"/>
                </linearGradient>
              </defs>
              <rect width="48" height="48" rx="10" fill="url(#msg-grad)"/>
              <path d="M24 8C15.16 8 8 14.71 8 23c0 4.5 1.9 8.55 4.97 11.43V39l4.86-2.67A16.8 16.8 0 0024 38c8.84 0 16-6.71 16-15S32.84 8 24 8zm1.6 20.2l-4.07-4.34-7.95 4.34 8.74-9.28 4.17 4.34 7.85-4.34-8.74 9.28z" fill="#fff"/>
            </svg>
          </div>
          <p class="card-name">Hà Hoạt Silk - Lụa tơ tằm</p>
          <p class="card-sub">Nhà Xá cao cấp</p>
        </a>
      </div>

      <div class="social-links">
        <a href="https://facebook.com/hahoatsilk" target="_blank" class="social-btn" aria-label="Facebook">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/>
          </svg>
        </a>
        <a href="https://tiktok.com/@hahoatsilk" target="_blank" class="social-btn" aria-label="TikTok">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1V9.01a6.33 6.33 0 00-.79-.05 6.34 6.34 0 00-6.34 6.34 6.34 6.34 0 006.34 6.34 6.34 6.34 0 006.33-6.34V8.75a8.18 8.18 0 004.78 1.52V6.82a4.85 4.85 0 01-1.01-.13z"/>
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.about-page {
  background: var(--bg-gray);
  padding: 100px 24px 48px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.contact-box {
  background: #fff;
  border-radius: 16px;
  padding: 40px 56px;
  text-align: center;
  width: 100%;
  max-width: 660px;
}

.contact-title {
  font-family: var(--font-body);
  font-size: 22px;
  font-weight: 600;
  color: var(--charcoal);
  margin-bottom: 28px;
}

.contact-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.contact-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 24px 16px;
  border: 1.5px solid var(--border);
  border-radius: 12px;
  text-decoration: none;
  transition: box-shadow var(--transition);
}
.contact-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,.08); }

.contact-icon svg {
  width: 52px;
  height: 52px;
}

.card-name {
  font-family: var(--font-body);
  font-size: 14px;
  font-weight: 600;
  color: var(--brand-red);
  text-align: center;
  line-height: 1.5;
}
.card-sub {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--brand-red);
  text-align: center;
  line-height: 1.5;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 14px;
}

.social-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1.5px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--charcoal);
  transition: border-color var(--transition), color var(--transition);
}
.social-btn:hover { border-color: var(--charcoal); color: var(--brand-red); }
.social-btn svg { width: 17px; height: 17px; }
</style>
