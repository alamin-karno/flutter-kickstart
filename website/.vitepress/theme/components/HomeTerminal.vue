<script setup lang="ts">
// A static recording of `fks create`, revealed line by line on load.
const lines: { kind: 'cmd' | 'q' | 'out' | 'ok'; text: string; answer?: string }[] = [
  { kind: 'cmd', text: 'fks create' },
  { kind: 'q', text: 'App display name?', answer: 'Acme Wallet' },
  { kind: 'q', text: 'Organization / reverse domain?', answer: 'com.acme' },
  { kind: 'q', text: 'State management? bloc / riverpod', answer: 'bloc' },
  { kind: 'q', text: 'Network client? viva / dio', answer: 'dio' },
  { kind: 'q', text: 'CI/CD? github / none', answer: 'github' },
  { kind: 'out', text: 'Generating 3 flavors, 2 features, AI layer…' },
  { kind: 'ok', text: 'flutter analyze: no issues' },
  { kind: 'ok', text: 'flutter test: all passed (95% coverage)' },
  { kind: 'cmd', text: 'cd acme_wallet && fks run' },
]
</script>

<template>
  <div class="fk-terminal" role="img" aria-label="Terminal running fks create: answer a few questions and get a tested Flutter app">
    <div class="bar" aria-hidden="true">
      <span class="dot r" /><span class="dot y" /><span class="dot g" />
      <span class="title">~/projects</span>
    </div>
    <div class="body" aria-hidden="true">
      <div v-for="(l, i) in lines" :key="i" class="line" :style="{ animationDelay: `${0.25 + i * 0.32}s` }">
        <template v-if="l.kind === 'cmd'"><span class="prompt">$</span> {{ l.text }}</template>
        <template v-else-if="l.kind === 'q'"><span class="q">?</span> <b>{{ l.text }}</b> <span class="a">{{ l.answer }}</span></template>
        <template v-else-if="l.kind === 'ok'"><span class="okmark">✓</span> {{ l.text }}</template>
        <span v-else class="dim">{{ l.text }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.fk-terminal {
  position: relative;
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  border-radius: 14px;
  overflow: hidden;
  background: #0b1622;
  border: 1px solid rgba(79, 195, 255, 0.25);
  box-shadow: 0 24px 60px -20px rgba(2, 86, 155, 0.55);
  text-align: left;
}
.bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  background: #102233;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.dot { width: 11px; height: 11px; border-radius: 50%; }
.r { background: #ff5f57; }
.y { background: #febc2e; }
.g { background: #28c840; }
.title { margin-left: 8px; font: 12px var(--vp-font-family-mono); color: #7f97ad; }
.body {
  margin: 0;
  padding: 16px 18px 18px;
  font: 13px/1.75 var(--vp-font-family-mono);
  color: #d6e6f5;
  overflow-wrap: anywhere;
}
.line { display: block; opacity: 0; animation: fk-in 0.35s ease forwards; }
.prompt { color: #4fc3ff; font-weight: 700; }
.q { color: #ff8a3d; font-weight: 700; }
.a { color: #4fc3ff; }
.okmark { color: #28c840; font-weight: 700; }
.dim { color: #7f97ad; }
b { font-weight: 600; color: #ffffff; }
@keyframes fk-in {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: none; }
}
@media (prefers-reduced-motion: reduce) {
  .line { animation: none; opacity: 1; }
}
@media (max-width: 480px) {
  .body { font-size: 12px; padding: 12px; }
}
</style>
