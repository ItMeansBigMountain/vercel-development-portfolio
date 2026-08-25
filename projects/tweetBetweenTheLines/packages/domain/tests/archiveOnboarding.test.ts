import assert from 'node:assert/strict'
import test from 'node:test'

import { ARCHIVE_INSTRUCTION_VERSION, ARCHIVE_ONBOARDING_PLATFORMS, validateOnboardingArchive } from '../src/archiveOnboarding.js'

test('onboarding instructions remain versioned and official', () => {
  assert.equal(ARCHIVE_INSTRUCTION_VERSION, 'tweetbetweenthelines-archive-registry@1')
  assert.equal(ARCHIVE_ONBOARDING_PLATFORMS.length, 6)
  for (const platform of ARCHIVE_ONBOARDING_PLATFORMS) {
    assert.match(platform.officialUrl, /^https:\/\//)
    assert.ok(platform.requestSteps.length >= 4)
    assert.ok(platform.expected.length > 0)
    assert.ok(platform.categories.length > 0)
  }
})

test('archive selection fails closed and reports filename confidence', () => {
  assert.deepEqual(validateOnboardingArchive('', { name: 'archive.zip', size: 5 }), { ok: false, error: 'Choose a supported platform first.' })
  assert.equal(validateOnboardingArchive('spotify', { name: 'data.json', size: 5 }).ok, false)
  assert.equal(validateOnboardingArchive('spotify', { name: 'spotify-data.zip', size: 250_000_001 }).ok, false)
  const high = validateOnboardingArchive('spotify', { name: 'spotify-mydata.zip', size: 5 })
  assert.equal(high.ok && high.confidence, 'high')
  const medium = validateOnboardingArchive('spotify', { name: 'download.zip', size: 5 })
  assert.equal(medium.ok && medium.confidence, 'medium')
})
