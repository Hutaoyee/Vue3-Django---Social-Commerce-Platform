import { defineStore } from 'pinia'  
import { ref, computed } from 'vue' 
import { shopping, cart } from '@/api/shopping'
import { useUserStore } from './user'

// 定义products store，使用组合式API
export const useProductsStore = defineStore('products', () => {
    // 商品列表，响应式数组
    const products = ref([])
    
    // 搜索查询字符串，响应式
    const searchQuery = ref('')
    
    // 分页信息
    const currentPage = ref(1)
    const totalPages = ref(1)
    const totalCount = ref(0)
    const pageSize = ref(20)
    
    // 加载状态
    const loading = ref(false)

    // 过滤后的商品列表（如果使用分页，这个计算属性可能不需要了）
    const filteredProducts = computed(() => {
        return products.value
    })

    // 异步获取商品数据函数
    const fetchProducts = async (page = 1, search = '', category = null) => {
        loading.value = true
        try {
            const params = {
                page,
                page_size: pageSize.value
            }
            
            if (search) {
                params.search = search
            }
            
            if (category) {
                params.category = category
            }
            
            const response = await shopping.getSPUList(params)
            
            // 处理分页响应
            products.value = response.data.results
            totalCount.value = response.data.count
            currentPage.value = page
            
            // 计算总页数
            totalPages.value = Math.ceil(totalCount.value / pageSize.value)
            
        } catch (error) {
            console.error('获取SPU失败:', error)
        } finally {
            loading.value = false
        }
    }
    
    // 搜索商品
    const searchProducts = async () => {
        await fetchProducts(1, searchQuery.value)
    }
    
    // 切换收藏
    const toggleFavorite = async (product) => {
        const userStore = useUserStore()
        if (!userStore.isLoggedIn) {
            alert('请先登录')
            return
        }
        
        try {
            const response = await shopping.toggleFavorite(product.id)
            // 更新本地状态
            product.is_favorited = response.data.is_favorited
        } catch (error) {
            console.error('收藏操作失败:', error)
            alert('收藏操作失败')
        }
    }
    
    // 获取SKU信息
    const getSPUSKUs = async (spuId) => {
        try {
            const response = await shopping.getSPUSKUs(spuId)
            return response.data
        } catch (error) {
            console.error('获取SKU信息失败:', error)
            throw error
        }
    }
    
    // 添加到购物车
    const addToCart = async (skuCode, quantity = 1) => {
        const userStore = useUserStore()
        if (!userStore.isLoggedIn) {
            alert('请先登录')
            return false
        }
        
        try {
            await cart.addToCart({ sku_code: skuCode, quantity })
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

    // 返回store的响应式属性和方法，供组件使用
    return {
        products,
        searchQuery,
        currentPage,
        totalPages,
        totalCount,
        pageSize,
        loading,
        filteredProducts,
        fetchProducts,
        searchProducts,
        toggleFavorite,
        getSPUSKUs,
        addToCart
    }
})