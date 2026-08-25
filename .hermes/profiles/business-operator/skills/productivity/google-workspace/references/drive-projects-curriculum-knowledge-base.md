# Google Drive Projects and curriculum knowledge-base workflow

Use this reference when the user wants a set of Drive files/folders grouped into a **Drive Project** (the Gemini-grounded Projects interface), especially for a curriculum, client, or business knowledge base.

## Durable workflow

1. **Confirm the target account/profile** and verify Drive/Docs/Sheets access.
2. **Build one canonical root folder** with stable, numbered subfolders. Prefer adding the root folder as the Project source so future files placed beneath it remain discoverable without manually selecting every document.
3. **Create a Project Index Doc** in the root folder containing:
   - purpose and canonical folder URL,
   - source-folder map,
   - program/business identity,
   - governance and permission boundaries.
4. **Keep sensitive lanes separate.** Internal answer keys, teacher notes, and customer-delivery folders should have distinct permissions even when the root is used as a Project source.
5. **Rebrand comprehensively** when a working name changes:
   - rename the root folder and file titles,
   - replace branding inside native Docs,
   - update the spreadsheet title/properties,
   - update uploaded visual media bytes as well as metadata,
   - preserve legitimate non-brand uses of the old word (for example an exercise’s required literal string).
6. **Verify by read-back:** root ownership/name, all file names, representative Doc body, Sheet title/range, uploaded media metadata, and a search for stale brand references. Inspect each remaining match before replacing it.
7. **Create the Drive Project through the best currently supported route.** First check current Google documentation/API support. If Projects remains UI-only, use an already authenticated user browser session when available. Never request or type the user’s password. If no authenticated UI session is available, complete the source folder/index and give a minimal handoff: Create project → name it → Add sources → select the canonical root folder.
8. **Verify the finished Project in the Projects UI** by checking its name and listed source folder/files. Do not report the Project itself as created when only the underlying Drive folder was created.

## Current product distinction

A normal Drive folder and a Drive Project are related but not identical. The folder is the durable file hierarchy; the Project is a Gemini-grounded curated workspace that references Drive sources and honors existing Drive permissions. Treat the canonical folder as the source of truth and the Project as the discovery/conversation layer.

## Pitfalls

- Do not confuse Drive Projects with Google Cloud Resource Manager projects.
- Do not claim completion after creating only a folder with “Project” in its name.
- Do not select dozens of files individually when one canonical root folder is a valid source.
- Do not make files public merely to make a Project work; existing Drive permissions should remain authoritative.
- Do not blindly replace every old-brand string. Review exercise literals, quoted source names, and historical references first.
- Product/API support evolves; re-check authoritative Google Workspace documentation rather than preserving a permanent claim that Projects is UI-only.
