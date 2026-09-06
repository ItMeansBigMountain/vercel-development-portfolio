const now = () => new Date().toISOString();

module.exports = (req, res) => {
  res.setHeader('content-type', 'application/json');
  res.status(200).json([
    {
      Id: 1,
      Title: 'Sample class recap — systems design',
      AudioUrl: null,
      Summary: 'Reviewed queue-based architectures, action items, and follow-up reading. This proves the meeting archive UI can load from a backend endpoint.',
      Transcript: 'Instructor: Today we covered queues, workers, retries, and searchable meeting notes. Student: The useful part is action-item extraction.',
      DiarizedTranscript: 'Instructor: Today we covered queues, workers, retries.\nStudent: The useful part is action-item extraction.',
      CreatedUtc: now(),
    },
    {
      Id: 2,
      Title: 'Zoom meeting-assets archive concept',
      AudioUrl: null,
      Summary: 'Meeting asset emails route into a Gmail label, then can be ingested into this searchable archive later.',
      Transcript: 'Hermes routes Zoom meeting-assets emails to a dedicated archive label for classes and summaries.',
      DiarizedTranscript: 'Hermes: Route Zoom meeting-assets emails into a class archive.',
      CreatedUtc: now(),
    },
  ]);
};
