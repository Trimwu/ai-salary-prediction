<template>
  <div class="app-wrapper">
    <!-- 背景粒子装饰 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="main-container">
      <!-- Header -->
      <header class="app-header">
        <div class="header-icon">🤖</div>
        <div class="header-text">
          <h1>AI 薪资预测系统</h1>
          <p>基于机器学习 · 多维度分析 · 精准预测</p>
        </div>
        <div class="header-badge">
          <el-tag type="success" effect="dark" size="large">
            <el-icon><CircleCheck /></el-icon> 模型已就绪
          </el-tag>
        </div>
      </header>

      <!-- 统计卡片 -->
      <div class="stats-row" v-if="stats">
        <div class="stat-card" v-for="item in statsCards" :key="item.label">
          <div class="stat-icon">{{ item.icon }}</div>
          <div class="stat-info">
            <div class="stat-value">{{ item.value }}</div>
            <div class="stat-label">{{ item.label }}</div>
          </div>
        </div>
      </div>

      <!-- 主内容区 -->
      <div class="content-grid">
        <!-- 左侧：输入表单 -->
        <div class="card form-card">
          <div class="card-title">
            <el-icon><Setting /></el-icon>
            <span>输入预测参数</span>
          </div>

          <el-form :model="form" label-position="top" class="predict-form" :disabled="loading">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="职位方向">
                  <el-select v-model="form.position" placeholder="选择职位" size="large" style="width:100%">
                    <el-option v-for="p in options.positions" :key="p" :label="p" :value="p" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="最高学历">
                  <el-select v-model="form.education" placeholder="选择学历" size="large" style="width:100%">
                    <el-option v-for="e in options.educations" :key="e" :label="e" :value="e" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="目标城市">
                  <el-select v-model="form.city" placeholder="选择城市" size="large" style="width:100%">
                    <el-option v-for="c in options.cities" :key="c" :label="c" :value="c" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="行业领域">
                  <el-select v-model="form.industry" placeholder="选择行业" size="large" style="width:100%">
                    <el-option v-for="i in options.industries" :key="i" :label="i" :value="i" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item label="公司规模">
              <el-select v-model="form.company_size" placeholder="选择规模" size="large" style="width:100%">
                <el-option v-for="s in options.company_sizes" :key="s" :label="s" :value="s" />
              </el-select>
            </el-form-item>

            <el-form-item :label="`工作年限：${form.experience} 年`">
              <el-slider
                v-model="form.experience"
                :min="0" :max="20" :step="1"
                show-stops
                :marks="{ 0: '应届', 3: '3年', 5: '5年', 10: '10年', 20: '20年' }"
                class="exp-slider"
              />
            </el-form-item>

            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handlePredict"
              class="predict-btn"
              :disabled="!isFormValid"
            >
              <el-icon v-if="!loading"><MagicStick /></el-icon>
              {{ loading ? '预测中...' : '开始预测' }}
            </el-button>
          </el-form>
        </div>

        <!-- 右侧：结果展示 -->
        <div class="card result-card">
          <div class="card-title">
            <el-icon><TrendCharts /></el-icon>
            <span>预测结果</span>
          </div>

          <!-- 空状态 -->
          <div v-if="!result && !loading" class="empty-state">
            <div class="empty-icon">📊</div>
            <p>填写左侧参数后点击「开始预测」</p>
            <p class="empty-sub">AI 将为你分析薪资水平</p>
          </div>

          <!-- 加载中 -->
          <div v-if="loading" class="loading-state">
            <el-icon class="loading-icon is-loading" :size="48"><Loading /></el-icon>
            <p>AI 模型分析中...</p>
          </div>

          <!-- 结果 -->
          <transition name="result-fade">
            <div v-if="result && !loading" class="result-content">
              <!-- 主薪资显示 -->
              <div class="salary-main">
                <div class="salary-label">预测年薪</div>
                <div class="salary-value" :style="{ color: result.level.color }">
                  ¥ {{ formatSalary(result.predicted_salary) }}
                </div>
                <el-tag :color="result.level.color" effect="dark" size="large" class="level-tag">
                  {{ result.level.label }}工程师
                </el-tag>
              </div>

              <el-divider />

              <!-- 详情指标 -->
              <div class="metrics-grid">
                <div class="metric-item">
                  <div class="metric-icon">💵</div>
                  <div class="metric-value">¥{{ formatSalary(result.monthly_salary) }}</div>
                  <div class="metric-label">预测月薪</div>
                </div>
                <div class="metric-item">
                  <div class="metric-icon">📉</div>
                  <div class="metric-value">¥{{ formatSalary(result.salary_range.low) }}</div>
                  <div class="metric-label">薪资下限</div>
                </div>
                <div class="metric-item">
                  <div class="metric-icon">📈</div>
                  <div class="metric-value">¥{{ formatSalary(result.salary_range.high) }}</div>
                  <div class="metric-label">薪资上限</div>
                </div>
              </div>

              <!-- 薪资区间进度条 -->
              <div class="range-bar-section">
                <div class="range-label">
                  <span>薪资区间分布</span>
                  <span class="range-text">{{ formatSalary(result.salary_range.low) }} \~ {{ formatSalary(result.salary_range.high) }}</span>
                </div>
                <el-progress
                  :percentage="rangePercent"
                  :color="result.level.color"
                  :stroke-width="14"
                  striped
                  striped-flow
                  :duration="10"
                />
              </div>

              <!-- 输入摘要 -->
              <div class="input-summary">
                <el-tag v-for="tag in summaryTags" :key="tag" size="small" class="summary-tag">{{ tag }}</el-tag>
              </div>
            </div>
          </transition>
        </div>
      </div>

      <!-- 底部说明 -->
      <footer class="app-footer">
        <p>本系统基于 GradientBoosting 机器学习模型 · 数据仅供参考 · 实际薪资受市场供需影响</p>
        <p>Tech Stack: Python · FastAPI · Scikit-learn · Vue 3 · Element Plus</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getOptions, predictSalary, getStats } from './api/salary.js'

const loading = ref(false)
const result = ref(null)
const stats = ref(null)
const options = reactive({ positions: [], educations: [], cities: [], company_sizes: [], industries: [] })

const form = reactive({
  position: '',
  education: '',
  city: '',
  company_size: '',
  industry: '',
  experience: 3
})

const isFormValid = computed(() =>
  form.position && form.education && form.city && form.company_size && form.industry
)

const statsCards = computed(() => stats.value ? [
  { icon: '🧠', value: stats.value.model_type.replace('Regressor', ''), label: '模型算法' },
  { icon: '📦', value: stats.value.training_samples.toLocaleString(), label: '训练样本' },
  { icon: '🎯', value: stats.value.r2_score, label: 'R² 准确率' },
  { icon: '🗺️', value: `${stats.value.supported_cities} 城市`, label: '覆盖范围' }
] : [])

const rangePercent = computed(() => {
  if (!result.value) return 0
  const { low, high, } = result.value.salary_range
  const val = result.value.predicted_salary
  return Math.round(((val - low) / (high - low)) * 100)
})

const summaryTags = computed(() => result.value ? [
  form.position, form.education, form.city,
  form.company_size, form.industry, `${form.experience}年经验`
] : [])

function formatSalary(val) {
  if (val >= 10000) return (val / 10000).toFixed(1) + 'w'
  return val.toLocaleString()
}

async function handlePredict() {
  if (!isFormValid.value) {
    ElMessage.warning('请填写所有必填项')
    return
  }
  loading.value = true
  result.value = null
  try {
    const res = await predictSalary({ ...form })
    result.value = res.data
    ElMessage.success('预测完成！')
  } catch (e) {
    ElMessage.error('预测失败，请检查后端服务是否启动')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const [optRes, statRes] = await Promise.all([getOptions(), getStats()])
    Object.assign(options, optRes.data)
    stats.value = statRes.data
  } catch {
    ElMessage.error('无法连接后端服务，请先启动后端')
  }
})
</script>

<style scoped>
* { box-sizing: border-box; }

.app-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  position: relative;
  overflow: hidden;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 背景装饰 */
.bg-decoration .circle {
  position: fixed;
  border-radius: 50%;
  opacity: 0.08;
  animation: float 8s ease-in-out infinite;
}
.circle-1 { width: 500px; height: 500px; background: #7c3aed; top: -200px; right: -100px; }
.circle-2 { width: 350px; height: 350px; background: #2563eb; bottom: -100px; left: -100px; animation-delay: -3s; }
.circle-3 { width: 250px; height: 250px; background: #059669; top: 50%; left: 50%; animation-delay: -6s; }

@keyframes float {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-30px) scale(1.05); }
}

.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
  position: relative;
  z-index: 1;
}

/* ===== Header ===== */
.app-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 32px;
  padding: 28px 36px;
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
}
.header-icon { font-size: 48px; }
.header-text { flex: 1; }
.header-text h1 { margin: 0; font-size: 28px; font-weight: 700; color: #fff; }
.header-text p  { margin: 4px 0 0; color: rgba(255,255,255,0.6); font-size: 14px; }

/* ===== 统计卡片 ===== */
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  transition: transform 0.3s, box-shadow 0.3s;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 8px 30px rgba(0,0,0,0.3); }
.stat-icon  { font-size: 28px; }
.stat-value { font-size: 18px; font-weight: 700; color: #fff; }
.stat-label { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 2px; }

/* ===== 主内容网格 ===== */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

/* ===== 卡片通用 ===== */
.card {
  background: rgba(255,255,255,0.07);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 20px;
  padding: 28px;
}
.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 17px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 24px;
}

/* ===== 表单样式 ===== */
:deep(.el-form-item__label) {
  color: rgba(255,255,255,0.8) !important;
  font-weight: 500;
}
:deep(.el-select .el-input__wrapper) {
  background: rgba(255,255,255,0.08) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  box-shadow: none !important;
  border-radius: 10px !important;
}
:deep(.el-select .el-input__wrapper:hover),
:deep(.el-select .el-input__wrapper.is-focus) {
  border-color: #7c3aed !important;
  background: rgba(124,58,237,0.12) !important;
}
:deep(.el-input__inner) { color: #fff !important; }
:deep(.el-select-dropdown) {
  background: #1e1b4b !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
}
:deep(.el-select-dropdown__item) { color: rgba(255,255,255,0.8) !important; }
:deep(.el-select-dropdown__item.hover),
:deep(.el-select-dropdown__item:hover) {
  background: rgba(124,58,237,0.3) !important;
  color: #fff !important;
}
:deep(.el-select-dropdown__item.selected) {
  color: #a78bfa !important;
  font-weight: 600;
}

/* 滑块 */
:deep(.el-slider__runway) { background: rgba(255,255,255,0.15) !important; }
:deep(.el-slider__bar)    { background: linear-gradient(90deg, #7c3aed, #2563eb) !important; }
:deep(.el-slider__button) {
  border-color: #7c3aed !important;
  background: #fff !important;
  box-shadow: 0 0 10px rgba(124,58,237,0.6) !important;
}
:deep(.el-slider__marks-text) { color: rgba(255,255,255,0.5) !important; font-size: 11px; }

/* 预测按钮 */
.predict-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px !important;
  background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
  border: none !important;
  margin-top: 16px;
  letter-spacing: 2px;
  transition: all 0.3s !important;
  box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}
.predict-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(124,58,237,0.6) !important;
}
.predict-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* ===== 结果卡片 ===== */
.empty-state, .loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 380px;
  color: rgba(255,255,255,0.4);
  gap: 12px;
}
.empty-icon  { font-size: 64px; opacity: 0.4; }
.empty-state p { margin: 0; font-size: 15px; }
.empty-sub   { font-size: 13px !important; opacity: 0.6; }
.loading-icon { color: #7c3aed; }
.loading-state p { color: rgba(255,255,255,0.6); font-size: 15px; }

/* 结果内容 */
.result-content { animation: slideUp 0.5s ease; }

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* 主薪资 */
.salary-main {
  text-align: center;
  padding: 20px 0 16px;
}
.salary-label {
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  letter-spacing: 2px;
  text-transform: uppercase;
  margin-bottom: 8px;
}
.salary-value {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.1;
  text-shadow: 0 0 30px currentColor;
  transition: color 0.5s;
}
.level-tag {
  margin-top: 12px;
  font-size: 14px !important;
  font-weight: 600 !important;
  border-radius: 20px !important;
  border: none !important;
  color: #fff !important;
}

/* 分割线 */
:deep(.el-divider) { border-color: rgba(255,255,255,0.1) !important; margin: 20px 0 !important; }

/* 指标网格 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.metric-item {
  text-align: center;
  padding: 16px 8px;
  background: rgba(255,255,255,0.05);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.08);
  transition: background 0.3s;
}
.metric-item:hover { background: rgba(255,255,255,0.1); }
.metric-icon  { font-size: 22px; margin-bottom: 6px; }
.metric-value { font-size: 18px; font-weight: 700; color: #fff; }
.metric-label { font-size: 11px; color: rgba(255,255,255,0.5); margin-top: 4px; }

/* 薪资区间进度条 */
.range-bar-section { margin-bottom: 20px; }
.range-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: rgba(255,255,255,0.6);
  margin-bottom: 10px;
}
.range-text { color: rgba(255,255,255,0.8); font-weight: 500; }
:deep(.el-progress-bar__outer) { background: rgba(255,255,255,0.1) !important; border-radius: 8px; }
:deep(.el-progress-bar__inner) { border-radius: 8px; }

/* 输入摘要标签 */
.input-summary { display: flex; flex-wrap: wrap; gap: 8px; }
.summary-tag {
  background: rgba(124,58,237,0.2) !important;
  border-color: rgba(124,58,237,0.4) !important;
  color: #c4b5fd !important;
  border-radius: 6px !important;
}

/* 过渡动画 */
.result-fade-enter-active { transition: all 0.5s ease; }
.result-fade-enter-from   { opacity: 0; transform: translateY(15px); }

/* ===== Footer ===== */
.app-footer {
  text-align: center;
  margin-top: 32px;
  padding: 20px;
  color: rgba(255,255,255,0.3);
  font-size: 13px;
  line-height: 1.8;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .content-grid  { grid-template-columns: 1fr; }
  .stats-row     { grid-template-columns: repeat(2, 1fr); }
  .salary-value  { font-size: 38px; }
  .app-header    { flex-wrap: wrap; padding: 20px; }
}
@media (max-width: 480px) {
  .stats-row { grid-template-columns: 1fr 1fr; }
  .metrics-grid { grid-template-columns: repeat(3, 1fr); }
}
</style>
