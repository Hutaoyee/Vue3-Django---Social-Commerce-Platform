import { ref } from 'vue'
import { defineStore } from 'pinia'
import { publicationAPI } from '@/api/publication'

export const useVideosStore = defineStore('videos', () => {

  const videos = ref([])

  const fetchVideos = async () => {
    try {
      const response = await publicationAPI.getVideos()
      videos.value = response.data
    } catch (error) {
      console.error('获取视频失败:', error)
    }
  }

  return { videos, fetchVideos }
})