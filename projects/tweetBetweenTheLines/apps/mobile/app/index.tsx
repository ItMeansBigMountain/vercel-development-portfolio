import { useMemo, useState } from 'react'
import { Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native'

import type { EvidenceRef, ExplainableMetricCard } from '../../../packages/domain/src/explainableMetrics'
import { buildPrivateReflection, type PrivateReflection } from '../../../packages/domain/src/privateReflection'
import { ArchiveWizard } from '../components/ArchiveWizard'
import { createPrivacyClient, validateArchiveSelection } from '../lib/privacyClient'
import { analyzeDataset, importTemplate, parseDatasetJson, syntheticDataset, type MvpDataset } from '../lib/mvpData'

type Section = 'account' | 'data' | 'metrics' | 'reflection' | 'control' | 'limits'
type Correction = { metricId: string; note: string }

function Button({ label, onPress, danger = false, disabled = false }: { label: string; onPress: () => void; danger?: boolean; disabled?: boolean }) {
  return <Pressable accessibilityRole="button" accessibilityState={{ disabled }} disabled={disabled} onPress={onPress} style={({ pressed }) => [styles.button, danger && styles.danger, disabled && styles.disabled, pressed && styles.pressed]}><Text style={styles.buttonText}>{label}</Text></Pressable>
}

function downloadJson(fileName: string, value: unknown) {
  if (Platform.OS !== 'web' || typeof document === 'undefined') return false
  const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2)], { type: 'application/json' }))
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = fileName
  anchor.style.display = 'none'
  document.body.appendChild(anchor)
  anchor.click()
  anchor.remove()
  window.setTimeout(() => URL.revokeObjectURL(url), 1_000)
  return true
}

function aggregateSummary(card: ExplainableMetricCard): string {
  const ranked = card.aggregates.ranked
  if (Array.isArray(ranked)) return ranked.slice(0, 5).map((row) => `${String((row as { label?: unknown }).label)} (${String((row as { count?: unknown }).count)})`).join(' · ') || 'No matching evidence'
  if (card.category === 'sentiment') return `positive ${card.aggregates.positive} · neutral ${card.aggregates.neutral} · negative ${card.aggregates.negative}`
  if (card.category === 'language-style') return `${card.aggregates.tokenCount} words · ${card.aggregates.uniqueTokens} unique · locales ${JSON.stringify(card.aggregates.localeCounts)}`
  if (card.category === 'attention-rhythm') return 'Event counts grouped by UTC hour and weekday; inspect derivation for the exact arrays.'
  return JSON.stringify(card.aggregates)
}

export default function HomeScreen() {
  const client = useMemo(createPrivacyClient, [])
  const [section, setSection] = useState<Section>('account')
  const [consented, setConsented] = useState(false)
  const [dataset, setDataset] = useState<MvpDataset | null>(null)
  const [snapshot, setSnapshot] = useState<ReturnType<typeof analyzeDataset> | null>(null)
  const [selected, setSelected] = useState<ExplainableMetricCard | null>(null)
  const [corrections, setCorrections] = useState<Correction[]>([])
  const [reflection, setReflection] = useState<PrivateReflection | null>(null)
  const [notice, setNotice] = useState('No data loaded. Start with the synthetic demo or explicitly consent to your own JSON export.')

  const load = (next: MvpDataset) => {
    const analyzed = analyzeDataset(next)
    setDataset(next); setSnapshot(analyzed); setSelected(null); setCorrections([]); setReflection(null); setSection('metrics')
    setNotice(`${next.events.length} events analyzed locally from ${next.label}.`)
  }

  const chooseJson = async () => {
    if (!consented) return setNotice('Check explicit consent before importing personal data.')
    const file = await client.chooseArchive()
    if (!file) return
    const selectionError = validateArchiveSelection(file)
    if (selectionError) return setNotice(selectionError)
    if (!file.name.toLowerCase().endsWith('.json')) return setNotice('This runnable web MVP accepts normalized JSON only. ZIP provider adapters remain a production integration gate.')
    try {
      const response = await fetch(file.uri)
      load(parseDatasetJson(await response.text()))
    } catch (error) {
      setNotice(`Import rejected: ${error instanceof Error ? error.message : 'invalid JSON'}`)
    }
  }

  const downloadTemplate = () => {
    const ok = downloadJson('tweet-between-the-lines-import-template.json', importTemplate)
    setNotice(ok ? 'Import template downloaded. Replace the example record with data you control, then import the JSON below.' : 'Template download is available in the web app.')
  }

  const correct = (metricId: string) => {
    setCorrections((items) => items.some((item) => item.metricId === metricId) ? items.filter((item) => item.metricId !== metricId) : [...items, { metricId, note: 'User marked this derived metric as inaccurate or unrepresentative.' }])
    setNotice('Correction saved separately from source evidence and included in export. It does not rewrite the original archive.')
  }

  const exportData = () => {
    if (!dataset || !snapshot) return setNotice('Load data before exporting.')
    const ok = downloadJson('tweet-between-the-lines-export.json', { schemaVersion: 1, exportedAt: new Date().toISOString(), dataset, metrics: snapshot, corrections, privateReflection: reflection, limitations: 'Deterministic reflections from only the imported data; not diagnosis or complete platform coverage.' })
    setNotice(ok ? 'Export downloaded as JSON.' : 'Export is available in the web MVP; native sharing is not wired in this milestone.')
  }

  const deleteData = () => {
    if (Platform.OS === 'web' && typeof window !== 'undefined' && !window.confirm('Delete this browser session’s imported data, metrics, and corrections?')) return
    setDataset(null); setSnapshot(null); setSelected(null); setCorrections([]); setReflection(null); setConsented(false); setSection('data')
    setNotice('Browser-session data deleted. This local MVP did not upload or persist it.')
  }

  return <View style={styles.root}><ScrollView contentContainerStyle={styles.page}>
    <Text style={styles.eyebrow}>tweetBetweenTheLines · runnable web MVP</Text>
    <Text accessibilityRole="header" style={styles.title}>See what your data can say — and exactly why.</Text>
    <Text style={styles.body}>Analyze a synthetic fixture or your explicitly consented normalized JSON locally. Every metric keeps source records, deterministic derivation, confidence, and limitations visible.</Text>
    <View accessibilityLiveRegion="polite" style={styles.notice}><Text style={styles.noticeText}>{notice}</Text></View>

    <View accessibilityRole="tablist" style={styles.tabs}>{(['account', 'data', 'metrics', 'reflection', 'control', 'limits'] as Section[]).map((item) => <Pressable key={item} accessibilityRole="tab" accessibilityState={{ selected: section === item }} onPress={() => setSection(item)} style={[styles.tab, section === item && styles.activeTab]}><Text style={styles.tabText}>{item}</Text></Pressable>)}</View>

    {section === 'account' && <>
      <View style={styles.panel}><Text style={styles.panelTitle}>Sign in to your BetweenLines account</Text><Text style={styles.body}>Google and Apple sign-in create the first-party app account. They do not connect social history or grant analysis access.</Text><Button label="Google sign-in · unavailable until configured" onPress={() => setNotice('Google sign-in is not configured in this testing build. No provider access was requested.')} /><Button label="Apple sign-in · unavailable until configured" onPress={() => setNotice('Apple sign-in is not configured in this testing build. No provider access was requested.')} /></View>
      <View style={styles.panel}><Text style={styles.panelTitle}>Linked social accounts are separate</Text><Text style={styles.body}>After sign-in, each supported platform has its own least-privilege consent screen, PKCE authorization, consent receipt, and unlink/revocation control.</Text><Text style={styles.meta}>Reddit and Discord: unavailable until app credentials are configured · Google/YouTube and Spotify: pending provider review · Instagram, Facebook, TikTok, LinkedIn, and Snapchat: official archive import only · Threads: unavailable.</Text></View>
    </>}

    {section === 'data' && <>
      <ArchiveWizard onNotice={setNotice} />
      <View style={styles.panel}><Text style={styles.panelTitle}>Try without personal data</Text><Text style={styles.body}>The bundled demo is clearly labeled synthetic. Its X, YouTube, and Reddit-style records are examples, not claims that accounts or live APIs are connected.</Text><Button label="Use synthetic demo" onPress={() => load(syntheticDataset)} /></View>
      <View style={styles.panel}><Text style={styles.panelTitle}>Advanced: import normalized JSON</Text><Text style={styles.body}>Use this developer lane only if you already have normalized events. Each event needs id, sourceId, sourceRecordId, occurredAt, kind, and content.</Text><Button label="Download JSON template" onPress={downloadTemplate} /><Text style={styles.body}>Analysis happens in this browser session; no upload occurs.</Text><Pressable accessibilityRole="checkbox" accessibilityState={{ checked: consented }} onPress={() => setConsented((value) => !value)} style={styles.checkRow}><View style={[styles.checkbox, consented && styles.checked]} /><Text style={styles.checkText}>I own or have explicit permission to analyze this file and choose local deterministic analysis.</Text></Pressable><Button label="Choose consented JSON" onPress={() => void chooseJson()} disabled={!consented} /></View>
      <View style={styles.panel}><Text style={styles.panelTitle}>Loaded data</Text><Text style={styles.body}>{dataset ? `${dataset.label}: ${dataset.events.length} records from ${new Set(dataset.events.map((event) => event.sourceId)).size} labeled source(s).` : 'None.'}</Text></View>
    </>}

    {section === 'metrics' && <>{!snapshot ? <View style={styles.panel}><Text style={styles.panelTitle}>No metrics yet</Text><Text style={styles.body}>Load the synthetic demo or a consented JSON file first.</Text><Button label="Go to data" onPress={() => setSection('data')} /></View> : <>
      <View style={styles.warning}><Text style={styles.warningTitle}>Not a diagnosis or complete profile</Text><Text style={styles.body}>{snapshot.eventCount} imported events only. Missing sources and uneven time windows can materially change results.</Text></View>
      {snapshot.cards.map((card) => <View key={card.id} style={styles.card}><View style={styles.row}><Text style={styles.cardTitle}>{card.title}</Text><Text style={styles.badge}>{card.confidence.level} · {Math.round(card.confidence.score * 100)}%</Text></View><Text style={styles.body}>{aggregateSummary(card)}</Text><Text style={styles.meta}>{card.evidence.length} evidence rows · {card.sourceCoverage.length} imported source labels</Text><View style={styles.actions}><Button label="Inspect derivation" onPress={() => setSelected(card)} /><Button label={corrections.some((item) => item.metricId === card.id) ? 'Remove correction' : 'Mark inaccurate'} onPress={() => correct(card.id)} /></View>{corrections.some((item) => item.metricId === card.id) && <Text style={styles.corrected}>User correction attached: inaccurate or unrepresentative.</Text>}</View>)}
      {selected && <View style={styles.panel}><Text style={styles.panelTitle}>How “{selected.title}” was derived</Text><Text style={styles.body}>Method: deterministic schema v{selected.analyzer.schemaVersion}. No generative model or diagnosis. Aggregate: {aggregateSummary(selected)}</Text>{selected.confidence.reasons.map((reason) => <Text key={reason} style={styles.meta}>• {reason}</Text>)}<Text style={styles.subhead}>Limitations</Text>{selected.limitations.map((item) => <Text key={item} style={styles.meta}>• {item}</Text>)}<Text style={styles.subhead}>Source coverage</Text>{selected.sourceCoverage.map((source) => <Text key={source.sourceId} style={styles.meta}>• {source.sourceId}: {source.events} events, {source.firstEventAt.slice(0, 10)} to {source.lastEventAt.slice(0, 10)}</Text>)}<Text style={styles.subhead}>Evidence</Text>{selected.evidence.map((item: EvidenceRef) => <View key={item.eventId} style={styles.evidence}><Text style={styles.meta}>{item.sourceId} / {item.sourceRecordId} · {item.occurredAt}</Text><Text style={styles.body}>{item.excerpt}</Text><Text style={styles.meta}>Matched: {item.matched.join(', ')}</Text></View>)}<Button label="Close derivation" onPress={() => setSelected(null)} /></View>}
    </>}</>}

    {section === 'reflection' && <>{!dataset ? <View style={styles.panel}><Text style={styles.panelTitle}>Private reflection needs selected data</Text><Text style={styles.body}>Load the synthetic demo or your explicitly consented JSON first. Nothing is inferred automatically.</Text><Button label="Go to data" onPress={() => setSection('data')} /></View> : !reflection ? <View style={styles.panel}><Text style={styles.panelTitle}>Create a private reflection period</Text><Text style={styles.body}>You initiate this lane. It uses only the currently selected records, stays private, and compares descriptive language counts across the first and second half of the period.</Text><Text style={styles.meta}>No automatic breakup inference · no relationship judgment · no diagnosis · public sharing unavailable</Text><Button label="Create private reflection from selected data" onPress={() => {
      const times = dataset.events.map((event) => new Date(event.occurredAt).getTime())
      setReflection(buildPrivateReflection({
        id: `private-reflection-${Date.now()}`, title: 'My private reflection period', purpose: 'breakup-recovery', visibility: 'private', consented: true,
        startAt: new Date(Math.min(...times)).toISOString(), endAt: new Date(Math.max(...times)).toISOString(), selectedEventIds: dataset.events.map((event) => event.id), notes: [],
        events: dataset.events.map((event) => ({ id: event.id, sourceId: event.sourceId, sourceRecordId: event.sourceRecordId, occurredAt: event.occurredAt, text: event.content })),
      }))
      setNotice('Private reflection created from the records you selected. Nothing was shared or uploaded.')
    }} /></View> : <><View style={styles.warning}><Text style={styles.warningTitle}>{reflection.title} · private only</Text><Text style={styles.body}>{reflection.boundary}</Text></View><View style={styles.panel}><Text style={styles.panelTitle}>Descriptive progress view</Text><Text style={styles.body}>{reflection.summary}</Text><Text style={styles.meta}>Earlier: {reflection.progress.earlier.events} events · {reflection.progress.earlier.strainLanguageEvents} strain-language · {reflection.progress.earlier.supportiveLanguageEvents} supportive-language</Text><Text style={styles.meta}>Later: {reflection.progress.later.events} events · {reflection.progress.later.strainLanguageEvents} strain-language · {reflection.progress.later.supportiveLanguageEvents} supportive-language</Text><Text style={styles.subhead}>Reflection prompts</Text>{reflection.prompts.map((prompt) => <Text key={prompt} style={styles.meta}>• {prompt}</Text>)}<Text style={styles.subhead}>Selected evidence</Text>{reflection.evidence.map((event) => <View key={event.eventId} style={styles.evidence}><Text style={styles.meta}>{event.sourceId} / {event.sourceRecordId} · {event.occurredAt}</Text><Text style={styles.body}>{event.text}</Text></View>)}<Text style={styles.subhead}>Limitations</Text>{reflection.limitations.map((item) => <Text key={item} style={styles.meta}>• {item}</Text>)}</View><Button label="Delete private reflection" danger onPress={() => { setReflection(null); setNotice('Private reflection deleted from this browser session. Source records were not changed.') }} /></>}</>}

    {section === 'control' && <><View style={styles.panel}><Text style={styles.panelTitle}>Your controls</Text><Text style={styles.body}>Corrections remain distinguishable from source evidence. Export includes the imported records, metrics, derivation evidence, limitations, and corrections.</Text><Text style={styles.meta}>{corrections.length} correction(s) · {dataset?.events.length ?? 0} loaded event(s)</Text></View><Button label="Download complete JSON export" onPress={exportData} disabled={!dataset} /><Button label="Delete browser-session data" danger onPress={deleteData} disabled={!dataset} /></>}

    {section === 'limits' && <><View style={styles.warning}><Text style={styles.warningTitle}>What this milestone is</Text><Text style={styles.body}>A runnable web/mobile onboarding flow with versioned official request instructions, local ZIP name/size checks, and an advanced normalized-JSON analysis lane. Deterministic metrics are inspectable, correctable, exportable, and deletable.</Text></View><View style={styles.panel}><Text style={styles.panelTitle}>What is not claimed</Text><Text style={styles.body}>The onboarding preview does not transmit archive bytes or claim an import before server malware scanning, sandbox extraction, and schema detection complete. It does not promise complete account history, production persistence, diagnosis, or a signed store release. Server upload wiring, deletion reconciliation, and release deployment remain separate gates.</Text></View></>}
  </ScrollView></View>
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#07111f' }, page: { width: '100%', maxWidth: 820, alignSelf: 'center', gap: 16, padding: 20, paddingTop: 48, paddingBottom: 80 }, eyebrow: { color: '#67e8f9', fontSize: 13, fontWeight: '800', letterSpacing: 1.2, textTransform: 'uppercase' }, title: { color: '#f8fafc', fontSize: 36, fontWeight: '900', lineHeight: 42 }, body: { color: '#cbd5e1', fontSize: 16, lineHeight: 24 }, notice: { backgroundColor: '#0c4a6e', borderRadius: 12, padding: 12 }, noticeText: { color: '#e0f2fe', lineHeight: 20 }, tabs: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 }, tab: { flexGrow: 1, minWidth: 100, borderColor: '#334155', borderWidth: 1, borderRadius: 12, padding: 12, alignItems: 'center' }, activeTab: { backgroundColor: '#155e75', borderColor: '#67e8f9' }, tabText: { color: '#f8fafc', fontWeight: '700', textTransform: 'capitalize' }, panel: { gap: 12, padding: 18, borderRadius: 18, backgroundColor: '#10213a', borderColor: '#1e40af', borderWidth: 1 }, panelTitle: { color: '#f8fafc', fontSize: 20, fontWeight: '800' }, card: { gap: 10, padding: 18, borderRadius: 18, backgroundColor: '#111827', borderColor: '#334155', borderWidth: 1 }, row: { flexDirection: 'row', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 }, cardTitle: { color: '#f8fafc', fontSize: 18, fontWeight: '800', flexShrink: 1 }, badge: { color: '#a5f3fc', fontSize: 12, fontWeight: '800', textTransform: 'uppercase' }, meta: { color: '#94a3b8', fontSize: 13, lineHeight: 19 }, subhead: { color: '#e2e8f0', fontWeight: '800', marginTop: 6 }, actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 }, button: { minHeight: 44, justifyContent: 'center', backgroundColor: '#0369a1', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 10 }, danger: { backgroundColor: '#991b1b' }, buttonText: { color: '#fff', fontWeight: '800' }, disabled: { opacity: 0.4 }, pressed: { opacity: 0.75 }, checkRow: { flexDirection: 'row', gap: 12, alignItems: 'flex-start', minHeight: 44 }, checkbox: { width: 24, height: 24, borderRadius: 5, borderWidth: 2, borderColor: '#67e8f9' }, checked: { backgroundColor: '#0891b2' }, checkText: { color: '#f1f5f9', flex: 1, lineHeight: 22 }, warning: { gap: 8, padding: 18, borderRadius: 18, borderColor: '#f59e0b', borderWidth: 1, backgroundColor: '#451a03' }, warningTitle: { color: '#fef3c7', fontSize: 18, fontWeight: '800' }, evidence: { borderTopColor: '#334155', borderTopWidth: 1, paddingTop: 10, gap: 4 }, corrected: { color: '#fde68a', fontWeight: '700' },
})
