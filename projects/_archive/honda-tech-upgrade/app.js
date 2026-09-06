const SERVICE_INTERVALS = {
  Civic: {
    'Oil Change': 5000,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000,
  },
  Accord: {
    'Oil Change': 7500,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000,
  },
  'CR-V': {
    'Oil Change': 7500,
    'Tire Rotation': 7500,
    'Brake Inspection': 30000,
    'Transmission Fluid': 60000,
    'Coolant Flush': 100000,
  },
};

const STORAGE_KEY = 'honda-tech-upgrade-demo-state';

function toMileage(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 0;
}

function createDemoState() {
  return {
    vehicle: 'CR-V',
    mileage: 68400,
    serviceEvent: 'Tire Rotation',
    serviceMileage: 60000,
  };
}

function normalizeOwnerInput(input = {}) {
  const vehicle = SERVICE_INTERVALS[input.vehicle] ? input.vehicle : 'Civic';
  const serviceEvent = SERVICE_INTERVALS[vehicle][input.serviceEvent]
    ? input.serviceEvent
    : 'Oil Change';
  const mileage = toMileage(input.mileage);
  const serviceMileage = Math.min(toMileage(input.serviceMileage), mileage || Number.MAX_SAFE_INTEGER);

  return {
    vehicle,
    mileage,
    serviceEvent,
    serviceMileage,
  };
}

function formatMiles(miles) {
  return `${Number(miles).toLocaleString('en-US')} miles`;
}

function buildTimeline(state) {
  const intervals = SERVICE_INTERVALS[state.vehicle] || SERVICE_INTERVALS.Civic;

  return Object.entries(intervals)
    .map(([service, interval]) => {
      const knownLastService = service === state.serviceEvent ? state.serviceMileage : 0;
      const cycleCount = knownLastService > 0
        ? Math.floor(knownLastService / interval) + 1
        : Math.floor(state.mileage / interval) + 1;
      const nextDue = Math.max(knownLastService + interval, cycleCount * interval);
      const milesUntilDue = nextDue - state.mileage;

      if (milesUntilDue <= 0) {
        return {
          service,
          interval,
          nextDue,
          status: 'overdue',
          milesOver: Math.abs(milesUntilDue),
          summary: `${service} is overdue by ${formatMiles(Math.abs(milesUntilDue))}.`,
        };
      }

      return {
        service,
        interval,
        nextDue,
        status: milesUntilDue <= 1500 ? 'due soon' : 'planned',
        milesLeft: milesUntilDue,
        summary: `${service} is due in ${formatMiles(milesUntilDue)}.`,
      };
    })
    .sort((a, b) => {
      const aDistance = a.status === 'overdue' ? -a.milesOver : a.milesLeft;
      const bDistance = b.status === 'overdue' ? -b.milesOver : b.milesLeft;
      return aDistance - bDistance;
    });
}

function computeOwnershipPlan(rawInput) {
  const state = normalizeOwnerInput(rawInput);
  const timeline = buildTimeline(state);
  const primary = timeline.find(item => item.service === state.serviceEvent) || timeline[0];
  const urgentCount = timeline.filter(item => item.status === 'overdue' || item.status === 'due soon').length;
  const nextPlanned = timeline.find(item => item.status === 'planned');

  return {
    state,
    primary,
    timeline,
    urgentCount,
    ownerSummary: `${state.vehicle} at ${formatMiles(state.mileage)}: ${primary.summary}`,
    planningNote: nextPlanned
      ? `Plan ahead for ${nextPlanned.service} at ${formatMiles(nextPlanned.nextDue)}.`
      : 'All tracked items need attention soon; prioritize a maintenance visit.',
  };
}

function readForm() {
  return normalizeOwnerInput({
    vehicle: document.getElementById('vehicle').value,
    mileage: document.getElementById('mileage').value,
    serviceEvent: document.getElementById('serviceEvent').value,
    serviceMileage: document.getElementById('serviceMileage').value,
  });
}

function writeForm(state) {
  document.getElementById('vehicle').value = state.vehicle;
  document.getElementById('mileage').value = state.mileage;
  document.getElementById('serviceEvent').value = state.serviceEvent;
  document.getElementById('serviceMileage').value = state.serviceMileage;
}

function saveState(state) {
  if (!window.localStorage) return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function loadState() {
  if (!window.localStorage) return createDemoState();
  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (!stored) return createDemoState();

  try {
    return normalizeOwnerInput(JSON.parse(stored));
  } catch (error) {
    return createDemoState();
  }
}

function badgeClass(status) {
  if (status === 'overdue') return 'badge overdue';
  if (status === 'due soon') return 'badge soon';
  return 'badge planned';
}

function renderPlan(plan) {
  const out = document.getElementById('output');
  out.innerHTML = '';

  const summary = document.createElement('section');
  summary.className = 'result-card';
  summary.innerHTML = `
    <p class="eyebrow">Next ownership action</p>
    <h2>${plan.primary.service}</h2>
    <p class="lead">${plan.ownerSummary}</p>
    <p>${plan.planningNote}</p>
  `;
  out.appendChild(summary);

  const list = document.createElement('ol');
  list.className = 'timeline';
  plan.timeline.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      <span class="${badgeClass(item.status)}">${item.status}</span>
      <strong>${item.service}</strong>
      <span>${item.summary} Next target: ${formatMiles(item.nextDue)}.</span>
    `;
    list.appendChild(li);
  });
  out.appendChild(list);

  const saved = document.createElement('p');
  saved.className = 'saved-note';
  saved.textContent = 'Saved locally in this browser only. No account, credentials, or paid APIs required.';
  out.appendChild(saved);
}

function updatePlan() {
  const state = readForm();
  const plan = computeOwnershipPlan(state);
  saveState(state);
  renderPlan(plan);
}

function resetToSample() {
  const state = createDemoState();
  writeForm(state);
  saveState(state);
  renderPlan(computeOwnershipPlan(state));
}

function clearDemo() {
  if (window.localStorage) {
    window.localStorage.removeItem(STORAGE_KEY);
  }
  const blank = normalizeOwnerInput({ vehicle: 'Civic', mileage: 0, serviceEvent: 'Oil Change', serviceMileage: 0 });
  writeForm(blank);
  renderPlan(computeOwnershipPlan(blank));
}

function initializeDemo() {
  writeForm(loadState());
  updatePlan();

  document.getElementById('ownerForm').addEventListener('submit', event => {
    event.preventDefault();
    updatePlan();
  });
  document.getElementById('sampleData').addEventListener('click', resetToSample);
  document.getElementById('clearDemo').addEventListener('click', clearDemo);
}

if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', initializeDemo);
}

if (typeof module !== 'undefined') {
  module.exports = {
    SERVICE_INTERVALS,
    computeOwnershipPlan,
    createDemoState,
    normalizeOwnerInput,
  };
}
