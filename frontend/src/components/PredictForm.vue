<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="rules"
    label-position="top"
    class="predict-form"
    :disabled="loading"
  >
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="职位方向" prop="position">
          <el-select
            v-model="form.position"
            placeholder="请选择职位"
            size="large"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="p in options.positions"
              :key="p"
              :label="p"
              :value="p"
            />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="最高学历" prop="education">
          <el-select
            v-model="form.education"
            placeholder="请选择学历"
            size="large"
            style="width: 100%"
          >
            <el-option
              v-for="e in options.educations"
              :key="e"
              :label="e"
              :value="e"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-form-item label="目标城市" prop="city">
          <el-select
            v-model="form.city"
            placeholder="请选择城市"
            size="large"
            style="width: 100%"
            filterable
          >
            <el-option
              v-for="c in options.cities"
              :key="c"
              :label="c"
              :value="c"
            />
          </el-select>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="行业领域" prop="industry">
          <el-select
            v-model="form.industry"
            placeholder="请选择行业"
            size="large"
            style="width: 100%"
          >
            <el-option
              v-for="i in options.industries"
              :key="i"
              :label="i"
              :value="i"
            />
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>

    <el-form-item label="公司规模" prop="company_size">
      <el-select
        v-model="form.company_size"
        placeholder="请选择公司规模"
        size="large"
        style="width: 100%"
      >
        <el-option
          v-for="s in options.company_sizes"
          :key="s"
          :label="s"
          :value="s"
        />
      </el-select>
    </el-form-item>

    <el-form-item :label="`工作年限：${form.experience} 年`" prop="experience">
      <el-slider
        v-model="form.experience"
        :min="0"
        :max="20"
        :step="1"
        show-stops
        :marks="{
          0:  '应届',
          3:  '3年',
          5:  '5年',
          10: '10年',
          20: '20年'
        }"
        class="exp-slider"
      />
    </el-form-item>

    <!-- 重置 + 预测 两个按钮 -->
    <el-row :gutter="12" style="margin-top: 24px">
      <el-col :span="8">
        <el-button
          size="large"
          style="width: 100%; border-radius: 10px;"
          @click="handleReset"
          :disabled="loading"
        >
          <el-icon><RefreshLeft /></el-icon>
          重置
        </el-button>
      </el-col>
      <el-col :span="16">
        <el-button
          type="primary"
          size="large"
          :loading="loading"
          @click="handleSubmit"
          class="predict-btn"
          :disabled="!isFormValid"
        >
          <el-icon v-if="!loading"><MagicStick /></el-icon>
          {{ loading ? 'AI 分析中...' : '开始预测' }}
        </el-button>
      </el-col>
    </el-row>
  </el-form>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'

// ---- Props & Emits ----
const props = defineProps({
  options: {
    type: Object,
    default: () => ({
      positions:     [],
      educations:    [],
      cities:        [],
      company_sizes: [],
      industries:    []
    })
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit', 'reset'])

// ---- 表单数据 ----
const formRef = ref(null)

const form = reactive({
  position:     '',
  education:    '',
  city:         '',
  company_size: '',
  industry:     '',
  experience:   3
})

// ---- 表单校验规则 ----
const rules = {
  position:     [{ required: true, message: '请选择职位方向', trigger: 'change' }],
  education:    [{ required: true, message: '请选择最高学历', trigger: 'change' }],
  city:         [{ required: true, message: '请选择目标城市', trigger: 'change' }],
  company_size: [{ required: true, message: '请选择公司规模', trigger: 'change' }],
  industry:     [{ required: true, message: '请选择行业领域', trigger: 'change' }]
}

// ---- 是否可提交 ----
const isFormValid = computed(() =>
  form.position &&
  form.education &&
  form.city &&
  form.company_size &&
  form.industry
)

// ---- 提交 ----
async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('submit', { ...form })
    } else {
      ElMessage.warning('请完整填写所有必填项')
    }
  })
}

// ---- 重置 ----
function handleReset() {
  formRef.value?.resetFields()
  form.experience = 3
  emit('reset')
}

// ---- 暴露给父组件（可选） ----
defineExpose({ form, handleReset })
</script>

<style scoped>
/* 滑块样式 */
.exp-slider {
  width: 100%;
  padding: 0 8px;
  margin-top: 8px;
}

:deep(.el-slider__runway)  { background: rgba(255,255,255,0.15) !important; }
:deep(.el-slider__bar)     { background: linear-gradient(90deg, #7c3aed, #2563eb) !important; }
:deep(.el-slider__button)  {
  border-color: #7c3aed !important;
  background: #fff !important;
  box-shadow: 0 0 10px rgba(124,58,237,0.6) !important;
}
:deep(.el-slider__marks-text) {
  color: rgba(255,255,255,0.5) !important;
  font-size: 11px;
}

/* 预测按钮 */
.predict-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 10px !important;
  background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
  border: none !important;
  letter-spacing: 1px;
  transition: all 0.3s !important;
  box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
}
.predict-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(124,58,237,0.6) !important;
}
.predict-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* 重置按钮 */
:deep(.el-button:not(.predict-btn)) {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.2) !important;
  color: rgba(255,255,255,0.7) !important;
  height: 48px;
}
:deep(.el-button:not(.predict-btn):hover) {
  background: rgba(255,255,255,0.15) !important;
  color: #fff !important;
}
</style>
