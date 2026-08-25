---
name: mlops-model-tooling
description: "Use when operating ML/LLM tooling across Hugging Face, local/server inference, evaluation, experiment tracking, model surgery, and specialist model workflows. Provides a class-level routing map for MLOps tasks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [mlops, llm, inference, evaluation, huggingface, wandb, vllm, llama-cpp]
    related_skills: []
---

# MLOps Model Tooling

## Overview

This umbrella routes ML and LLM operational tasks to the right tooling class: model discovery/download, local inference, server inference, evaluation, experiment tracking, fine-tuning support, model surgery, and specialist model workflows.

## When to Use

- Search, download, upload, or manage models/datasets on Hugging Face Hub.
- Run local GGUF inference with llama.cpp or serve OpenAI-compatible LLM APIs with vLLM.
- Benchmark models with lm-eval-harness or API-based evaluation.
- Track experiments, sweeps, artifacts, and model registries in W&B.
- Work with specialist model packages such as AudioCraft or Segment Anything.

## Capability Map

### Hub Discovery and Artifacts

Use Hugging Face CLI/API for model/dataset search, download, upload, token checks, and artifact inspection. Verify license, file sizes, and expected formats before downloading large assets.

### Local Inference: llama.cpp

Best for local GGUF inference, quant selection, llama.cpp server mode, CPU/GPU split tuning, and extracting available GGUFs from Hub repositories.

### Server Inference: vLLM

Best for high-throughput GPU serving, OpenAI-compatible APIs, tensor parallelism, quantized serving, and deployment performance tuning.

### Evaluation

Use lm-eval-harness for benchmark suites and custom tasks. Pin model, revision, prompt format, batch size, seeds, and hardware/API endpoints in result reports.

### Tracking and Experiment Management

Use W&B for run logging, sweeps, artifacts, dashboards, and integration with training/eval scripts. Check login and project/entity settings first.

### Specialist Models

- AudioCraft: MusicGen, AudioGen, EnCodec text/audio generation.
- Segment Anything: point/box/mask prompting, automatic masks, batched inference, ONNX export.
- Model surgery/obliteration workflows need careful before/after evaluation and reproducibility notes.

## Standard Workflow

1. Identify task class: hub, inference, serving, eval, tracking, training, or specialist model.
2. Check hardware, credentials, installed commands, Python environment, and disk budget.
3. Run the smallest verification first.
4. Scale to the requested job.
5. Record exact commands, model IDs/revisions, parameters, hardware, and outputs.

## Common Pitfalls

1. **Downloading huge models before checking disk/VRAM.** Inspect files first.
2. **Mixing model formats.** GGUF, safetensors, checkpoints, and server endpoints require different tools.
3. **Unreproducible evals.** Report revision, prompt format, seeds, and harness version.
4. **Assuming GPU availability.** Check live system state.
5. **Trusting dashboards without artifact IDs.** Capture run URLs/IDs and output files.

## Verification Checklist

- [ ] Tool class selected correctly.
- [ ] Credentials/hardware/disk/environment checked.
- [ ] Small smoke test passed before large job.
- [ ] Outputs include model ID/revision, commands, metrics, and artifact paths/URLs.
