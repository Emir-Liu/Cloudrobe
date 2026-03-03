// 用户相关API
import request from '@/utils/request'

// 获取当前用户信息
export const getCurrentUser = () => {
  return request.get('/users/me')
}

// 更新用户信息
export const updateCurrentUser = (data: {
  nickname?: string
  avatar?: string
  gender?: number
  height?: number
  weight?: number
  bio?: string
}) => {
  return request.put('/users/me', data)
}

// 实名认证
export const verifyUser = (data: {
  id_card_name: string
  id_card_number: string
  id_card_front: string
  id_card_back: string
}) => {
  return request.post('/users/verify', data)
}

// 获取信用积分
export const getUserCredit = () => {
  return request.get('/users/credit')
}

// 获取余额信息
export const getUserBalance = () => {
  return request.get('/users/balance')
}
