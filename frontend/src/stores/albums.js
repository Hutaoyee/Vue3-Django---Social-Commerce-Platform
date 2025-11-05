import { ref } from 'vue'
import { defineStore } from 'pinia'
import { publicationAPI } from '@/api/publication'

export const useAlbumsStore = defineStore('albums', () => {

  const albums = ref([])

  const fetchAlbums = async () => {
    try {
      const response = await publicationAPI.getAlbums()
      albums.value = response.data
    } catch (error) {
      console.error('获取专辑失败:', error)
    }
  }

  return { albums, fetchAlbums }
})