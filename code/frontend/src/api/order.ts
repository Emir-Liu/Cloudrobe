// 订单相关API
import request from '@/utils/request'

// 创建订单
export const createOrder = (data: {
  clothing_id: number
  start_date: string
  end_date: string
  rent_days: number
}) => {
  return request.post('/orders/', data)
}

// 获取订单列表
export const getOrderList = (params?: {
  page?: number
  page_size?: number
  status?: number
}) => {
  return request.get('/orders/', params)
}

// 获取订单详情
export const getOrderDetail = (id: string) => {
  return request.get(`/orders/${id}`)
}

// 确认订单
export const confirmOrder = (id: string) => {
  return request.put(`/orders/${id}/confirm`)
}

// 发货
export const shipOrder = (id: string, data: {
  express_company: string
  express_no: string
}) => {
  return request.put(`/orders/${id}/ship`, data)
}

// 确认收货
export const receiveOrder = (id: string) => {
  return request.put(`/orders/${id}/receive`)
}

// 申请归还
export const returnOrder = (id: string) => {
  return request.put(`/orders/${id}/return`)
}

// 完成订单
export const completeOrder = (id: string, data?: {
  renter_rating?: number
  renter_comment?: string
  renter_images?: string[]
  owner_rating?: number
  owner_comment?: string
  owner_images?: string[]
}) => {
  return request.put(`/orders/${id}/complete`, data)
}

// 取消订单
export const cancelOrder = (id: string, reason?: string) => {
  return request.put(`/orders/${id}/cancel`, { reason })
}

// 评价订单
export const rateOrder = (id: string, data: {
  rating: number
  comment?: string
  images?: string[]
}) => {
  return request.post(`/orders/${id}/rating`, data)
}

// 创建售后争议
export const createDispute = (id: string, data: {
  reason: string
  description: string
  images?: string[]
}) => {
  return request.post(`/orders/${id}/dispute`, data)
}
