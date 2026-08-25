import { createElement, type ReactNode, useMemo, useState } from 'react'
import * as DocumentPicker from 'expo-document-picker'
import { Linking, Platform, Pressable, StyleSheet, Text, View } from 'react-native'

import { ARCHIVE_INSTRUCTION_VERSION, ARCHIVE_ONBOARDING_PLATFORMS, validateOnboardingArchive, type ArchiveOnboardingPlatform } from '../../../packages/domain/src/archiveOnboarding'

type SelectedFile = { name: string; size: number }
type Validation = ReturnType<typeof validateOnboardingArchive>

function DropZone({ children, onDrop }: { children: ReactNode; onDrop: (file: SelectedFile) => void }) {
  if (Platform.OS === 'web') {
    return createElement('div', {
      role: 'button',
      'aria-label': 'Archive drop zone',
      onDragOver: (event: DragEvent) => event.preventDefault(),
      onDrop: (event: DragEvent) => {
        event.preventDefault()
        const dropped = event.dataTransfer?.files?.[0]
        if (dropped) onDrop({ name: dropped.name, size: dropped.size })
      },
      style: { minHeight: 170, borderRadius: 16, border: '2px dashed #38bdf8', padding: 18, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 10 },
    }, children)
  }
  return <View accessibilityLabel="Archive drop zone" style={styles.dropZone}>{children}</View>
}

function formatBytes(bytes: number) {
  if (bytes < 1_000_000) return `${Math.max(1, Math.round(bytes / 1_000))} KB`
  return `${(bytes / 1_000_000).toFixed(1)} MB`
}

export function ArchiveWizard({ onNotice }: { onNotice: (message: string) => void }) {
  const [platformId, setPlatformId] = useState('')
  const [step, setStep] = useState<1 | 2 | 3>(1)
  const [file, setFile] = useState<SelectedFile | null>(null)
  const [validation, setValidation] = useState<Validation | null>(null)
  const platform = useMemo(() => ARCHIVE_ONBOARDING_PLATFORMS.find((item) => item.id === platformId) ?? null, [platformId])

  const selectPlatform = (item: ArchiveOnboardingPlatform) => {
    setPlatformId(item.id); setStep(2); setFile(null); setValidation(null)
    onNotice(`${item.label} selected. Follow the official request steps before choosing a ZIP.`)
  }

  const inspect = (nextFile: SelectedFile) => {
    const result = validateOnboardingArchive(platformId, nextFile)
    setFile(nextFile); setValidation(result); setStep(3)
    onNotice(result.ok ? 'Local intake checks completed. The archive contents have not been uploaded or imported.' : result.error)
  }

  const chooseFile = async () => {
    const result = await DocumentPicker.getDocumentAsync({ type: ['application/zip', 'application/x-zip-compressed'], copyToCacheDirectory: false })
    if (result.canceled) return
    const asset = result.assets[0]
    if (!asset) return
    inspect({ name: asset.name, size: asset.size ?? 0 })
  }

  const clear = () => {
    setFile(null); setValidation(null); setStep(platform ? 2 : 1)
    onNotice('Selected archive removed from this browser session. No archive bytes were retained by this onboarding screen.')
  }


  return <View style={styles.stack}>
    <View style={styles.progress} accessibilityLabel={`Archive onboarding step ${step} of 3`}>
      {[1, 2, 3].map((number) => <View key={number} style={[styles.progressItem, number <= step && styles.progressActive]}><Text style={styles.progressText}>{number === 1 ? 'Platform' : number === 2 ? 'Request' : 'Validate'}</Text></View>)}
    </View>

    <View style={styles.panel}>
      <Text accessibilityRole="header" style={styles.title}>1. Which platform made your archive?</Text>
      <Text style={styles.body}>Only deterministic, versioned import lanes are selectable. “Sample required” means the secure importer will abstain unless the internal layout matches a reviewed schema.</Text>
      <View style={styles.platformGrid}>{ARCHIVE_ONBOARDING_PLATFORMS.map((item) => <Pressable key={item.id} accessibilityRole="radio" accessibilityState={{ checked: platformId === item.id }} onPress={() => selectPlatform(item)} style={[styles.platform, platformId === item.id && styles.platformSelected]}><Text style={styles.platformName}>{item.label}</Text><Text style={styles.meta}>{item.status === 'enabled' ? 'Parser enabled' : 'Sample required'} · {item.parserVersion}</Text></Pressable>)}</View>
    </View>

    {platform && <View style={styles.panel}>
      <Text accessibilityRole="header" style={styles.title}>2. Request and download from {platform.label}</Text>
      {platform.requestSteps.map((item, index) => <View key={item} style={styles.stepRow}><Text style={styles.stepNumber}>{index + 1}</Text><Text style={styles.stepText}>{item}</Text></View>)}
      <Pressable accessibilityRole="link" onPress={() => void Linking.openURL(platform.officialUrl)} style={styles.link}><Text style={styles.linkText}>Open official {platform.label} instructions ↗</Text></Pressable>
      <Text style={styles.subhead}>What to expect</Text>{platform.expected.map((item) => <Text key={item} style={styles.body}>• {item}</Text>)}
      <View style={styles.warning}><Text style={styles.warningTitle}>Private and potentially large</Text><Text style={styles.body}>{platform.privacyWarning}</Text><Text style={styles.meta}>ZIP only · 250 MB compressed maximum · 1 GB extracted maximum · never include passwords or credentials</Text></View>
    </View>}

    {platform && <View style={styles.panel}>
      <Text accessibilityRole="header" style={styles.title}>3. Choose or drop the original ZIP</Text>
      <DropZone onDrop={inspect}><Text style={styles.dropTitle}>{file ? file.name : 'Drop a ZIP here on web'}</Text><Text style={styles.meta}>{file ? formatBytes(file.size) : 'or use the file picker on web, iPhone, or Android'}</Text><Pressable accessibilityRole="button" onPress={() => void chooseFile()} style={styles.button}><Text style={styles.buttonText}>{file ? 'Choose a different ZIP' : 'Choose ZIP archive'}</Text></Pressable></DropZone>

      {validation && !validation.ok && <View accessibilityRole="alert" style={styles.error}><Text style={styles.errorTitle}>Archive not accepted</Text><Text style={styles.body}>{validation.error}</Text><Text style={styles.meta}>Remove it and choose the original platform ZIP. Nothing was uploaded.</Text></View>}
      {validation?.ok && <View style={styles.result}>
        <Text accessibilityRole="header" style={styles.resultTitle}>Ready for secure import</Text>
        <Text style={styles.body}>Local validation 100% · ZIP name and size accepted</Text>
        <Text style={styles.meta}>Detected platform: {validation.platform.label} · schema {validation.platform.parserVersion} · {validation.confidence} filename confidence</Text>
        <Text style={styles.subhead}>Eligible imported categories</Text><Text style={styles.body}>{validation.platform.categories.join(' · ')}</Text>
        <Text style={styles.meta}>Coverage is provisional until the server scans and parses internal files. Unknown layouts are quarantined; no AI guesses missing fields. This preview does not transmit archive bytes.</Text>
        {validation.warnings.map((warning) => <Text key={warning} style={styles.warningText}>• {warning}</Text>)}
      </View>}
      {file && <Pressable accessibilityRole="button" onPress={clear} style={styles.deleteButton}><Text style={styles.buttonText}>Remove selected archive</Text></Pressable>}
      <Text style={styles.meta}>Instructions: {ARCHIVE_INSTRUCTION_VERSION}. Deleting here clears the browser selection. After a real import, account deletion must remove raw archive objects, normalized events, and derived metrics by provenance.</Text>
    </View>}
  </View>
}

const styles = StyleSheet.create({
  stack: { gap: 16 }, progress: { flexDirection: 'row', gap: 6 }, progressItem: { flex: 1, minHeight: 36, borderRadius: 10, backgroundColor: '#1e293b', alignItems: 'center', justifyContent: 'center' }, progressActive: { backgroundColor: '#155e75' }, progressText: { color: '#e2e8f0', fontSize: 12, fontWeight: '800' }, panel: { gap: 12, padding: 18, borderRadius: 18, backgroundColor: '#10213a', borderColor: '#1e40af', borderWidth: 1 }, title: { color: '#f8fafc', fontSize: 20, fontWeight: '800' }, body: { color: '#cbd5e1', fontSize: 16, lineHeight: 24 }, meta: { color: '#94a3b8', fontSize: 13, lineHeight: 19 }, platformGrid: { gap: 8 }, platform: { minHeight: 64, borderRadius: 12, borderWidth: 1, borderColor: '#475569', padding: 12, justifyContent: 'center' }, platformSelected: { borderColor: '#67e8f9', backgroundColor: '#164e63' }, platformName: { color: '#f8fafc', fontSize: 16, fontWeight: '800' }, stepRow: { flexDirection: 'row', gap: 12, alignItems: 'flex-start' }, stepNumber: { color: '#07111f', backgroundColor: '#67e8f9', width: 26, height: 26, borderRadius: 13, textAlign: 'center', lineHeight: 26, fontWeight: '900' }, stepText: { color: '#cbd5e1', fontSize: 16, lineHeight: 24, flex: 1 }, link: { minHeight: 44, justifyContent: 'center', borderRadius: 10, borderWidth: 1, borderColor: '#38bdf8', padding: 12 }, linkText: { color: '#7dd3fc', fontWeight: '800' }, subhead: { color: '#e2e8f0', fontWeight: '800', marginTop: 4 }, warning: { gap: 6, backgroundColor: '#422006', borderRadius: 12, borderWidth: 1, borderColor: '#d97706', padding: 12 }, warningTitle: { color: '#fde68a', fontWeight: '900' }, dropZone: { minHeight: 170, borderRadius: 16, borderWidth: 2, borderStyle: 'dashed', borderColor: '#38bdf8', padding: 18, alignItems: 'center', justifyContent: 'center', gap: 10 }, dropTitle: { color: '#f8fafc', fontSize: 17, fontWeight: '800', textAlign: 'center' }, button: { minHeight: 44, justifyContent: 'center', backgroundColor: '#0369a1', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 10 }, deleteButton: { minHeight: 44, justifyContent: 'center', alignItems: 'center', backgroundColor: '#991b1b', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 10 }, buttonText: { color: '#fff', fontWeight: '800' }, error: { gap: 6, borderRadius: 12, backgroundColor: '#450a0a', borderColor: '#ef4444', borderWidth: 1, padding: 12 }, errorTitle: { color: '#fecaca', fontWeight: '900', fontSize: 17 }, result: { gap: 8, borderRadius: 12, backgroundColor: '#052e16', borderColor: '#22c55e', borderWidth: 1, padding: 14 }, resultTitle: { color: '#bbf7d0', fontWeight: '900', fontSize: 18 }, warningText: { color: '#fde68a', fontSize: 13, lineHeight: 19 },
})
