import { ref } from 'vue'

/**
 * Carousel VÔ TẬN (seamless infinite loop).
 *
 * Nguyên lý:
 *  - Component render danh sách item LẶP 2 LẦN (real + clone) nên khi cuộn
 *    hết phần thật sẽ trượt mượt sang phần clone (giống hệt phần thật).
 *  - Khi đã vào nửa clone, ta "snap" (bỏ transition) về vị trí tương đương
 *    ở nửa thật → người dùng không thấy nhảy.
 *
 * Component cần:
 *  - `:class="{ 'no-anim': !animate }"` trên phần tử track.
 *  - `transform: translateX(-${currentIndex * step}px)` với step = itemWidth + gap.
 *  - CSS `.no-anim { transition: none; }`.
 *  - Render item 2× (vd: `[...items, ...items]`).
 *
 * @param {() => number} getCount  Trả về số item THẬT (N).
 * @param {() => number} getStep   Trả về bước dịch px (= itemWidth + gap).
 * @param {{ duration?: number }} [opts]  duration = thời gian transition (ms) + đệm.
 */
export function useInfiniteCarousel(getCount, getStep, opts = {}) {
  const duration = opts.duration ?? 570

  const currentIndex = ref(0)
  const animate      = ref(true)
  let   locked       = false

  /** Force paint trạng thái "không animation" trước khi bật lại transition */
  function paintThen(cb) {
    requestAnimationFrame(() => requestAnimationFrame(cb))
  }

  /** Sau khi transition kết thúc: snap vô hình về nửa thật nếu cần, rồi mở khoá */
  function releaseAfterSnap() {
    setTimeout(() => {
      const n = getCount()
      if (currentIndex.value >= n) {
        animate.value = false
        currentIndex.value -= n
        paintThen(() => {
          animate.value = true
          locked = false
        })
      } else {
        locked = false
      }
    }, duration)
  }

  function next() {
    if (locked) return
    animate.value = true
    currentIndex.value += 1
    locked = true
    releaseAfterSnap()
  }

  function prev() {
    if (locked) return
    const n = getCount()

    // Đang ở item đầu tiên: nhảy (không anim) tới clone[0], rồi trượt tới clone[last]
    if (currentIndex.value <= 0) {
      locked = true
      animate.value = false
      currentIndex.value = n
      paintThen(() => {
        animate.value = true
        currentIndex.value = n - 1
        releaseAfterSnap() // currentIndex = n-1 < n → chỉ mở khoá
      })
      return
    }

    animate.value = true
    currentIndex.value -= 1
    locked = true
    releaseAfterSnap()
  }

  /** Về đầu, không animation (dùng khi resize / đổi cấu hình) */
  function reset() {
    locked = false
    animate.value = false
    currentIndex.value = 0
    paintThen(() => { animate.value = true })
  }

  return { currentIndex, animate, next, prev, reset }
}
