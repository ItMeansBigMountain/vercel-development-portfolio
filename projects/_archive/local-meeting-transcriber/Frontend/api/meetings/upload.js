module.exports = (req, res) => {
  res.setHeader('content-type', 'application/json');
  res.status(200).json({
    Id: 99,
    Title: 'Demo upload received',
    AudioUrl: null,
    Summary: 'The production transcription worker is not attached on Vercel yet. This backend function verifies the upload endpoint contract for the frontend MVP.',
    Transcript: 'Demo transcript placeholder. Local or hosted transcription worker integration is the next backend milestone.',
    DiarizedTranscript: 'System: Demo upload endpoint reached successfully.',
    CreatedUtc: new Date().toISOString(),
  });
};
