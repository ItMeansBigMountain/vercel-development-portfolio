import AsyncStorage from '@react-native-async-storage/async-storage';

export type Submission = {
  lessonId: string;
  code: string;
  reflection: string;
  traceAnswer?: string;
  selectedBanks?: string[];
  status: 'pending' | 'approved' | 'needs-revision';
  queuedAt: string;
};

export type Draft = {
  lessonId: string;
  code: string;
  reflection: string;
  traceAnswer: string;
  selectedBanks: string[];
};

const KEY = 'algorithm-academy:demo-submissions:v1';
const DRAFT_KEY = 'algorithm-academy:demo-draft:v1';

export async function loadSubmissions(): Promise<Submission[]> {
  const stored = await AsyncStorage.getItem(KEY);
  if (!stored) return [];
  try {
    const value: unknown = JSON.parse(stored);
    return Array.isArray(value) ? value as Submission[] : [];
  } catch {
    return [];
  }
}

export async function saveSubmissions(items: Submission[]) {
  await AsyncStorage.setItem(KEY, JSON.stringify(items));
}

export async function loadDraft(): Promise<Draft | null> {
  const stored = await AsyncStorage.getItem(DRAFT_KEY);
  if (!stored) return null;
  try {
    const value: unknown = JSON.parse(stored);
    return value && typeof value === 'object' ? value as Draft : null;
  } catch {
    return null;
  }
}

export async function saveDraft(item: Draft) {
  await AsyncStorage.setItem(DRAFT_KEY, JSON.stringify(item));
}
