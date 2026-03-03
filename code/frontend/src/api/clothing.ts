// 衣物相关API
import request from '@/utils/request'

// 衣物列表查询参数
export interface ClothingListQuery {
  page?: number
  page_size?: number
  category?: string
  size?: string
  brand?: string
  min_price?: number
  max_price?: number
  keyword?: string
  sort?: 'created_at' | 'price_asc' | 'price_desc' | 'rent_count'
}

// 获取衣物列表
export const getClothingList = (params: ClothingListQuery) => {
  return request.get('/clothings/', params, { showLoading: false })
}

// 获取热门衣物
export const getPopularClothings = (params?: {
  limit?: number
}) => {
  return request.get('/clothings/popular', params, { showLoading: false })
}

// 获取最新衣物
export const getLatestClothings = (params?: {
  limit?: number
}) => {
  return request.get('/clothings/latest', params, { showLoading: false })
}

// 获取衣物详情
export const getClothingDetail = (id: number) => {
  return request.get(`/clothings/${id}`)
}

// 发布衣物
export const createClothing = (data: {
  name: string
  brand?: string
  category: string
  size: string
  condition: string
  description?: string
  images: string[]
  daily_rent: number
  deposit: number
  min_rent_days?: number
  max_rent_days?: number
  require_wash?: boolean
  delivery_type: number
  delivery_fee?: number
}) => {
  return request.post('/clothings/', data)
}

// 编辑衣物
export const updateClothing = (id: number, data: {
  name?: string
  brand?: string
  category?: string
  size?: string
  condition?: string
  description?: string
  images?: string[]
  daily_rent?: number
  deposit?: number
  min_rent_days?: number
  max_rent_days?: number
  require_wash?: boolean
  delivery_type?: number
  delivery_fee?: number
}) => {
  return request.put(`/clothings/${id}`, data)
}

// 删除衣物
export const deleteClothing = (id: number) => {
  return request.delete(`/clothings/${id}`)
}

// 收藏衣物
export const favoriteClothing = (id: number) => {
  return request.post(`/clothings/${id}/favorite`)
}

// 取消收藏
export const unfavoriteClothing = (id: number) => {
  return request.delete(`/clothings/${id}/favorite`)
}
