<template>
  <div class="personal-center">
    <el-row :gutter="20">
      <!-- 左侧个人信息卡片 -->
      <el-col :xs="24" :sm="24" :md="8" :lg="6">
        <el-card class="profile-card" shadow="hover">
          <div class="profile-header">
            <div class="avatar-container">
              <el-avatar :size="120" :src="avatarUrl" @error="handleAvatarError">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="avatar-overlay" @click="triggerAvatarSelect">
                <el-icon><Camera /></el-icon>
                <span>更换头像</span>
              </div>
              <input type="file" ref="fileInput" @change="handleAvatarChange" accept="image/*" style="display: none;" />
            </div>

            <h2 class="username">{{ username }}</h2>
            <p class="user-role">普通用户</p>

            <div class="user-stats">
              <div class="stat-item">
                <span class="stat-value">{{ userStats.detectionCount }}</span>
                <span class="stat-label">检测次数</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-value">{{ userStats.daysJoined }}</span>
                <span class="stat-label">加入天数</span>
              </div>
            </div>
          </div>

          <div class="profile-actions">
            <el-button type="primary" @click="handleLogout">
              <el-icon><SwitchButton /></el-icon> 退出登录
            </el-button>
          </div>
        </el-card>

        <!-- 帐号安全卡片 -->
        <el-card class="security-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><Lock /></el-icon>
              <span>帐号安全</span>
            </div>
          </template>

          <div class="security-items">
            <div class="security-item">
              <div class="security-item-info">
                <el-icon><Key /></el-icon>
                <span>修改密码</span>
              </div>
              <el-button text @click="showChangePasswordDialog">修改</el-button>
            </div>

            <div class="security-item">
              <div class="security-item-info">
                <el-icon><Message /></el-icon>
                <span>绑定手机号</span>
              </div>
              <el-tag v-if="userSecurity.phoneVerified" type="success" size="small">已绑定</el-tag>
              <el-button v-else text @click="showBindPhoneDialog">绑定</el-button>
            </div>

            <div class="security-item">
              <div class="security-item-info">
                <el-icon><Connection /></el-icon>
                <span>两步验证</span>
              </div>
              <el-switch v-model="userSecurity.twoFactorEnabled" @change="handleTwoFactorChange" />
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧内容区 -->
      <el-col :xs="24" :sm="24" :md="16" :lg="18">
        <el-card class="main-card">
          <template #header>
            <div class="card-header">
              <el-icon><Setting /></el-icon>
              <span>个人设置</span>
            </div>
          </template>

          <el-tabs v-model="activeTab">
            <!-- 基本信息标签页 -->
            <el-tab-pane label="基本信息" name="basic">
              <el-form
                ref="basicFormRef"
                :model="basicForm"
                :rules="basicRules"
                label-width="100px"
                status-icon
              >
                <el-form-item label="用户名" prop="username">
                  <el-input v-model="basicForm.username" placeholder="请输入用户名" />
                </el-form-item>

                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="basicForm.email" placeholder="请输入邮箱" disabled />
                  <template #append>
                    <el-button @click="showChangeEmailDialog">修改</el-button>
                  </template>
                </el-form-item>

                <el-form-item label="昵称" prop="nickname">
                  <el-input v-model="basicForm.nickname" placeholder="请输入昵称" />
                </el-form-item>

                <el-form-item label="个人简介">
                  <el-input
                    v-model="basicForm.bio"
                    type="textarea"
                    :rows="4"
                    placeholder="请输入个人简介"
                  />
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="saveBasicInfo" :loading="saving">
                    <el-icon><Check /></el-icon> 保存修改
                  </el-button>
                  <el-button @click="resetBasicForm">
                    <el-icon><Refresh /></el-icon> 重置
                  </el-button>
                </el-form-item>
              </el-form>
            </el-tab-pane>

            <!-- 通知设置标签页 -->
            <el-tab-pane label="通知设置" name="notifications">
              <div class="notification-settings">
                <div class="setting-item">
                  <div class="setting-info">
                    <h3>系统通知</h3>
                    <p>接收系统更新、维护和安全提醒</p>
                  </div>
                  <el-switch v-model="notificationSettings.system" />
                </div>

                <div class="setting-item">
                  <div class="setting-info">
                    <h3>检测结果通知</h3>
                    <p>当新闻检测完成时发送通知</p>
                  </div>
                  <el-switch v-model="notificationSettings.detection" />
                </div>

                <div class="setting-item">
                  <div class="setting-info">
                    <h3>邮件通知</h3>
                    <p>将通知发送到您的邮箱</p>
                  </div>
                  <el-switch v-model="notificationSettings.email" />
                </div>

                <div class="setting-actions">
                  <el-button type="primary" @click="saveNotificationSettings" :loading="saving">
                    <el-icon><Check /></el-icon> 保存设置
                  </el-button>
                </div>
              </div>
            </el-tab-pane>

            <!-- 检测历史标签页 -->
            <el-tab-pane label="检测历史" name="history">
              <div class="detection-history">
                <div class="history-header">
                  <h3>最近的检测</h3>
                  <el-button text type="primary" @click="viewAllHistory">
                    查看全部 <el-icon><ArrowRight /></el-icon>
                  </el-button>
                </div>

                <el-empty v-if="recentDetections.length === 0" description="暂无检测记录" />

                <el-timeline v-else>
                  <el-timeline-item
                    v-for="(detection, index) in recentDetections"
                    :key="index"
                    :type="detection.isReal ? 'success' : 'danger'"
                    :timestamp="formatTime(detection.time)"
                  >
                    <el-card class="timeline-card">
                      <div class="detection-item">
                        <div class="detection-content">
                          <p>{{ detection.content }}</p>
                        </div>
                        <div class="detection-result">
                          <el-tag :type="detection.isReal ? 'success' : 'danger'">
                            {{ detection.isReal ? '真实新闻' : '虚假新闻' }}
                          </el-tag>
                          <el-button text size="small" @click="viewDetectionDetail(detection)">查看详情</el-button>
                        </div>
                      </div>
                    </el-card>
                  </el-timeline-item>
                </el-timeline>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
    </el-row>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="passwordDialogVisible"
      title="修改密码"
      width="30%"
      destroy-on-close
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="当前密码" prop="currentPassword">
          <el-input
            v-model="passwordForm.currentPassword"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="changePassword" :loading="saving">确认修改</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 绑定手机对话框 -->
    <el-dialog
      v-model="phoneDialogVisible"
      title="绑定手机号"
      width="30%"
      destroy-on-close
    >
      <el-form
        ref="phoneFormRef"
        :model="phoneForm"
        :rules="phoneRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="phoneForm.phone" placeholder="请输入手机号" />
        </el-form-item>

        <el-form-item label="验证码" prop="code">
          <el-input v-model="phoneForm.code" placeholder="请输入验证码">
            <template #append>
              <el-button :disabled="countdown > 0" @click="sendVerificationCode">
                {{ countdown > 0 ? `${countdown}s后重试` : '获取验证码' }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="phoneDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="bindPhone" :loading="saving">确认绑定</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 修改邮箱对话框 -->
    <el-dialog
      v-model="emailDialogVisible"
      title="修改邮箱"
      width="30%"
      destroy-on-close
    >
      <el-form
        ref="emailFormRef"
        :model="emailForm"
        :rules="emailRules"
        label-width="100px"
        status-icon
      >
        <el-form-item label="当前邮箱">
          <el-input v-model="email" disabled />
        </el-form-item>

        <el-form-item label="新邮箱" prop="newEmail">
          <el-input v-model="emailForm.newEmail" placeholder="请输入新邮箱" />
        </el-form-item>

        <el-form-item label="验证码" prop="code">
          <el-input v-model="emailForm.code" placeholder="请输入验证码">
            <template #append>
              <el-button :disabled="emailCountdown > 0" @click="sendEmailVerificationCode">
                {{ emailCountdown > 0 ? `${emailCountdown}s后重试` : '获取验证码' }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="emailDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="changeEmail" :loading="saving">确认修改</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const router = useRouter()

// 基本信息
const username = ref('')
const email = ref('')
const avatarUrl = ref('https://via.placeholder.com/100') // 默认头像
const fileInput = ref(null)
const saving = ref(false)
const activeTab = ref('basic')

// 表单引用
const basicFormRef = ref(null)
const passwordFormRef = ref(null)
const phoneFormRef = ref(null)
const emailFormRef = ref(null)

// 对话框状态
const passwordDialogVisible = ref(false)
const phoneDialogVisible = ref(false)
const emailDialogVisible = ref(false)

// 倒计时
const countdown = ref(0)
const emailCountdown = ref(0)
const countdownTimer = ref(null)
const emailCountdownTimer = ref(null)

// 用户统计信息
const userStats = reactive({
  detectionCount: 0,
  daysJoined: 0
})

// 用户安全信息
const userSecurity = reactive({
  phoneVerified: false,
  twoFactorEnabled: false
})

// 基本信息表单
const basicForm = reactive({
  username: '',
  email: '',
  nickname: '',
  bio: ''
})

// 密码表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 手机表单
const phoneForm = reactive({
  phone: '',
  code: ''
})

// 邮箱表单
const emailForm = reactive({
  newEmail: '',
  code: ''
})

// 通知设置
const notificationSettings = reactive({
  system: true,
  detection: true,
  email: false
})

// 最近检测记录
const recentDetections = ref([])

// 表单验证规则
const basicRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  nickname: [
    { max: 30, message: '长度不能超过 30 个字符', trigger: 'blur' }
  ]
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const phoneRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '验证码为6位数字', trigger: 'blur' }
  ]
}

const emailRules = {
  newEmail: [
    { required: true, message: '请输入新邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { pattern: /^\d{6}$/, message: '验证码为6位数字', trigger: 'blur' }
  ]
}

// 方法
const triggerAvatarSelect = () => {
  fileInput.value.click()
}

const handleAvatarChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      avatarUrl.value = reader.result
      // 这里可以添加上传头像到服务器的逻辑
      ElMessage.success('头像已更新')
    }
    reader.readAsDataURL(file)
  }
}

const handleAvatarError = () => {
  // 头像加载失败时显示默认头像
  avatarUrl.value = 'https://via.placeholder.com/100'
}

const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    // 尝试从后端获取数据
    try {
      const response = await axios.get('http://127.0.0.1:5000/user/info', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (response.data.code === 200) {
        const data = response.data.data
        username.value = data.username
        email.value = data.email
        avatarUrl.value = data.avatar_url || 'https://via.placeholder.com/100'

        // 填充表单数据
        basicForm.username = data.username
        basicForm.email = data.email
        basicForm.nickname = data.nickname || ''
        basicForm.bio = data.bio || ''
      } else {
        // 如果API返回错误，使用模拟数据
        generateMockUserData()
      }
    } catch (error) {
      console.error('获取用户信息失败', error)
      // 如果请求失败，使用模拟数据
      generateMockUserData()
    }

    // 获取用户统计信息
    fetchUserStats()

    // 获取最近检测记录
    fetchRecentDetections()
  } catch (err) {
    console.error('初始化失败', err)
    ElMessage.error('加载用户信息失败')
  }
}

const generateMockUserData = () => {
  // 生成模拟用户数据
  username.value = 'demo_user'
  email.value = 'demo@example.com'
  avatarUrl.value = 'https://via.placeholder.com/100'

  // 填充表单数据
  basicForm.username = 'demo_user'
  basicForm.email = 'demo@example.com'
  basicForm.nickname = '演示用户'
  basicForm.bio = '这是一个演示账号，用于展示个人中心功能。'

  // 模拟用户统计
  userStats.detectionCount = 28
  userStats.daysJoined = 15

  // 模拟安全信息
  userSecurity.phoneVerified = false
  userSecurity.twoFactorEnabled = false
}

const fetchUserStats = async () => {
  // 这里应该调用后端API获取用户统计信息
  // 由于后端可能没有这个接口，这里使用模拟数据

  // 模拟数据
  userStats.detectionCount = 28

  // 计算加入天数
  const now = new Date()
  const joinDate = new Date(now.getTime() - Math.random() * 90 * 24 * 60 * 60 * 1000) // 随机1-90天前加入
  const diffTime = Math.abs(now - joinDate)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  userStats.daysJoined = diffDays
}

const fetchRecentDetections = async () => {
  // 这里应该调用后端API获取最近检测记录
  // 由于后端可能没有这个接口，这里使用模拟数据

  // 生成模拟数据
  const mockDetections = []
  const contents = [
    '中国经济增长超出预期，第二季度GDP同比增长6.3%',
    '科学家发现新型可再生能源，有望解决能源危机',
    '国际会议达成气候变化新协议，全球承诺减排',
    '新研究表明健康饮食习惯可显著降低心血管疾病风险',
    '技术公司宣布突破性人工智能研发，股价大涨',
  ]

  // 生成5条模拟记录
  for (let i = 0; i < 5; i++) {
    const isReal = Math.random() > 0.3
    const date = new Date()
    date.setDate(date.getDate() - i) // 最近几天的记录

    mockDetections.push({
      id: i + 1,
      time: date.toISOString(),
      content: contents[i],
      isReal: isReal,
      result: isReal ? '真实' : '虚假',
    })
  }

  recentDetections.value = mockDetections
}

const saveBasicInfo = async () => {
  if (!basicFormRef.value) return

  await basicFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true

      try {
        // 这里应该调用后端API保存用户信息
        // const token = localStorage.getItem('token')
        // await axios.post('http://127.0.0.1:5000/user/update', basicForm, {
        //   headers: { Authorization: `Bearer ${token}` }
        // })

        // 模拟保存成功
        setTimeout(() => {
          username.value = basicForm.username
          ElMessage.success('个人信息已更新')
          saving.value = false
        }, 1000)
      } catch (error) {
        console.error('保存失败', error)
        ElMessage.error('保存失败，请重试')
        saving.value = false
      }
    }
  })
}

const resetBasicForm = () => {
  if (basicFormRef.value) {
    basicFormRef.value.resetFields()
  }
}

const saveNotificationSettings = async () => {
  saving.value = true

  try {
    // 这里应该调用后端API保存通知设置
    // const token = localStorage.getItem('token')
    // await axios.post('http://127.0.0.1:5000/user/notifications', notificationSettings, {
    //   headers: { Authorization: `Bearer ${token}` }
    // })

    // 模拟保存成功
    setTimeout(() => {
      ElMessage.success('通知设置已更新')
      saving.value = false
    }, 1000)
  } catch (error) {
    console.error('保存失败', error)
    ElMessage.error('保存失败，请重试')
    saving.value = false
  }
}

const showChangePasswordDialog = () => {
  passwordDialogVisible.value = true
  passwordForm.currentPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
}

const changePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true

      try {
        // 这里应该调用后端API修改密码
        // const token = localStorage.getItem('token')
        // await axios.post('http://127.0.0.1:5000/user/change-password', {
        //   current_password: passwordForm.currentPassword,
        //   new_password: passwordForm.newPassword
        // }, {
        //   headers: { Authorization: `Bearer ${token}` }
        // })

        // 模拟修改成功
        setTimeout(() => {
          ElMessage.success('密码已修改，请使用新密码登录')
          passwordDialogVisible.value = false
          saving.value = false

          // 退出登录，重新登录
          setTimeout(() => {
            handleLogout()
          }, 1500)
        }, 1000)
      } catch (error) {
        console.error('修改密码失败', error)
        ElMessage.error('修改密码失败，请重试')
        saving.value = false
      }
    }
  })
}

const showBindPhoneDialog = () => {
  phoneDialogVisible.value = true
  phoneForm.phone = ''
  phoneForm.code = ''
}

const sendVerificationCode = () => {
  if (!phoneForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }

  if (!/^1[3-9]\d{9}$/.test(phoneForm.phone)) {
    ElMessage.warning('请输入正确的手机号')
    return
  }

  // 开始倒计时
  countdown.value = 60
  countdownTimer.value = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer.value)
    }
  }, 1000)

  // 这里应该调用后端API发送验证码
  ElMessage.success(`验证码已发送至 ${phoneForm.phone}`)
}

const bindPhone = async () => {
  if (!phoneFormRef.value) return

  await phoneFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true

      try {
        // 这里应该调用后端API绑定手机
        // const token = localStorage.getItem('token')
        // await axios.post('http://127.0.0.1:5000/user/bind-phone', phoneForm, {
        //   headers: { Authorization: `Bearer ${token}` }
        // })

        // 模拟绑定成功
        setTimeout(() => {
          userSecurity.phoneVerified = true
          ElMessage.success('手机号绑定成功')
          phoneDialogVisible.value = false
          saving.value = false
        }, 1000)
      } catch (error) {
        console.error('绑定失败', error)
        ElMessage.error('绑定失败，请重试')
        saving.value = false
      }
    }
  })
}

const showChangeEmailDialog = () => {
  emailDialogVisible.value = true
  emailForm.newEmail = ''
  emailForm.code = ''
}

const sendEmailVerificationCode = () => {
  if (!emailForm.newEmail) {
    ElMessage.warning('请先输入新邮箱')
    return
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(emailForm.newEmail)) {
    ElMessage.warning('请输入正确的邮箱地址')
    return
  }

  // 开始倒计时
  emailCountdown.value = 60
  emailCountdownTimer.value = setInterval(() => {
    emailCountdown.value--
    if (emailCountdown.value <= 0) {
      clearInterval(emailCountdownTimer.value)
    }
  }, 1000)

  // 这里应该调用后端API发送验证码
  ElMessage.success(`验证码已发送至 ${emailForm.newEmail}`)
}

const changeEmail = async () => {
  if (!emailFormRef.value) return

  await emailFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true

      try {
        // 这里应该调用后端API修改邮箱
        // const token = localStorage.getItem('token')
        // await axios.post('http://127.0.0.1:5000/user/change-email', emailForm, {
        //   headers: { Authorization: `Bearer ${token}` }
        // })

        // 模拟修改成功
        setTimeout(() => {
          email.value = emailForm.newEmail
          basicForm.email = emailForm.newEmail
          ElMessage.success('邮箱修改成功')
          emailDialogVisible.value = false
          saving.value = false
        }, 1000)
      } catch (error) {
        console.error('修改失败', error)
        ElMessage.error('修改失败，请重试')
        saving.value = false
      }
    }
  })
}

const handleTwoFactorChange = (value) => {
  if (value && !userSecurity.phoneVerified) {
    ElMessage.warning('启用两步验证前，请先绑定手机号')
    userSecurity.twoFactorEnabled = false
    return
  }

  // 这里应该调用后端API更新两步验证设置
  ElMessage.success(value ? '两步验证已启用' : '两步验证已关闭')
}

const viewAllHistory = () => {
  router.push('/history-detection')
}

const viewDetectionDetail = (detection) => {
  // 这里可以实现查看详情的逻辑，例如打开一个对话框或导航到详情页
  router.push(`/history-detection?id=${detection.id}`)
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

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  return date.toLocaleString()
}

// 生命周期钩子
onMounted(() => {
  fetchUserInfo()
})
</script>


<style scoped>
.personal-center {
  padding: 0;
}

/* 左侧个人信息卡片 */
.profile-card {
  margin-bottom: 20px;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.avatar-container {
  position: relative;
  margin-bottom: 20px;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
  color: white;
}

.avatar-overlay:hover {
  opacity: 1;
}

.avatar-overlay .el-icon {
  font-size: 24px;
  margin-bottom: 5px;
}

.username {
  font-size: 1.5rem;
  margin: 10px 0 5px;
  color: var(--primary-color);
}

.user-role {
  color: var(--light-text);
  margin: 0 0 15px;
  font-size: 0.9rem;
}

.user-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 15px 0;
  border-top: 1px solid var(--border-color);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0 20px;
}

.stat-divider {
  width: 1px;
  height: 30px;
  background-color: var(--border-color);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--light-text);
  margin-top: 5px;
}

.profile-actions {
  display: flex;
  justify-content: center;
  padding: 15px 0;
  border-top: 1px solid var(--border-color);
}

/* 帐号安全卡片 */
.security-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
}

.card-header .el-icon {
  margin-right: 8px;
  font-size: 18px;
}

.security-items {
  padding: 10px 0;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color);
}

.security-item:last-child {
  border-bottom: none;
}

.security-item-info {
  display: flex;
  align-items: center;
}

.security-item-info .el-icon {
  margin-right: 10px;
  font-size: 18px;
  color: var(--primary-color);
}

/* 主卡片内容 */
.main-card {
  height: 100%;
}

/* 通知设置 */
.notification-settings {
  padding: 10px 0;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid var(--border-color);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info h3 {
  margin: 0 0 5px 0;
  font-size: 16px;
  color: var(--primary-color);
}

.setting-info p {
  margin: 0;
  color: var(--light-text);
  font-size: 14px;
}

.setting-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 检测历史 */
.detection-history {
  padding: 10px 0;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--primary-color);
}

.timeline-card {
  margin-bottom: 10px;
}

.detection-item {
  display: flex;
  flex-direction: column;
}

.detection-content {
  margin-bottom: 10px;
}

.detection-content p {
  margin: 0;
  line-height: 1.5;
}

.detection-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .el-row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .el-col {
    padding-left: 0 !important;
    padding-right: 0 !important;
  }

  .profile-card,
  .security-card,
  .main-card {
    margin-bottom: 15px;
  }

  .setting-item,
  .security-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .setting-info,
  .security-item-info {
    margin-bottom: 10px;
  }

  .detection-result {
    flex-direction: column;
    align-items: flex-start;
  }

  .detection-result .el-tag {
    margin-bottom: 10px;
  }
}
</style>
