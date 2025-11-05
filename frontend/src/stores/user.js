import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import defaultAvatar from '@/assets/defaultAvatar.png'

export const useUserStore = defineStore('user', () => {
    // 状态
    const token = ref(localStorage.getItem('token') || null)
    const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

    // 计算属性：是否已登录
    /* 
    第一个 ! 取反
    !null → true

    第二个 ! 再取反
    !!null → false
    */
    const isLoggedIn = computed(() => !!token.value)

    // 计算属性：
    /* 
    未登录
    user.value = null
    username.value = ''

    已登录
    user.value = { username: 'john' }
    username.value = 'john'
    */
    const username = computed(() => user.value?.username || '')
    const email = computed(() => user.value?.email || '')
    const id = computed(() => user.value?.id || '')
    const bio = computed(() => user.value?.bio || '')
    const dateJoined = computed(() => user.value?.date_joined || '')


    const avatar = computed(() => {
        if (isLoggedIn.value && user.value?.avatar) {
            // 已登录且有头像
            return user.value.avatar
        } else {
            // 未登录或没有头像，显示默认
            return defaultAvatar
        }
    })


    // 方法：登录
    function login(userData, userToken) {
        token.value = userToken
        user.value = userData

        // 持久化到 localStorage
        localStorage.setItem('token', userToken)
        localStorage.setItem('user', JSON.stringify(userData))
    }

    // 方法：退出登录
    function logout() {
        token.value = null
        user.value = null

        // 清除 localStorage
        localStorage.removeItem('token')
        localStorage.removeItem('user')
    }

    return { 
    token, 
    user, 
    isLoggedIn, 
    username,
    email,
    id,
    bio,
    dateJoined,
    avatar,
    login, 
    logout,
    }
})