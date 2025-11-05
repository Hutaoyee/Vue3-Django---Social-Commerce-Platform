import axios from './axios'

const productFavoriteAPI = {
    // 切换商品收藏状态
    toggleProductFavorite(productId) {
        return axios.post(`/products/${productId}/favorite/`)
    },

    // 检查商品是否已收藏
    checkProductFavorite(productId) {
        return axios.get(`/products/${productId}/check-favorite/`)
    },

    // 获取用户的所有商品收藏
    getUserFavorites(params = {}) {
        return axios.get('/product-favorites/', {
            params: {
                page_size: 1000,  // 获取最多1000条
                ...params
            }
        })
    },

    // 移除商品收藏
    removeFavorite(favoriteId) {
        return axios.delete(`/product-favorites/${favoriteId}/`)
    }
}

export default productFavoriteAPI
