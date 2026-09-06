async function getJson(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Request failed: ${url}`);
  return response.json();
}

function renderConfig(config) {
  document.getElementById('configPanel').innerHTML = `
    <strong>Runtime:</strong> ${config.appEnv} ?
    <strong>Market data:</strong> ${config.marketDataProvider} ?
    <strong>Sentiment:</strong> ${config.sentimentProvider} ?
    <strong>Email:</strong> ${config.emailProvider}
  `;
}

function renderDashboard(payload) {
  document.getElementById('overallScore').textContent = payload.overall_score;
  document.getElementById('overallLabel').textContent = payload.overall_label;
  const grid = document.getElementById('watchlist');
  grid.innerHTML = payload.watchlist.map(row => `
    <article class="ticker-card">
      <span>${row.headline_count} headlines</span>
      <h2>${row.ticker}</h2>
      <p><strong>Score:</strong> ${row.sentiment_score} <span class="badge ${row.sentiment_label}">${row.sentiment_label}</span></p>
      <ul>
        ${row.headlines.map(h => `<li>${h.title}<br><span class="source">${h.source} ? ${h.date}</span></li>`).join('')}
      </ul>
    </article>
  `).join('');
}

async function main() {
  const [config, dashboard] = await Promise.all([
    getJson('/api/config'),
    getJson('/api/dashboard'),
  ]);
  renderConfig(config);
  renderDashboard(dashboard);
}

main().catch(error => {
  document.getElementById('watchlist').innerHTML = `<article class="ticker-card"><h2>Load failed</h2><p>${error.message}</p></article>`;
});
