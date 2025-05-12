<template>
  <div class="history-detection">
    <h2>历史检测信息</h2>
    <p>这里是历史检测信息栏目，您可以查看您的历史检测记录。</p>

    <div v-if="detections.length === 0">暂无检测记录。</div>
    <ul v-else class="detection-list">
      <li v-for="(item, index) in detections" :key="index" class="detection-item">
        <p><strong>检测时间：</strong>{{ formatTime(item.time) }}</p>
        <p><strong>检测结果：</strong>{{ item.result }}</p>
        <div v-if="item.picture_url">
          <strong>检测图片：</strong><br />
          <img :src="item.picture_url" alt="检测图片" class="detection-image" />
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const detections = ref([])

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleString()
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:5000/user/record', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.code === 200) {
      detections.value = response.data.data.detections
    } else {
      console.error('获取记录失败：', response.data.message)
    }
  } catch (error) {
    console.error('请求失败：', error)
  }
})
</script>

<style scoped>
.history-detection {
  padding: 20px;
}

.detection-list {
  list-style-type: none;
  padding: 0;
}

.detection-item {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  background-color: #f9f9f9;
}

.detection-image {
  max-width: 300px;
  margin-top: 8px;
  border: 1px solid #ddd;
}
</style>
