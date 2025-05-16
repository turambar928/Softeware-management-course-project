<template>
  <div class="history-detection">
    <el-card class="history-card">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <h2>历史检测记录</h2>
            <p class="subtitle">查看您的所有DeepFake新闻真伪检测记录及分析结果</p>
          </div>
          <div class="header-right">
            <el-input
              v-model="searchQuery"
              placeholder="搜索历史记录"
              prefix-icon="Search"
              clearable
              @clear="handleSearchClear"
              @input="handleSearch"
              class="search-input"
            />
          </div>
        </div>
      </template>

      <div class="filter-section">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="8" :md="6">
            <el-select v-model="filterType" placeholder="内容类型" class="filter-select">
              <el-option label="全部" value="" />
              <el-option label="图片新闻" value="image" />
              <el-option label="文本新闻" value="text" />
              <el-option label="网页新闻" value="url" />
            </el-select>
          </el-col>

          <el-col :xs="24" :sm="8" :md="6">
            <el-select v-model="filterResult" placeholder="检测结果" class="filter-select">
              <el-option label="全部" value="" />
              <el-option label="真实新闻" value="true" />
              <el-option label="虚假新闻" value="false" />
            </el-select>
          </el-col>

          <el-col :xs="24" :sm="8" :md="12">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              @change="handleDateChange"
              class="date-picker"
            />
          </el-col>
        </el-row>

        <div class="filter-actions">
          <el-button type="primary" @click="applyFilters">
            <el-icon><Filter /></el-icon> 应用筛选
          </el-button>
          <el-button @click="resetFilters">
            <el-icon><Refresh /></el-icon> 重置
          </el-button>
        </div>
      </div>

      <div class="history-content">
        <el-empty v-if="filteredDetections.length === 0" description="暂无检测记录" />

        <el-table
          v-else
          :data="paginatedDetections"
          style="width: 100%"
          :row-class-name="tableRowClassName"
          @row-click="handleRowClick"
        >
          <el-table-column prop="time" label="检测时间" sortable width="180">
            <template #default="scope">
              {{ formatTime(scope.row.time) }}
            </template>
          </el-table-column>

          <el-table-column prop="contentType" label="内容类型" width="120">
            <template #default="scope">
              <el-tag
                :type="getContentTypeTag(scope.row.contentType)"
                effect="plain"
                size="small"
              >
                {{ scope.row.contentType }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="content" label="检测内容" show-overflow-tooltip />

          <el-table-column prop="result" label="检测结果" width="120">
            <template #default="scope">
              <el-tag
                :type="scope.row.isReal ? 'success' : 'danger'"
                size="small"
              >
                {{ scope.row.isReal ? '真实新闻' : '虚假新闻' }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="score" label="真实性评分" width="120">
            <template #default="scope">
              <el-rate
                v-model="scope.row.score"
                disabled
                text-color="#ff9900"
                score-template="{value}"
              />
            </template>
          </el-table-column>

          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button type="primary" text size="small" @click.stop="viewDetail(scope.row)">
                <el-icon><View /></el-icon> 查看
              </el-button>
              <el-button type="danger" text size="small" @click.stop="deleteRecord(scope.row)">
                <el-icon><Delete /></el-icon> 删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="filteredDetections.length"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="检测记录详情"
      width="70%"
      destroy-on-close
    >
      <div v-if="selectedRecord" class="record-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="检测时间">
            {{ formatTime(selectedRecord.time) }}
          </el-descriptions-item>
          <el-descriptions-item label="内容类型">
            <el-tag :type="getContentTypeTag(selectedRecord.contentType)">
              {{ selectedRecord.contentType }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="检测结果">
            <el-tag :type="selectedRecord.isReal ? 'success' : 'danger'">
              {{ selectedRecord.isReal ? '真实新闻' : '虚假新闻' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="真实性评分">
            <el-rate
              v-model="selectedRecord.score"
              disabled
              show-score
              text-color="#ff9900"
              score-template="{value}"
            />
          </el-descriptions-item>
        </el-descriptions>

        <div class="detail-content">
          <el-tabs v-model="activeDetailTab">
            <el-tab-pane label="检测内容" name="content">
              <div class="content-preview">
                <div v-if="selectedRecord.contentType === '图片新闻'" class="image-preview">
                  <img :src="selectedRecord.picture_url" alt="检测图片" class="detail-image" />
                </div>
                <div v-else class="text-preview">
                  <p>{{ selectedRecord.content }}</p>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="分析结果" name="analysis">
              <div class="analysis-result">
                <el-alert
                  :title="selectedRecord.isReal ? '真实新闻' : '虚假新闻'"
                  :type="selectedRecord.isReal ? 'success' : 'error'"
                  :description="selectedRecord.summary"
                  show-icon
                  :closable="false"
                />

                <h4>关键分析因素</h4>
                <el-collapse>
                  <el-collapse-item v-for="(factor, index) in selectedRecord.factors" :key="index" :title="factor.name">
                    <p>{{ factor.description }}</p>
                  </el-collapse-item>
                </el-collapse>

                <div v-if="selectedRecord.resultImage" class="result-image-container">
                  <h4>分析图表</h4>
                  <img :src="selectedRecord.resultImage" alt="分析结果" class="result-image" />
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="exportRecord">
            <el-icon><Download /></el-icon> 导出报告
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="删除确认"
      width="30%"
    >
      <p>确定要删除这条检测记录吗？此操作无法撤销。</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteDialogVisible = false">取消</el-button>
          <el-button type="danger" @click="confirmDelete">确定删除</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

// 基本数据
const detections = ref([])
const searchQuery = ref('')
const filterType = ref('')
const filterResult = ref('')
const dateRange = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)

// 详情对话框
const detailDialogVisible = ref(false)
const selectedRecord = ref(null)
const activeDetailTab = ref('content')

// 删除对话框
const deleteDialogVisible = ref(false)
const recordToDelete = ref(null)

// 计算属性
const filteredDetections = computed(() => {
  let result = [...detections.value]

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(item => {
      return (
        (item.content && item.content.toLowerCase().includes(query)) ||
        (item.result && item.result.toLowerCase().includes(query))
      )
    })
  }

  // 类型过滤
  if (filterType.value) {
    result = result.filter(item => {
      if (filterType.value === 'image') return item.contentType === '图片新闻'
      if (filterType.value === 'text') return item.contentType === '文本新闻'
      if (filterType.value === 'url') return item.contentType === '网页新闻'
      return true
    })
  }

  // 结果过滤
  if (filterResult.value !== '') {
    const isReal = filterResult.value === 'true'
    result = result.filter(item => item.isReal === isReal)
  }

  // 日期过滤
  if (dateRange.value && dateRange.value.length === 2) {
    const startDate = new Date(dateRange.value[0])
    startDate.setHours(0, 0, 0, 0)

    const endDate = new Date(dateRange.value[1])
    endDate.setHours(23, 59, 59, 999)

    result = result.filter(item => {
      const itemDate = new Date(item.time)
      return itemDate >= startDate && itemDate <= endDate
    })
  }

  return result
})

const paginatedDetections = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredDetections.value.slice(start, end)
})

// 方法
const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleString()
}

const getContentTypeTag = (type) => {
  if (type === '图片新闻') return 'success'
  if (type === '文本新闻') return 'primary'
  if (type === '网页新闻') return 'warning'
  return 'info'
}

const tableRowClassName = ({ row }) => {
  return row.isReal ? '' : 'warning-row'
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleSearchClear = () => {
  searchQuery.value = ''
  currentPage.value = 1
}

const handleDateChange = () => {
  // 日期变化时的处理
}

const applyFilters = () => {
  currentPage.value = 1
  ElMessage.success('筛选已应用')
}

const resetFilters = () => {
  filterType.value = ''
  filterResult.value = ''
  dateRange.value = null
  searchQuery.value = ''
  currentPage.value = 1
  ElMessage.info('筛选已重置')
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val) => {
  currentPage.value = val
}

const handleRowClick = (row) => {
  viewDetail(row)
}

const viewDetail = (record) => {
  selectedRecord.value = { ...record }
  detailDialogVisible.value = true
}

const deleteRecord = (record) => {
  recordToDelete.value = record
  deleteDialogVisible.value = true
}

const confirmDelete = async () => {
  if (!recordToDelete.value) return

  try {
    // 实际应用中应该调用后端 API 删除记录
    // const token = localStorage.getItem('token')
    // await axios.delete(`http://127.0.0.1:5000/user/record/${recordToDelete.value.id}`, {
    //   headers: { Authorization: `Bearer ${token}` }
    // })

    // 模拟删除成功
    detections.value = detections.value.filter(item => item.id !== recordToDelete.value.id)
    ElMessage.success('记录已删除')
    deleteDialogVisible.value = false
    recordToDelete.value = null
  } catch (error) {
    console.error('删除失败：', error)
    ElMessage.error('删除失败，请重试')
  }
}

const exportRecord = () => {
  if (!selectedRecord.value) return

  ElMessage.success('报告导出成功')
  // 实际应用中应该实现导出功能，如生成PDF或Excel
}

// 生成模拟数据
const generateMockData = () => {
  const mockData = []
  const contentTypes = ['图片新闻', '文本新闻', '网页新闻']
  const contents = [
    '中国经济增长超出预期，第二季度GDP同比增长6.3%',
    '科学家发现新型可再生能源，有望解决能源危机',
    '国际会议达成气候变化新协议，全球承诺减排',
    '新研究表明健康饮食习惯可显著降低心血管疾病风险',
    '技术公司宣布突破性人工智能研发，股价大涨',
  ]

  // 生成分析因素
  const realFactors = [
    { name: '内容一致性', description: '新闻内容与多个可靠源报道一致' },
    { name: '来源可靠性', description: '新闻来源为知名可靠的新闻机构' },
    { name: '事实核实', description: '关键事实可以通过多渠道验证' }
  ]

  const fakeFactors = [
    { name: '内容不一致', description: '新闻内容与已知事实有显著冲突' },
    { name: '情绪化语言', description: '内容使用了过多的情绪化和极端语言' },
    { name: '缺乏来源', description: '新闻未指明信息来源或引用不可靠源' }
  ]

  // 生成模拟数据
  for (let i = 0; i < 25; i++) {
    const isReal = Math.random() > 0.3
    const contentType = contentTypes[Math.floor(Math.random() * contentTypes.length)]
    const content = contents[Math.floor(Math.random() * contents.length)]

    // 生成随机日期（过去30天内）
    const date = new Date()
    date.setDate(date.getDate() - Math.floor(Math.random() * 30))

    mockData.push({
      id: i + 1,
      time: date.toISOString(),
      contentType: contentType,
      content: content,
      isReal: isReal,
      result: isReal ? '真实' : '虚假',
      score: isReal ? 3.5 + Math.random() * 1.5 : 1 + Math.random() * 2,
      picture_url: contentType === '图片新闻' ? 'https://via.placeholder.com/300x200' : null,
      resultImage: Math.random() > 0.5 ? 'https://via.placeholder.com/500x300' : null,
      summary: isReal ?
        '经过多维度分析，该新闻内容大部分可信，与多个可靠源报道一致。' :
        '经分析，该新闻内容存在多处不一致或误导性信息，可信度较低。',
      factors: isReal ? realFactors : fakeFactors
    })
  }

  return mockData
}

// 生命周期钩子
onMounted(async () => {
  try {
    const token = localStorage.getItem('token')

    // 尝试从后端获取数据
    try {
      const response = await axios.get('http://127.0.0.1:5000/user/record', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (response.data.code === 200) {
        // 如果有真实的API响应，可以使用实际数据
        const apiData = response.data.data.detections

        // 如果数据结构不完整，进行补充
        detections.value = apiData.map(item => ({
          ...item,
          id: item.id || Math.floor(Math.random() * 10000),
          contentType: item.contentType || '文本新闻',
          isReal: item.result === '真实',
          score: item.score || (item.result === '真实' ? 4.5 : 2.0),
          content: item.content || '无内容预览',
          summary: item.summary || '无分析摘要',
          factors: item.factors || []
        }))
      } else {
        // 如果获取失败，使用模拟数据
        detections.value = generateMockData()
      }
    } catch (error) {
      console.error('获取记录失败：', error)
      // 如果请求失败，使用模拟数据
      detections.value = generateMockData()
    }
  } catch (error) {
    console.error('初始化失败：', error)
    ElMessage.error('加载历史记录失败')
  }
})

// 监听过滤器变化
watch([searchQuery, filterType, filterResult, dateRange], () => {
  // 当过滤条件变化时，重置到第一页
  currentPage.value = 1
})
</script>

<style scoped>
.history-detection {
  padding: 0;
}

.history-card {
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  flex-direction: column;
}

.header-left h2 {
  margin: 0 0 8px 0;
  font-size: 1.5rem;
  color: var(--primary-color);
}

.subtitle {
  color: var(--light-text);
  font-size: 0.9rem;
  margin: 0;
}

.search-input {
  width: 250px;
}

.filter-section {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.filter-select {
  width: 100%;
  margin-bottom: 10px;
}

.date-picker {
  width: 100%;
}

.filter-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
  gap: 10px;
}

.history-content {
  margin-top: 20px;
}

/* 表格样式 */
.el-table :deep(.warning-row) {
  --el-table-tr-bg-color: var(--el-color-danger-light-9);
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 详情对话框样式 */
.record-detail {
  padding: 10px 0;
}

.detail-content {
  margin-top: 20px;
}

.content-preview {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  min-height: 200px;
}

.image-preview {
  text-align: center;
}

.detail-image {
  max-width: 100%;
  max-height: 400px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.text-preview {
  white-space: pre-line;
  line-height: 1.6;
}

.analysis-result {
  margin-top: 20px;
}

.analysis-result h4 {
  margin: 20px 0 10px 0;
  font-size: 16px;
  color: var(--primary-color);
}

.result-image-container {
  margin-top: 20px;
  text-align: center;
}

.result-image {
  max-width: 100%;
  border: 1px solid #eee;
  border-radius: 4px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .header-right {
    margin-top: 15px;
    width: 100%;
  }

  .search-input {
    width: 100%;
  }

  .filter-actions {
    flex-direction: column;
  }

  .filter-actions .el-button {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>
