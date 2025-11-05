<template>
  <div class="container">

    <div class="columns ">

      <router-link class="" to="/merch">
          
        <div class="column">
          <section class="hero is-danger is-halfheight"
          :class="{ 'hovered': isHovered }"
          @mouseover="isHovered = true"
          @mouseleave="isHovered = false"
          >
            <div class="hero-body">
              <div class="">
                <p class="title">Merch</p>
              </div>
            </div>
          </section>
        </div>
      </router-link>
      
      <router-link class="" to="/publication">

        <div class="column">
          <section class="hero is-warning is-halfheight"
          :class="{ 'hovered': isHovered2 }"
          @mouseover="isHovered2 = true"
          @mouseleave="isHovered2 = false"
          >
            <div class="hero-body">
              <div class="">
                <p class="title">Publication</p>
              </div>
            </div>
          </section>
        </div>
      </router-link>

      <router-link class="" to="/communicate">

        <div class="column">
          <section class="hero is-success is-halfheight"
          :class="{ 'hovered': isHovered3 }"
          @mouseover="isHovered3 = true"
          @mouseleave="isHovered3 = false"
          >
            <div class="hero-body">
              <div class="">
                <p class="title">Communicate</p>
              </div>
            </div>
          </section>
        </div>
      </router-link>
      
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isHovered = ref(false);
const isHovered2 = ref(false);
const isHovered3 = ref(false);
</script>

<style scoped>
  .container {

    grid-column: 1/ -1
  }

  .hero {

    border-radius: 100%
  }

  .hero.hovered {
    background-color: #000000;
    box-shadow: -4px -4px 5px rgba(0,209,178);
    border-radius: 0%;

    /* 平滑过渡 */
    transition: all 1s ease;
  }

  .title {

    width: 240px;
  }
</style>