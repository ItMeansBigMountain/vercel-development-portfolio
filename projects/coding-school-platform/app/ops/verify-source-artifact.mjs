import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const required = ['GH_REPOSITORY', 'SOURCE_RUN_ID', 'SOURCE_SHA', 'SOURCE_EVENT'];
for (const name of required) if (!process.env[name]) throw new Error(`Missing ${name}`);
const manifest = JSON.parse(fs.readFileSync('release-manifest.json', 'utf8'));
const run = JSON.parse(execFileSync('gh', ['api', `repos/${process.env.GH_REPOSITORY}/actions/runs/${process.env.SOURCE_RUN_ID}`], { encoding: 'utf8' }));
const sameActiveRun = process.env.ALLOW_IN_PROGRESS === 'true' && run.id === Number(process.env.GITHUB_RUN_ID) && run.status === 'in_progress';
if (run.conclusion !== 'success' && !sameActiveRun) throw new Error(`Source run is not successful or the current gated run: ${run.status}/${run.conclusion}`);
if (run.event !== process.env.SOURCE_EVENT) throw new Error(`Unexpected source event ${run.event}`);
if (run.head_sha !== process.env.SOURCE_SHA) throw new Error('Source run SHA mismatch');
if (manifest.source_run_id !== Number(process.env.SOURCE_RUN_ID) || manifest.source_sha !== process.env.SOURCE_SHA) throw new Error('Release manifest source mismatch');
if (process.env.SOURCE_EVENT === 'push' && run.head_branch !== 'coding-school') throw new Error('Production source is not coding-school');
const artifacts = JSON.parse(execFileSync('gh', ['api', `repos/${process.env.GH_REPOSITORY}/actions/runs/${process.env.SOURCE_RUN_ID}/artifacts`], { encoding: 'utf8' })).artifacts;
const artifact = artifacts.find(item => item.name === 'coding-school-web' && !item.expired);
if (!artifact || !artifact.digest?.startsWith('sha256:')) throw new Error('Artifact ID/digest unavailable');
execFileSync('sha256sum', ['--check', 'artifact-files.sha256'], { stdio: 'inherit' });
console.log(JSON.stringify({ run_id: run.id, source_sha: run.head_sha, artifact_id: artifact.id, artifact_digest: artifact.digest }));
