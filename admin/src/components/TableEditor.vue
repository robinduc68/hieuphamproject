<template>
  <div class="tbl-editor">
    <div class="tbl-scroll">
      <table class="tbl">
        <thead>
          <tr>
            <th class="row-num">#</th>
            <th v-for="(col, ci) in columns" :key="ci">
              <div class="th-cell">
                <input
                  class="cell-input head"
                  :value="col"
                  :placeholder="`Cột ${ci + 1}`"
                  @input="setColumn(ci, $event.target.value)"
                />
                <button
                  class="mini-btn danger"
                  title="Xoá cột"
                  :disabled="columns.length <= 1"
                  @click="removeColumn(ci)"
                >✕</button>
              </div>
            </th>
            <th class="row-act"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, ri) in rows" :key="ri">
            <td class="row-num">{{ ri + 1 }}</td>
            <td v-for="(col, ci) in columns" :key="ci">
              <input
                class="cell-input"
                :value="row[ci] ?? ''"
                @input="setCell(ri, ci, $event.target.value)"
              />
            </td>
            <td class="row-act">
              <button class="mini-btn" title="Lên"  :disabled="ri === 0"               @click="moveRow(ri, -1)">↑</button>
              <button class="mini-btn" title="Xuống" :disabled="ri === rows.length - 1" @click="moveRow(ri, 1)">↓</button>
              <button class="mini-btn danger" title="Xoá dòng" @click="removeRow(ri)">✕</button>
            </td>
          </tr>
          <tr v-if="!rows.length">
            <td :colspan="columns.length + 2" class="tbl-empty">Chưa có dòng nào — bấm “+ Thêm dòng”.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="tbl-actions">
      <button class="btn btn-secondary btn-sm" @click="addRow">+ Thêm dòng</button>
      <button class="btn btn-secondary btn-sm" @click="addColumn">+ Thêm cột</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// modelValue = { columns: [...], rows: [[...], ...] }
const props = defineProps({
  modelValue: { type: Object, default: () => ({ columns: [], rows: [] }) },
})
const emit = defineEmits(['update:modelValue'])

const columns = computed(() => props.modelValue?.columns ?? [])
const rows    = computed(() => props.modelValue?.rows ?? [])

function update(columnsNext, rowsNext) {
  emit('update:modelValue', { columns: columnsNext, rows: rowsNext })
}

function setColumn(ci, value) {
  const next = [...columns.value]
  next[ci] = value
  update(next, rows.value)
}

function setCell(ri, ci, value) {
  const next = rows.value.map(r => [...r])
  next[ri][ci] = value
  update(columns.value, next)
}

function addRow() {
  update(columns.value, [...rows.value, columns.value.map(() => '')])
}

function removeRow(ri) {
  update(columns.value, rows.value.filter((_, i) => i !== ri))
}

function moveRow(ri, delta) {
  const next = rows.value.map(r => [...r])
  const [moved] = next.splice(ri, 1)
  next.splice(ri + delta, 0, moved)
  update(columns.value, next)
}

function addColumn() {
  update([...columns.value, ''], rows.value.map(r => [...r, '']))
}

function removeColumn(ci) {
  update(
    columns.value.filter((_, i) => i !== ci),
    rows.value.map(r => r.filter((_, i) => i !== ci)),
  )
}
</script>

<style scoped>
.tbl-editor { border: 1px solid var(--border); border-radius: 8px; overflow: hidden; background: #fff; }
.tbl-scroll { overflow-x: auto; }
.tbl { width: 100%; border-collapse: collapse; font-size: 13px; }
.tbl th, .tbl td { border-bottom: 1px solid var(--border); border-right: 1px solid var(--border); padding: 0; }
.tbl th:last-child, .tbl td:last-child { border-right: none; }
.tbl thead th { background: #FAFBFC; }

.th-cell { display: flex; align-items: center; }
.cell-input {
  width: 100%; min-width: 92px; padding: 8px 10px;
  border: none; outline: none; background: transparent;
  font-size: 13px; color: var(--text);
}
.cell-input:focus { background: #F0F6FF; }
.cell-input.head { font-weight: 600; }

.row-num {
  width: 34px; text-align: center; color: var(--text-2);
  font-size: 12px; background: #FAFBFC; padding: 8px 0;
}
.row-act { width: 96px; white-space: nowrap; text-align: center; padding: 0 4px; }

.mini-btn {
  border: none; background: none; color: var(--text-2);
  padding: 4px 5px; border-radius: 4px; font-size: 12px; line-height: 1;
}
.mini-btn:hover:not(:disabled) { background: #EEF1F4; color: var(--text); }
.mini-btn.danger:hover:not(:disabled) { background: #FEF2F2; color: #DC2626; }
.mini-btn:disabled { opacity: .3; cursor: default; }

.tbl-empty { padding: 16px; text-align: center; color: var(--text-2); font-size: 13px; }
.tbl-actions { display: flex; gap: 8px; padding: 10px; background: #FAFBFC; border-top: 1px solid var(--border); }

@media (max-width: 760px) {
  .tbl-scroll { -webkit-overflow-scrolling: touch; }
  .tbl { min-width: 520px; }
  .tbl-actions { flex-wrap: wrap; }
  .tbl-actions .btn { flex: 1; justify-content: center; }
}
</style>
