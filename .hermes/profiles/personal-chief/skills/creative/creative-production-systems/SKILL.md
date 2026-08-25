---
name: creative-production-systems
description: "Use when generating or orchestrating creative media with specialized systems: ComfyUI workflows, Manim animations, TouchDesigner networks, or prose humanization."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, media, comfyui, manim, touchdesigner, animation, visual-production]
    related_skills: [visual-artifact-design, popular-web-designs]
---

# Creative Production Systems

## Overview

Use this umbrella when the user asks for a creative artifact that depends on a specialized production environment rather than simple text or image prompting. It routes between node-based image/video/audio generation, mathematical animation, real-time visual systems, and prose voice editing.

## Choose the System

| Need | System |
|---|---|
| Run/install/debug ComfyUI workflows or batches | ComfyUI |
| Create 3Blue1Brown-style math/algorithm animations | Manim CE |
| Control a TouchDesigner project through MCP/Python/operators | TouchDesigner |
| Rewrite text to sound more human and less AI-like | Humanizer |

## Workflow

1. Identify the target artifact and runtime: image workflow, animation scene, TD network, or prose rewrite.
2. Check environment readiness before promising output (GPU, CLI, Python deps, server health, project files).
3. Use the system-specific reference package for commands and pitfalls.
4. Produce a real artifact or verified preview when tools are available; report blockers honestly.
5. Preserve reusable workflows/scripts/templates inside the umbrella support tree.

## Re-homed Playbooks

Former specialized skills are preserved as support packages:

- `references/comfyui/original-skill.md` plus ComfyUI API, workflow, setup, health, and run scripts.
- `references/manim-video/original-skill.md` plus Manim planning/rendering/design references and setup script.
- `references/touchdesigner-mcp/original-skill.md` plus TouchDesigner MCP/operator/layout references and setup script.
- `references/humanizer/original-skill.md` for prose humanization patterns and voice editing.

## Pitfalls

- Do not claim a media artifact was generated without a file path, URL, render log, or screenshot.
- Do not flatten node/workflow support files; keep package-relative references intact under each re-homed subdirectory.
- Do not use a heavyweight creative runtime when a simple artifact tool is enough.
- Always distinguish design guidance from verified runtime execution.

## Verification Checklist

- [ ] Runtime/tool availability checked.
- [ ] System-specific reference consulted when commands/API details matter.
- [ ] Output artifact or exact blocker reported.
- [ ] Reusable workflows/scripts kept under the umbrella support tree.
