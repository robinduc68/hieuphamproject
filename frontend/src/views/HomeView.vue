<template>
  <main>
    <!-- Lớp nền fixed chung: 3 section đổi màu sẽ animate lên đây → không bao giờ lộ đường nối -->
    <div class="page-bg" data-page-bg aria-hidden="true"></div>
    <HeroSection />
    <ModernHeritage />
    <MasterCraft />
    <FabricShowcase />
    <NewArrivals />
    <QuoteSection />
    <CollectionsGrid />
    <IconicProducts />
  </main>
</template>

<script setup>
import HeroSection    from '@/components/home/HeroSection.vue'
import ModernHeritage from '@/components/home/ModernHeritage.vue'
import MasterCraft    from '@/components/home/MasterCraft.vue'
import FabricShowcase from '@/components/home/FabricShowcase.vue'
import NewArrivals    from '@/components/home/NewArrivals.vue'
import QuoteSection   from '@/components/home/QuoteSection.vue'
import CollectionsGrid from '@/components/home/CollectionsGrid.vue'
import IconicProducts from '@/components/home/IconicProducts.vue'
</script>

<style scoped>
/* Lớp nền chung fixed – nằm sau mọi content (z-index:-1).
   Trong suốt tại 3 section đổi màu → hiện lớp này liên tục, không đường nối. */
.page-bg {
  position: fixed;
  inset: 0;
  z-index: -1;
  background: var(--bg-gray);
  pointer-events: none;
}
</style>
