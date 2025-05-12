<template>
  <div class="main-page">
    <aside class="sidebar">
      <ul>
        <li @click="navigateTo('personal-center')">个人中心</li>
        <li @click="navigateTo('news-detection')">新闻检测</li>
        <li @click="navigateTo('history-detection')">历史检测</li>
      </ul>
    </aside>
    <main class="content">
      <router-view /> <!-- 显示点击对应的子页面 -->
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (path) => {
  router.push(`/${path}`)
}
</script>

<style scoped>
.main-page {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 200px;
  background-color: #f5f5f5;
  padding: 1rem;
  border-right: 1px solid #ddd;
}

.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.sidebar li {
  padding: 0.75rem 1rem;
  cursor: pointer;
  color: #409eff;
  transition: background 0.2s;
}

.sidebar li:hover {
  background-color: #e6f7ff;
  color: #307ec7;
}

.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>
