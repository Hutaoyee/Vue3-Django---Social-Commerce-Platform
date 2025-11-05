<!-- 未使用 -->
<template>

    <div v-if="artists.length === 0">暂无艺术家</div>

    <div v-else>

        <div v-for="artist in artists" :key="artist.id" class="box">

            <p class="title is-4">{{ artist.name }}</p>
            <p class="subtitle is-6"><span class="has-text-weight-bold">{{ artist.genre }}</span> | {{ artist.created_at }}</p>
            <p>{{ artist.bio }}</p>
        </div>
    </div>
</template>

<script setup>
    import { storeToRefs } from 'pinia'
    import { useArtistsStore } from '@/stores/artists'
    import { onMounted } from 'vue'

    const artistStore = useArtistsStore()
    const { artists } = storeToRefs(artistStore)

    onMounted(() => {
        artistStore.fetchArtists()
    })
</script>

<style lang="scss" scoped>

</style>
