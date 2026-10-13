---
layout: home
title: "Flutter Kickstart: production-ready Flutter apps from one interview"
titleTemplate: false
description: Flutter Kickstart creates a production-ready Flutter app from one short interview. Flavors, clean architecture, Bloc or Riverpod, Dio networking, go_router, tests, CI/CD and AI-agent rules, verified before you see it.

hero:
  name: Flutter Kickstart
  text: Production-ready Flutter apps from one short interview
  tagline: Answer a few questions. Get flavors, clean architecture, Bloc or Riverpod, networking, tests, CI/CD and AI-agent rules, already passing flutter analyze and flutter test.
  actions:
    - theme: brand
      text: Get started
      link: /guide/quick-start
    - theme: alt
      text: What you get
      link: /app/overview
    - theme: alt
      text: View on GitHub
      link: https://github.com/alamin-karno/flutter-kickstart

features:
  - icon: 🧭
    title: One interview, same result every time
    details: The interview feeds a deterministic generator, so any agent or teammate gets the same project from the same answers.
    link: /guide/interview
    linkText: See the questions
  - icon: ✅
    title: Verified before you see it
    details: The generator runs codegen, format, flutter analyze and flutter test, and checks the coverage floor. If anything fails, it stops and tells you why.
    link: /app/testing
    linkText: Testing and quality gate
  - icon: 🏗️
    title: Clean architecture
    details: Feature-first domain, data and presentation layers, with core contracts for networking, logging, crash reporting, routing and theming.
    link: /app/architecture
    linkText: Architecture
  - icon: 🔀
    title: Bloc or Riverpod, viva or Dio
    details: You choose state management and the HTTP client. Feature code only sees the AppApiClient contract, so both paths look the same.
    link: /app/state-management
    linkText: State management
  - icon: 🚀
    title: CI/CD that knows your flavors
    details: GitHub Actions for PR checks, Android and iOS builds, Firebase App Distribution, Play and TestFlight, plus Fastlane and a setup guide.
    link: /app/ci-cd
    linkText: CI/CD and releases
  - icon: 🤖
    title: Built for AI coding agents
    details: Every app ships AGENTS.md, ten project skills, Cursor and Windsurf rules, Copilot instructions and reviewer subagents.
    link: /app/ai-layer
    linkText: AI layer
---
