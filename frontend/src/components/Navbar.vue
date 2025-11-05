<template>
  <nav class="navbar is-fixed-top">
    <div class="container">
      <div class="navbar-brand">

        <router-link class="navbar-item" to="/">
          
          <img :src="logoUrl" alt="Logo" width="80" height="80">
        </router-link>

        <a class="navbar-burger" role="button" aria-label="menu" aria-expanded="false">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navMenu" class="navbar-menu">
        <!-- #TODO 菜单 -->
        <div class="navbar-start">
          <router-link class="navbar-item has-text-primary has-text-weight-bold" to="/merch">Merch</router-link>
          <router-link class="navbar-item has-text-primary has-text-weight-bold" to="/publication">Publication</router-link>
          <router-link class="navbar-item has-text-primary has-text-weight-bold" to="/communicate">Communicate</router-link>
        </div>

        <div class="navbar-end">

          <div class="navbar-item">

            <!-- 购物车功能 - 使用span而非router-link -->
            <span class="navbar-item has-text-primary is-size-5" @click="openCartModal" style="cursor: pointer;">
              <font-awesome-icon icon="fa-solid fa-cart-shopping" />
              <span v-if="cartStore.totalItems > 0" class="tag is-danger is-rounded ml-1">{{ cartStore.totalItems }}</span>
            </span>

            <!-- 头像 -->
            <router-link :to="userStore.isLoggedIn ? '/myself' : '/login'">
              <figure class="image is-flex is-align-items-center is-justify-content-center">

                <img 
                  class="is-rounded" 
                  :src="userStore.avatar" 
                >
              </figure>
            </router-link>
          </div>
        </div>

      </div>
    </div>
  </nav>

  <!-- 购物车模态框 -->
  <div class="modal" :class="{ 'is-active': showCart }">
    <div class="modal-background"></div>
    <div class="modal-card" style="width: 90%; max-width: 800px;">
      <header class="modal-card-head">
        <p class="modal-card-title">购物车</p>
      </header>
      <section class="modal-card-body">
        <div v-if="cartStore.loading" class="has-text-centered">
          <p>加载中...</p>
        </div>
        
        <div v-else-if="cartStore.cartItems.length === 0" class="notification">
          <p class="has-text-centered">购物车是空的</p>
        </div>
        
        <div v-else>
          <!-- 购物车项列表 -->
          <div class="box mb-4" v-for="item in cartStore.cartItems" :key="item.id">
            <div class="columns is-mobile">
              <div class="column is-2">
                <figure class="image is-64x64">
                  <img :src="item.sku.image" :alt="item.sku.spu_name">
                </figure>
              </div>
              <div class="column">
                <p class="title is-6">{{ item.sku.spu_name }}</p>
                <p class="subtitle is-7">{{ item.sku.title }}</p>
                <p class="has-text-danger">¥{{ item.sku.price }}</p>
              </div>
              <div class="column is-narrow">
                <div class="field has-addons">
                  <p class="control">
                    <button class="button is-small" @click="cartStore.updateQuantity(item.id, item.quantity - 1)" :disabled="item.quantity <= 1">
                      -
                    </button>
                  </p>
                  <p class="control">
                    <input class="input is-small" type="text" :value="item.quantity" readonly style="width: 50px; text-align: center;">
                  </p>
                  <p class="control">
                    <button class="button is-small" @click="cartStore.updateQuantity(item.id, item.quantity + 1)" :disabled="item.quantity >= item.sku.stock">
                      +
                    </button>
                  </p>
                </div>
              </div>
              <div class="column is-narrow">
                <button class="button is-danger is-small" @click="cartStore.removeItem(item.id)">
                  <span class="icon">
                    <font-awesome-icon icon="fa-solid fa-trash" />
                  </span>
                </button>
              </div>
            </div>
          </div>
          
          <!-- 总计 -->
          <div class="box has-background-light">
            <div class="level">
              <div class="level-left">
                <div class="level-item">
                  <p class="title has-text-black is-5">总计：{{ cartStore.totalItems }} 件商品</p>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <p class="title is-4 has-text-danger">¥{{ cartStore.totalPrice }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <footer class="modal-card-foot">
        <button class="button is-success mr-3" :disabled="cartStore.cartItems.length === 0">结算</button>
        <button class="button" @click="closeCartModal">继续购物</button>
      </footer>
    </div>
  </div>
</template>

<script>

  import { ref } from 'vue'
  import { useUserStore } from '@/stores/user'
  import { useCartStore } from '@/stores/cart'

  import logoUrl from '@/assets/logoFront.png';

  export default {

    setup() {
      const userStore = useUserStore()
      const cartStore = useCartStore()
      const showCart = ref(false)

      const openCartModal = () => {
        showCart.value = true
        cartStore.fetchCartItems()
      }

      const closeCartModal = () => {
        showCart.value = false
      }

      return {
        userStore,
        cartStore,
        showCart,
        openCartModal,
        closeCartModal
      }
    },

    data() {
      return {
        logoUrl: logoUrl,
      }
    }
  }

</script>

<style lang="scss" scoped>

</style>