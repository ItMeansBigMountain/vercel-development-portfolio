import fs from 'node:fs';
import path from 'node:path';

const projectId = process.env.VERCEL_PROJECT_ID;
const orgId = process.env.VERCEL_ORG_ID;
if (!projectId || !orgId) throw new Error('Missing Vercel project binding');
fs.rmSync('.vercel-deploy', { recursive: true, force: true });
fs.cpSync('dist', '.vercel-deploy', { recursive: true });
fs.mkdirSync(path.join('.vercel-deploy', '.vercel'), { recursive: true });
fs.writeFileSync(path.join('.vercel-deploy', '.vercel', 'project.json'), `${JSON.stringify({ projectId, orgId })}\n`);
const config = {
  cleanUrls: true,
  trailingSlash: false,
  headers: [{
    source: '/(.*)',
    headers: [
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
    ],
  }],
};
fs.writeFileSync(path.join('.vercel-deploy', 'vercel.json'), `${JSON.stringify(config)}\n`);
