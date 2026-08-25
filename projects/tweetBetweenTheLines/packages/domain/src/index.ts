export * from './safetyPolicy.js'
export * from './accountData.js'
export * from './connectors.js'
export * from './explainableMetrics.js'
export * from './personalityWellbeing.js'
export * from './operations.js'
export * from './archiveEngine.js'
export * from './archiveOnboarding.js'
export * from './privateReflection.js'

export type PersonalEventKind = 'post' | 'message' | 'reaction' | 'view' | 'listen' | 'search' | 'import-note'

export type PersonalEventInput = {
  occurredAt: string
  source: string
  sourceRecordId: string
  kind: PersonalEventKind
  text: string
  metadata?: Record<string, string | number | boolean | null>
}

export type EventProvenance = {
  source: string
  sourceRecordId: string
  deletionLineage: string
}

export type PersonalEvent = {
  id: string
  occurredAt: string
  kind: PersonalEventKind
  text: string
  metadata: Record<string, string | number | boolean | null>
  provenance: EventProvenance
  features: {
    words: string[]
    keywords: string[]
    wordCount: number
    signalCounts: Record<SignalKind, number>
  }
}

export type SignalKind = 'interest' | 'positive' | 'strain' | 'connection'

export type ProfileCardKind = 'attention' | 'language' | 'wellbeing-pattern' | 'provenance'

export type ProfileEvidence = {
  source: string
  sourceRecordId: string
  occurredAt: string
  excerpt: string
}

export type ProfileCard = {
  kind: ProfileCardKind
  title: string
  summary: string
  confidence: 'low' | 'medium' | 'high'
  evidence: ProfileEvidence[]
}

export type ProfileSnapshot = {
  mission: 'Free the minds of the consumer with data'
  generatedAt: string
  eventsAnalyzed: number
  revokedSources: string[]
  safetyBoundary: string
  cards: ProfileCard[]
}

type SnapshotOptions = {
  revokedSources?: string[]
  generatedAt?: string
}

const stopWords = new Set([
  'a',
  'an',
  'am',
  'and',
  'are',
  'as',
  'at',
  'be',
  'but',
  'by',
  'for',
  'from',
  'i',
  'in',
  'is',
  'it',
  'me',
  'my',
  'of',
  'on',
  'or',
  'the',
  'to',
  'we',
  'with',
])

const signalLexicon: Record<SignalKind, string[]> = {
  interest: ['music', 'fitness', 'school', 'work', 'creator', 'creators', 'production', 'data'],
  positive: ['grateful', 'hopeful', 'clear', 'helped', 'excited', 'proud', 'calm'],
  strain: ['overwhelmed', 'deadline', 'deadlines', 'stress', 'worried', 'tired', 'angry', 'sad'],
  connection: ['family', 'friends', 'friend', 'community', 'partner', 'team'],
}

function wordsFrom(text: string): string[] {
  return text.toLowerCase().match(/[a-z0-9']+/g) ?? []
}

function keywordList(words: string[]): string[] {
  const seen = new Set<string>()
  return words.filter((word) => {
    if (stopWords.has(word) || seen.has(word)) {
      return false
    }
    seen.add(word)
    return true
  })
}

function countSignal(words: string[], signal: SignalKind): number {
  const lexicon = new Set(signalLexicon[signal])
  return words.filter((word) => lexicon.has(word)).length
}

function excerpt(text: string): string {
  const trimmed = text.trim().replace(/\s+/g, ' ')
  return trimmed.length <= 140 ? trimmed : `${trimmed.slice(0, 137)}...`
}

export function normalizePersonalEvent(input: PersonalEventInput): PersonalEvent {
  const source = input.source.trim()
  const sourceRecordId = input.sourceRecordId.trim()
  const words = wordsFrom(input.text)
  const keywords = keywordList(words)
  const signalCounts = Object.keys(signalLexicon).reduce(
    (counts, signal) => ({ ...counts, [signal]: countSignal(words, signal as SignalKind) }),
    {} as Record<SignalKind, number>,
  )

  return {
    id: `${source}:${sourceRecordId}`,
    occurredAt: new Date(input.occurredAt).toISOString(),
    kind: input.kind,
    text: input.text.trim(),
    metadata: input.metadata ?? {},
    provenance: {
      source,
      sourceRecordId,
      deletionLineage: `${source}:${sourceRecordId}`,
    },
    features: {
      words,
      keywords,
      wordCount: words.filter((word) => word !== 'i').length,
      signalCounts,
    },
  }
}

function evidenceFor(events: PersonalEvent[], predicate: (event: PersonalEvent) => boolean): ProfileEvidence[] {
  return events.filter(predicate).slice(0, 3).map((event) => ({
    source: event.provenance.source,
    sourceRecordId: event.provenance.sourceRecordId,
    occurredAt: event.occurredAt,
    excerpt: excerpt(event.text),
  }))
}

function confidenceFor(evidence: ProfileEvidence[]): ProfileCard['confidence'] {
  if (evidence.length >= 3) return 'high'
  if (evidence.length === 2) return 'medium'
  return 'low'
}

function topKeywords(events: PersonalEvent[]): string[] {
  const counts = new Map<string, number>()
  for (const event of events) {
    for (const keyword of event.features.keywords) {
      counts.set(keyword, (counts.get(keyword) ?? 0) + 1)
    }
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, 5)
    .map(([keyword]) => keyword)
}

export function buildProfileSnapshot(inputs: PersonalEventInput[], options: SnapshotOptions = {}): ProfileSnapshot {
  const revokedSources = [...new Set(options.revokedSources ?? [])].sort()
  const activeEvents = inputs
    .map(normalizePersonalEvent)
    .filter((event) => !revokedSources.includes(event.provenance.source))
    .sort((a, b) => a.occurredAt.localeCompare(b.occurredAt))

  const interestEvidence = evidenceFor(activeEvents, (event) => event.features.signalCounts.interest > 0)
  const strainEvidence = evidenceFor(activeEvents, (event) => event.features.signalCounts.strain > 0)
  const positiveEvidence = evidenceFor(activeEvents, (event) => event.features.signalCounts.positive > 0)
  const provenanceEvidence = evidenceFor(activeEvents, () => true)
  const keywords = topKeywords(activeEvents)

  const cards: ProfileCard[] = [
    {
      kind: 'attention',
      title: keywords.length > 0 ? `Attention clusters: ${keywords.join(', ')}` : 'Attention clusters need more data',
      summary: keywords.length > 0
        ? `Your imported events most often point toward ${keywords.slice(0, 3).join(', ')}.`
        : 'Import more events to identify repeated topics without guessing.',
      confidence: confidenceFor(interestEvidence),
      evidence: interestEvidence.length > 0 ? interestEvidence : provenanceEvidence,
    },
    {
      kind: 'language',
      title: 'Language balance',
      summary: positiveEvidence.length >= strainEvidence.length
        ? 'Positive or constructive language appears at least as often as strain language in this slice.'
        : 'Strain language appears more often than positive language in this slice.',
      confidence: confidenceFor([...positiveEvidence, ...strainEvidence]),
      evidence: [...positiveEvidence, ...strainEvidence].slice(0, 3),
    },
    {
      kind: 'wellbeing-pattern',
      title: 'Non-diagnostic wellbeing pattern',
      summary: strainEvidence.length > 0
        ? 'Some imported language contains stress or depletion signals; treat this as a reflection prompt, not a medical conclusion.'
        : 'This slice does not show strong stress-language evidence; absence of evidence is not proof of wellbeing.',
      confidence: confidenceFor(strainEvidence),
      evidence: strainEvidence,
    },
    {
      kind: 'provenance',
      title: 'Source-backed profile',
      summary: `This snapshot used ${activeEvents.length} event${activeEvents.length === 1 ? '' : 's'} after source revocation filters.`,
      confidence: confidenceFor(provenanceEvidence),
      evidence: provenanceEvidence,
    },
  ]

  return {
    mission: 'Free the minds of the consumer with data',
    generatedAt: options.generatedAt ?? new Date(0).toISOString(),
    eventsAnalyzed: activeEvents.length,
    revokedSources,
    safetyBoundary:
      'This profile is not a diagnosis and must keep validated self-report screening separate from observational social-media signals.',
    cards,
  }
}
