// 配置文件

// 环境类型
export type EnvType = 'dev' | 'prod' | 'test'

// 当前环境
const ENV: EnvType = import.meta.env.MODE as EnvType || 'dev'

// API配置
export const API_CONFIG = {
  // 开发环境
  dev: {
    BASE_URL: 'http://localhost:8000/api/v1',
    TIMEOUT: 10000
  },
  // 测试环境
  test: {
    BASE_URL: 'https://test-api.cloudrobe.com/api/v1',
    TIMEOUT: 10000
  },
  // 生产环境
  prod: {
    BASE_URL: 'https://api.cloudrobe.com/api/v1',
    TIMEOUT: 10000
  }
}

// 获取当前环境配置
export const getCurrentConfig = () => {
  return API_CONFIG[ENV]
}

// 导出当前配置
export const config = getCurrentConfig()

// 文件上传配置
export const UPLOAD_CONFIG = {
  MAX_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/webp'],
  CLOTHING_MAX_COUNT: 5,
  CLOTHING_MIN_COUNT: 3
}

// 分页配置
export const PAGE_CONFIG = {
  PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50]
}

// 路由配置
export const ROUTE_CONFIG = {
  LOGIN: '/pages/auth/login',
  HOME: '/pages/index/index',
  CLOTHING_DETAIL: '/pages/clothing/detail',
  PUBLISH: '/pages/publish/publish',
  ORDER_DETAIL: '/pages/order/detail',
  PROFILE: '/pages/profile/profile'
}

// 存储键
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER_INFO: 'userInfo',
  OPENID: 'openid'
}
