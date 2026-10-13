<script setup lang="ts">
// The default theme renders the home page without a <main> landmark (doc pages
// get one from VPDoc). This wraps the stock VPHome so screen readers can jump to it.
import VPHome from 'vitepress/dist/client/theme-default/components/VPHome.vue'
</script>

<template>
  <main class="VPHomeMain">
    <VPHome>
      <template v-for="(_, name) in $slots" #[name]="props">
        <slot :name="name" v-bind="props ?? {}" />
      </template>
    </VPHome>
  </main>
</template>
