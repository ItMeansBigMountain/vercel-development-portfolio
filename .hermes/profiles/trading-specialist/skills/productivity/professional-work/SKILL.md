---
name: professional-work
description: "Provides guidance, research, and actionable advice for the user's professional role as a Cloud Engineer at GM Financial. Handles questions about job responsibilities, career development, compensation, market research, internal processes, and skill improvement. Stores context-specific facts about the user's current role, preferred technologies, and goals."
version: 1.0.0
author: Hermes Agent
license: MIT
---

# Professional Work Skill

## Purpose
This skill is invoked whenever the user asks about their job, career growth, market salaries, interview preparation, or any professional‑development topic related to their role as a Cloud Engineer at **GM Financial**.

## Core Functions
1. **Job‑Description Retrieval** – Returns a concise summary of the user’s current responsibilities (cloud platform focus, IaC, CI/CD, security, FinOps, finance‑specific workloads).
2. **Compensation Benchmarking** – Provides up‑to‑date salary ranges for comparable Cloud Engineer roles in Texas, including bonus structures and benefits.
3. **Skill Gap Analysis** – Compares the user’s stated experience/technologies against typical GM Financial job requirements and suggests concrete learning actions (certifications, projects, internal training).
4. **Interview & Promotion Prep** – Generates tailored talking points, STAR stories, and a checklist of artifacts (architecture diagrams, cost‑savings reports, compliance checklists) to bring to performance reviews or internal interview panels.
5. **Internal Process Guidance** – Answers questions about GM Financial specific tools (e.g., internal ticketing, compliance review flow, FinOps reporting) by pulling from the shared knowledge base.
6. **Productivity Framing** – For ambiguous or broad professional goals, default to SMART goals, Feynman/ELI5 simplification, and 80/20 prioritization. For job-search or promotion work, use resume tailoring, STAR story extraction, and salary-negotiation framing.
7. **Persona-Based Coaching** – When useful, answer through a clear role lens such as career strategist, life coach, mental-performance adviser, or personal trainer; keep it practical and avoid generic motivational filler.
8. **Memory Integration** – When the user provides new information (e.g., a certification earned, a new project, a salary target), the skill updates the persistent memory store so future queries remember the latest state.

## Usage Pattern
The skill can be called directly via `skill_view` or automatically by the assistant when the user’s prompt contains any of the following triggers:
- "cloud engineer"
- "GM Financial"
- "salary"
- "promotion"
- "career"
- "job description"
- "interview"
- "performance review"
- "certification"

## Example Interaction
**User:** *What should I emphasize in my next performance review?*  
**Assistant (using professional-work):**
- Summarize the user’s recent achievements (cost‑savings, compliance automation, CI/CD pipelines).
- Provide a bullet list of high‑impact metrics and suggested STAR stories.
- Recommend attaching a one‑page architecture diagram and a FinOps cost‑analysis report.

## Configuration (optional)
- `show_salary_ranges` (boolean): Whether to display detailed compensation tables by default.
- `include_internal_processes` (boolean): Toggle inclusion of GM Financial‑specific workflow details.

## Extensibility
The skill can be patched later to add new sections (e.g., “remote‑work policy”, “internal mentorship programs”).

## Persistence
Key facts stored in the user memory store:
- Current role title and location.
- Preferred cloud platform (AWS/Azure/GCP).
- Certifications owned.
- Target salary/bonus range.
- Ongoing project identifiers (e.g., "Risk Engine Migration").

Whenever the user provides an update, call `memory` with `action":"add"` and `target":"user"` to keep the profile current.
