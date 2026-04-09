---
source: https://github.com/openclaw/openclaw
category: agent
sub_categories: [framework, protocol]
tags: [Swift, Kotlin, TypeScript, AI-assistant, multi-platform, voice-interface, plugin-system, LLM-gateway]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# openclaw

# openclaw

## 基本情報
- リポジトリ: https://github.com/openclaw/openclaw
- カテゴリ: agent
- サブカテゴリ: framework, protocol
- タグ: Swift, Kotlin, TypeScript, AI-assistant, multi-platform, voice-interface, plugin-system, LLM-gateway
- 最終確認日: 2026-04-09

## 概要
OpenClaw is a multi-platform AI assistant framework with native apps for macOS, iOS, Android, and Apple Watch, connected to a central gateway server. It enables LLM-powered agents to interact with device capabilities (camera, calendar, contacts, location, SMS) and dozens of messaging channels (Discord, Telegram, iMessage, etc.) through a plugin-based architecture. The system exposes a rich tool/skill ecosystem and supports voice wake, talk mode, browser automation, and multi-agent workflows.

## 設計思想
OpenClaw follows a hub-and-spoke architecture: a macOS/Linux gateway node acts as the central AI runtime and protocol bridge, while mobile/watch clients connect to it via a custom TLS-pinned WebSocket protocol (BonjourService-based local discovery or remote tunnel). The platform is heavily plugin-driven, with each channel, provider, and tool implemented as an isolated extension module exposing typed contract APIs. Separation between setup, runtime, and protocol layers is enforced across every plugin. Cross-platform shared logic lives in an OpenClawKit Swift package and TypeScript extension packages.

## 主要コンポーネント
- Gateway Server (macOS): Central AI runtime and WebSocket bridge connecting mobile nodes to LLM providers and tool backends
- GatewayChannel / GatewayNodeSession: Custom TLS-pinned WebSocket protocol layer for secure client-gateway communication
- OpenClawKit (Swift): Shared Swift package providing protocol models, chat UI, camera/audio/location abstractions, and canvas primitives for iOS/macOS/watchOS
- Android Node App: Kotlin-based mobile agent node exposing device capabilities via an InvokeCommandRegistry to the gateway
- Plugin Extension System (TypeScript): Modular extensions for 50+ channel integrations, LLM providers, search tools, and browser automation
- CanvasA2UI: Agent-to-UI action protocol enabling the AI to drive native canvas/webview interfaces on client devices
- TalkMode / VoiceWake: Voice interaction layer with wake-word detection, push-to-talk, streaming TTS, and directive parsing
- Skills / SKILL.md: Declarative agent skill definitions that extend agent capabilities with curated instruction sets
- ExecApprovals: Security layer requiring human approval before executing shell commands, with allowlist matching and gateway prompting
- Browser Plugin (Playwright): Headless browser automation tool with CDP proxy, snapshot, and agent-act routes for web interaction

## 実装パターン
- Contract-API separation: Each plugin exposes typed contract-api.ts, runtime-api.ts, setup-api.ts, and channel-config-api.ts files, enforcing strict interface boundaries between lifecycle phases
- Plugin manifest registration: Plugins declare capabilities via openclaw.plugin.json manifests and register providers/channels/tools at startup through typed entry points
- TLS pinning + TOFU gateway auth: Mobile clients perform device identity authentication and TLS certificate pinning against the gateway, with a Bonjour-based local discovery and QR-code pairing flow
- InvokeDispatcher / CommandRegistry: Android and iOS nodes implement a command registry pattern mapping string capability names to handler classes, dispatched via the gateway protocol
- JSONL streaming canvas protocol: Agent-to-UI actions are streamed as JSONL over the gateway channel, allowing incremental rendering of canvas content on client devices
- Skill-based agent extension: SKILL.md files in .agents/skills/ and extension skill folders define declarative agent behaviors that are injected into the system prompt context
- Session compaction: Long-running sessions are compacted via checkpoint snapshots to manage context window limits while preserving conversation continuity

## 適用シーン
Building a personal AI assistant with deep device integration across Apple and Android ecosystems; deploying a self-hosted LLM gateway with multi-channel reach (iMessage, Discord, Telegram, etc.); creating automation workflows triggered by cron, webhooks, or messaging; developing custom AI tools/skills that leverage camera, location, screen recording, or browser automation; running multi-agent coordination with sub-agent delegation and exec approval flows.

## 注意点・制約
The gateway requires macOS or Linux as the primary runtime host; mobile apps depend on a running gateway instance and cannot operate standalone as AI agents. The plugin ecosystem has complex inter-package dependencies requiring careful version alignment. Browser automation relies on system Chrome/Playwright availability. Voice wake and camera features require explicit OS permission grants. Exec approval security policies must be carefully configured to avoid unintended shell access.


## 関連ナレッジ
- (なし)
