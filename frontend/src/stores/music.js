import { ref } from 'vue'
import { defineStore } from 'pinia'
import { publicationAPI } from '@/api/publication'

export const useMusicStore = defineStore('music', () => {
  const music = ref([])

  const fetchMusic = async (params = {}) => {
    try {
      const response = await publicationAPI.getMusic(params)
      music.value = response.data
    } catch (error) {
      console.error('获取音乐失败:', error)
    }
  }

  return { music, fetchMusic }
})