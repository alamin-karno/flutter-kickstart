import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import { h } from 'vue'
import HomeTerminal from './components/HomeTerminal.vue'
import HomeSections from './components/HomeSections.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () =>
    h(DefaultTheme.Layout, null, {
      'home-hero-image': () => h(HomeTerminal),
      'home-features-after': () => h(HomeSections),
    }),
} satisfies Theme
