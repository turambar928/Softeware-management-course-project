<template>
  <div class="dashboard">
    <div class="welcome-section">
      <h2>欢迎使用DeepFake新闻真伪检测系统</h2>
      <p class="subtitle">专业的DeepFake媒体内容鉴别平台，帮助您识别虚假新闻和深度伪造内容</p>
    </div>

    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-info">
              <h3>{{ stats.totalDetections }}</h3>
              <p>总检测次数</p>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-icon success-icon">
              <el-icon><Check /></el-icon>
            </div>
            <div class="stat-info">
              <h3>{{ stats.realNews }}</h3>
              <p>真实新闻</p>
            </div>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-icon warning-icon">
              <el-icon><Warning /></el-icon>
            </div>
            <div class="stat-info">
              <h3>{{ stats.fakeNews }}</h3>
              <p>虚假新闻</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="quick-actions">
      <div class="section-header">
        <h3>快速操作</h3>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card class="action-card" @click="navigateTo('news-detection')">
            <el-icon><Search /></el-icon>
            <h4>新闻检测</h4>
            <p>上传新闻内容进行真伪检测</p>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="action-card" @click="navigateTo('history-detection')">
            <el-icon><List /></el-icon>
            <h4>历史记录</h4>
            <p>查看您的历史检测记录</p>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="action-card" @click="navigateTo('personal-center')">
            <el-icon><User /></el-icon>
            <h4>个人中心</h4>
            <p>管理您的个人信息和设置</p>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="recent-detections">
      <div class="section-header">
        <h3>最近检测</h3>
        <el-button type="primary" text @click="navigateTo('history-detection')">
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>

      <el-table :data="recentDetections" style="width: 100%">
        <el-table-column prop="time" label="检测时间" width="180" />
        <el-table-column prop="content" label="检测内容" />
        <el-table-column prop="result" label="检测结果" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.result === '真实' ? 'success' : 'danger'">
              {{ scope.row.result }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="primary" text size="small" @click="viewDetail(scope.row)">
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

const stats = ref({
  totalDetections: 0,
  realNews: 0,
  fakeNews: 0
})

const recentDetections = ref([])

const navigateTo = (path) => {
  router.push(`/${path}`)
}

const viewDetail = (row) => {
  // 这里可以实现查看详情的逻辑，例如打开一个对话框或导航到详情页
  console.log('查看详情', row)
}

const fetchDashboardData = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return

    // 这里应该调用后端API获取仪表盘数据
    // 由于后端可能没有这个接口，这里使用模拟数据

    // 模拟数据
    stats.value = {
      totalDetections: 28,
      realNews: 20,
      fakeNews: 8
    }

    recentDetections.value = [
      { id: 1, time: '2025-05-17 10:30', content: '关于新冠疫情的最新报道', result: '真实' },
      { id: 2, time: '2025-05-16 15:45', content: '某明星涉嫌违法的新闻', result: '虚假' },
      { id: 3, time: '2025-05-15 09:20', content: '国际贸易协议签署的报道', result: '真实' },
      { id: 4, time: '2025-05-14 14:10', content: '某公司股价暴涨的消息', result: '真实' },
      { id: 5, time: '2025-05-13 11:25', content: '网传某地区发生自然灾害', result: '虚假' }
    ]

    // 如果后端有相应接口，可以使用以下代码获取真实数据
    /*
    const response = await axios.get('http://127.0.0.1:5000/dashboard/stats', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.code === 200) {
      stats.value = response.data.data.stats
      recentDetections.value = response.data.data.recentDetections
    }
    */
  } catch (err) {
    console.error('获取仪表盘数据失败', err)
  }
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard {
  padding: 20px 10px;
}

.welcome-section {
  margin-bottom: 30px;
}

.subtitle {
  color: var(--light-text);
  font-size: 1rem;
  margin-top: 5px;
}

.stats-section {
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  height: 100%;
}

.stat-icon {
  font-size: 2.5rem;
  color: var(--secondary-color);
  margin-right: 20px;
}

.success-icon {
  color: var(--success-color);
}

.warning-icon {
  color: var(--warning-color);
}

.stat-info h3 {
  font-size: 1.8rem;
  margin: 0 0 5px 0;
  font-weight: 600;
}

.stat-info p {
  margin: 0;
  color: var(--light-text);
}

.quick-actions {
  margin-top: 40px;
  margin-bottom: 40px;
}

.quick-actions h3, .recent-detections h3 {
  margin-top: 10px;
  margin-bottom: 20px;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-color);
  padding-left: 10px;
  border-left: 3px solid var(--secondary-color);
}

.action-card {
  text-align: center;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.action-card .el-icon {
  font-size: 2rem;
  color: var(--secondary-color);
  margin-bottom: 10px;
}

.action-card h4 {
  margin: 10px 0;
  font-size: 1.1rem;
}

.action-card p {
  color: var(--light-text);
  font-size: 0.9rem;
  margin: 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.recent-detections {
  margin-top: 40px;
  margin-bottom: 30px;
}
</style>
