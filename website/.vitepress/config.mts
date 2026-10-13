import { defineConfig, type HeadConfig } from 'vitepress'

const SITE_URL = 'https://alamin-karno.github.io/flutter-kickstart/'
const BASE = '/flutter-kickstart/'
const REPO = 'https://github.com/alamin-karno/flutter-kickstart'
const TITLE = 'Flutter Kickstart'
const DESCRIPTION =
  'Create a production-ready Flutter app from a few quick questions: flavors, clean architecture, Bloc or Riverpod, ' +
  'Dio networking, go_router, tests, GitHub Actions + Fastlane CI/CD, and AI-agent rules for Claude Code, Cursor, ' +
  'Windsurf, Antigravity, Codex, Gemini CLI and Copilot.'
const OG_IMAGE = `${SITE_URL}og-image.jpg`

export default defineConfig({
  lang: 'en-US',
  title: TITLE,
  titleTemplate: ':title | Flutter Kickstart',
  description: DESCRIPTION,
  base: BASE,
  cleanUrls: true,
  lastUpdated: true,
  srcExclude: ['README.md'],

  sitemap: { hostname: SITE_URL },

  markdown: {
    theme: { light: 'github-light', dark: 'github-dark' },
    lineNumbers: false,
  },

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${BASE}favicon.svg` }],
    ['link', { rel: 'icon', type: 'image/png', sizes: '32x32', href: `${BASE}favicon-32.png` }],
    ['link', { rel: 'apple-touch-icon', sizes: '180x180', href: `${BASE}apple-touch-icon.png` }],
    ['meta', { name: 'theme-color', content: '#0468D7' }],
    ['meta', { name: 'author', content: 'Md. Al-Amin' }],
    ['meta', { name: 'google-site-verification', content: 'gjJvl6jAwo8pORAiWoawGoaLl9DNNyoA9Mo73_M7AQY' }],
    [
      'meta',
      {
        name: 'keywords',
        content:
          'flutter, flutter starter, flutter boilerplate, flutter template, flutter scaffold, flutter clean architecture, ' +
          'flutter bloc, flutter riverpod, very good cli, flutter flavors, flutter ci cd, fastlane, go_router, ' +
          'claude code, cursor, windsurf, ai coding agent, agents.md',
      },
    ],
    ['meta', { property: 'og:site_name', content: TITLE }],
    ['meta', { property: 'og:locale', content: 'en_US' }],
    ['meta', { property: 'og:image', content: OG_IMAGE }],
    ['meta', { property: 'og:image:width', content: '1200' }],
    ['meta', { property: 'og:image:height', content: '630' }],
    ['meta', { property: 'og:image:alt', content: 'Flutter Kickstart: production-ready Flutter apps from a few quick questions' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }],
    ['meta', { name: 'twitter:site', content: '@alamin_karno' }],
    ['meta', { name: 'twitter:image', content: OG_IMAGE }],
  ],

  // Per-page canonical URL, Open Graph / Twitter text and JSON-LD.
  transformHead({ pageData }) {
    const path = pageData.relativePath.replace(/(^|\/)index\.md$/, '$1').replace(/\.md$/, '')
    const url = `${SITE_URL}${path}`
    const isHome = path === ''
    const title = isHome ? `${TITLE}: production-ready Flutter apps from a few quick questions` : `${pageData.title} | ${TITLE}`
    const description = pageData.description || DESCRIPTION

    const head: HeadConfig[] = [
      ['link', { rel: 'canonical', href: url }],
      ['meta', { property: 'og:type', content: isHome ? 'website' : 'article' }],
      ['meta', { property: 'og:url', content: url }],
      ['meta', { property: 'og:title', content: title }],
      ['meta', { property: 'og:description', content: description }],
      ['meta', { name: 'twitter:title', content: title }],
      ['meta', { name: 'twitter:description', content: description }],
    ]

    if (isHome) {
      head.push([
        'script',
        { type: 'application/ld+json' },
        JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'SoftwareApplication',
          name: TITLE,
          alternateName: 'fks',
          description: DESCRIPTION,
          url: SITE_URL,
          image: OG_IMAGE,
          applicationCategory: 'DeveloperApplication',
          operatingSystem: 'macOS, Linux, Windows',
          offers: { '@type': 'Offer', price: '0', priceCurrency: 'USD' },
          license: `${REPO}/blob/main/LICENSE`,
          codeRepository: REPO,
          author: { '@type': 'Person', name: 'Md. Al-Amin', url: 'https://github.com/alamin-karno' },
        }),
      ])
    }
    return head
  },

  themeConfig: {
    logo: { src: '/logo.svg', alt: 'Flutter Kickstart logo', width: 28, height: 28 },

    nav: [
      { text: 'Guide', link: '/guide/introduction', activeMatch: '/guide/' },
      { text: 'Generated app', link: '/app/overview', activeMatch: '/app/' },
      { text: 'Reference', link: '/reference/cli', activeMatch: '/reference/' },
      { text: 'Contributing', link: '/contributing/', activeMatch: '/contributing/' },
      {
        text: 'Links',
        items: [
          { text: 'Changelog', link: `${REPO}/blob/main/CHANGELOG.md` },
          { text: 'Releases', link: `${REPO}/releases` },
          { text: 'Report an issue', link: `${REPO}/issues/new/choose` },
        ],
      },
    ],

    sidebar: {
      '/': [
        {
          text: 'Getting started',
          items: [
            { text: 'Introduction', link: '/guide/introduction' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Quick start', link: '/guide/quick-start' },
            { text: 'Setup questions', link: '/guide/setup-questions' },
          ],
        },
        {
          text: 'Using it',
          items: [
            { text: 'Using it with AI agents', link: '/guide/ai-agents' },
            { text: 'Adding features', link: '/guide/adding-features' },
            { text: 'Figma to Flutter', link: '/guide/figma-to-flutter' },
          ],
        },
        {
          text: 'The generated app',
          items: [
            { text: 'What you get', link: '/app/overview' },
            { text: 'Architecture', link: '/app/architecture' },
            { text: 'State management', link: '/app/state-management' },
            { text: 'Networking and errors', link: '/app/networking' },
            { text: 'Flavors and config', link: '/app/flavors' },
            { text: 'Testing and quality gate', link: '/app/testing' },
            { text: 'CI/CD and releases', link: '/app/ci-cd' },
            { text: 'AI layer', link: '/app/ai-layer' },
          ],
        },
        {
          text: 'Reference',
          items: [
            { text: 'fks CLI', link: '/reference/cli' },
            { text: 'Generator flags', link: '/reference/flags' },
            { text: 'Troubleshooting', link: '/reference/troubleshooting' },
            { text: 'FAQ', link: '/reference/faq' },
          ],
        },
        {
          text: 'Contributing',
          items: [
            { text: 'How to contribute', link: '/contributing/' },
            { text: 'Branches and releases', link: '/contributing/git-flow' },
            { text: 'Changing the templates', link: '/contributing/templates' },
          ],
        },
      ],
    },

    socialLinks: [{ icon: 'github', link: REPO }],

    editLink: {
      pattern: `${REPO}/edit/dev/website/:path`,
      text: 'Edit this page on GitHub',
    },

    search: { provider: 'local' },

    outline: { level: [2, 3] },

    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 Md. Al-Amin',
    },
  },
})
