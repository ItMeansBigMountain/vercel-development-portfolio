const test = require('node:test');
const assert = require('node:assert/strict');
const {
  computeOwnershipPlan,
  createDemoState,
  normalizeOwnerInput,
} = require('./app.js');

test('normalizes anonymous owner input into local demo state', () => {
  const state = normalizeOwnerInput({
    vehicle: 'Accord',
    mileage: '48250',
    serviceEvent: 'Oil Change',
    serviceMileage: '43000',
  });

  assert.deepEqual(state, {
    vehicle: 'Accord',
    mileage: 48250,
    serviceEvent: 'Oil Change',
    serviceMileage: 43000,
  });
});

test('computes next maintenance plan from mileage and selected service event', () => {
  const plan = computeOwnershipPlan({
    vehicle: 'Civic',
    mileage: 45200,
    serviceEvent: 'Oil Change',
    serviceMileage: 40000,
  });

  assert.equal(plan.primary.service, 'Oil Change');
  assert.equal(plan.primary.status, 'overdue');
  assert.equal(plan.primary.nextDue, 45000);
  assert.equal(plan.primary.milesOver, 200);
  assert.match(plan.ownerSummary, /Civic at 45,200 miles/);
  assert.ok(plan.timeline.some(item => item.service === 'Tire Rotation'));
});

test('creates resettable sample data for an anonymous Honda owner', () => {
  const sample = createDemoState();
  assert.equal(sample.vehicle, 'CR-V');
  assert.equal(sample.mileage, 68400);
  assert.equal(sample.serviceEvent, 'Tire Rotation');
  assert.equal(sample.serviceMileage, 60000);

  const plan = computeOwnershipPlan(sample);
  assert.match(plan.ownerSummary, /CR-V/);
  assert.ok(plan.primary.milesOver > 0);
});
