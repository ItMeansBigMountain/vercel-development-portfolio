import { readdir, readFile } from 'node:fs/promises';
import { extname, join, relative } from 'node:path';
import { spawnSync } from 'node:child_process';

const root = new URL('..', import.meta.url).pathname;
const ignored = new Set(['node_modules', 'dist', '.expo', 'combatAtlas_Backend', 'imports', 'mobile']);
const sourceExtensions = new Set(['.js', '.mjs']);
const jsonExtensions = new Set(['.json']);
const failures = [];
let checked = 0;

async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (ignored.has(entry.name)) continue;
    const path = join(directory, entry.name);
    if (entry.isDirectory()) {
      await walk(path);
      continue;
    }

    const extension = extname(entry.name);
    if (jsonExtensions.has(extension)) {
      checked += 1;
      try {
        JSON.parse(await readFile(path, 'utf8'));
      } catch (error) {
        failures.push(`${relative(root, path)}: invalid JSON (${error.message})`);
      }
    } else if (sourceExtensions.has(extension)) {
      checked += 1;
      const result = spawnSync(process.execPath, ['--check', path], { encoding: 'utf8' });
      if (result.status !== 0) failures.push(`${relative(root, path)}: ${result.stderr.trim()}`);
    }
  }
}

await walk(root);
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`Syntax/JSON lint passed for ${checked} files.`);
