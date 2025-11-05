<template>
    <div class="container mt-6">
        <h1 class="title is-3 mb-5">购物车</h1>

        <div v-if="cartStore.loading" class="has-text-centered">
            <p>加载中...</p>
        </div>

        <div v-else-if="!cartStore.cartItems || cartStore.cartItems.length === 0" class="box has-text-centered">
            <p class="subtitle">购物车是空的</p>
            <router-link to="/merch" class="button is-primary">去逛逛</router-link>
        </div>

        <div v-else>
            <!-- 批量操作栏 -->
            <div class="box mb-4">
                <div class="level">
                    <div class="level-left">
                        <div class="level-item">
                            <label class="checkbox">
                                <input type="checkbox" v-model="selectAll" @change="toggleSelectAll">
                                全选
                            </label>
                        </div>
                        <div class="level-item">
                            <button class="button is-danger is-small" 
                                    @click="batchDelete" 
                                    :disabled="selectedItems.length === 0">
                                删除选中 ({{ selectedItems.length }})
                            </button>
                        </div>
                        <div class="level-item">
                            <button class="button is-warning is-small" 
                                    @click="clearInvalid" 
                                    :disabled="invalidItems.length === 0">
                                清理失效商品 ({{ invalidItems.length }})
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 购物车商品列表 -->
            <div class="box mb-2" v-for="item in cartStore.cartItems" :key="item.id">
                <div class="columns is-vcentered">
                    <!-- 选择框 -->
                    <div class="column is-narrow">
                        <label class="checkbox">
                            <input type="checkbox" 
                                   :value="item.id" 
                                   v-model="selectedItems"
                                   :disabled="!item.sku.is_active">
                        </label>
                    </div>

                    <!-- 商品图片 -->
                    <div class="column is-narrow">
                        <figure class="image is-96x96">
                            <img :src="item.sku.image || defaultImage" :alt="item.sku.title">
                        </figure>
                    </div>

                    <!-- 商品信息 -->
                    <div class="column">
                        <div class="content">
                            <p class="title is-6 mb-1">
                                {{ item.sku.spu_name }}
                                <span v-if="!item.sku.is_active" class="tag is-danger ml-2">已失效</span>
                            </p>
                            <p class="subtitle is-7 has-text-grey mb-2">{{ item.sku.title }}</p>
                            <p class="has-text-weight-semibold has-text-primary">¥{{ item.sku.price }}</p>
                        </div>
                    </div>

                    <!-- 数量控制 -->
                    <div class="column is-narrow">
                        <div class="field has-addons">
                            <p class="control">
                                <button class="button is-small" 
                                        @click="decreaseQuantity(item)"
                                        :disabled="item.quantity <= 1 || !item.sku.is_active">
                                    <span class="icon is-small">
                                        <font-awesome-icon icon="fa-solid fa-minus" />
                                    </span>
                                </button>
                            </p>
                            <p class="control">
                                <input class="input is-small quantity-input" 
                                       type="number" 
                                       v-model.number="item.quantity"
                                       @change="updateQuantity(item)"
                                       :disabled="!item.sku.is_active"
                                       :min="1"
                                       :max="item.sku.stock"
                                       style="width: 60px; text-align: center;">
                            </p>
                            <p class="control">
                                <button class="button is-small" 
                                        @click="increaseQuantity(item)"
                                        :disabled="item.quantity >= item.sku.stock || !item.sku.is_active">
                                    <span class="icon is-small">
                                        <font-awesome-icon icon="fa-solid fa-plus" />
                                    </span>
                                </button>
                            </p>
                        </div>
                        <p class="help" :class="{ 'has-text-danger': item.quantity > item.sku.stock }">
                            库存: {{ item.sku.stock }}
                        </p>
                        <p v-if="item.quantity > item.sku.stock" class="help has-text-danger">
                            库存不足
                        </p>
                    </div>

                    <!-- 小计 -->
                    <div class="column is-narrow">
                        <p class="has-text-weight-bold has-text-danger is-size-5">
                            ¥{{ item.total_price }}
                        </p>
                    </div>

                    <!-- 删除按钮 -->
                    <div class="column is-narrow">
                        <button class="button is-small is-ghost" 
                                @click="removeItem(item.id)"
                                title="删除">
                            <span class="icon">
                                <font-awesome-icon icon="fa-solid fa-trash" />
                            </span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- 结算栏 -->
            <div class="box has-background-light">
                <div class="level">
                    <div class="level-left">
                        <div class="level-item">
                            <span class="has-text-weight-semibold">
                                已选 {{ selectedItems.length }} 件商品
                            </span>
                        </div>
                    </div>
                    <div class="level-right">
                        <div class="level-item">
                            <span class="mr-3">
                                合计: <span class="has-text-danger has-text-weight-bold is-size-4">¥{{ selectedTotalPrice }}</span>
                            </span>
                        </div>
                        <div class="level-item">
                            <button class="button is-primary is-medium" 
                                    @click="checkout"
                                    :disabled="selectedItems.length === 0 || hasInvalidSelected">
                                结算
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useRouter } from 'vue-router'

export default {
    setup() {
        const cartStore = useCartStore()
        const router = useRouter()
        const selectedItems = ref([])
        const selectAll = ref(false)
        const defaultImage = '/default-product.png'

        // 计算失效商品
        const invalidItems = computed(() => {
            return cartStore.cartItems.filter(item => !item.sku.is_active)
        })

        // 计算选中商品的总价
        const selectedTotalPrice = computed(() => {
            const total = cartStore.cartItems
                .filter(item => selectedItems.value.includes(item.id))
                .reduce((sum, item) => sum + parseFloat(item.total_price), 0)
            return total.toFixed(2)
        })

        // 检查选中项中是否有失效商品
        const hasInvalidSelected = computed(() => {
            return cartStore.cartItems
                .filter(item => selectedItems.value.includes(item.id))
                .some(item => !item.sku.is_active || item.quantity > item.sku.stock)
        })

        // 全选/取消全选
        const toggleSelectAll = () => {
            if (selectAll.value) {
                // 只选择有效商品
                selectedItems.value = cartStore.cartItems
                    .filter(item => item.sku.is_active)
                    .map(item => item.id)
            } else {
                selectedItems.value = []
            }
        }

        // 减少数量
        const decreaseQuantity = (item) => {
            if (item.quantity > 1) {
                cartStore.updateQuantity(item.id, item.quantity - 1)
            }
        }

        // 增加数量
        const increaseQuantity = (item) => {
            if (item.quantity < item.sku.stock) {
                cartStore.updateQuantity(item.id, item.quantity + 1)
            } else {
                alert('库存不足')
            }
        }

        // 更新数量
        const updateQuantity = (item) => {
            if (item.quantity < 1) {
                item.quantity = 1
                return
            }
            if (item.quantity > item.sku.stock) {
                alert('库存不足')
                item.quantity = item.sku.stock
                return
            }
            cartStore.updateQuantity(item.id, item.quantity)
        }

        // 删除单个商品
        const removeItem = async (itemId) => {
            if (confirm('确定要删除这个商品吗？')) {
                await cartStore.removeItem(itemId)
                // 从选中列表中移除
                selectedItems.value = selectedItems.value.filter(id => id !== itemId)
            }
        }

        // 批量删除
        const batchDelete = async () => {
            if (selectedItems.value.length === 0) return
            
            if (confirm(`确定要删除选中的 ${selectedItems.value.length} 个商品吗？`)) {
                const success = await cartStore.batchRemoveItems(selectedItems.value)
                if (success) {
                    selectedItems.value = []
                    selectAll.value = false
                }
            }
        }

        // 清理失效商品
        const clearInvalid = async () => {
            const invalidIds = invalidItems.value.map(item => item.id)
            if (invalidIds.length === 0) return

            if (confirm(`确定要清理 ${invalidIds.length} 个失效商品吗？`)) {
                const success = await cartStore.batchRemoveItems(invalidIds)
                if (success) {
                    selectedItems.value = selectedItems.value.filter(id => !invalidIds.includes(id))
                    selectAll.value = false
                }
            }
        }

        // 结算
        const checkout = () => {
            if (selectedItems.value.length === 0) {
                alert('请选择要结算的商品')
                return
            }

            if (hasInvalidSelected.value) {
                alert('选中的商品中有失效或库存不足的商品，请重新选择')
                return
            }

            // TODO: 跳转到结算页面
            alert('结算功能开发中...')
        }

        onMounted(() => {
            cartStore.fetchCartItems()
        })

        return {
            cartStore,
            selectedItems,
            selectAll,
            defaultImage,
            invalidItems,
            selectedTotalPrice,
            hasInvalidSelected,
            toggleSelectAll,
            decreaseQuantity,
            increaseQuantity,
            updateQuantity,
            removeItem,
            batchDelete,
            clearInvalid,
            checkout
        }
    }
}
</script>

<style scoped>
.quantity-input::-webkit-outer-spin-button,
.quantity-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.quantity-input[type=number] {
    -moz-appearance: textfield;
    appearance: textfield;
}
</style>
