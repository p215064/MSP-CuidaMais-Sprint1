import test from 'node:test';
import assert from 'node:assert/strict';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { Store } from './store.js';
import { createApp, classifyBloodPressure } from './index.js';

async function fixture() {
  const directory = await fs.mkdtemp(path.join(os.tmpdir(), 'cuida-test-'));
  const store = await new Store(path.join(directory, 'db.json')).init();
  const server = createApp(store).listen(0, '127.0.0.1');
  await new Promise((resolve) => server.once('listening', resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  return { store, base, close: () => new Promise((resolve) => { server.closeAllConnections(); server.close(resolve); }) };
}

async function call(base, route, method = 'GET', body) {
  const response = await fetch(`${base}${route}`, { method, headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined });
  return { status: response.status, body: response.status === 204 ? null : await response.json() };
}

test('classifica tensão normal, elevada, baixa e crise', () => {
  assert.equal(classifyBloodPressure(120, 80).level, 'normal');
  assert.equal(classifyBloodPressure(145, 85).level, 'high');
  assert.equal(classifyBloodPressure(85, 55).level, 'low');
  assert.equal(classifyBloodPressure(185, 125).level, 'emergency');
});

test('atualiza o perfil e rejeita dados inválidos', async () => {
  const { base, close } = await fixture();
  const valid = await call(base, '/api/elder', 'PUT', { name: 'António Costa', birthDate: '1940-02-10', phone: '912 345 678', address: 'Porto', conditions: '', notes: '' });
  assert.equal(valid.status, 200);
  assert.equal(valid.body.name, 'António Costa');
  const invalid = await call(base, '/api/elder', 'PUT', { name: '', birthDate: '1940-02-10', phone: 'abc', address: '' });
  assert.equal(invalid.status, 400);
  await close();
});

test('adiciona contactos por prioridade e remove', async () => {
  const { base, close } = await fixture();
  const created = await call(base, '/api/contacts', 'POST', { name: 'Rita Costa', relationship: 'Neta', phone: '916 222 333', email: '', priority: 1 });
  assert.equal(created.status, 201);
  const state = await call(base, '/api/state');
  assert.equal(state.body.contacts.length, 3);
  assert.ok(state.body.contacts.some((contact) => contact.name === 'Rita Costa'));
  assert.deepEqual(state.body.contacts.map((contact) => contact.priority), [1, 1, 2]);
  const removed = await call(base, `/api/contacts/${created.body.id}`, 'DELETE');
  assert.equal(removed.status, 204);
  await close();
});

test('regista medição válida e valida limites', async () => {
  const { base, close } = await fixture();
  const created = await call(base, '/api/readings', 'POST', { systolic: 142, diastolic: 91, pulse: 76 });
  assert.equal(created.status, 201);
  assert.equal(created.body.classification.level, 'high');
  const invalid = await call(base, '/api/readings', 'POST', { systolic: 999, diastolic: 80, pulse: 70 });
  assert.equal(invalid.status, 400);
  await close();
});

test('deteta queda, notifica contactos e resolve sem duplicar alerta ativo', async () => {
  const { base, close } = await fixture();
  const fall = await call(base, '/api/falls/simulate', 'POST', {});
  assert.equal(fall.status, 201);
  assert.equal(fall.body.notifications.length, 2);
  assert.equal((await call(base, '/api/falls/simulate', 'POST', {})).status, 409);
  const resolved = await call(base, `/api/falls/${fall.body.id}/resolve`, 'POST', { outcome: 'false_alarm' });
  assert.equal(resolved.status, 200);
  assert.equal(resolved.body.status, 'false_alarm');
  await close();
});
