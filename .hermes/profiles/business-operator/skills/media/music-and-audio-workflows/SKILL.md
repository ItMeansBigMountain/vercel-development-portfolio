---
name: music-and-audio-workflows
description: "Use when working with music and audio: songwriting, AI music prompts/generation, MusicGen/HeartMuLa-style generation, spectrogram or feature analysis, Spotify control, and music-app modernization patterns."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [music, audio, songwriting, ai-music, spotify, spectrograms, musicgen]
    related_skills: []
---

# Music and Audio Workflows

## Overview

This is the umbrella for music/audio creation, generation, analysis, playback control, and app/API modernization. Choose the narrowest workflow: lyric craft, model generation, audio analysis, streaming control, or product engineering.

## When to Use

- Write lyrics, song structure, or AI music prompts.
- Generate songs/sounds with Suno-like or MusicGen/AudioGen tooling.
- Analyze audio with spectrograms, mel/chroma/MFCC features, or visualizations.
- Control Spotify playback, queue, playlists, or devices.
- Modernize music apps with OAuth providers, provider fallback, and music intelligence UX.

## Capability Map

### Songwriting and AI Music Prompts

Start with structure, emotional arc, meter/rhyme, and genre references. For AI singers, include section tags, concise style tags, pronunciation hints, and avoid overloading prompts.

### Generation Engines

- HeartMuLa/Suno-like flows: lyrics + tags -> generated audio; check hardware/CUDA requirements before promising local generation.
- AudioCraft/MusicGen/AudioGen: text-to-music/sound, melody conditioning, EnCodec workflows; verify GPU/installation state.

### Audio Analysis

Use CLI feature extraction or visualization for spectrograms, mel, chroma, MFCC, and related views. Save generated artifacts and report file paths.

### Spotify Operations

Use API/tool calls for search, play, queue, playlists, and devices. Be explicit about URIs/IDs and handle device-not-active failures.

### Music-App Engineering

For music product modernization, plan provider OAuth, unified schemas, provider-specific callbacks, caching, fallback behavior, and user-facing music intelligence features.

## Standard Workflow

1. Identify whether the request is creative writing, generation, analysis, playback, or app engineering.
2. Check required credentials, binaries, GPU, or provider access.
3. Produce the artifact or perform the action.
4. Verify by reading output metadata, saved files, playback state, or app smoke tests.

## Common Pitfalls

1. **Confusing prompt-writing with generation.** A finished prompt is not generated audio.
2. **Ignoring GPU/tool prerequisites.** Check before launching heavy model workflows.
3. **Not saving artifacts.** Audio/visual outputs need stable paths or media attachments.
4. **Overwriting provider differences.** Spotify, YouTube, SoundCloud, and local files expose different IDs and metadata.

## Verification Checklist

- [ ] Workflow type selected correctly.
- [ ] Credentials/hardware/tooling checked.
- [ ] Artifact/action verified with output path, playback state, or test result.
- [ ] Limitations and provider-specific caveats reported.
