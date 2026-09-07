<template>
  <div class="card no-access">
    <div class="no-access-icon">🔒</div>
    <div class="no-access-title">Bạn không có quyền vào mục này</div>
    <p class="no-access-text">
      Tài khoản <strong>{{ auth.user?.email }}</strong>
      <template v-if="auth.user?.role_name"> đang ở vai trò <strong>{{ auth.user.role_name }}</strong></template>
      <template v-else> chưa được gán vai trò nào</template>.
      Liên hệ quản trị viên để được cấp thêm quyền.
    </p>
    <RouterLink v-if="home" :to="home" class="btn btn-secondary">← Về mục bạn được xem</RouterLink>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth.js'
import { firstAllowedPath } from '@/router/index.js'

const auth = useAuthStore()
const home = computed(() => firstAllowedPath(auth))
</script>

<style scoped>
.no-access {
  padding: 60px 24px;
  display: flex; flex-direction: column; align-items: center; gap: 12px;
  text-align: center;
}
.no-access-icon  { font-size: 34px; }
.no-access-title { font-size: 16px; font-weight: 600; }
.no-access-text  { font-size: 13px; color: var(--text-2); max-width: 460px; line-height: 1.7; }
</style>
