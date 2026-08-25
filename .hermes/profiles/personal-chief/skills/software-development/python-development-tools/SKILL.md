---
name: python-development-tools
description: "Use when developing, debugging, or automating Python workflows across local debugpy sessions, live Jupyter kernels, and Pythonista/iOS automation."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [python, debugging, jupyter, ios, automation, debugpy]
    related_skills: [software-quality-workflows]
---

# Python Development Tools

## Overview

This umbrella covers Python-specific development environments and runtime workflows: debugger attachment with `debugpy`, iterative execution through a live Jupyter kernel, and Pythonista/iOS automation scripts. Use it when the user's task is about operating Python tooling rather than general software quality.

## Choose the Mode

| Task | Mode |
|---|---|
| Step through Python code, inspect variables, debug tests | `debugpy` / DAP workflow |
| Iterate on data analysis or notebook-style code in a persistent kernel | Jupyter live kernel workflow |
| Build or modernize scripts meant to run in Pythonista on iOS | Pythonista/iOS automation workflow |

## Core Practices

- Use project-local virtual environments or `uv` on PEP 668 systems; avoid mutating system Python.
- Keep debugger, notebook, and mobile automation setup separate from production code paths.
- Verify with the actual runtime: attach to the process, execute the notebook cell/code, or run the Pythonista-compatible script path.
- Document environment-specific assumptions such as iOS APIs, kernel names, ports, and launch commands.

## Re-homed Playbooks

Former narrow skills are preserved as references:

- `references/python-debugpy/original-skill.md` — `debugpy` launch/attach patterns, DAP flow, test debugging, and breakpoints.
- `references/jupyter-live-kernel/original-skill.md` — live Jupyter kernel usage and iterative analysis loop.
- `references/pythonista-ios-automation/original-skill.md` plus nested references for iOS/Pythonista script modernization.

## Pitfalls

- Do not assume notebook state matches the filesystem; rerun cells or restart the kernel when state matters.
- Do not expose debug ports broadly; bind to localhost unless remote debugging is explicitly intended.
- Do not use desktop-only Python packages/APIs in Pythonista scripts without checking iOS compatibility.
- Do not report a debugger workflow as working until an attach/step/evaluate action succeeded.

## Verification Checklist

- [ ] Correct Python environment selected.
- [ ] Runtime-specific command actually executed.
- [ ] Debug/notebook/mobile assumptions documented.
- [ ] Outputs or breakpoints verified with real tool output.
