import { ref } from 'vue'
import { defineStore } from 'pinia'
import { publicationAPI } from '@/api/publication'

export const useNoticesStore = defineStore('notices', () => {

  const notices = ref([])

  const fetchNotices = async () => {
    try {
        const response = await publicationAPI.getNotices()
        notices.value = response.data
    } catch (error) {
        console.error('获取公告失败:', error)
    }
  }

  return { notices, fetchNotices }
})