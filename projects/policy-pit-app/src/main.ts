import "./style.css";
import { nextIndex, policyCards, progressLabel, type Lean } from "./policies";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("Application root not found");
const root = app;

let cardIndex = 0;
const votes: Lean[] = [];

function render(): void {
  const done = cardIndex >= policyCards.length;
  const card = policyCards[cardIndex];
  root.innerHTML = `
    <header class="site-header">
      <a class="brand" href="#main" aria-label="Policy Pit home"><span aria-hidden="true">PP</span> Policy Pit</a>
      <span class="preview-badge">Development preview · sample data</span>
    </header>
    <main id="main" tabindex="-1">
      <section class="hero" aria-labelledby="page-title">
        <p class="eyebrow">Compare ideas before parties</p>
        <h1 id="page-title">Which policy approach fits you?</h1>
        <p class="lede">Try one small, private-on-this-device comparison flow using fictional candidates and illustrative policy statements.</p>
      </section>
      <section class="comparison" aria-live="polite" tabindex="-1">
        ${done ? completionMarkup() : cardMarkup(cardIndex)}
      </section>
      <aside class="scope-note" aria-labelledby="scope-title">
        <h2 id="scope-title">What this preview proves</h2>
        <ul>
          <li>A keyboard- and touch-friendly policy preference loop.</li>
          <li>No account, analytics, server storage, or real crowd results.</li>
          <li>No claims about real politicians; source verification is a future gate.</li>
        </ul>
      </aside>
    </main>
    <footer>Development scaffold · not a finished product · not production</footer>
  `;
  bindActions();
}

function cardMarkup(index: number): string {
  const card = policyCards[index];
  return `
    <div class="progress-row">
      <span>Sample comparison</span>
      <span>${progressLabel(index, policyCards.length)}</span>
    </div>
    <div class="progress" role="progressbar" aria-label="Comparison progress" aria-valuemin="1" aria-valuemax="${policyCards.length}" aria-valuenow="${index + 1}"><span style="width:${((index + 1) / policyCards.length) * 100}%"></span></div>
    <article class="policy-card">
      <p class="topic">${card.topic}</p>
      <h2>${card.prompt}</h2>
      <div class="positions">
        <section class="position blue"><h3>Candidate Blue</h3><p>${card.bluePosition}</p></section>
        <section class="position red"><h3>Candidate Red</h3><p>${card.redPosition}</p></section>
      </div>
      <p class="source-note">${card.sourceNote}</p>
      <fieldset class="actions"><legend>Choose the approach you prefer</legend>
        <button type="button" data-vote="blue">Prefer Blue</button>
        <button type="button" data-vote="neutral">Neutral / skip</button>
        <button type="button" data-vote="red">Prefer Red</button>
      </fieldset>
    </article>`;
}

function completionMarkup(): string {
  const count = (lean: Lean) => votes.filter((vote) => vote === lean).length;
  return `
    <article class="policy-card result-card">
      <p class="topic">Sample complete</p>
      <h2>Your local preview result</h2>
      <p>This is a simple interaction summary, not a political identity score.</p>
      <div class="result-grid">
        <span><strong>${count("blue")}</strong> Blue choices</span>
        <span><strong>${count("neutral")}</strong> Neutral / skipped</span>
        <span><strong>${count("red")}</strong> Red choices</span>
      </div>
      <button type="button" data-restart>Try again</button>
    </article>`;
}

function bindActions(): void {
  document.querySelectorAll<HTMLButtonElement>("[data-vote]").forEach((button) => {
    button.addEventListener("click", () => {
      votes.push(button.dataset.vote as Lean);
      cardIndex = nextIndex(cardIndex, policyCards.length);
      render();
      document.querySelector<HTMLElement>(".comparison")?.focus();
    });
  });
  document.querySelector<HTMLButtonElement>("[data-restart]")?.addEventListener("click", () => {
    cardIndex = 0;
    votes.length = 0;
    render();
    document.querySelector<HTMLElement>(".comparison")?.focus();
  });
}

render();
