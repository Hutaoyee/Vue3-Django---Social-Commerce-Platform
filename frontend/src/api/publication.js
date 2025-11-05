import apiClient from './axios';

export const publicationAPI = {
  
    // 获取艺术家列表
    getArtists(params = {}) {
        return apiClient.get('/artists/', { params });
    },

    // 获取专辑列表
    getAlbums(params = {}) {
        return apiClient.get('/albums/', { params });
    },

    // 获取音乐列表
    getMusic(params = {}) {
        return apiClient.get('/music/', { params });
    },

    // 获取公告列表
    getNotices(params = {}) {
        return apiClient.get('/notices/', { params });
    },

    // 获取视频列表
    getVideos(params = {}) {
        return apiClient.get('/videos/', { params });
    }
};