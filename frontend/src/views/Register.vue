<template>
  <div class="page-wrapper">
    <div class="register-container">
    <h2>注册</h2>
    <input v-model="newUsername" placeholder="用户名" />
    <input type="password" v-model="newPassword" placeholder="密码" />
    <input type="password" v-model="confirmPassword" placeholder="确认密码" />
    <input v-model="email" placeholder="邮箱" />
    <button @click="handleRegister">注册</button>
    <p>{{ message }}</p>
  </div>
  </div>
</template>

  
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const newUsername = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const email = ref('')
const message = ref('')

const router = useRouter()

const handleRegister = async () => {
  if (!newUsername.value || !newPassword.value || !confirmPassword.value || !email.value) {
    message.value = '请填写所有字段'
    return
  }

  try {
    const formData = new FormData()
    formData.append('username', newUsername.value)
    formData.append('password', newPassword.value)
    formData.append('confirm_password', confirmPassword.value)
    formData.append('email', email.value)

    const response = await axios.post('http://127.0.0.1:5000/user/register', formData)

    if (response.data.code === 200) {
      message.value = '注册成功！返回登录界面...'
      setTimeout(() => {
        router.push('/')
      }, 1500)
    } else {
      message.value = response.data.data.content || '注册失败'
    }
  } catch (error) {
    message.value = '请求失败，请检查网络或后端服务'
  }
}
</script>

  
  <style scoped>
  .page-wrapper {
    background-image: url('../assets/background.jpg'); /* 替换成你的图片路径 */
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;     /* 不重复平铺 */
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .register-container {
    width: 300px;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    background: #fff;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  input {
    width: 100%;
    margin: 0.5rem 0;
    padding: 0.5rem;
    border-radius: 6px;
    border: 1px solid #ccc;
  }
  
  button {
    width: 100%;
    padding: 0.7rem;
    background-color: #409eff;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-top: 1rem;
  }
  
  button:hover {
    background-color: #307ec7;
  }
  
  .message {
    margin-top: 1rem;
    font-size: 0.9rem;
    color: green;
  }
  </style>
  