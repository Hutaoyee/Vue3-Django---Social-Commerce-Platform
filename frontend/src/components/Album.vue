<template>
    <div v-if="albums.length === 0">暂无专辑</div>

    <div v-else class="is-flex is-flex-wrap-wrap is-justify-content-center">

        <div v-for="album in albums" :key="album.id" class="box box-size m-3 has-text-centered">

            <figure class="image image-size is-1by1">
                <img :src="album.cover_image" alt="" @click="openModal(album)" />
            </figure>
            <p class="title is-5 m-1" @click="openModal(album)">{{ album.name }}</p>
            <p class="subtitle is-6">
                <!-- <span class="has-text-weight-bold">{{ album.artist.name }}</span> |  -->
                {{ album.release_date }}
            </p>
        </div>
    </div>

    <div class="modal" :class="{ 'is-active': isModalActive }">
        <div class="modal-background" @click="closeModal"></div>
        <div class="modal-content ">
            
            <div v-if="isnotpublic" class="box">
                <p class="title has-text-centered">COMING SOON</p>
            </div>
            
            <div v-else-if="selectedAlbum && dynamicPlaylistId && isModalActive">
                <iframe @load="onIframeLoaded" data-testid="embed-iframe" style="border-radius:12px" :src="`https://open.spotify.com/embed/album/${dynamicPlaylistId}?utm_source=generator`" width="100%" height="352" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
                
                <div v-if="isIframeLoaded">
                    <router-link class="navbar-item" to="/">
                        <button class="button">购买专辑</button>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { storeToRefs } from 'pinia'
    import { useAlbumsStore } from '@/stores/albums'
    import { ref, computed, onMounted } from 'vue'

    const albumStore = useAlbumsStore()
    const { albums } = storeToRefs(albumStore)

    const isModalActive = ref(false)
    const selectedAlbum = ref(null)
    const isnotpublic = ref(false)

    const isIframeLoaded = ref(false)

    const openModal = (album) => {
        selectedAlbum.value = album
        isModalActive.value = true
        isIframeLoaded.value = false
        isnotpublic.value = album.name === 'BULLY'
    }

    const closeModal = () => {
        isModalActive.value = false
        selectedAlbum.value = null
        isIframeLoaded.value = false
    }

    const onIframeLoaded = () => {
         isIframeLoaded.value = true
    }

    // Spotify Playlist IDs for albums
    const playlistMap = {
        'The College Dropout': '4Uv86qWpGTxf7fU7lG5X6F',
        'Late Registration': '5ll74bqtkcXlKE7wwkMq4g',
        'Graduation': '4SZko61aMnmgvNhfhgTuD3',
        '808s & Heartbreak': '3WFTGIO6E3Xh4paEOBY9OU',
        'My Beautiful Dark Twisted Fantasy': '20r762YmB5HeofjMCiPMLv',
        'Watch The Throne': '2if1gb3t6IkhiKzrtS9Glc',
        'Yeezus': '7D2NdGvBHIavgLhmcwhluK',
        'The Life Of Pablo': '7gsWAHLeT0w7es6FofOXk1',
        'ye': '2Ek1q2haOnxVqhvVKqMvJe',
        'KIDS SEE GHOSTS': '6pwuKxMUkNg673KETsXPUV',
        'JESUS IS KING': '0FgZKfoU2Br5sHOfvZKTI9',
        'Donda': '2Wiyo7LzdeBCsVZiRA6vVZ',
        'VULTURES 1': '4DOsPwJtokv6HEifZ6t5j6',
        'VULTURES 2': '5RV2TNyjylqWJNxQyHBTeJ',
        'DONDA 2': '1ZkGNUz1un0b3Z7EsJl3ci'
    }

    const dynamicPlaylistId = computed(() => {
        const a = selectedAlbum.value
        if (!a || !a.name) return ''
        return playlistMap[a.name] || ''
    })

    onMounted(() => {
        albumStore.fetchAlbums()
    })
</script>

<style lang="scss" scoped>
.box-size {

    width: 20%;
}

.image-size {

    width: 100%;
}
</style>
