// 消息相关API
import request from '@/utils/request'

// 消息列表查询参数
export interface MessageListQuery {
  page?: number
  page_size?: number
  type?: number
}

// 获取消息列表
export const getMessageList = (params?: MessageListQuery) => {
  return request.get('/messages/', params, { showLoading: false })
}

// 标记消息已读
export const markMessageRead = (id: number) => {
  return request.put(`/messages/${id}/read`)
}

// 获取未读消息数
export const getUnreadCount = () => {
  return request.get('/messages/unread-count')
}

// 批量标记已读
export const markAllRead = () => {
  return request.post('/messages/mark-all-read')
}
