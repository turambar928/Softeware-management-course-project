<template>
    <div class="page-wrapper">
      <div class="login-container">
        <h2>用户登录</h2>
        <input v-model="username" type="text" placeholder="用户名" />
        <input v-model="password" type="password" placeholder="密码" />
        <button @click="handleLogin">登录</button>
        <button class="register-button" @click="goToRegister">注册</button>
        <div v-if="message" class="message">{{ message }}</div>
        
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'

  const username = ref('')
  const password = ref('')
  const message = ref('')
  const router = useRouter()
  
  const handleLogin = async() => {
    if (!username.value || !password.value) {
      message.value = '请输入用户名和密码'
      return
    }
  
    // 模拟登录校验逻辑
    try {
      const formData = new URLSearchParams()
      formData.append('username', username.value)
      formData.append('password', password.value)

      const response = await axios.post('http://127.0.0.1:5000/user/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })

      if (response.data.code === 200) {
        message.value = '登录成功！'
        // 保存 token（可存在 localStorage 或 pinia）
        localStorage.setItem('token', response.data.data.token)
        localStorage.setItem('username',username.value)
        localStorage.setItem('password', password.value)
        router.push('/main')
      } else {
        message.value = response.data.message || '登录失败'
      }
    } catch (error) {
      console.error('登录失败，错误信息：', error)
      
      message.value = '登录请求失败，请检查网络或服务器'
    }
  }
  const goToRegister = () => {
    router.push('/register')
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

    .login-container {
      width: 300px;
      margin: 100px auto;
      padding: 2rem;
      border-radius: 12px;
      box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
      background: #fff;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .register-button {
      width: 100%;
      padding: 0.7rem;
      background-color: #67c23a;
      color: white;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      margin-top: 0.5rem;
    }
    .register-button:hover {
      background-color: #4caf50;
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
    }
    .success {
      color: green;
    }
    .error {
      color: red;
    }
  </style>
  