// 网络请求封装
import { config, STORAGE_KEYS } from '@/config'
import type { ApiResponse, ApiError } from '@/types/api'

// 请求配置
interface RequestConfig {
  showLoading?: boolean
  showError?: boolean
  skipAuth?: boolean
}

class Request {
  private baseURL: string
  private timeout: number

  constructor() {
    this.baseURL = config.BASE_URL
    this.timeout = config.TIMEOUT
  }

  /**
   * 获取token
   */
  private getToken(): string | null {
    return uni.getStorageSync(STORAGE_KEYS.TOKEN) || null
  }

  /**
   * 统一请求方法
   */
  request<T = any>(
    url: string,
    method: 'GET' | 'POST' | 'PUT' | 'DELETE',
    data?: any,
    options?: RequestConfig
  ): Promise<T> {
    const { showLoading = true, showError = true, skipAuth = false } = options || {}

    // 显示loading
    if (showLoading) {
      uni.showLoading({ title: '加载中...', mask: true })
    }

    // 构建请求头
    const header: Record<string, string> = {
      'Content-Type': 'application/json'
    }

    // 添加认证token
    if (!skipAuth) {
      const token = this.getToken()
      if (token) {
        header['Authorization'] = `Bearer ${token}`
      }
    }

    return new Promise<T>((resolve, reject) => {
      uni.request({
        url: `${this.baseURL}${url}`,
        method,
        data,
        header,
        timeout: this.timeout,
        success: (res: any) => {
          // 隐藏loading
          if (showLoading) {
            uni.hideLoading()
          }

          const response = res.data as ApiResponse<T>

          // HTTP状态码检查
          if (res.statusCode >= 200 && res.statusCode < 300) {
            // 业务状态码检查
            if (response.code === 0 || response.code === 200) {
              resolve(response.data as T)
            } else {
              // 业务错误
              const error: ApiError = {
                code: response.code,
                message: response.message || '请求失败',
                errors: (response as any).errors
              }
              
              if (showError) {
                this.showErrorToast(error.message)
              }
              
              reject(error)
            }
          } else {
            // HTTP错误
            const error: ApiError = {
              code: res.statusCode,
              message: `请求失败: ${res.statusCode}`,
              errors: null
            }
            
            if (showError) {
              this.showErrorToast(error.message)
            }
            
            reject(error)
          }
        },
        fail: (err) => {
          // 隐藏loading
          if (showLoading) {
            uni.hideLoading()
          }

          // 网络错误
          const error: ApiError = {
            code: -1,
            message: '网络连接失败，请检查网络设置',
            errors: null
          }
          
          if (showError) {
            this.showErrorToast(error.message)
          }
          
          reject(error)
        }
      })
    })
  }

  /**
   * GET请求
   */
  get<T = any>(url: string, data?: any, options?: RequestConfig): Promise<T> {
    return this.request<T>(url, 'GET', data, options)
  }

  /**
   * POST请求
   */
  post<T = any>(url: string, data?: any, options?: RequestConfig): Promise<T> {
    return this.request<T>(url, 'POST', data, options)
  }

  /**
   * PUT请求
   */
  put<T = any>(url: string, data?: any, options?: RequestConfig): Promise<T> {
    return this.request<T>(url, 'PUT', data, options)
  }

  /**
   * DELETE请求
   */
  delete<T = any>(url: string, data?: any, options?: RequestConfig): Promise<T> {
    return this.request<T>(url, 'DELETE', data, options)
  }

  /**
   * 显示错误提示
   */
  private showErrorToast(message: string) {
    uni.showToast({
      title: message,
      icon: 'none',
      duration: 3000
    })
  }

  /**
   * 显示成功提示
   */
  showSuccess(message: string) {
    uni.showToast({
      title: message,
      icon: 'success',
      duration: 2000
    })
  }
}

// 创建实例
const request = new Request()

export default request
