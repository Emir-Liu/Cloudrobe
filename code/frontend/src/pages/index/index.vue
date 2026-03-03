<template>
  <view class="index-page">
    <!-- 顶部搜索 -->
    <view class="search-bar">
      <view class="search-input" @tap="handleSearch">
        <text class="icon">🔍</text>
        <text class="placeholder">搜索衣物、品牌</text>
      </view>
      <view class="cart-icon">🛒</view>
    </view>

    <!-- 分类筛选 -->
    <scroll-view class="category-scroll" scroll-x>
      <view class="category-list">
        <view 
          v-for="cat in categories" 
          :key="cat.value"
          class="category-item"
          :class="{ active: selectedCategory === cat.value }"
          @tap="selectCategory(cat.value)"
        >
          {{ cat.label }}
        </view>
      </view>
    </scroll-view>

    <!-- 热门推荐 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">🔥 热门推荐</text>
        <text class="section-more" @tap="viewMore('popular')">更多</text>
      </view>
      
      <scroll-view class="popular-scroll" scroll-x>
        <view 
          v-for="item in popularClothings" 
          :key="item.id"
          class="clothing-card popular"
          @tap="goToDetail(item.id)"
        >
          <image :src="item.images[0]" mode="aspectFill" class="card-image" />
          <view class="card-info">
            <text class="card-title">{{ item.name }}</text>
            <view class="card-bottom">
              <text class="card-price">¥{{ item.daily_rent }}/天</text>
              <text class="card-rating">⭐ {{ item.rating_avg }}</text>
            </view>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 最新上架 -->
    <view class="section">
      <view class="section-header">
        <text class="section-title">✨ 最新上架</text>
        <text class="section-more" @tap="viewMore('latest')">更多</text>
      </view>
      
      <view class="clothing-grid">
        <view 
          v-for="item in latestClothings" 
          :key="item.id"
          class="clothing-card"
          @tap="goToDetail(item.id)"
        >
          <image :src="item.images[0]" mode="aspectFill" class="card-image" />
          <view class="card-info">
            <text class="card-title">{{ item.name }}</text>
            <view class="card-bottom">
              <text class="card-price">¥{{ item.daily_rent }}/天</text>
              <text class="card-rent-count">已租{{ item.rent_count }}次</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as clothingApi from '@/api/clothing'

// 分类列表
const categories = ref([
  { label: '全部', value: '' },
  { label: '连衣裙', value: '连衣裙' },
  { label: '上装', value: '上装' },
  { label: '下装', value: '下装' },
  { label: '裙装', value: '裙装' },
  { label: '礼服', value: '礼服' },
  { label: '外套', value: '外套' }
])

// 状态
const selectedCategory = ref('')
const popularClothings = ref<any[]>([])
const latestClothings = ref<any[]>([])
const loading = ref(false)

// 选择分类
const selectCategory = (category: string) => {
  selectedCategory.value = category
  // 重新加载数据
  loadData()
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const [popularRes, latestRes] = await Promise.all([
      clothingApi.getPopularClothings({ limit: 10 }),
      clothingApi.getLatestClothings({ limit: 20 })
    ])

    popularClothings.value = popularRes
    latestClothings.value = latestRes
  } catch (error: any) {
    uni.showToast({ title: error.message || '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  uni.navigateTo({
    url: '/pages/search/search'
  })
}

// 查看更多
const viewMore = (type: string) => {
  uni.navigateTo({
    url: `/pages/clothing/list?type=${type}&category=${selectedCategory.value}`
  })
}

// 跳转到详情
const goToDetail = (id: number) => {
  uni.navigateTo({
    url: `/pages/clothing/detail?id=${id}`
  })
}

// 下拉刷新
const onRefresh = async () => {
  await loadData()
  uni.stopPullDownRefresh()
}

// 上拉加载
const onReachBottom = () => {
  // 加载更多
}

onMounted(() => {
  loadData()
})

// 暴露给页面的方法
defineExpose({
  onRefresh,
  onReachBottom
})
</script>

<style lang="scss" scoped>
.index-page {
  min-height: 100vh;
  background: var(--bg-color);
}

.search-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 24rpx;
  padding: 24rpx 32rpx;
  background: var(--bg-white);
  box-shadow: var(--shadow-sm);
}

.search-input {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 16rpx;
  height: 64rpx;
  padding: 0 24rpx;
  background: var(--bg-gray);
  border-radius: 32rpx;
  
  .icon {
    font-size: 32rpx;
  }
  
  .placeholder {
    font-size: 28rpx;
    color: var(--text-tertiary);
  }
}

.cart-icon {
  font-size: 40rpx;
}

.category-scroll {
  white-space: nowrap;
  padding: 24rpx 32rpx;
  background: var(--bg-white);
}

.category-list {
  display: inline-flex;
  gap: 24rpx;
}

.category-item {
  padding: 12rpx 32rpx;
  font-size: 28rpx;
  color: var(--text-secondary);
  background: var(--bg-gray);
  border-radius: 32rpx;
  white-space: nowrap;
  
  &.active {
    color: var(--bg-white);
    background: var(--primary-color);
  }
}

.section {
  margin-top: 24rpx;
  padding: 0 32rpx 32rpx;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}

.section-title {
  font-size: 36rpx;
  font-weight: bold;
  color: var(--text-primary);
}

.section-more {
  font-size: 28rpx;
  color: var(--text-tertiary);
}

.popular-scroll {
  white-space: nowrap;
}

.clothing-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24rpx;
}

.clothing-card {
  display: inline-block;
  background: var(--bg-white);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  
  &.popular {
    width: 480rpx;
    margin-right: 24rpx;
  }
}

.card-image {
  width: 100%;
  height: 480rpx;
  background: var(--bg-gray);
}

.card-info {
  padding: 24rpx;
}

.card-title {
  font-size: 28rpx;
  font-weight: 500;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16rpx;
}

.card-price {
  font-size: 32rpx;
  font-weight: bold;
  color: var(--primary-color);
  font-family: var(--font-family-number);
}

.card-rating,
.card-rent-count {
  font-size: 24rpx;
  color: var(--text-tertiary);
}
</style>
