import fs from 'node:fs';

const required = ['VERCEL_TOKEN', 'VERCEL_ORG_ID', 'VERCEL_PROJECT_ID', 'IMMUTABLE_URL', 'SOURCE_SHA', 'SOURCE_RUN_ID', 'WORKFLOW_RUN_URL'];
for (const name of required) if (!process.env[name]) throw new Error(`Missing ${name}`);
const hostname = new URL(process.env.IMMUTABLE_URL).hostname;
const response = await fetch(`https://api.vercel.com/v13/deployments/${encodeURIComponent(hostname)}?teamId=${encodeURIComponent(process.env.VERCEL_ORG_ID)}`, { headers: { Authorization: `Bearer ${process.env.VERCEL_TOKEN}` } });
if (!response.ok) throw new Error(`Vercel deployment lookup failed: ${response.status}`);
const deployment = await response.json();
if (deployment.projectId !== process.env.VERCEL_PROJECT_ID || deployment.name !== 'coding-school-platform' || deployment.readyState !== 'READY') throw new Error('Vercel deployment identity mismatch');
const metadata = {
  app: 'coding-school-platform',
  immutable_url: process.env.IMMUTABLE_URL,
  commit_sha: process.env.SOURCE_SHA,
  source_run_id: Number(process.env.SOURCE_RUN_ID),
  workflow_run_url: process.env.WORKFLOW_RUN_URL,
  vercel_deployment_id: deployment.id,
  vercel_project_id: deployment.projectId,
  vercel_project_name: deployment.name,
  ready_state: deployment.readyState,
};
fs.writeFileSync('deployment-metadata.json', `${JSON.stringify(metadata, null, 2)}\n`);
console.log(JSON.stringify(metadata));
