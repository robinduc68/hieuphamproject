import { createApp }    from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia }  from 'pinia'
import App              from './App.vue'
import HomeView         from './views/HomeView.vue'
import AboutView        from './views/AboutView.vue'
import ProductDetailView from './views/ProductDetailView.vue'
import CheckoutView     from './views/CheckoutView.vue'
import ShopView         from './views/ShopView.vue'
import FabricView       from './views/FabricView.vue'
import FaqView          from './views/FaqView.vue'
import NewsView         from './views/NewsView.vue'
import NewsDetailView   from './views/NewsDetailView.vue'
import '@/assets/base.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',               component: HomeView,          name: 'home' },
    { path: '/ve-chung-toi',   component: AboutView,         name: 'about' },
    { path: '/cua-hang',       component: ShopView,          name: 'shop' },
    { path: '/lua-to-tam',     component: FabricView,        name: 'fabric' },
    { path: '/faq',            component: FaqView,           name: 'faq' },
    { path: '/tin-tuc',           component: NewsView,          name: 'news' },
    { path: '/tin-tuc/:slug',     component: NewsDetailView,    name: 'news-detail' },
    { path: '/san-pham/:slug', component: ProductDetailView, name: 'product-detail' },
    { path: '/thanh-toan',     component: CheckoutView,      name: 'checkout' },
    { path: '/danh-muc/:slug', redirect: to => ({ name: 'shop', query: { category: to.params.slug } }) },
  ],
  scrollBehavior: () => ({ top: 0, behavior: 'smooth' }),
})

const pinia = createPinia()
const app   = createApp(App)

app.use(pinia)
app.use(router)
app.mount('#app')
