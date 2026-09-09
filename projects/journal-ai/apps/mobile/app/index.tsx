import AsyncStorage from '@react-native-async-storage/async-storage'
import { RecordingPresets, requestRecordingPermissionsAsync, setAudioModeAsync, useAudioRecorder } from 'expo-audio'
import * as DocumentPicker from 'expo-document-picker'
import * as Linking from 'expo-linking'
import * as Notifications from 'expo-notifications'
import * as WebBrowser from 'expo-web-browser'
import { useEffect, useMemo, useState } from 'react'
import { Alert, Pressable, ScrollView, Share, StyleSheet, Text, TextInput, View } from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'
import { createJournalEntry, deleteJournalEntry, exportJournal, queueOfflineMutation, type JournalEntry, type OfflineMutation } from '../../../frontend/journal-app/src/journalDomain'
import { createMeetingJob, transitionJob, type MeetingJob } from '../../../frontend/journal-app/src/meetingWorkflow'
import { clearAllPrivateData, loadEntries, loadQueue, saveEntries, saveQueue, saveSession } from '../src/storage'

const meetingKey = 'journal-ai.meetings.v1'
type Tab = 'journal' | 'meetings' | 'settings'
const nowId = () => `${Date.now()}-${Math.random().toString(36).slice(2)}`

export default function Home() {
  const [tab, setTab] = useState<Tab>('journal')
  const [entries, setEntries] = useState<JournalEntry[]>([])
  const [meetings, setMeetings] = useState<MeetingJob[]>([])
  const [queue, setQueue] = useState<OfflineMutation[]>([])
  const [body, setBody] = useState('')
  const [mood, setMood] = useState('steady')
  const [consented, setConsented] = useState(false)
  const [offline, setOffline] = useState(false)
  const [recording, setRecording] = useState(false)
  const recorder = useAudioRecorder(RecordingPresets.HIGH_QUALITY)
  const activeEntries = useMemo(() => entries.filter((entry) => !entry.deletedAt), [entries])
  const oauthConfigured = Boolean(process.env.EXPO_PUBLIC_OAUTH_URL)

  useEffect(() => {
    Promise.all([loadEntries(), loadQueue(), AsyncStorage.getItem(meetingKey)]).then(([savedEntries, savedQueue, savedMeetings]) => {
      setEntries(savedEntries); setQueue(savedQueue); setMeetings(JSON.parse(savedMeetings ?? '[]') as MeetingJob[])
    }).catch(() => setOffline(true))
  }, [])

  async function persistEntries(next: JournalEntry[], mutation: OfflineMutation) {
    const nextQueue = queueOfflineMutation(queue, mutation)
    setEntries(next); setQueue(nextQueue)
    await Promise.all([saveEntries(next), saveQueue(nextQueue)])
  }

  async function addEntry() {
    try {
      const entry = createJournalEntry({ id: nowId(), body, mood, createdAt: new Date().toISOString() })
      await persistEntries([entry, ...entries], { id: `upsert-${entry.id}`, kind: 'upsert', entryId: entry.id, queuedAt: new Date().toISOString() })
      setBody('')
    } catch (error) { Alert.alert('Entry not saved', error instanceof Error ? error.message : 'Try again.') }
  }

  async function removeEntry(entry: JournalEntry) {
    const deleted = deleteJournalEntry(entry, new Date().toISOString())
    await persistEntries(entries.map((item) => item.id === entry.id ? deleted : item), { id: `delete-${entry.id}`, kind: 'delete', entryId: entry.id, queuedAt: deleted.updatedAt })
  }

  async function importMeeting() {
    if (!consented) return Alert.alert('Consent required', 'Confirm that everyone agreed before recording or uploading.')
    const result = await DocumentPicker.getDocumentAsync({ type: ['audio/*', 'video/*'], copyToCacheDirectory: true })
    if (result.canceled) return
    const asset = result.assets[0]
    let job = createMeetingJob({ id: nowId(), fileName: asset.name, retention: 'delete-after-transcription', consentedAt: new Date().toISOString() })
    job = transitionJob(job, 'normalizing')
    const next = [job, ...meetings]
    setMeetings(next); await AsyncStorage.setItem(meetingKey, JSON.stringify(next))
  }

  async function toggleRecording() {
    if (!consented) return Alert.alert('Consent required', 'Confirm that everyone agreed before recording.')
    if (!recording) {
      const permission = await requestRecordingPermissionsAsync()
      if (!permission.granted) return Alert.alert('Microphone unavailable', 'Enable microphone access in system settings.')
      await setAudioModeAsync({ allowsRecording: true, playsInSilentMode: true })
      await recorder.prepareToRecordAsync()
      recorder.record()
      setRecording(true)
      return
    }
    await recorder.stop()
    setRecording(false)
    const name = recorder.uri?.split('/').pop() ?? `meeting-${Date.now()}.m4a`
    let job = createMeetingJob({ id: nowId(), fileName: name, retention: 'delete-after-transcription', consentedAt: new Date().toISOString() })
    job = transitionJob(job, 'normalizing')
    const next = [job, ...meetings]
    setMeetings(next); await AsyncStorage.setItem(meetingKey, JSON.stringify(next))
  }

  async function enableReminder() {
    const permission = await Notifications.requestPermissionsAsync()
    if (!permission.granted) return Alert.alert('Notifications are off', 'Enable them in system settings for reflection reminders.')
    await Notifications.scheduleNotificationAsync({ content: { title: 'Private reflection', body: 'Take two minutes to capture what matters.' }, trigger: { type: Notifications.SchedulableTriggerInputTypes.TIME_INTERVAL, seconds: 60 * 60 * 24, repeats: true } })
    Alert.alert('Reminder enabled', 'A daily reflection reminder is scheduled on this device.')
  }

  async function signIn() {
    const callback = Linking.createURL('/auth/callback')
    const authUrl = process.env.EXPO_PUBLIC_OAUTH_URL
    if (!authUrl) return Alert.alert('OAuth not configured', 'Set EXPO_PUBLIC_OAUTH_URL for this release environment.')
    const result = await WebBrowser.openAuthSessionAsync(`${authUrl}?redirect_uri=${encodeURIComponent(callback)}`, callback)
    if (result.type === 'success') await saveSession(result.url)
  }

  async function eraseEverything() {
    await clearAllPrivateData(); await AsyncStorage.removeItem(meetingKey)
    setEntries([]); setMeetings([]); setQueue([])
  }

  function confirmEraseEverything() {
    Alert.alert('Erase all local data?', 'This removes journals, meeting metadata, queued changes, and the saved session from this device.', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Erase', style: 'destructive', onPress: () => { void eraseEverything() } },
    ])
  }

  async function shareExport() {
    await Share.share({ title: 'Private journal export', message: exportJournal(activeEntries, 'markdown') })
  }

  return <SafeAreaView style={styles.safe}>
    <View style={styles.header}><View><Text style={styles.eyebrow}>PRIVATE BY DEFAULT</Text><Text style={styles.title}>Journal AI</Text></View><Text style={offline ? styles.offline : styles.local}>{offline ? 'Offline' : `${queue.length} local changes`}</Text></View>
    <View style={styles.tabs}>{(['journal', 'meetings', 'settings'] as Tab[]).map((item) => <Pressable key={item} onPress={() => setTab(item)} style={[styles.tab, tab === item && styles.tabActive]}><Text style={tab === item ? styles.tabTextActive : styles.tabText}>{item}</Text></Pressable>)}</View>
    <ScrollView contentContainerStyle={styles.content}>
      {tab === 'journal' && <>
        <View style={styles.card}><Text style={styles.cardTitle}>What deserves your attention?</Text><TextInput accessibilityLabel="Private journal entry" multiline value={body} onChangeText={setBody} placeholder="Write without polishing…" placeholderTextColor="#72808f" style={styles.input}/><View style={styles.row}>{['low','steady','good'].map((item) => <Pressable key={item} onPress={() => setMood(item)} style={[styles.chip, mood === item && styles.chipActive]}><Text>{item}</Text></Pressable>)}</View><Pressable style={styles.primary} onPress={addEntry}><Text style={styles.primaryText}>Save privately</Text></Pressable></View>
        {activeEntries.length === 0 && <Text style={styles.empty}>Your entries stay on this device until sync is configured.</Text>}
        {activeEntries.map((entry) => <View style={styles.card} key={entry.id}><Text style={styles.meta}>{new Date(entry.createdAt).toLocaleString()} · {entry.mood}</Text><Text style={styles.body}>{entry.body}</Text><Pressable onPress={() => removeEntry(entry)}><Text style={styles.danger}>Remove from this device</Text></Pressable></View>)}
      </>}
      {tab === 'meetings' && <>
        <View style={styles.card}><Text style={styles.cardTitle}>Meeting capture</Text><Text style={styles.body}>Record or upload only after every participant agrees. This preview stores files in app cache; verified automatic media erasure is not implemented yet.</Text><Pressable onPress={() => setConsented(!consented)} style={[styles.consent, consented && styles.consentActive]}><Text>{consented ? '✓ Consent confirmed' : 'Confirm everyone consented'}</Text></Pressable><Pressable style={styles.primary} onPress={toggleRecording}><Text style={styles.primaryText}>{recording ? 'Stop & save recording' : 'Start recording'}</Text></Pressable><Pressable style={styles.secondary} onPress={importMeeting}><Text>Upload recording</Text></Pressable></View>
        {meetings.map((meeting) => <View style={styles.card} key={meeting.id}><Text style={styles.cardTitle}>{meeting.fileName}</Text><Text style={styles.meta}>{meeting.state.replaceAll('_', ' ')} · {meeting.progress}%</Text><Text style={styles.body}>Stored in the app cache. Processing resumes when a transcription service is configured.</Text></View>)}
      </>}
      {tab === 'settings' && <View style={styles.card}><Text style={styles.cardTitle}>Privacy & portability</Text><Text style={styles.body}>Journal text is stored on this device, but encryption at rest is not implemented in this preview.</Text>{oauthConfigured && <Pressable style={styles.secondary} onPress={signIn}><Text>Connect configured account</Text></Pressable>}<Pressable style={styles.secondary} onPress={enableReminder}><Text>Enable daily reminder</Text></Pressable><Pressable style={styles.secondary} onPress={shareExport}><Text>Share journal export</Text></Pressable><Text style={styles.label}>Export preview</Text><Text selectable style={styles.export}>{exportJournal(activeEntries, 'markdown')}</Text><Pressable onPress={confirmEraseEverything}><Text style={styles.danger}>Clear known local app data</Text></Pressable></View>}
    </ScrollView>
  </SafeAreaView>
}

const styles = StyleSheet.create({
  safe:{flex:1,backgroundColor:'#f4f1e9'},header:{padding:20,flexDirection:'row',justifyContent:'space-between',alignItems:'center'},eyebrow:{fontSize:11,letterSpacing:2,color:'#526558'},title:{fontSize:32,fontWeight:'700',color:'#17241c'},local:{fontSize:12,color:'#526558'},offline:{fontSize:12,color:'#a94737'},tabs:{flexDirection:'row',paddingHorizontal:16,gap:8},tab:{flex:1,padding:12,alignItems:'center',borderRadius:14},tabActive:{backgroundColor:'#173f32'},tabText:{textTransform:'capitalize',color:'#526558'},tabTextActive:{textTransform:'capitalize',color:'white',fontWeight:'700'},content:{padding:16,gap:14},card:{backgroundColor:'#fffdf8',borderRadius:20,padding:18,gap:12,borderWidth:1,borderColor:'#ded9cc'},cardTitle:{fontSize:19,fontWeight:'700',color:'#17241c'},input:{minHeight:120,textAlignVertical:'top',fontSize:16,color:'#17241c',padding:14,backgroundColor:'#f5f2ea',borderRadius:14},row:{flexDirection:'row',gap:8},chip:{paddingVertical:8,paddingHorizontal:14,borderRadius:20,backgroundColor:'#e6e3da'},chipActive:{backgroundColor:'#b8d4c2'},primary:{backgroundColor:'#d35f45',padding:14,borderRadius:14,alignItems:'center'},primaryText:{color:'white',fontWeight:'700'},secondary:{padding:14,borderRadius:14,backgroundColor:'#e7eee9'},consent:{padding:14,borderRadius:14,backgroundColor:'#f1d9d1'},consentActive:{backgroundColor:'#cfe4d6'},meta:{fontSize:12,color:'#66736a',textTransform:'capitalize'},body:{fontSize:15,lineHeight:22,color:'#26372d'},danger:{color:'#a43a2a',fontWeight:'600',paddingVertical:8},empty:{textAlign:'center',color:'#66736a',padding:24},label:{fontWeight:'700',marginTop:8},export:{fontFamily:'monospace',fontSize:11,backgroundColor:'#f5f2ea',padding:12,borderRadius:10}
})
