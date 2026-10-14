<script setup lang="ts">
import { withBase } from 'vitepress'

const steps = [
  { n: '1', title: 'Install once', body: 'One line puts the fks command on your machine and the skills in every AI agent you use.', code: 'curl -fsSL …/install.sh | bash' },
  { n: '2', title: 'Answer a few questions', body: 'Name, organization, Bloc or Riverpod, network client, CI/CD. Press Enter to accept a default.', code: 'fks create' },
  { n: '3', title: 'Run a tested app', body: 'The generator only reports success after flutter analyze and flutter test pass.', code: 'cd my_app && fks run' },
]

const agents = ['Claude Code', 'Cursor', 'Windsurf', 'Antigravity', 'Codex', 'Gemini CLI', 'GitHub Copilot']
</script>

<template>
  <div class="fk-sections">
    <section class="block" aria-labelledby="how-it-works">
      <h2 id="how-it-works">How it works</h2>
      <p class="lead">From an empty folder to a project you can ship, in three steps.</p>
      <ol class="steps">
        <li v-for="s in steps" :key="s.n" class="step">
          <span class="num" aria-hidden="true">{{ s.n }}</span>
          <h3>{{ s.title }}</h3>
          <p>{{ s.body }}</p>
          <code>{{ s.code }}</code>
        </li>
      </ol>
    </section>

    <section class="block" aria-labelledby="agents">
      <h2 id="agents">Works with the AI agent you already use</h2>
      <p class="lead">
        Ask in plain words, like <span class="prompt">“Create a new Flutter app called Acme Wallet for com.acme”</span>.
        Every generated app also ships an <code>AGENTS.md</code> and project skills, so your agent keeps following
        the same rules after day one.
      </p>
      <ul class="fk-chips">
        <li v-for="a in agents" :key="a">{{ a }}</li>
      </ul>
    </section>

    <section class="block cta" aria-labelledby="cta">
      <h2 id="cta">Stop rebuilding the same app shell</h2>
      <p class="lead">Flavors, architecture, networking, tests and CI are the same on every project. Generate them, then spend your time on the features.</p>
      <div class="actions">
        <a class="btn brand" :href="withBase('/guide/quick-start')">Start in 2 minutes</a>
        <a class="btn alt" :href="withBase('/app/overview')">See what you get</a>
      </div>
    </section>
  </div>
</template>

<style scoped>
.fk-sections { padding: 0 24px; }
@media (min-width: 640px) { .fk-sections { padding: 0 48px; } }
@media (min-width: 960px) { .fk-sections { padding: 0 64px; } }
.block { max-width: 1152px; margin: 72px auto 0; }
h2 { font-size: 28px; line-height: 1.3; font-weight: 700; letter-spacing: -0.01em; margin: 0 0 8px; }
.lead { color: var(--vp-c-text-2); max-width: 720px; margin: 0 0 24px; line-height: 1.7; }
/* Upright on purpose: an italic run here would pull in the 74 KB Inter italic font just for this line. */
.prompt { color: var(--vp-c-text-1); font-weight: 500; }
.steps { display: grid; gap: 16px; grid-template-columns: 1fr; list-style: none; padding: 0; margin: 0; }
@media (min-width: 768px) { .steps { grid-template-columns: repeat(3, 1fr); } }
.step { position: relative; padding: 24px; border-radius: 12px; background: var(--vp-c-bg-soft); border: 1px solid var(--vp-c-divider); }
.num {
  display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%;
  background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); font-weight: 700; margin-bottom: 12px;
}
.step h3 { margin: 0 0 6px; font-size: 18px; font-weight: 600; }
.step p { margin: 0 0 14px; color: var(--vp-c-text-2); font-size: 15px; line-height: 1.6; }
.step code { font-size: 13px; padding: 4px 8px; border-radius: 6px; background: var(--vp-c-bg); color: var(--vp-c-text-1); border: 1px solid var(--vp-c-divider); }
.cta { text-align: center; margin-bottom: 96px; padding: 48px 24px; border-radius: 16px; background: linear-gradient(135deg, var(--vp-c-brand-soft), rgba(255, 138, 61, 0.1)); }
.cta .lead { margin-left: auto; margin-right: auto; }
.actions { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
.btn { display: inline-block; padding: 0 20px; line-height: 40px; border-radius: 20px; font-weight: 600; font-size: 14px; text-decoration: none; transition: background-color 0.2s; }
.btn.brand { background: var(--vp-button-brand-bg); color: var(--vp-button-brand-text); }
.btn.brand:hover { background: var(--vp-button-brand-hover-bg); }
.btn.alt { background: var(--vp-button-alt-bg); color: var(--vp-button-alt-text); border: 1px solid var(--vp-button-alt-border); }
.btn.alt:hover { background: var(--vp-button-alt-hover-bg); }
</style>
