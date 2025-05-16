<template>
  <div class="register-page">
    <div class="register-content">
      <!-- 左侧信息区 -->
      <div class="info-section">
        <div class="logo-container">
          <img src="../assets/images/logo.svg" alt="Logo" class="logo" />
          <h1 class="app-name">DeepFake新闻真伪检测系统</h1>
        </div>

        <div class="welcome-section">
          <h2>欢迎加入我们</h2>
          <p class="welcome-text">注册账号后，您将获得以下功能：</p>

          <ul class="benefits-list">
            <li>
              <el-icon><Check /></el-icon>
              <span>新闻真伪智能检测</span>
            </li>
            <li>
              <el-icon><Check /></el-icon>
              <span>检测历史记录管理</span>
            </li>
            <li>
              <el-icon><Check /></el-icon>
              <span>个性化检测报告</span>
            </li>
            <li>
              <el-icon><Check /></el-icon>
              <span>多平台同步访问</span>
            </li>
          </ul>
        </div>

        <div class="copyright">
          <p>&copy; 2025 DeepFake新闻真伪检测系统 - 保护您的信息安全</p>
        </div>
      </div>

      <!-- 右侧注册区 -->
      <div class="register-section">
        <div class="register-card">
          <div class="register-header">
            <h2>创建账号</h2>
            <p class="register-subtitle">请填写以下信息完成注册</p>
          </div>

          <el-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            class="register-form"
            status-icon
          >
            <el-form-item prop="username">
              <el-input
                v-model="registerForm.username"
                placeholder="用户名"
                prefix-icon="User"
                clearable
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="registerForm.password"
                type="password"
                placeholder="密码"
                prefix-icon="Lock"
                show-password
                clearable
              />
            </el-form-item>

            <el-form-item prop="confirmPassword">
              <el-input
                v-model="registerForm.confirmPassword"
                type="password"
                placeholder="确认密码"
                prefix-icon="Lock"
                show-password
                clearable
              />
            </el-form-item>

            <el-form-item prop="email">
              <el-input
                v-model="registerForm.email"
                placeholder="邮箱"
                prefix-icon="Message"
                clearable
              />
            </el-form-item>

            <el-form-item>
              <el-checkbox v-model="agreeTerms">我已阅读并同意<a href="#" class="terms-link">用户协议</a>和<a href="#" class="terms-link">隐私政策</a></el-checkbox>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                class="register-button"
                :loading="loading"
                :disabled="!agreeTerms"
                @click="handleRegister"
              >
                <el-icon v-if="!loading"><UserPlus /></el-icon>
                <span>注册</span>
              </el-button>
            </el-form-item>
          </el-form>

          <div class="login-section">
            <p>已有账号？</p>
            <el-button type="info" plain @click="goToLogin">
              <el-icon><Right /></el-icon> 返回登录
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

          <el-alert
            v-if="successMessage"
            :title="successMessage"
            type="success"
            show-icon
            :closable="true"
            @close="successMessage = ''"
          />
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)
const agreeTerms = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

// 注册表单
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  email: ''
})

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 处理注册
const handleRegister = async () => {
  if (!agreeTerms.value) {
    ElMessage.warning('请阅读并同意用户协议和隐私政策')
    return
  }

  if (!registerFormRef.value) return

  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        const formData = new FormData()
        formData.append('username', registerForm.username)
        formData.append('password', registerForm.password)
        formData.append('confirm_password', registerForm.confirmPassword)
        formData.append('email', registerForm.email)

        const response = await axios.post('http://127.0.0.1:5000/user/register', formData)

        if (response.data.code === 200) {
          successMessage.value = '注册成功！正在返回登录界面...'

          // 清空表单
          registerFormRef.value.resetFields()

          // 延时跳转到登录页面
          setTimeout(() => {
            router.push('/login')
          }, 2000)
        } else {
          errorMessage.value = response.data.data?.content || response.data.message || '注册失败'
        }
      } catch (error) {
        console.error('注册失败，错误信息：', error)
        errorMessage.value = '请求失败，请检查网络或后端服务'
      } finally {
        loading.value = false
      }
    }
  })
}

// 跳转到登录页面
const goToLogin = () => {
  router.push('/login')
}
</script>


<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.register-content {
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

.welcome-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.welcome-section h2 {
  font-size: 2rem;
  margin: 0 0 20px 0;
}

.welcome-text {
  font-size: 1rem;
  margin-bottom: 30px;
  opacity: 0.8;
}

.benefits-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.benefits-list li {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
  font-size: 1rem;
}

.benefits-list li .el-icon {
  margin-right: 10px;
  color: var(--accent-color);
  font-size: 18px;
}

.copyright {
  font-size: 0.8rem;
  opacity: 0.7;
  text-align: center;
  margin-top: 40px;
}

/* 右侧注册区样式 */
.register-section {
  flex: 1;
  padding: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-card {
  width: 100%;
  max-width: 400px;
}

.register-header {
  text-align: center;
  margin-bottom: 30px;
}

.register-header h2 {
  font-size: 1.8rem;
  color: var(--primary-color);
  margin: 0 0 10px 0;
}

.register-subtitle {
  color: var(--light-text);
  margin: 0;
}

.register-form {
  margin-bottom: 20px;
}

.terms-link {
  color: var(--secondary-color);
  text-decoration: none;
}

.terms-link:hover {
  text-decoration: underline;
}

.register-button {
  width: 100%;
  height: 44px;
  font-size: 1rem;
  margin-top: 10px;
}

.login-section {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.login-section p {
  margin-bottom: 15px;
  color: var(--light-text);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .register-content {
    flex-direction: column;
  }

  .info-section {
    padding: 30px 20px;
  }

  .register-section {
    padding: 30px 20px;
  }

  .welcome-section {
    margin: 20px 0;
  }

  .benefits-list li {
    margin-bottom: 10px;
  }
}
</style>
