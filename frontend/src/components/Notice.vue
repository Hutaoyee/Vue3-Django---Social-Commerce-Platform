<template>

    <div v-if="notices.length === 0">暂无公告</div>

    <div v-else>

        <div v-for="notice in notices" :key="notice.id" class="box">

            <p class="title is-4">{{ notice.title }}</p>
            <p class="subtitle is-6"><span class="has-text-weight-bold">{{ notice.author }}</span> | {{ notice.created_at }}</p>
            <p>{{ notice.content }}</p>
        </div>
    </div>
</template>

<script setup>
    import { storeToRefs } from 'pinia'
    import { useNoticesStore } from '@/stores/notices'
    import { onMounted } from 'vue'

    const noticeStore = useNoticesStore()
    const { notices } = storeToRefs(noticeStore)

    onMounted(() => {
        noticeStore.fetchNotices()
    })
</script>

<style lang="scss" scoped>

</style>
