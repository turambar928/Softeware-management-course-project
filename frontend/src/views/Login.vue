<template>
  <div class="login-page">
    <div class="login-content">
      <!-- 左侧信息区 -->
      <div class="info-section">
        <div class="logo-container">
          <img src="../assets/images/logo.svg" alt="Logo" class="logo" />
          <h1 class="app-name">DeepFake新闻真伪检测系统</h1>
        </div>

        <div class="features">
          <div class="feature-item">
            <el-icon class="feature-icon"><Shield /></el-icon>
            <div class="feature-text">
              <h3>专业检测</h3>
              <p>采用先进的人工智能技术，精准识别虚假新闻</p>
            </div>
          </div>

          <div class="feature-item">
            <el-icon class="feature-icon"><DataAnalysis /></el-icon>
            <div class="feature-text">
              <h3>数据分析</h3>
              <p>提供详细分析报告，帮助理解检测结果</p>
            </div>
          </div>

          <div class="feature-item">
            <el-icon class="feature-icon"><Lock /></el-icon>
            <div class="feature-text">
              <h3>安全可靠</h3>
              <p>保护您的数据安全，确保检测结果准确可靠</p>
            </div>
          </div>
        </div>

        <div class="copyright">
          <p>&copy; 2025 DeepFake新闻真伪检测系统 - 保护您的信息安全</p>
        </div>
      </div>

      <!-- 右侧登录区 -->
      <div class="login-section">
        <div class="login-card">
          <div class="login-header">
            <h2>欢迎登录</h2>
            <p class="login-subtitle">请使用您的账号登录系统</p>
          </div>

          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名"
                prefix-icon="User"
                clearable
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                prefix-icon="Lock"
                show-password
                clearable
              />
            </el-form-item>

            <div class="form-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a href="#" class="forgot-link">忘记密码?</a>
            </div>

            <el-form-item>
              <el-button
                type="primary"
                class="login-button"
                :loading="loading"
                @click="handleLogin"
              >
                <el-icon v-if="!loading"><Right /></el-icon>
                <span>登录</span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="register-section">
            <p>还没有账号？</p>
            <el-button type="success" plain @click="goToRegister">
              <el-icon><Plus /></el-icon> 注册新账号
            </el-button>
          </div>

          <el-alert
            v-if="errorMessage"
            :title="errorMessage"
            type="error"
            show-icon
            :closable="true"
            @close="errorMessage = ''"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)
const errorMessage = ref('')

// 登录表单
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      errorMessage.value = ''

      try {
        const formData = new URLSearchParams()
        formData.append('username', loginForm.username)
        formData.append('password', loginForm.password)

        const response = await axios.post('http://127.0.0.1:5000/user/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        if (response.data.code === 200) {
          ElMessage.success('登录成功！')

          // 保存 token
          localStorage.setItem('token', response.data.data.token)

          // 如果选择了记住我，则保存用户名
          if (rememberMe.value) {
            localStorage.setItem('username', loginForm.username)
          } else {
            localStorage.removeItem('username')
          }

          // 跳转到主页
          router.push('/main')
        } else {
          errorMessage.value = response.data.message || '登录失败，请检查用户名和密码'
        }
      } catch (error) {
        console.error('登录失败，错误信息：', error)
        errorMessage.value = '登录请求失败，请检查网络或服务器'
      } finally {
        loading.value = false
      }
    }
  })
}

// 跳转到注册页面
const goToRegister = () => {
  router.push('/register')
}

// 生命周期钩子
onMounted(() => {
  // 如果之前选择了记住我，自动填充用户名
  const savedUsername = localStorage.getItem('username')
  if (savedUsername) {
    loginForm.username = savedUsername
    rememberMe.value = true
  }
})
  </script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.login-content {
  display: flex;
  width: 100%;
  max-width: 1200px;
  min-height: 600px;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

/* 左侧信息区样式 */
.info-section {
  flex: 1;
  background-color: var(--primary-color);
  color: white;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.logo-container {
  display: flex;
  align-items: center;
  margin-bottom: 40px;
}

.logo {
  width: 50px;
  height: 50px;
  margin-right: 15px;
}

.app-name {
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.features {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 30px;
}

.feature-icon {
  font-size: 24px;
  margin-right: 15px;
  color: var(--accent-color);
}

.feature-text h3 {
  margin: 0 0 10px 0;
  font-size: 1.2rem;
}

.feature-text p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.8;
  line-height: 1.5;
}

.copyright {
  font-size: 0.8rem;
  opacity: 0.7;
  text-align: center;
  margin-top: 40px;
}

/* 右侧登录区样式 */
.login-section {
  flex: 1;
  padding: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 0 0 10px 0;
}

.login-subtitle {
  color: var(--light-text);
  margin: 0;
}

.login-form {
  margin-bottom: 20px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.forgot-link {
  color: var(--secondary-color);
  text-decoration: none;
  font-size: 0.9rem;
}

.forgot-link:hover {
  text-decoration: underline;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 1rem;
}

.register-section {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.register-section p {
  margin-bottom: 15px;
  color: var(--light-text);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .login-content {
    flex-direction: column;
  }

  .info-section {
    padding: 30px 20px;
  }

  .login-section {
    padding: 30px 20px;
  }

  .features {
    margin: 20px 0;
  }

  .feature-item {
    margin-bottom: 20px;
  }
}
</style>
