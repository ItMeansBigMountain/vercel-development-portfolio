import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const registryPath = new URL("../archive_schema_registry.json", import.meta.url);
const fixturesPath = new URL(
  "../fixtures/archive-synthetic/social_archive_synthetic_fixtures.json",
  import.meta.url,
);

const [registry, fixtureDocument] = await Promise.all(
  [registryPath, fixturesPath].map(async (path) =>
    JSON.parse(await readFile(path, "utf8")),
  ),
);

assert.equal(
  registry.schema_version,
  "tweetbetweenthelines-archive-registry@1",
  "unexpected archive registry version",
);
assert.equal(
  fixtureDocument.fixture_version,
  "archive-synthetic-fixtures@1",
  "unexpected synthetic fixture version",
);
assert.match(
  fixtureDocument.notice,
  /synthetic fixture data only/i,
  "fixture notice must identify synthetic-only data",
);
assert.ok(Array.isArray(registry.normalized_categories));
assert.ok(Array.isArray(registry.platforms) && registry.platforms.length > 0);
assert.ok(Array.isArray(fixtureDocument.fixtures) && fixtureDocument.fixtures.length > 0);

const registryParsers = new Map(
  registry.platforms.map((entry) => [entry.parser_version, entry]),
);
const categories = new Set(registry.normalized_categories);
const seen = new Set();

for (const fixture of fixtureDocument.fixtures) {
  assert.equal(typeof fixture.platform, "string");
  assert.equal(typeof fixture.parser_version, "string");
  assert.ok(!seen.has(fixture.platform), `duplicate fixture: ${fixture.platform}`);
  seen.add(fixture.platform);

  const registryEntry = registryParsers.get(fixture.parser_version);
  assert.ok(
    registryEntry,
    `fixture parser missing from registry: ${fixture.parser_version}`,
  );

  const expected = fixture.expected_manifest;
  assert.equal(expected.schema_version, "archive-manifest@1");
  assert.equal(expected.platform, fixture.platform);
  assert.equal(expected.parser_version, fixture.parser_version);

  for (const category of expected.accepted_categories) {
    assert.ok(categories.has(category), `unknown category: ${category}`);
  }
  for (const record of fixture.normalized_records) {
    assert.ok(categories.has(record.category), `unknown record category: ${record.category}`);
    assert.equal(record.kind, "archive-import");
    assert.equal(typeof record.sourceRecordId, "string");
    assert.ok(record.sourceRecordId.length > 0);
  }
}

console.log(
  `Validated ${fixtureDocument.fixtures.length} synthetic fixtures against ${registry.schema_version}.`,
);
