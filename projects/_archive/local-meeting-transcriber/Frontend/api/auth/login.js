module.exports = (req, res) => {
  res.setHeader('content-type', 'application/json');
  res.status(200).json({
    token: 'demo-local-meeting-token',
    user: { email: 'demo@local-meeting-transcriber.app', mode: 'demo' },
  });
};
