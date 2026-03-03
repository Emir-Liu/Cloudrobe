<template>
  <view class="login-page">
    <!-- 顶部区域 -->
    <view class="header">
      <view class="logo">云衣橱</view>
      <view class="subtitle">让闲置衣物创造价值</view>
    </view>

    <!-- 登录表单 -->
    <view class="form-container">
      <!-- 切换 -->
      <view class="tabs">
        <view 
          class="tab-item" 
          :class="{ active: loginType === 'phone' }"
          @tap="loginType = 'phone'"
        >
          手机登录
        </view>
        <view 
          class="tab-item" 
          :class="{ active: loginType === 'wechat' }"
          @tap="loginType = 'wechat'"
        >
          微信登录
        </view>
      </view>

      <!-- 手机号登录 -->
      <view v-if="loginType === 'phone'" class="login-form">
        <view class="form-item">
          <input 
            v-model="phone" 
            type="number" 
            maxlength="11" 
            placeholder="请输入手机号" 
            class="input"
          />
        </view>

        <view class="form-item code-item">
          <input 
            v-model="code" 
            type="number" 
            maxlength="6" 
            placeholder="请输入验证码" 
            class="input code-input"
          />
          <button 
            class="code-btn" 
            :disabled="countdown > 0" 
            @tap="sendCode"
          >
            {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
          </button>
        </view>

        <button class="login-btn primary" @tap="handleLogin" :loading="loading">
          登录
        </button>

        <view class="register-tip">
          没有账号？
          <text class="link" @tap="isRegister = true">立即注册</text>
        </view>
      </view>

      <!-- 微信登录 -->
      <view v-else class="wechat-login">
        <view class="wechat-tip">使用微信快速登录</view>
        <!-- #ifdef MP-WEIXIN -->
        <button class="wechat-btn" open-type="getUserInfo" @getuserinfo="handleWechatLogin">
          <text class="icon">📱</text> 微信一键登录
        </button>
        <!-- #endif -->
        <!-- #ifndef MP-WEIXIN -->
        <view class="tip">微信登录仅在小程序中可用</view>
        <!-- #endif -->
      </view>
    </view>

    <!-- 用户协议 -->
    <view class="agreement">
      登录即表示同意
      <text class="link">《用户协议》</text>
      和
      <text class="link">《隐私政策》</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// 状态
const loginType = ref<'phone' | 'wechat'>('phone')
const phone = ref('')
const code = ref('')
const countdown = ref(0)
const loading = ref(false)
const isRegister = ref(false)

// 发送验证码
const sendCode = async () => {
  if (!phone.value || phone.value.length !== 11) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
    return
  }

  try {
    await userStore.sendSms(phone.value)
    uni.showToast({ title: '验证码已发送', icon: 'success' })
    
    // 倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error: any) {
    uni.showToast({ title: error.message || '发送失败', icon: 'none' })
  }
}

// 登录
const handleLogin = async () => {
  if (!phone.value || phone.value.length !== 11) {
    uni.showToast({ title: '请输入正确的手机号', icon: 'none' })
    return
  }

  if (!code.value || code.value.length !== 6) {
    uni.showToast({ title: '请输入验证码', icon: 'none' })
    return
  }

  loading.value = true
  try {
    if (isRegister.value) {
      // 注册
      await userStore.register({ 
        phone: phone.value, 
        code: code.value 
      })
      uni.showToast({ title: '注册成功', icon: 'success' })
    } else {
      // 登录
      await userStore.loginByPhone(phone.value, code.value)
      uni.showToast({ title: '登录成功', icon: 'success' })
    }

    // 跳转到首页
    setTimeout(() => {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
  } catch (error: any) {
    uni.showToast({ title: error.message || '登录失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

// 微信登录
const handleWechatLogin = async (e: any) => {
  try {
    await userStore.loginByWechat()
    uni.showToast({ title: '登录成功', icon: 'success' })
    
    setTimeout(() => {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }, 1500)
  } catch (error: any) {
    uni.showToast({ title: error.message || '登录失败', icon: 'none' })
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  padding: 0 32rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(135deg, #FFF5F8 0%, #F0F8FF 100%);
}

.header {
  margin-top: 120rpx;
  margin-bottom: 80rpx;
  text-align: center;
}

.logo {
  font-size: 64rpx;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 16rpx;
}

.subtitle {
  font-size: 28rpx;
  color: var(--text-secondary);
}

.form-container {
  width: 100%;
  background: var(--bg-white);
  border-radius: var(--radius-lg);
  padding: 48rpx 32rpx;
  box-shadow: var(--shadow-md);
}

.tabs {
  display: flex;
  margin-bottom: 48rpx;
}

.tab-item {
  flex: 1;
  text-align: center;
  font-size: 32rpx;
  color: var(--text-secondary);
  position: relative;
  padding-bottom: 16rpx;
  
  &.active {
    color: var(--primary-color);
    font-weight: 600;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 60rpx;
      height: 4rpx;
      background: var(--primary-color);
      border-radius: 2rpx;
    }
  }
}

.form-item {
  margin-bottom: 32rpx;
}

.input {
  width: 100%;
  height: 88rpx;
  padding: 0 24rpx;
  border: 2rpx solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 32rpx;
  
  &:focus {
    border-color: var(--primary-color);
  }
}

.code-item {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.code-input {
  flex: 1;
}

.code-btn {
  width: 200rpx;
  height: 88rpx;
  font-size: 28rpx;
  color: var(--primary-color);
  background: var(--bg-gray);
  
  &[disabled] {
    color: var(--text-tertiary);
  }
}

.login-btn {
  width: 100%;
  height: 96rpx;
  margin-top: 32rpx;
  font-size: 32rpx;
  color: var(--bg-white);
  background: var(--primary-color);
  border-radius: var(--btn-border-radius);
}

.register-tip {
  margin-top: 32rpx;
  text-align: center;
  font-size: 28rpx;
  color: var(--text-secondary);
}

.link {
  color: var(--primary-color);
  text-decoration: underline;
}

.wechat-login {
  text-align: center;
  padding: 40rpx 0;
}

.wechat-tip {
  font-size: 28rpx;
  color: var(--text-secondary);
  margin-bottom: 32rpx;
}

.wechat-btn {
  width: 100%;
  height: 96rpx;
  font-size: 32rpx;
  color: var(--bg-white);
  background: #07C160;
  border-radius: var(--btn-border-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
}

.icon {
  font-size: 40rpx;
}

.agreement {
  position: fixed;
  bottom: 48rpx;
  left: 50%;
  transform: translateX(-50%);
  font-size: 24rpx;
  color: var(--text-tertiary);
  text-align: center;
  width: 90%;
}
</style>
