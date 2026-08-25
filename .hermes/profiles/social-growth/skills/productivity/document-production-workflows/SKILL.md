---
name: document-production-workflows
description: "Use when extracting, editing, creating, or QAing documents from Hermes: PDFs, OCR/scanned documents, PowerPoint decks, research papers, and document-to-artifact conversions."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [documents, pdf, ocr, powerpoint, papers, productivity]
    related_skills: []
---

# Document Production Workflows

## Overview

This umbrella covers document extraction, editing, deck creation, and long-form paper production. Pick the path by artifact type: PDF/scanned docs, PowerPoint decks, or research manuscripts.

## When to Use

- Extract text from PDFs, scans, or remote documents.
- Edit PDF text, typo, or title metadata with a natural-language PDF editor.
- Create/read/edit/QA `.pptx` decks.
- Draft and manage ML/research paper writing workflows.

## Capability Map

### OCR and Document Extraction

- Prefer direct web/PDF extraction when a URL is available.
- Use lightweight PyMuPDF for digital PDFs.
- Use marker/OCR paths for scans or layout-heavy documents.
- Save extracted text and report limitations for tables, math, and image-only regions.

### PDF Editing

Use nano-pdf-style natural-language edits for small PDF text/metadata changes. Verify by extracting or rendering the changed page after editing.

### PowerPoint Decks

For `.pptx`, support reading content, editing slides/notes, creating decks from scratch, applying templates, and rendering thumbnails/images for QA. Always inspect rendered output, not just XML or generation logs.

### Research Paper Writing

For ML conference papers, manage project setup, literature review, experiment design, result analysis, writing, citations, checklists, and submission formatting. Preserve templates and conference style files.

## Standard Workflow

1. Identify input artifact type and desired output.
2. Choose extractor/editor/generator path.
3. Preserve originals; write outputs to explicit paths.
4. Verify by read-back, extraction, render, or compile.
5. Report produced files and any fidelity caveats.

## Common Pitfalls

1. **Assuming PDF text extraction means OCR succeeded.** Check for empty/garbled output.
2. **Editing decks without rendering.** Visual regressions are common in `.pptx` workflows.
3. **Overwriting source documents.** Work on copies unless explicitly asked.
4. **Ignoring style/template files.** Paper and slide artifacts often depend on support files.

## Verification Checklist

- [ ] Source artifact and intended output path confirmed.
- [ ] Original preserved or overwrite explicitly requested.
- [ ] Output verified by extraction/render/compile.
- [ ] Produced paths and fidelity limitations reported.
