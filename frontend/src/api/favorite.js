import apiClient from './axios';

export const favoriteAPI = {
    // 切换帖子收藏状态
    togglePostFavorite(postId) {
        return apiClient.post(`/posts/${postId}/favorite/`);
    },

    // 检查帖子是否已收藏
    checkPostFavorite(postId) {
        return apiClient.get(`/posts/${postId}/check-favorite/`);
    },

    // 获取用户的所有收藏帖子
    getUserFavorites(params = {}) {
        return apiClient.get('/post-favorites/', { 
            params: {
                page_size: 1000,  // 获取最多1000条
                ...params
            }
        });
    },

    // 取消收藏（通过favoriteId）
    removeFavorite(favoriteId) {
        return apiClient.delete(`/post-favorites/${favoriteId}/`);
    }
};
