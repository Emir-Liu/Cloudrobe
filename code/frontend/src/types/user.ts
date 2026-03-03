// 用户类型定义

export interface User {
  id: number
  openid?: string
  phone?: string
  nickname?: string
  avatar?: string
  gender?: number
  height?: number
  weight?: number
  size_preferences?: any
  bio?: string
  credit_score?: number
  credit_level?: string
  balance?: number
  is_verified?: boolean
  id_card_name?: string
  id_card_number?: string
  status?: number
  created_at?: string
  updated_at?: string
}

export interface UserLoginResponse {
  user: User
  token: string
  refresh_token?: string
}

export interface CreditInfo {
  credit_score: number
  credit_level: string
  level_name: string
  next_level_score: number
}

export interface BalanceInfo {
  balance: number
  total_income?: number
  total_withdraw?: number
}
