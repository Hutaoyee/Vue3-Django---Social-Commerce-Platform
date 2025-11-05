<template>
    <div class="container container-top">

        <div class="tabs is-toggle is-toggle-rounded is-fullwidth">
            <ul>

                <li :class="{ 'is-active': activeTab === 'music' }">
                    <a @click="setActiveTab('music')">
                        <span>音乐</span>
                    </a>
                </li>

                <li :class="{ 'is-active': activeTab === 'notice' }">
                    <a @click="setActiveTab('notice')">
                        <span>公告</span>
                    </a>
                </li>

                <li :class="{ 'is-active': activeTab === 'video' }">
                    <a @click="setActiveTab('video')">
                        <span>视频</span>
                    </a>
                </li>
            </ul>
        </div>

        <!-- 根据activeTab显示不同内容 -->
        <div v-if="activeTab === 'music'" class="tab-content">
            
            <AlbumComponent />
        </div>

        <div v-else-if="activeTab === 'notice'" class="tab-content">

            <NoticeComponent />
        </div>

        <div v-else-if="activeTab === 'video'" class="tab-content">

            <VideoComponent />
        </div>
    </div>
</template>

<script>
    import { onMounted, onUnmounted, ref } from 'vue'

    import AlbumComponent from '@/components/Album.vue'
    import NoticeComponent from '@/components/Notice.vue'
    import VideoComponent from '@/components/Video.vue'

    export default {
        setup() {

            // 进入默认显示公告页面
            const activeTab = ref('notice')
            const setActiveTab = (tab) => {
                activeTab.value = tab
            }

            // 组件挂载时添加样式类
            onMounted(() => {
                document.body.classList.add('publication-page-active')
                document.getElementById('app')?.classList.add('publication-page-active')
            })

            // 组件卸载时移除样式类
            onUnmounted(() => {
                document.body.classList.remove('publication-page-active')
                document.getElementById('app')?.classList.remove('publication-page-active')
            })

            return { activeTab, setActiveTab }
        },

        components: {
            
            AlbumComponent,
            NoticeComponent,
            VideoComponent
        },
    }
</script>

<style>
    
    body.publication-page-active{
        align-items: start;
    }

    #app.publication-page-active{

        display: flex;
        justify-content: center;
        padding: 0 2rem;
        width: 100%;
    }
</style>

<style lang="scss" scoped>
.container-top{

    width: 100%;
    padding: 1rem;
}

.tabs ul li.is-active a {
    background-color: rgba(0, 209, 175, 1);
    border: none;
}
</style>