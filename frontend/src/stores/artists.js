import { ref } from 'vue'
import { defineStore } from 'pinia'
import { publicationAPI } from '@/api/publication'

export const useArtistsStore = defineStore('artists', () => {
  
  const artists = ref([])

  const fetchArtists = async () => {
    try {
      const response = await publicationAPI.getArtists()
      artists.value = response.data
    } catch (error) {
      console.error('获取艺术家失败:', error)
    }
  }

  return { artists, fetchArtists }
})