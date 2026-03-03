<script setup lang="ts">
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

onLaunch(() => {
  console.log('App Launch')
  
  // 恢复登录状态
  userStore.restoreAuth()
  
  // 检查登录状态
  if (!userStore.isLoggedIn) {
    uni.reLaunch({
      url: '/pages/auth/login'
    })
  }
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})
</script>

<style lang="scss">
@import '@/styles/global.scss';

/* 每个页面公共css */
page {
  font-family: var(--font-family-primary);
  font-size: var(--font-size-body);
  line-height: var(--line-height-base);
  color: var(--text-primary);
  background-color: var(--bg-color);
}
</style>
