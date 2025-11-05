import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cart } from '@/api/shopping'
import { useUserStore } from './user'

export const useCartStore = defineStore('cart', () => {
    const cartItems = ref([])
    const loading = ref(false)
    
    // 购物车商品总数
    const totalItems = computed(() => {
        if (!Array.isArray(cartItems.value)) return 0
        return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
    })
    
    // 购物车总价
    const totalPrice = computed(() => {
        if (!Array.isArray(cartItems.value)) return '0.00'
        return cartItems.value.reduce((sum, item) => sum + parseFloat(item.total_price), 0).toFixed(2)
    })
    
    // 获取购物车列表
    const fetchCartItems = async () => {
        const userStore = useUserStore()
        if (!userStore.isLoggedIn) {
            cartItems.value = []
            return
        }
        
        loading.value = true
        try {
            const response = await cart.getCartItems()
            console.log('购物车API响应:', response.data)
            
            // 处理分页数据：DRF返回的格式可能是 {results: [...]} 或直接是数组
            let data = response.data
            if (data && typeof data === 'object' && 'results' in data) {
                // 分页格式
                cartItems.value = Array.isArray(data.results) ? data.results : []
            } else if (Array.isArray(data)) {
                // 直接数组格式
                cartItems.value = data
            } else {
                cartItems.value = []
            }
            
            console.log('购物车商品数量:', cartItems.value.length)
        } catch (error) {
            console.error('获取购物车失败:', error)
            cartItems.value = []
        } finally {
            loading.value = false
        }
    }
    
    // 添加到购物车
    const addItem = async (skuCode, quantity = 1) => {
        const userStore = useUserStore()
        if (!userStore.isLoggedIn) {
            alert('请先登录')
            return false
        }
        
        try {
            console.log('添加到购物车:', skuCode, quantity)
            const response = await cart.addToCart({ sku_code: skuCode, quantity })
            console.log('添加响应:', response.data)
            await fetchCartItems() // 刷新购物车
            console.log('刷新后购物车商品数量:', cartItems.value.length)
            return true
        } catch (error) {
            console.error('添加到购物车失败:', error)
            if (error.response?.data?.error) {
                alert(error.response.data.error)
            } else {
                alert('添加到购物车失败')
            }
            return false
        }
    }
    
    // 更新商品数量
    const updateQuantity = async (cartItemId, quantity) => {
        if (quantity < 1) return
        
        try {
            await cart.updateQuantity(cartItemId, quantity)
            await fetchCartItems() // 刷新购物车
        } catch (error) {
            console.error('更新数量失败:', error)
            if (error.response?.data?.error) {
                alert(error.response.data.error)
            } else {
                alert('更新数量失败')
            }
        }
    }
    
    // 从购物车移除商品
    const removeItem = async (cartItemId) => {
        try {
            await cart.removeFromCart(cartItemId)
            await fetchCartItems() // 刷新购物车
        } catch (error) {
            console.error('删除失败:', error)
            alert('删除失败')
        }
    }
    
    // 批量删除购物车商品
    const batchRemoveItems = async (cartItemIds) => {
        if (!cartItemIds || cartItemIds.length === 0) {
            return
        }
        
        try {
            await cart.batchRemoveFromCart(cartItemIds)
            await fetchCartItems() // 刷新购物车
            return true
        } catch (error) {
            console.error('批量删除失败:', error)
            alert('批量删除失败')
            return false
        }
    }
    
    return {
        cartItems,
        loading,
        totalItems,
        totalPrice,
        fetchCartItems,
        addItem,
        updateQuantity,
        removeItem,
        batchRemoveItems
    }
})
