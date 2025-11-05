<template>

    <div class="box">

        <h4 class="title is-4">Live</h4>
        <div class="fixed-grid">
            <div class="grid grid-set">

                <div v-if="liveVideos.length > 0" v-for="video in liveVideos" :key="video.id" class="video-container cell">

                    <h5 class="has-text-weight-bold is-5 m-1">{{ video.title }}</h5>
                    <iframe class="video-set" 
                        :src="video.bilibili_url + '&autoplay=0'" 
                        scrolling="no" 
                        border="0" 
                        frameborder="no" 
                        framespacing="0" 
                        allowfullscreen="true">
                    </iframe>
                </div>

                <div v-else>
                    <p class="has-text-centered">暂无视频</p>
                </div>
            </div>
        </div>
    </div>

    <div class="box">

        <h4 class="title is-4">Interview</h4>
        <div class="fixed-grid">
            <div class="grid grid-set">

                <div v-if="interviewVideos.length > 0" v-for="video in interviewVideos" :key="video.id" class="video-container cell">

                    <h5 class="has-text-weight-bold is-5 m-1">{{ video.title }}</h5>
                    <iframe class="video-set" 
                        :src="video.bilibili_url + '&autoplay=0'" 
                        scrolling="no" 
                        border="0" 
                        frameborder="no" 
                        framespacing="0" 
                        allowfullscreen="true">
                    </iframe>
                </div>

                <div v-else>
                    <p class="has-text-centered">暂无视频</p>
                </div>
            </div>
        </div>
    </div>

    <div class="box">

        <h4 class="title is-4">Documentary</h4>
        <div class="fixed-grid">
            <div class="grid grid-set">

                <div v-if="documentaryVideos.length > 0" v-for="video in documentaryVideos" :key="video.id" class="video-container cell">

                    <h5 class="has-text-weight-bold is-5 m-1">{{ video.title }}</h5>
                    <iframe class="video-set" 
                        :src="video.bilibili_url + '&autoplay=0'" 
                        scrolling="no" 
                        border="0" 
                        frameborder="no" 
                        framespacing="0" 
                        allowfullscreen="true">
                    </iframe>
                </div>

                <div v-else>
                    <p class="has-text-centered">暂无视频</p>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>

    import { storeToRefs } from 'pinia'
    import { useVideosStore } from '@/stores/videos'
    import { ref, computed, onMounted } from 'vue'

    const videoStore = useVideosStore()
    const { videos } = storeToRefs(videoStore)

    const liveVideos = computed(() => videos.value.filter(v => v.video_type === 'live'))
    const interviewVideos = computed(() => videos.value.filter(v => v.video_type === 'interview'))
    const documentaryVideos = computed(() => videos.value.filter(v => v.video_type === 'documentary'))

    onMounted(() => {
        videoStore.fetchVideos()
    })
</script>

<style lang="scss" scoped>
.video-set{
    width: 100%;
    height: 40vh;
}

.grid-set {

    max-height: 850px;
    overflow-y: auto;

    &::-webkit-scrollbar {
        width: 2px;
    }
    
    &::-webkit-scrollbar-track {
        background: transparent;
    }
    
    &::-webkit-scrollbar-thumb {
        background: rgba(0, 209, 175, 1);
        border-radius: 3px;
        
    }
}
</style>