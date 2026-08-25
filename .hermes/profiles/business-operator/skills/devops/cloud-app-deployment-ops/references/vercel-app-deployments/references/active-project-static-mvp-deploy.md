# Active project static MVP deploy pattern

Use when the user says something like "pick up a project and complete it; deploy it on Vercel" without naming a project, especially in a workspace where the current conversation has an active project that is not yet a web app.

## Pattern

1. Pick the current active/highest-context project instead of asking for a project name, unless there is a dangerous ambiguity.
2. If the project is mostly docs/scripts, convert it into an honest static Vite/React MVP that explains or operationalizes the project rather than pretending all backend automation is done.
3. Add:
   - `package.json` with Vite build scripts
   - `index.html`
   - `src/main.jsx`
   - `src/styles.css`
   - `vercel.json` with `buildCommand: "npm run build"`, `outputDirectory: "dist"`, `framework: "vite"`
   - `.gitignore` excluding `node_modules/`, `dist/`, `.vercel/`, env/log files
4. Run `npm install && npm run build` locally before deploying.
5. Deploy with Vercel token fallback: `TOKEN="${VERCEL_TOKEN:-$VERCEL_API_TOKEN}"; npx vercel --prod --yes --token "$TOKEN"`.
6. Verify the friendly alias/public URL anonymously with `curl -L` and, when possible, browser render. A generated production deployment URL may return `401` while the aliased public URL returns `200`; report the public alias as the usable URL.
7. Update project README with the live URL and project purpose.
8. Commit only source/docs/config, not generated `.vercel`, `dist`, or `node_modules`.

## Example outcome shape

For a docs/scripts project like a faceless YouTube automation workspace, the MVP can be a landing/dashboard showing:

- free trend radar sources,
- content generation pipeline,
- cheap/free cost strategy,
- next build queue.

This creates a real deployable review artifact while preserving honesty about which automation steps are future work.