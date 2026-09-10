#!/usr/bin/env node
/**
 * Build-time provenance assertion: ensures personal email, Drive/Docs URLs,
 * and token-path metadata are NOT present in the public web bundle.
 * 
 * This addresses CS-08: the curriculum manifest contains operational provenance
 * that should not leak into public artifacts.
 */

const fs = require('fs');
const path = require('path');

const distDir = path.resolve(__dirname, '..', 'dist');

// Strings that MUST NOT appear in public bundles
const FORBIDDEN_STRINGS = [
  'affan.fareed@gmail.com',
  'drive.google.com/drive/folders',
  'docs.google.com/document',
  '1pI-haF9EhHcHU__8zIRn1OPf4aH374TP', // pragma: allowlist secret
  '1xb-cnvu2I_LR8YotTEzHrDZDDVINwJr9EvbjoS7Ti0Y', // pragma: allowlist secret
  '1RnlWxt0SUfy92-PbiCO0YfQy233YZ7GJS9vfC6FNTVA', // pragma: allowlist secret
  '1Jar1_DWBR50Sdfnl3mu_LH7UoEN-Wg86lIhcgxD1G0M', // pragma: allowlist secret
  '1QgBkr-DD89e6UW1oRy9w89wt_6N_frJFV1_XuDOsJmw', // pragma: allowlist secret
  'HERMES_HOME',
  'syncVerification',
  'syncVerifiedAt',
  'readbackNeedles',
  'CANONICAL MODULE MAP SYNC',
  'drive-sync-note',
];

function scanDirectory(dir) {
  const results = [];
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...scanDirectory(fullPath));
    } else if (entry.isFile()) {
      const ext = path.extname(entry.name).toLowerCase();
      // Only scan text-based files that could contain provenance
      if (['.html', '.js', '.json', '.css', '.txt', '.map', '.ico'].includes(ext)) {
        try {
          const content = fs.readFileSync(fullPath, 'utf8');
          for (const forbidden of FORBIDDEN_STRINGS) {
            if (content.includes(forbidden)) {
              results.push({
                file: path.relative(distDir, fullPath),
                forbiddenString: forbidden,
              });
            }
          }
        } catch (e) {
          // Binary file or read error - skip
        }
      }
    }
  }
  
  return results;
}

console.log('Running build-time provenance assertion...');
console.log(`Scanning: ${distDir}`);

if (!fs.existsSync(distDir)) {
  console.error('ERROR: dist directory not found. Run build first.');
  process.exit(1);
}

const violations = scanDirectory(distDir);

if (violations.length > 0) {
  console.error('\n❌ PROVENANCE ASSERTION FAILED:');
  console.error('The following forbidden strings were found in the public bundle:');
  for (const v of violations) {
    console.error(`  - ${v.file}: contains "${v.forbiddenString}"`);
  }
  console.error('\nRemediation: remove these strings from source or ensure they are stripped at build time.');
  process.exit(1);
} else {
  console.log('\n✅ Provenance assertion passed: no forbidden strings found in public bundle.');
  console.log(`Scanned ${FORBIDDEN_STRINGS.length} forbidden patterns across all text files in dist/.`);
  process.exit(0);
}