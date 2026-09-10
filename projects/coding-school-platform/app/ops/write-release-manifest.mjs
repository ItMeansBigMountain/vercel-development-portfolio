import fs from 'node:fs';

const required = ['BUILD_SHA', 'SOURCE_SHA', 'SOURCE_EVENT', 'SOURCE_REF', 'SOURCE_RUN_ID'];
for (const name of required) {
  if (!process.env[name]) throw new Error(`Missing ${name}`);
}
const manifest = {
  schema_version: 1,
  app: 'coding-school-platform',
  build_sha: process.env.BUILD_SHA,
  source_sha: process.env.SOURCE_SHA,
  source_event: process.env.SOURCE_EVENT,
  source_ref: process.env.SOURCE_REF,
  source_run_id: Number(process.env.SOURCE_RUN_ID),
  files_manifest: 'artifact-files.sha256',
};
fs.writeFileSync('release-manifest.json', `${JSON.stringify(manifest, null, 2)}\n`);
