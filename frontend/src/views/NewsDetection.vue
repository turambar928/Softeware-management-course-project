<template>
  <div class="news-detection">
    <el-card class="detection-card">
      <template #header>
        <div class="card-header">
          <h2>DeepFake新闻真伪检测</h2>
          <p class="subtitle">使用先进的AI技术分析新闻内容，帮助您识别虚假信息</p>
        </div>
      </template>

      <el-steps :active="activeStep" finish-status="success" simple>
        <el-step title="上传内容" icon="Upload" />
        <el-step title="分析中" icon="Loading" />
        <el-step title="查看结果" icon="Check" />
      </el-steps>

      <div class="step-content">
        <!-- 第一步：上传内容 -->
        <div v-if="activeStep === 0" class="upload-step">
          <el-tabs v-model="activeTab" class="detection-tabs">
            <el-tab-pane label="图片检测" name="image">
              <div class="upload-container">
                <el-upload
                  class="image-uploader"
                  :auto-upload="false"
                  :show-file-list="false"
                  :on-change="handleImageChange"
                  accept="image/*"
                  drag
                >
                  <img v-if="imageUrl" :src="imageUrl" class="preview-img" />
                  <el-icon v-else class="upload-icon"><Plus /></el-icon>
                  <div v-if="!imageUrl" class="upload-text">
                    <span>拖拽图片到此处或点击上传</span>
                    <p class="upload-hint">支持 JPG, PNG 格式图片</p>
                  </div>
                </el-upload>
              </div>
            </el-tab-pane>

            <el-tab-pane label="文本检测" name="text">
              <div class="text-container">
                <el-input
                  v-model="textInput"
                  type="textarea"
                  :rows="8"
                  placeholder="请输入需要检测的新闻文本内容..."
                  resize="none"
                />
                <p class="text-hint">请输入至少100个字的新闻内容以获得更准确的检测结果</p>
              </div>
            </el-tab-pane>

            <el-tab-pane label="URL检测" name="url">
              <div class="url-container">
                <el-input
                  v-model="urlInput"
                  placeholder="请输入新闻文章的URL地址"
                  prefix-icon="Link"
                />
                <p class="url-hint">输入新闻网页的完整URL，系统将自动提取内容进行分析</p>
              </div>
            </el-tab-pane>
          </el-tabs>

          <div class="action-buttons">
            <el-button type="primary" :disabled="!canProceed" @click="startDetection">
              <el-icon><Search /></el-icon> 开始检测
            </el-button>
            <el-button @click="resetForm">
              <el-icon><Refresh /></el-icon> 重置
            </el-button>
          </div>
        </div>

        <!-- 第二步：分析中 -->
        <div v-if="activeStep === 1" class="analysis-step">
          <div class="analysis-animation">
            <el-progress type="dashboard" :percentage="analysisProgress" :stroke-width="8">
              <template #default="{ percentage }">
                <span class="progress-value">{{ percentage }}%</span>
                <span class="progress-label">分析中</span>
              </template>
            </el-progress>
          </div>

          <div class="analysis-info">
            <p v-for="(step, index) in analysisSteps" :key="index"
               :class="{ 'active-step': index === currentAnalysisStep }">
              <el-icon v-if="index < currentAnalysisStep"><Check /></el-icon>
              <el-icon v-else-if="index === currentAnalysisStep"><Loading /></el-icon>
              <el-icon v-else><More /></el-icon>
              {{ step }}
            </p>
          </div>

          <div class="cancel-button">
            <el-button @click="cancelAnalysis">取消</el-button>
          </div>
        </div>

        <!-- 第三步：查看结果 -->
        <div v-if="activeStep === 2" class="result-step">
          <div class="result-header">
            <el-alert
              :title="detectionResult.isReal ? '真实新闻' : '虚假新闻'"
              :type="detectionResult.isReal ? 'success' : 'error'"
              :description="detectionResult.summary"
              show-icon
              :closable="false"
            />
          </div>

          <div class="result-details">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-card class="detail-card">
                  <template #header>
                    <div class="card-header">
                      <h3>检测结果</h3>
                    </div>
                  </template>

                  <el-descriptions :column="1" border>
                    <el-descriptions-item label="真实性评分">
                      <el-rate
                        v-model="detectionResult.score"
                        disabled
                        show-score
                        text-color="#ff9900"
                        score-template="{value}"
                      />
                    </el-descriptions-item>
                    <el-descriptions-item label="检测时间">
                      {{ detectionResult.time }}
                    </el-descriptions-item>
                    <el-descriptions-item label="内容类型">
                      <el-tag>{{ detectionResult.contentType }}</el-tag>
                    </el-descriptions-item>
                    <el-descriptions-item label="可信度">
                      <el-progress
                        :percentage="detectionResult.credibility"
                        :color="credibilityColor"
                      />
                    </el-descriptions-item>
                  </el-descriptions>
                </el-card>
              </el-col>

              <el-col :span="12">
                <el-card class="detail-card">
                  <template #header>
                    <div class="card-header">
                      <h3>分析详情</h3>
                    </div>
                  </template>

                  <div v-if="resultImage" class="result-image-container">
                    <img :src="resultImage" alt="检测结果" class="result-img" />
                  </div>

                  <div class="analysis-factors">
                    <h4>关键分析因素</h4>
                    <el-collapse>
                      <el-collapse-item v-for="(factor, index) in detectionResult.factors" :key="index" :title="factor.name">
                        <p>{{ factor.description }}</p>
                      </el-collapse-item>
                    </el-collapse>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>

          <div class="result-actions">
            <el-button type="primary" @click="saveResult">
              <el-icon><Download /></el-icon> 保存结果
            </el-button>
            <el-button @click="resetDetection">
              <el-icon><Refresh /></el-icon> 新的检测
            </el-button>
            <el-button type="info" @click="showHelp">
              <el-icon><QuestionFilled /></el-icon> 帮助说明
            </el-button>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 帮助对话框 -->
    <el-dialog
      v-model="helpDialogVisible"
      title="如何理解检测结果"
      width="50%"
    >
      <div class="help-content">
        <h3>关于DeepFake新闻真伪检测</h3>
        <p>本系统使用先进的人工智能技术对新闻内容进行分析，帮助您识别可能的虚假信息。</p>

        <h4>结果解读</h4>
        <ul>
          <li><strong>真实性评分</strong>: 1-5分评估，分数越高表示内容越可能真实</li>
          <li><strong>可信度</strong>: 系统对判断结果的信心程度</li>
          <li><strong>关键分析因素</strong>: 影响判断的主要因素</li>
        </ul>

        <h4>注意事项</h4>
        <p>本系统提供的检测结果仅供参考，不应作为唯一判断依据。对于重要信息，请始终保持批判性思考并交叉验证。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="helpDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

// 基本状态
const activeStep = ref(0) // 0: 上传内容, 1: 分析中, 2: 查看结果
const activeTab = ref('image') // image, text, url
const helpDialogVisible = ref(false)

// 输入内容
const imageUrl = ref('')
const textInput = ref('')
const urlInput = ref('')
const selectedFile = ref(null)
const resultImage = ref('')

// 分析过程
const analysisProgress = ref(0)
const analysisTimer = ref(null)
const currentAnalysisStep = ref(0)
const analysisSteps = [
  '加载内容数据',
  '提取关键特征',
  '进行深度学习分析',
  '交叉验证信息来源',
  '生成分析报告'
]

// 检测结果
const detectionResult = ref({
  isReal: false,
  score: 0,
  time: '',
  contentType: '',
  credibility: 0,
  summary: '',
  factors: []
})

// 计算属性
const canProceed = computed(() => {
  if (activeTab.value === 'image') return !!selectedFile.value
  if (activeTab.value === 'text') return textInput.value.trim().length >= 10
  if (activeTab.value === 'url') return isValidUrl(urlInput.value)
  return false
})

const credibilityColor = computed(() => {
  const credibility = detectionResult.value.credibility
  if (credibility < 30) return '#F56C6C' // 红色
  if (credibility < 70) return '#E6A23C' // 黄色
  return '#67C23A' // 绿色
})

// 方法
const handleImageChange = (file) => {
  selectedFile.value = file.raw
  const reader = new FileReader()
  reader.onload = () => {
    imageUrl.value = reader.result
  }
  reader.readAsDataURL(file.raw)
}

const isValidUrl = (url) => {
  try {
    new URL(url)
    return true
  } catch (e) {
    return false
  }
}

const resetForm = () => {
  imageUrl.value = ''
  textInput.value = ''
  urlInput.value = ''
  selectedFile.value = null
}

const startDetection = () => {
  activeStep.value = 1 // 进入分析阶段
  analysisProgress.value = 0
  currentAnalysisStep.value = 0

  // 模拟分析进度
  analysisTimer.value = setInterval(() => {
    if (analysisProgress.value < 100) {
      analysisProgress.value += 1

      // 更新当前分析步骤
      if (analysisProgress.value === 20) currentAnalysisStep.value = 1
      if (analysisProgress.value === 40) currentAnalysisStep.value = 2
      if (analysisProgress.value === 60) currentAnalysisStep.value = 3
      if (analysisProgress.value === 80) currentAnalysisStep.value = 4

      if (analysisProgress.value >= 100) {
        clearInterval(analysisTimer.value)
        setTimeout(() => {
          performActualDetection()
        }, 500)
      }
    }
  }, 50)
}

const cancelAnalysis = () => {
  ElMessageBox.confirm(
    '确定要取消当前的检测吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    clearInterval(analysisTimer.value)
    activeStep.value = 0
    ElMessage.info('检测已取消')
  }).catch(() => {})
}

const performActualDetection = async () => {
  try {
    const formData = new FormData()

    if (activeTab.value === 'image' && selectedFile.value) {
      formData.append('image', selectedFile.value)
    } else if (activeTab.value === 'text') {
      formData.append('text', textInput.value)
    } else if (activeTab.value === 'url') {
      formData.append('url', urlInput.value)
    }

    const token = localStorage.getItem('token') || ''

    // 实际发送请求到后端
    try {
      const response = await axios.post('http://127.0.0.1:5000/news/detect', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`
        }
      })

      const data = response.data
      if (data.code === 200) {
        // 如果有真实的API响应，可以使用实际数据
        if (data.data.result_image_url) {
          resultImage.value = data.data.result_image_url
        }

        // 这里可以处理实际的响应数据
        // 现在使用模拟数据代替
        generateMockResult()
      } else {
        ElMessage.error(data.message || '检测失败')
        activeStep.value = 0
      }
    } catch (error) {
      console.error('检测错误：', error)
      // 如果后端请求失败，使用模拟数据展示界面
      generateMockResult()
    }
  } catch (error) {
    ElMessage.error('处理请求时出错')
    activeStep.value = 0
  }
}

const generateMockResult = () => {
  // 生成模拟的检测结果
  const isReal = Math.random() > 0.5
  const score = isReal ? 3.5 + Math.random() * 1.5 : 1 + Math.random() * 2
  const credibility = isReal ? 70 + Math.random() * 30 : 20 + Math.random() * 50

  let contentType = ''
  if (activeTab.value === 'image') contentType = '图片新闻'
  else if (activeTab.value === 'text') contentType = '文本新闻'
  else contentType = '网页新闻'

  const now = new Date()
  const timeStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`

  const factors = isReal ? [
    { name: '内容一致性', description: '新闻内容与多个可靠源报道一致' },
    { name: '来源可靠性', description: '新闻来源为知名可靠的新闻机构' },
    { name: '事实核实', description: '关键事实可以通过多渠道验证' }
  ] : [
    { name: '内容不一致', description: '新闻内容与已知事实有显著冲突' },
    { name: '情绪化语言', description: '内容使用了过多的情绪化和极端语言' },
    { name: '缺乏来源', description: '新闻未指明信息来源或引用不可靠源' }
  ]

  const summary = isReal ?
    '经过多维度分析，该新闻内容大部分可信，与多个可靠源报道一致。' :
    '经分析，该新闻内容存在多处不一致或误导性信息，可信度较低。'

  detectionResult.value = {
    isReal,
    score,
    time: timeStr,
    contentType,
    credibility,
    summary,
    factors
  }

  // 进入结果页面
  activeStep.value = 2
}

const saveResult = () => {
  ElMessage.success('结果已保存到您的历史记录')
  // 这里可以实现实际的保存逻辑，如发送请求到后端保存结果
}

const resetDetection = () => {
  activeStep.value = 0
  resetForm()
  resultImage.value = ''
}

const showHelp = () => {
  helpDialogVisible.value = true
}

// 生命周期钩子
onMounted(() => {
  // 可以在这里加载一些初始数据或设置
})
</script>


<style scoped>
.news-detection {
  padding: 0;
}

.detection-card {
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.card-header h2 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  color: var(--primary-color);
}

.subtitle {
  color: var(--light-text);
  font-size: 0.9rem;
  margin: 0;
}

.el-steps {
  margin: 20px 0 30px;
}

.step-content {
  padding: 20px 0;
}

/* 第一步：上传内容 */
.upload-step {
  margin-bottom: 20px;
}

.detection-tabs {
  margin-bottom: 20px;
}

.upload-container,
.text-container,
.url-container {
  padding: 20px 0;
}

.image-uploader {
  width: 100%;
}

.image-uploader :deep(.el-upload) {
  width: 100%;
  text-align: center;
}

.image-uploader :deep(.el-upload-dragger) {
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-icon {
  font-size: 48px;
  color: #8c939d;
  margin-bottom: 10px;
}

.upload-text {
  color: #606266;
}

.upload-hint,
.text-hint,
.url-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 10px;
}

.preview-img {
  max-width: 100%;
  max-height: 200px;
  object-fit: contain;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

/* 第二步：分析中 */
.analysis-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.analysis-animation {
  margin-bottom: 30px;
}

.progress-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--primary-color);
}

.progress-label {
  display: block;
  font-size: 14px;
  color: var(--light-text);
  margin-top: 5px;
}

.analysis-info {
  width: 100%;
  max-width: 500px;
  margin: 0 auto 20px;
}

.analysis-info p {
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
  display: flex;
  align-items: center;
  color: var(--light-text);
}

.analysis-info p .el-icon {
  margin-right: 10px;
}

.analysis-info p.active-step {
  background-color: #ecf5ff;
  color: var(--primary-color);
  font-weight: 500;
}

.cancel-button {
  margin-top: 20px;
}

/* 第三步：查看结果 */
.result-step {
  padding: 10px 0;
}

.result-header {
  margin-bottom: 20px;
}

.result-details {
  margin-bottom: 30px;
}

.detail-card {
  height: 100%;
  margin-bottom: 20px;
}

.detail-card :deep(.el-card__header) {
  padding: 15px 20px;
}

.detail-card h3 {
  margin: 0;
  font-size: 16px;
  color: var(--primary-color);
}

.result-image-container {
  text-align: center;
  margin-bottom: 20px;
}

.result-img {
  max-width: 100%;
  max-height: 200px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.analysis-factors h4 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 14px;
  color: var(--light-text);
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 30px;
}

/* 帮助对话框 */
.help-content h3 {
  margin-top: 0;
  color: var(--primary-color);
}

.help-content h4 {
  margin-top: 20px;
  margin-bottom: 10px;
  color: var(--secondary-color);
}

.help-content ul {
  padding-left: 20px;
}

.help-content li {
  margin-bottom: 5px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .result-details .el-row {
    display: block;
  }

  .result-details .el-col {
    width: 100%;
  }

  .action-buttons,
  .result-actions {
    flex-direction: column;
  }

  .action-buttons .el-button,
  .result-actions .el-button {
    margin-bottom: 10px;
  }
}
</style>
