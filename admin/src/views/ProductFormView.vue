<template>
  <div>
    <div class="page-header">
      <div>
        <div class="page-title">{{ isEdit ? 'Chỉnh sửa sản phẩm' : 'Thêm sản phẩm mới' }}</div>
        <div class="page-sub">{{ isEdit ? `ID: ${productId}` : 'Điền thông tin sản phẩm' }}</div>
      </div>
      <RouterLink to="/products" class="btn btn-secondary">← Quay lại</RouterLink>
    </div>

    <div v-if="loading" class="card empty-state">Đang tải...</div>

    <div v-else class="form-layout">

      <!-- ── Cột trái ── -->
      <div class="form-main">

        <!-- Thông tin cơ bản -->
        <div class="card form-section">
          <div class="section-title">Thông tin cơ bản</div>
          <div class="form-group">
            <label class="form-label">Tên sản phẩm *</label>
            <input v-model="form.name" class="form-input" placeholder="VD: Áo dài lụa tơ tằm..." @input="autoSlug" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Slug *</label>
              <input v-model="form.slug" class="form-input" placeholder="ao-dai-lua-to-tam" />
              <span class="form-hint">URL thân thiện, không dấu, dùng dấu -</span>
            </div>
            <div class="form-group">
              <label class="form-label">Giá (VNĐ) *</label>
              <input v-model.number="form.price" type="number" min="0" class="form-input" placeholder="5000000" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Giá gốc / Giá so sánh (VNĐ)</label>
            <input v-model.number="form.compare_at_price" type="number" min="0" class="form-input" placeholder="Để trống nếu không khuyến mãi" />
            <span class="form-hint">Hiển thị gạch ngang nếu đang sale</span>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Danh mục *</label>
              <select v-model="form.category_id" class="form-select" @change="onCategoryChange">
                <option value="">Chọn danh mục</option>
                <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
              </select>
              <span v-if="!categories.length" class="form-hint" style="color:var(--brand)">
                Chưa có danh mục nào — vào trang Danh mục tạo trước.
              </span>
              <span v-else class="form-hint">Quyết định sản phẩm nằm ở mục nào trên website</span>
            </div>
            <div class="form-group">
              <label class="form-label">Danh mục con{{ subcategories.length ? ' *' : '' }}</label>
              <select v-model="form.subcategory_id" class="form-select" :disabled="!subcategories.length">
                <option value="">{{ form.category_id ? 'Chọn danh mục con' : 'Chọn danh mục trước' }}</option>
                <option v-for="s in subcategories" :key="s.id" :value="s.id">{{ s.name }}</option>
              </select>
              <span class="form-hint">
                {{ !form.category_id
                    ? 'Chọn danh mục ở ô bên trái trước'
                    : (subcategories.length
                        ? 'Danh mục này có mục con — phải chọn một mục.'
                        : 'Danh mục này không có mục con.') }}
              </span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Mô tả</label>
            <RichTextEditor v-model="form.description" placeholder="Mô tả sản phẩm — có thể thêm tiêu đề H1/H2, in đậm, in nghiêng và chèn ảnh..." :min-height="180" />
            <span class="form-hint">Dùng thanh công cụ để thêm tiêu đề, in đậm/nghiêng, danh sách, liên kết và ảnh.</span>
          </div>
        </div>

        <!-- Chi tiết -->
        <div class="card form-section">
          <div class="section-title">Chi tiết sản phẩm</div>
          <div class="form-group">
            <label class="form-label">Chất liệu vải</label>
            <RichTextEditor v-model="form.fabric" placeholder="Lụa tơ tằm 100%..." :min-height="110" />
          </div>
          <div class="form-group">
            <label class="form-label">Hướng dẫn bảo quản</label>
            <RichTextEditor v-model="form.care_instructions" placeholder="Giặt tay, không vắt..." :min-height="110" />
          </div>
          <div class="form-group">
            <label class="form-label">Thông tin giao hàng</label>
            <RichTextEditor v-model="form.shipping_info" placeholder="Giao hàng 3-5 ngày..." :min-height="110" />
          </div>
        </div>

        <!-- Thông số vải (chỉ hiện với sản phẩm vải) -->
        <div v-if="isFabric" class="card form-section">
          <div class="section-title">Thông số vải</div>
          <div class="create-note" style="margin-bottom:16px">
            🧵 Sản phẩm loại <strong>Vải</strong> dùng trang chi tiết riêng ngoài website:
            bán theo đơn vị (mét), không có chọn size / hình thức may.
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Mã sản phẩm</label>
              <input v-model="form.sku_code" class="form-input" placeholder="VD: TD01" />
            </div>
            <div class="form-group">
              <label class="form-label">Khổ vải</label>
              <input v-model="form.fabric_width" class="form-input" placeholder="VD: 90cm" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Quy cách</label>
              <input v-model="form.specification" class="form-input" placeholder="VD: 100% Tơ Tằm (Chi Số Tơ 32-33)" />
            </div>
            <div class="form-group">
              <label class="form-label">Đơn vị bán</label>
              <input v-model="form.unit_label" class="form-input" placeholder="mét" />
              <span class="form-hint">Hiện dưới giá: “Đơn giá trên 1 {{ form.unit_label || 'mét' }} vải”</span>
            </div>
          </div>

          <div class="section-title" style="margin-top:22px">Bộ lọc ngoài website</div>
          <div class="create-note" style="margin-bottom:16px">
            🔎 Ba ô dưới đây quyết định sản phẩm có hiện ra khi khách lọc ở sidebar
            trang <strong>Lụa Nha Xá thông dụng</strong> / <strong>100% tơ tằm</strong> hay không.
            Bỏ trống = sản phẩm bị ẩn khi khách bật bộ lọc tương ứng.
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">Họa tiết</label>
              <input v-model="form.pattern" class="form-input" list="pattern-options" placeholder="VD: Thọ Dơi" />
              <datalist id="pattern-options">
                <option v-for="p in PATTERNS" :key="p" :value="p" />
              </datalist>
              <span class="form-hint">
                Chọn trong gợi ý để khớp với bộ lọc “HỌA TIẾT”. Gõ tên mới cũng được — tên mới sẽ
                tự xuất hiện thành một mục lọc ngoài website.
              </span>
            </div>
            <div class="form-group">
              <label class="form-label">Tone màu</label>
              <select v-model="form.color_tag" class="form-select">
                <option value="">— Không chọn —</option>
                <option v-for="c in COLOR_TAGS" :key="c.name" :value="c.name">{{ c.name }}</option>
              </select>
              <span class="form-hint">Khớp với ô màu ở bộ lọc “MÀU SẮC” của cả hai trang vải.</span>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Loại lụa</label>
            <select v-model="form.silk_type" class="form-select">
              <option value="">— Không chọn —</option>
              <option v-for="t in SILK_TYPES" :key="t" :value="t">{{ t }}</option>
            </select>
            <span class="form-hint">
              Chỉ dùng cho bộ lọc của trang <strong>Lụa Nha Xá 100% tơ tằm</strong>
              (sản phẩm thuộc danh mục con đó).
            </span>
          </div>
        </div>

        <!-- Quản lý ảnh -->
        <div class="card form-section">
          <div class="section-title">Quản lý ảnh</div>

          <div v-if="!isEdit" class="create-note">
            💡 Lưu sản phẩm trước, sau đó bạn sẽ được chuyển sang trang chỉnh sửa để upload ảnh.
          </div>

          <template v-else>
            <!-- Danh sách ảnh hiện tại -->
            <template v-if="images.length">
              <div class="reorder-hint">
                ↕ Kéo thả ảnh để đổi thứ tự hiển thị ngoài website (ảnh đầu tiên đứng đầu thư viện).
                <span v-if="savingOrder" class="reorder-saving">Đang lưu thứ tự…</span>
              </div>
              <div class="images-grid">
                <div
                  v-for="(img, i) in images"
                  :key="img.id"
                  class="img-item"
                  :class="{ primary: img.is_primary, dragging: dragIndex === i, 'drop-target': dropIndex === i && dragIndex !== i }"
                  draggable="true"
                  @dragstart="onImgDragStart(i, $event)"
                  @dragover.prevent="onImgDragOver(i)"
                  @drop.prevent="onImgDrop"
                  @dragend="onImgDragEnd"
                >
                  <img :src="img.url" :alt="img.alt_text || ''" draggable="false" />
                  <div class="img-order">{{ i + 1 }}</div>
                  <div class="img-overlay">
                    <button class="img-btn" @click="setPrimary(img)" title="Đặt làm ảnh chính">
                      <svg viewBox="0 0 16 16" fill="currentColor" style="width:13px;height:13px"><path d="M8 1l2 4h4l-3 3 1 5L8 11l-4 2 1-5L2 5h4z"/></svg>
                    </button>
                    <button class="img-btn danger" @click="deleteImage(img)" title="Xoá ảnh">
                      <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" style="width:13px;height:13px"><path d="M2 4h12M5 4V2h6v2M6 7v5M10 7v5M3 4l1 10h8l1-10"/></svg>
                    </button>
                  </div>
                  <div class="img-primary-tag" v-if="img.is_primary">Ảnh chính</div>
                </div>
              </div>
            </template>
            <div v-else class="empty-state" style="padding:24px;font-size:13px">Chưa có ảnh nào</div>

            <!-- Upload -->
            <div class="upload-area" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
              <input ref="fileInput" type="file" accept="image/*" multiple style="display:none" @change="handleFileSelect" />
              <svg viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" style="width:36px;height:36px;color:var(--text-2)"><path d="M24 8v24M12 20l12-12 12 12"/><path d="M8 36h32"/></svg>
              <p>Kéo thả hoặc <strong>click để chọn ảnh</strong></p>
              <p style="font-size:12px;color:var(--text-2)">PNG, JPG, WEBP — tối đa 10MB mỗi ảnh</p>
            </div>

            <div v-if="uploading" class="upload-progress">
              Đang upload {{ uploadProgress }}...
            </div>
          </template>
        </div>

        <!-- Kích thước -->
        <div class="card form-section">
          <div class="section-title">Kích thước</div>

          <div v-if="!isEdit" class="create-note">
            💡 Lưu sản phẩm trước, sau đó bạn có thể thêm kích thước.
          </div>

          <template v-else>
            <div class="sizes-row" v-if="sizes.length">
              <span v-for="s in sizes" :key="s.id" class="size-chip" :class="{unavailable: !s.in_stock}">
                {{ s.size }}
                <button @click="toggleSize(s)" class="size-toggle" :title="s.in_stock ? 'Tắt' : 'Bật'">{{ s.in_stock ? '✓' : '✕' }}</button>
                <button @click="deleteSize(s)" class="size-del" title="Xoá">×</button>
              </span>
            </div>
            <div v-else style="font-size:13px;color:var(--text-2);margin-bottom:12px">Chưa có size nào</div>

            <div style="display:flex;gap:8px;margin-top:12px">
              <input v-model="newSize" class="form-input" placeholder="VD: S, M, L, 36, 38..." style="max-width:160px" @keyup.enter="addSize" />
              <button class="btn btn-secondary" @click="addSize">Thêm size</button>
            </div>
          </template>
        </div>

      </div>

      <!-- ── Cột phải ── -->
      <div class="form-side">

        <div class="card form-section">
          <div class="section-title">Hiển thị</div>
          <div class="form-group">
            <label class="form-label">Loại sản phẩm</label>
            <select v-model="form.product_type" class="form-select">
              <option value="apparel">Quần áo / phụ kiện</option>
              <option value="fabric">Vải (bán theo mét)</option>
            </select>
            <span class="form-hint">
              Quyết định trang chi tiết ngoài website: <strong>Vải</strong> dùng layout riêng
              (thông số vải, mua theo mét), <strong>Quần áo</strong> có chọn size &amp; hình thức may.
              Tự đặt theo danh mục, có thể sửa lại.
            </span>
          </div>
          <div class="form-group">
            <label class="form-label">Màu chính (HEX)</label>
            <div style="display:flex;gap:8px;align-items:center">
              <input v-model="form.primary_color" type="color" style="width:40px;height:36px;padding:2px;border:1px solid var(--border);border-radius:6px;cursor:pointer" />
              <input v-model="form.primary_color" class="form-input" placeholder="#B8965A" />
            </div>
            <span class="form-hint">
              Màu nền/ô màu của sản phẩm ngoài website (trang chi tiết, giỏ hàng, thanh toán)
              và màu nền ảnh placeholder khi chưa có ảnh thật. Không đổi gì trong trang admin này.
            </span>
          </div>
          <div class="form-group">
            <label class="form-label">Thứ tự hiển thị</label>
            <input v-model.number="form.sort_order" type="number" class="form-input" placeholder="0" />
            <span class="form-hint">
              Số nhỏ đứng trước khi liệt kê ở trang Cửa hàng / danh mục. Bằng nhau thì sản phẩm mới hơn đứng trước.
            </span>
          </div>
        </div>

        <!-- Khoảng giá hiển thị ngoài web -->
        <div class="card form-section">
          <div class="section-title">Giá hiển thị ngoài web</div>
          <div class="price-preview">
            <span class="price-preview-val">{{ pricePreview }}</span>
          </div>
          <p v-if="isFabric" class="form-hint" style="margin-top:10px">
            Sản phẩm vải hiển thị đúng một mức giá — phụ thu tuỳ chỉnh chỉ áp dụng cho quần áo.
          </p>
          <template v-else>
            <p class="form-hint" style="margin-top:10px">
              Không có ô “giá tối đa”: mức cao nhất được cộng tự động từ phụ thu đắt nhất của các nhóm
              tuỳ chỉnh (hình thức may, tà trong, màu sắc). Khách chọn xong tuỳ chọn thì chỉ còn một giá.
            </p>
            <div v-if="maxAdjustment > 0" class="adj-list">
              <div v-for="g in adjustmentBreakdown" :key="g.key" class="adj-row">
                <span>{{ g.label }}</span>
                <span>+{{ formatVnd(g.max) }}</span>
              </div>
            </div>
            <RouterLink to="/customization" class="btn btn-secondary" style="width:100%;justify-content:center;margin-top:12px">
              Sửa mức phụ thu →
            </RouterLink>
          </template>
        </div>

        <div class="card form-section">
          <div class="section-title">Trạng thái</div>
          <label class="toggle-row">
            <span>Hiển thị trên cửa hàng</span>
            <div class="toggle" :class="{on: form.is_active}" @click="form.is_active = !form.is_active" />
          </label>
          <label class="toggle-row">
            <span>Sản phẩm mới</span>
            <div class="toggle" :class="{on: form.is_new}" @click="form.is_new = !form.is_new" />
          </label>
          <label class="toggle-row">
            <span>Nổi bật</span>
            <div class="toggle" :class="{on: form.is_featured}" @click="form.is_featured = !form.is_featured" />
          </label>
        </div>

        <div v-if="saveError" class="error-box">{{ saveError }}</div>

        <button class="btn btn-primary" style="width:100%;justify-content:center;padding:12px" @click="save" :disabled="saving">
          {{ saving ? 'Đang lưu...' : (isEdit ? 'Lưu thay đổi' : 'Tạo sản phẩm') }}
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productsApi, categoriesApi, customizationApi } from '@/api/index.js'
import { useToastStore } from '@/stores/toast.js'
import RichTextEditor from '@/components/RichTextEditor.vue'
import { PATTERNS, COLOR_TAGS, SILK_TYPES } from '@/data/fabricOptions.js'
import { toSlug } from '@/utils/slug.js'

const route  = useRoute()
const router = useRouter()
const toast  = useToastStore()

const productId = computed(() => route.params.id)
const isEdit    = computed(() => !!productId.value)

const loading        = ref(false)
const saving         = ref(false)
const saveError      = ref('')
const uploading      = ref(false)
const uploadProgress = ref('')
const fileInput      = ref(null)

const images    = ref([])
const sizes     = ref([])
const categories = ref([])
const newSize   = ref('')

const form = ref({
  name: '', slug: '', price: null, compare_at_price: null,
  description: '', fabric: '', care_instructions: '', shipping_info: '',
  category_id: '', subcategory_id: '', primary_color: '', sort_order: 0,
  is_active: true, is_new: false, is_featured: false,
  product_type: 'apparel', sku_code: '', specification: '', fabric_width: '', unit_label: '',
  pattern: '', color_tag: '', silk_type: '',
})

const isFabric = computed(() => form.value.product_type === 'fabric')

// Danh mục con của danh mục đang chọn
const subcategories = computed(() => {
  const cat = categories.value.find(c => c.id === Number(form.value.category_id))
  return cat?.subcategories ?? []
})

// Slug danh mục vải — khớp với backend (app/routers/products.py FABRIC_CATEGORY_SLUG)
const FABRIC_CATEGORY_SLUG = 'lua-to-tam'

// Đổi danh mục cha thì bỏ danh mục con cũ (tránh gửi lên sub không thuộc cat).
// Gắn vào @change chứ không dùng watch: watch sẽ chạy cả lúc preload form khi sửa
// và xoá mất subcategory_id vừa nạp.
function onCategoryChange() {
  form.value.subcategory_id = ''
  const cat = categories.value.find(c => c.id === Number(form.value.category_id))
  form.value.product_type = cat?.slug === FABRIC_CATEGORY_SLUG ? 'fabric' : 'apparel'
}

// ── Khoảng giá hiển thị ngoài web ─────────────────────────────────────────
// Không có ô "giá tối đa": mức max = giá + phụ thu cao nhất của từng nhóm tuỳ
// chỉnh (quản lý ở trang Tuỳ chỉnh). Hiện ở đây để admin biết web đang show gì.
const customizationGroups = ref([])

const CUSTOMIZATION_GROUP_LABELS = {
  tailoring_method: 'Hình thức may',
  lining_type:      'Tà trong',
  color_option:     'Màu sắc',
}

const adjustmentBreakdown = computed(() =>
  Object.entries(CUSTOMIZATION_GROUP_LABELS).map(([key, label]) => {
    const group = customizationGroups.value.find(g => g.group_key === key)
    const max = group?.options?.length
      ? Math.max(...group.options.map(o => Number(o.price_adjustment) || 0))
      : 0
    return { key, label, max }
  }).filter(g => g.max > 0)
)

const maxAdjustment = computed(() =>
  adjustmentBreakdown.value.reduce((sum, g) => sum + g.max, 0)
)

function formatVnd(n) {
  return Number(n || 0).toLocaleString('vi-VN') + ' đ'
}

const pricePreview = computed(() => {
  const base = Number(form.value.price) || 0
  if (!base) return 'Chưa nhập giá'
  if (isFabric.value || maxAdjustment.value === 0) return formatVnd(base)
  return `${formatVnd(base)} – ${formatVnd(base + maxAdjustment.value)}`
})

let slugTouched = false  // nếu user tự sửa slug thì không auto-gen nữa

function autoSlug() {
  if (!slugTouched) form.value.slug = toSlug(form.value.name)
}

watch(() => form.value.slug, (val, old) => {
  if (val !== toSlug(form.value.name)) slugTouched = true
})

// ── Load data ─────────────────────────────────────────────────────────────
async function loadData() {
  loading.value = true
  saveError.value = ''
  try {
    const cats = await categoriesApi.list()
    categories.value = Array.isArray(cats) ? cats : (cats?.results ?? [])

    try {
      const groups = await customizationApi.listGrouped()
      customizationGroups.value = Array.isArray(groups) ? groups : []
    } catch { /* không lấy được phụ thu → chỉ hiện 1 mức giá */ }

    if (isEdit.value) {
      const p = await productsApi.get(productId.value)
      Object.assign(form.value, {
        name:              p.name,
        slug:              p.slug,
        price:             Number(p.price),
        compare_at_price:  p.compare_at_price ? Number(p.compare_at_price) : null,
        description:       p.description       || '',
        fabric:            p.fabric            || '',
        care_instructions: p.care_instructions || '',
        shipping_info:     p.shipping_info     || '',
        category_id:       p.category_id       || '',
        subcategory_id:    p.subcategory_id    || '',
        primary_color:     p.primary_color     || p.images?.[0]?.color_hex || '',
        sort_order:        p.sort_order        || 0,
        is_active:         p.is_active  ?? true,
        is_new:            p.is_new     ?? false,
        is_featured:       p.is_featured ?? false,
        product_type:      p.product_type  || 'apparel',
        sku_code:          p.sku_code      || '',
        specification:     p.specification || '',
        fabric_width:      p.fabric_width  || '',
        unit_label:        p.unit_label    || '',
        pattern:           p.pattern       || '',
        color_tag:         p.color_tag     || '',
        silk_type:         p.silk_type     || '',
      })
      images.value = p.images || []
      sizes.value  = p.sizes  || []
      slugTouched  = true  // không auto-gen slug khi edit
    }
  } catch (e) {
    toast.error('Lỗi tải dữ liệu: ' + e)
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
watch(() => route.params.id, loadData)

// ── Save ──────────────────────────────────────────────────────────────────
async function save() {
  saveError.value = ''

  if (!form.value.name.trim()) { saveError.value = 'Vui lòng nhập tên sản phẩm.'; return }
  if (!form.value.slug.trim()) { saveError.value = 'Vui lòng nhập slug.'; return }
  if (!form.value.price)       { saveError.value = 'Vui lòng nhập giá.'; return }
  if (!form.value.category_id) {
    saveError.value = 'Vui lòng chọn danh mục — sản phẩm không có danh mục sẽ không hiện ở mục nào trên website.'
    return
  }
  if (subcategories.value.length && !form.value.subcategory_id) {
    saveError.value = 'Danh mục này có danh mục con, vui lòng chọn một danh mục con.'
    return
  }

  saving.value = true
  try {
    const data = { ...form.value }
    if (!data.category_id)      delete data.category_id
    if (!data.subcategory_id)   delete data.subcategory_id
    if (!data.compare_at_price) delete data.compare_at_price

    if (isEdit.value) {
      await productsApi.update(productId.value, data)
      toast.success('Đã lưu thay đổi')
    } else {
      const created = await productsApi.create({ ...data, sizes: [] })
      toast.success('Tạo sản phẩm thành công! Giờ bạn có thể upload ảnh và thêm size.')
      router.push(`/products/${created.id}/edit`)
    }
  } catch (e) {
    saveError.value = typeof e === 'string' ? e : (e?.message || 'Có lỗi xảy ra')
  } finally {
    saving.value = false
  }
}

// ── Upload images ─────────────────────────────────────────────────────────
async function handleFileSelect(e) { await uploadFiles(Array.from(e.target.files)); e.target.value = '' }
async function handleDrop(e) { await uploadFiles(Array.from(e.dataTransfer.files)) }

async function uploadFiles(files) {
  if (!files.length) return
  uploading.value = true
  for (let i = 0; i < files.length; i++) {
    uploadProgress.value = `${i + 1}/${files.length}`
    const fd = new FormData()
    fd.append('file', files[i])
    if (form.value.primary_color) fd.append('color_hex', form.value.primary_color)
    try {
      const img = await productsApi.uploadImage(productId.value, fd)
      images.value.push({
        id: img.id, url: img.url, alt_text: '',
        sort_order: img.position, is_primary: images.value.length === 0,
      })
    } catch (e) { toast.error(`Lỗi upload ảnh: ${e}`) }
  }
  uploading.value = false
  uploadProgress.value = ''
  if (images.value.length) toast.success('Upload ảnh thành công')
}

// ── Kéo thả đổi thứ tự ảnh ────────────────────────────────────────────────
const dragIndex   = ref(null)
const dropIndex   = ref(null)
const savingOrder = ref(false)

function onImgDragStart(i, e) {
  dragIndex.value = i
  e.dataTransfer.effectAllowed = 'move'
  // Firefox chỉ bắt đầu kéo khi dataTransfer có dữ liệu
  e.dataTransfer.setData('text/plain', String(i))
}

function onImgDragOver(i) {
  dropIndex.value = i
}

function onImgDrop() {
  const from = dragIndex.value
  const to   = dropIndex.value
  onImgDragEnd()
  if (from === null || to === null || from === to) return

  const next = [...images.value]
  next.splice(to, 0, next.splice(from, 1)[0])
  images.value = next
  persistImageOrder()
}

function onImgDragEnd() {
  dragIndex.value = null
  dropIndex.value = null
}

async function persistImageOrder() {
  savingOrder.value = true
  const payload = images.value.map((img, i) => ({ id: img.id, sort_order: i }))
  try {
    await productsApi.reorderImages(productId.value, payload)
    images.value.forEach((img, i) => { img.sort_order = i; img.position = i })
  } catch (e) {
    toast.error('Không lưu được thứ tự ảnh: ' + e)
    await loadData()   // nạp lại thứ tự thật từ server
  } finally {
    savingOrder.value = false
  }
}

async function setPrimary(img) {
  try {
    await productsApi.updateImage(productId.value, img.id, { is_primary: true })
    images.value.forEach(i => i.is_primary = (i.id === img.id))
  } catch (e) { toast.error(String(e)) }
}

async function deleteImage(img) {
  if (!confirm('Xoá ảnh này?')) return
  try {
    await productsApi.deleteImage(productId.value, img.id)
    images.value = images.value.filter(i => i.id !== img.id)
  } catch (e) { toast.error(String(e)) }
}

// ── Sizes ─────────────────────────────────────────────────────────────────
async function addSize() {
  const sz = newSize.value.trim().toUpperCase()
  if (!sz) return
  try {
    const s = await productsApi.addSize(productId.value, { size: sz })
    sizes.value.push(s)
    newSize.value = ''
  } catch (e) { toast.error(String(e)) }
}

async function toggleSize(s) {
  try {
    const updated = await productsApi.updateSize(productId.value, s.id, { is_available: !s.in_stock })
    s.in_stock = updated.in_stock
  } catch (e) { toast.error(String(e)) }
}

async function deleteSize(s) {
  try {
    await productsApi.deleteSize(productId.value, s.id)
    sizes.value = sizes.value.filter(x => x.id !== s.id)
  } catch (e) { toast.error(String(e)) }
}
</script>

<style scoped>
.form-layout { display: flex; gap: 20px; align-items: flex-start; }
.form-main   { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 16px; }
.form-side   { width: 280px; flex-shrink: 0; display: flex; flex-direction: column; gap: 16px; }

.form-section  { padding: 20px; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.form-row      { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }

.create-note {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 13px;
  color: #1d4ed8;
}

/* Images */
.reorder-hint {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  font-size: 12px; color: var(--text-2); margin-bottom: 10px;
}
.reorder-saving { color: var(--brand); font-weight: 500; }

.images-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 16px; }
.img-item { position: relative; aspect-ratio: 3/4; border-radius: 8px; overflow: hidden; border: 2px solid transparent; cursor: grab; }
.img-item:active { cursor: grabbing; }
.img-item.dragging { opacity: .4; }
.img-item.drop-target { border-color: var(--blue); }
.img-order {
  position: absolute; top: 6px; left: 6px; z-index: 2;
  min-width: 20px; height: 20px; padding: 0 5px;
  border-radius: 10px; background: rgba(0,0,0,.6); color: #fff;
  font-size: 11px; font-weight: 600; line-height: 20px; text-align: center;
}

/* Giá hiển thị */
.price-preview {
  background: var(--bg); border: 1px solid var(--border); border-radius: 6px;
  padding: 12px 14px; text-align: center;
}
.price-preview-val { font-size: 15px; font-weight: 600; color: var(--brand); }
.adj-list { margin-top: 12px; border-top: 1px solid var(--border); padding-top: 10px; }
.adj-row {
  display: flex; justify-content: space-between; gap: 8px;
  font-size: 12px; color: var(--text-2); padding: 3px 0;
}
.img-item.primary { border-color: var(--brand); }
.img-item img { width: 100%; height: 100%; object-fit: cover; display: block; }
.img-overlay {
  position: absolute; inset: 0; background: rgba(0,0,0,.5);
  display: flex; align-items: center; justify-content: center; gap: 8px;
  opacity: 0; transition: opacity .2s;
}
.img-item:hover .img-overlay { opacity: 1; }
.img-btn { width: 32px; height: 32px; border-radius: 50%; border: none; background: rgba(255,255,255,.9); color: var(--text); cursor: pointer; display: flex; align-items: center; justify-content: center; }
.img-btn.danger { color: #DC2626; }
.img-primary-tag { position: absolute; bottom: 0; left: 0; right: 0; background: var(--brand); color: #fff; font-size: 10px; font-weight: 600; text-align: center; padding: 3px; }

.upload-area {
  border: 2px dashed var(--border);
  border-radius: 8px;
  padding: 28px;
  text-align: center;
  cursor: pointer;
  transition: border-color .2s;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.upload-area:hover { border-color: var(--brand); }
.upload-area p { font-size: 13px; color: var(--text); margin: 0; }

.upload-progress { margin-top: 10px; font-size: 13px; color: var(--text-2); }

/* Sizes */
.sizes-row { display: flex; flex-wrap: wrap; gap: 8px; }
.size-chip {
  display: flex; align-items: center; gap: 4px;
  padding: 6px 10px; border-radius: 6px;
  background: var(--bg); border: 1px solid var(--border);
  font-size: 13px; font-weight: 500;
}
.size-chip.unavailable { opacity: .5; text-decoration: line-through; }
.size-toggle, .size-del {
  background: none; border: none; cursor: pointer;
  font-size: 12px; color: var(--text-2); padding: 0 2px; line-height: 1;
}
.size-toggle:hover { color: #16a34a; }
.size-del:hover    { color: #DC2626; }

/* Toggle */
.toggle-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid var(--border); cursor: pointer; font-size: 13px; }
.toggle-row:last-child { border-bottom: none; }
.toggle { width: 36px; height: 20px; border-radius: 10px; background: #D1D5DB; position: relative; transition: background .2s; flex-shrink: 0; }
.toggle.on { background: var(--brand); }
.toggle::after { content: ''; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; border-radius: 50%; background: #fff; transition: transform .2s; }
.toggle.on::after { transform: translateX(16px); }

.error-box { background: #fef2f2; color: #dc2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; }

@media (max-width: 900px) {
  .form-layout { flex-direction: column; }
  .form-side { width: 100%; }
  .images-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
