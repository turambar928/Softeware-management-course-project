import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import Dashboard from '../views/Dashboard.vue'
import PersonalCenter from '../views/PersonalCenter.vue'
import NewsDetection from '../views/NewsDetection.vue'
import HistoryDetection from '../views/HistoryDetection.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'

const routes = [
  { path: '/', redirect: '/login' },
  {
    path: '/main',
    component: MainPage,
    children: [
      { path: '', component: Dashboard }, // 默认显示仪表盘
      { path: '/personal-center', component: PersonalCenter },  // 个人中心
      { path: '/news-detection', component: NewsDetection },  // 新闻检测
      { path: '/history-detection', component: HistoryDetection },  // 历史检测
    ]
  },
  { path: '/login', component: Login},
  { path: '/register', component: Register },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
