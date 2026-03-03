// 用户状态管理
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, UserLoginResponse, CreditInfo, BalanceInfo } from '@/types/user'
import * as authApi from '@/api/auth'
import * as userApi from '@/api/user'
import { STORAGE_KEYS } from '@/config'
import request from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string>('')
  const openid = ref<string>('')

  // Getters
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const userId = computed(() => user.value?.id || 0)
  const avatarUrl = computed(() => user.value?.avatar || '/static/images/default-avatar.png')

  // Actions

  /**
   * 发送短信验证码
   */
  const sendSms = async (phone: string) => {
    await authApi.sendSmsCode(phone)
    return true
  }

  /**
   * 手机号登录
   */
  const loginByPhone = async (phone: string, code: string) => {
    const res = await authApi.login({ phone, code }) as UserLoginResponse
    
    // 保存用户信息和token
    user.value = res.user
    token.value = res.token
    
    // 持久化存储
    uni.setStorageSync(STORAGE_KEYS.TOKEN, res.token)
    uni.setStorageSync(STORAGE_KEYS.USER_INFO, res.user)
    
    return res
  }

  /**
   * 微信登录
   */
  const loginByWechat = async () => {
    // #ifdef MP-WEIXIN
    // 获取微信登录code
    const { code } = await uni.login({ provider: 'weixin' })
    
    const res = await authApi.wechatLogin({ code }) as UserLoginResponse
    
    user.value = res.user
    token.value = res.token
    
    uni.setStorageSync(STORAGE_KEYS.TOKEN, res.token)
    uni.setStorageSync(STORAGE_KEYS.USER_INFO, res.user)
    // #endif
    
    return user.value
  }

  /**
   * 注册
   */
  const register = async (data: {
    phone: string
    code: string
    nickname?: string
    avatar?: string
  }) => {
    const res = await authApi.register(data) as UserLoginResponse
    
    user.value = res.user
    token.value = res.token
    
    uni.setStorageSync(STORAGE_KEYS.TOKEN, res.token)
    uni.setStorageSync(STORAGE_KEYS.USER_INFO, res.user)
    
    return res
  }

  /**
   * 登出
   */
  const logout = () => {
    user.value = null
    token.value = ''
    
    uni.removeStorageSync(STORAGE_KEYS.TOKEN)
    uni.removeStorageSync(STORAGE_KEYS.USER_INFO)
    uni.removeStorageSync(STORAGE_KEYS.OPENID)
    
    // 跳转到登录页
    uni.reLaunch({
      url: '/pages/auth/login'
    })
  }

  /**
   * 获取用户信息
   */
  const fetchUserInfo = async () => {
    const userInfo = await userApi.getCurrentUser() as User
    user.value = userInfo
    uni.setStorageSync(STORAGE_KEYS.USER_INFO, userInfo)
    return userInfo
  }

  /**
   * 更新用户信息
   */
  const updateUserInfo = async (data: Partial<User>) => {
    const userInfo = await userApi.updateCurrentUser(data) as User
    user.value = userInfo
    uni.setStorageSync(STORAGE_KEYS.USER_INFO, userInfo)
    return userInfo
  }

  /**
   * 从存储恢复登录状态
   */
  const restoreAuth = () => {
    const savedToken = uni.getStorageSync(STORAGE_KEYS.TOKEN)
    const savedUser = uni.getStorageSync(STORAGE_KEYS.USER_INFO)
    const savedOpenid = uni.getStorageSync(STORAGE_KEYS.OPENID)
    
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = savedUser
    }
    
    if (savedOpenid) {
      openid.value = savedOpenid
    }
  }

  return {
    // State
    user,
    token,
    openid,
    
    // Getters
    isLoggedIn,
    userId,
    avatarUrl,
    
    // Actions
    sendSms,
    loginByPhone,
    loginByWechat,
    register,
    logout,
    fetchUserInfo,
    updateUserInfo,
    restoreAuth
  }
})
