<template>
    <figure class="logo-container image is-128x128 mr-6">
        <img :src="logoUrl" alt="Logo" />
    </figure>
</template>

<script>
import logoUrl from '@/assets/logo.svg'
    export default {
    data() {
      return {
        logoUrl: logoUrl
      }
    }
    }
</script>

<style lang="scss" scoped>
.logo-container{

  justify-self: center;
  align-self: center;
}
</style>