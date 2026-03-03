// API类型定义

// 通用响应
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

// 分页响应
export interface PageResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
}

// 错误响应
export interface ApiError {
  code: number
  message: string
  errors?: any[]
}
