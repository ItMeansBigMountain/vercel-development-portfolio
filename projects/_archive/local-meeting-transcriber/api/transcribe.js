export default async function handler(req, res) {
  const { audioUrl } = req.body;
  if (!audioUrl) {
    return res.status(400).json({ error: 'audioUrl required' });
  }
  // Mock transcription - replace with real service (e.g., Whisper, Deepgram) later
  const mockTranscript = `Mock transcription of audio from ${audioUrl}`;
  return res.status(200).json({ transcript: mockTranscript });
}