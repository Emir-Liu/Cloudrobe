// 认证相关API
import request from '@/utils/request'

// 发送短信验证码
export const sendSmsCode = (phone: string) => {
  return request.post('/auth/send-sms', { phone }, { showLoading: false })
}

// 手机号注册
export const register = (data: {
  phone: string
  code: string
  nickname?: string
  avatar?: string
}) => {
  return request.post('/auth/register', data)
}

// 手机号登录
export const login = (data: {
  phone: string
  code: string
}) => {
  return request.post('/auth/login', data)
}

// 微信登录
export const wechatLogin = (data: {
  code: string
  encryptedData?: string
  iv?: string
}) => {
  return request.post('/auth/wechat-login', data)
}

// 刷新token
export const refreshToken = (refreshToken: string) => {
  return request.post('/auth/refresh', { refresh_token: refreshToken })
}
