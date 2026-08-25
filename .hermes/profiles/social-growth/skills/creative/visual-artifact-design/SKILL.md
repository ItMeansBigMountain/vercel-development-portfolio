---
name: visual-artifact-design
description: "Use when creating visual artifacts from Hermes: diagrams, HTML/SVG mockups, Excalidraw sketches, p5.js/pretext demos, ASCII art/video, infographics, design tokens, or browser-based visual prototypes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [creative, diagrams, mockups, html, svg, p5js, excalidraw, ascii, infographics]
    related_skills: []
---

# Visual Artifact Design

## Overview

This umbrella covers creation of visual artifacts: diagrams, mockups, generative sketches, typographic demos, ASCII art/video, infographics, and design-token specs. Select the output medium based on the user's goal and verify visually whenever possible.

## When to Use

- Make architecture/cloud/infra diagrams or hand-drawn Excalidraw diagrams.
- Produce throwaway HTML mockups, visual variants, or browser prototypes.
- Build p5.js generative/interactive sketches or pretext text-layout demos.
- Create ASCII banners, image-to-ASCII, or ASCII video/GIF pipelines.
- Generate infographics or DESIGN.md token specifications.

## Medium Map

### Architecture and Excalidraw Diagrams

Use architecture-diagram style for polished dark SVG/HTML system diagrams. Use Excalidraw style for hand-drawn architecture, flow, and sequence diagrams where editable JSON matters.

### HTML Mockups and Browser Prototypes

Use sketch/HTML approaches for 2-3 design variants, landing pages, decks, and prototypes. Keep artifacts single-file when useful and open them in a browser for visual QA.

### p5.js and Pretext

Use p5.js for generative art, shaders, animation, interaction, WebGL, and exports. Use pretext for DOM-free text layout, kinetic typography, text-as-geometry, and ASCII-like browser demos.

### ASCII Art and ASCII Video

Use ASCII-art tooling for banners, cowsay, boxes, image-to-ASCII, and decorative text. Use ASCII-video workflows for frame extraction, shader/effect composition, optimization, and MP4/GIF outputs.

### Infographics and Design Tokens

Use infographic workflows for structured visual explanation with layout/style galleries. Use DESIGN.md workflows for token specs, validation, and export.

## Standard Workflow

1. Clarify or infer the artifact type and audience.
2. Choose a medium and style system.
3. Generate an actual file, not just a prompt.
4. Render or open the artifact for visual inspection.
5. Iterate on layout, legibility, contrast, and export format.
6. Return the file path/media attachment and concise usage notes.

## Repository README SVGs

For architecture diagrams and plain-language formula graphics embedded in GitHub READMEs:

1. Prefer repository-owned SVGs when editable labels, small diffs, and dependency-free rendering matter.
2. Include `<title>`, `<desc>`, `role="img"`, and useful Markdown alt text. Avoid scripts, tracking, remote fonts, and remote image dependencies.
3. Use a restrained high-contrast palette, system fonts, and a wide README-friendly view box. Keep jokes audience-appropriate and subordinate to the explanation.
4. Render each local SVG directly in the browser and visually inspect clipping, overlap, contrast, alignment, and README-scale legibility.
5. After publishing, inspect the live GitHub README DOM: verify the expected copy, support-link destination, and every README image's `complete`, `naturalWidth`, `naturalHeight`, and final `currentSrc`. Local XML validity alone does not prove GitHub rendered it.
6. Validate SVG XML and all local Markdown image paths deterministically before commit.

## Common Pitfalls

1. **Stopping at a description.** The deliverable is a rendered artifact or source file.
2. **Skipping visual QA.** Browser/SVG/deck/ASCII outputs often look different than expected.
3. **Mixing incompatible output goals.** Editable Excalidraw JSON, polished SVG, and generative canvas sketches serve different needs.
4. **Flattening large creative support packages.** Keep reusable references/templates/scripts organized under the umbrella.

## Verification Checklist

- [ ] Output medium selected for the user's actual goal.
- [ ] Artifact file generated.
- [ ] Visual render/screenshot/export inspected.
- [ ] File path or media attachment returned.
- [ ] Any external dependencies or edit instructions documented.
