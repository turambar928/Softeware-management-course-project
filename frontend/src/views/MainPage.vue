<template>
  <div class="main-layout">
    <!-- 顶部导航栏 -->
    <header class="main-header">
      <div class="logo-container">
        <img src="../assets/images/logo.svg" alt="Logo" class="logo" />
        <h1>DeepFake新闻真伪检测系统</h1>
      </div>

      <div class="user-menu">
        <el-dropdown trigger="click">
          <div class="user-info">
            <el-avatar :size="32" :src="userAvatar" />
            <span>{{ username }}</span>
            <el-icon><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="navigateTo('personal-center')">
                <el-icon><User /></el-icon> 个人中心
              </el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">
                <el-icon><SwitchButton /></el-icon> 退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>

    <div class="main-container">
      <!-- 侧边栏 -->
      <aside class="main-sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="dashboard">
            <el-icon><HomeFilled /></el-icon>
            <span>控制面板</span>
          </el-menu-item>

          <el-menu-item index="news-detection">
            <el-icon><Search /></el-icon>
            <span>新闻检测</span>
          </el-menu-item>

          <el-menu-item index="history-detection">
            <el-icon><List /></el-icon>
            <span>历史检测</span>
          </el-menu-item>

          <el-menu-item index="personal-center">
            <el-icon><Setting /></el-icon>
            <span>个人中心</span>
          </el-menu-item>
        </el-menu>

        <div class="sidebar-footer">
          <p>版本 v1.0.0</p>
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
        <div class="content-header">
          <h2>{{ pageTitle }}</h2>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/main' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ pageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="content-body">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const username = ref('用户')
const userAvatar = ref('https://via.placeholder.com/100')

// 根据当前路由设置活动菜单项
const activeMenu = computed(() => {
  const path = route.path
  if (path.includes('news-detection')) return 'news-detection'
  if (path.includes('history-detection')) return 'history-detection'
  if (path.includes('personal-center')) return 'personal-center'
  return 'dashboard'
})

// 根据活动菜单设置页面标题
const pageTitle = computed(() => {
  switch (activeMenu.value) {
    case 'news-detection': return '新闻检测'
    case 'history-detection': return '历史检测'
    case 'personal-center': return '个人中心'
    default: return '控制面板'
  }
})

const handleMenuSelect = (key) => {
  if (key === 'dashboard') {
    router.push('/main')
  } else {
    router.push(`/${key}`)
  }
}

const navigateTo = (path) => {
  router.push(`/${path}`)
}

const handleLogout = () => {
  ElMessageBox.confirm(
    '确定要退出登录吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    localStorage.removeItem('token')
    router.push('/login')
  }).catch(() => {})
}

const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    const response = await axios.get('http://127.0.0.1:5000/user/info', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (response.data.code === 200) {
      const data = response.data.data
      username.value = data.username
      if (data.avatar_url) {
        userAvatar.value = data.avatar_url
      }
    }
  } catch (err) {
    console.error('获取用户信息失败', err)
  }
}

onMounted(() => {
  fetchUserInfo()
})
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-header {
  height: 60px;
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 10;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  width: 36px;
  height: 36px;
  margin-right: 10px;
}

.logo-container h1 {
  font-size: 1.2rem;
  color: var(--primary-color);
  margin: 0;
}

.user-menu {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.user-info span {
  margin: 0 8px;
  font-size: 14px;
}

.main-container {
  display: flex;
  flex: 1;
}

.main-sidebar {
  width: 220px;
  background-color: white;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-footer {
  padding: 15px;
  text-align: center;
  font-size: 12px;
  color: var(--light-text);
  border-top: 1px solid var(--border-color);
}

.main-content {
  flex: 1;
  padding: 20px;
  background-color: var(--background-color);
  overflow-y: auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid var(--border-color);
}

.content-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--primary-color);
}

.content-body {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

@media (max-width: 768px) {
  .main-sidebar {
    width: 60px;
  }

  .main-sidebar .el-menu-item span {
    display: none;
  }

  .sidebar-footer {
    display: none;
  }
}
</style>
