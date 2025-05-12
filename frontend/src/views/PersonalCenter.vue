<template>
  <div class="personal-center">
    <h2>个人中心</h2>

    <div class="profile">
      <div class="avatar-wrapper" @click="triggerAvatarSelect">
        <img :src="avatarUrl" alt="头像" class="avatar" />
      </div>
      <input type="file" ref="fileInput" @change="handleAvatarChange" accept="image/*" style="display: none;" />
    </div>

    <div class="info">
      <label>用户名：</label>
      <input v-model="editableUsername" />
    </div>

    <div class="info">
      <label>邮箱：</label>
      <input :value="email" disabled />
    </div>

    <button @click="saveChanges">保存修改</button>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'

const username = ref('')
const editableUsername = ref('')
const email = ref('')
const avatarUrl = ref('https://via.placeholder.com/100') // 默认头像
const fileInput = ref(null)
const message = ref('')

const triggerAvatarSelect = () => {
  fileInput.value.click()
}

const handleAvatarChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      avatarUrl.value = reader.result
    }
    reader.readAsDataURL(file)
  }
}

const fetchUserInfo = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:5000/user/info', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (response.data.code === 200) {
      const data = response.data.data
      username.value = data.username
      editableUsername.value = data.username
      email.value = data.email
      avatarUrl.value = data.avatar_url || 'https://via.placeholder.com/100'
    } else {
      message.value = response.data.message || '获取用户信息失败'
    }
  } catch (err) {
    message.value = '请求失败，请稍后重试'
    console.error('获取用户信息失败', err)
  }
}

const saveChanges = () => {
  username.value = editableUsername.value
  alert('修改已保存（前端展示，需实现更新接口）')
}

onMounted(() => {
  fetchUserInfo()
})
</script>


<style scoped>
.personal-center {
  padding: 20px;
  max-width: 500px;
}

.profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.avatar-wrapper {
  cursor: pointer;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #409eff;
  width: 100px;
  height: 100px;
  display: inline-block;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  margin-bottom: 1rem;
}

label {
  display: inline-block;
  width: 70px;
}

input[type="text"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  padding: 0.5rem 1rem;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #307ec7;
}
</style>
