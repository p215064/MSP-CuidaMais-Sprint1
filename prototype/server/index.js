import express from 'express';
import { randomUUID } from 'node:crypto';
import { Store } from './store.js';

export function classifyBloodPressure(systolic, diastolic) {
  if (systolic >= 180 || diastolic >= 120) return { level: 'emergency', label: 'Crise hipertensiva', color: 'red' };
  if (systolic >= 140 || diastolic >= 90) return { level: 'high', label: 'Tensão elevada', color: 'amber' };
  if (systolic < 90 || diastolic < 60) return { level: 'low', label: 'Tensão baixa', color: 'blue' };
  return { level: 'normal', label: 'Dentro dos valores de referência', color: 'green' };
}

const text = (value, max = 300) => typeof value === 'string' && value.trim().length > 0 && value.trim().length <= max;
const phone = (value) => typeof value === 'string' && /^[+\d][\d\s()-]{7,19}$/.test(value);
const date = (value) => typeof value === 'string' && !Number.isNaN(Date.parse(value));

export function createApp(store) {
  const app = express();
  app.use(express.json({ limit: '100kb' }));
  app.use((req, res, next) => {
    res.setHeader('X-Content-Type-Options', 'nosniff');
    next();
  });

  app.get('/api/health', (_req, res) => res.json({ status: 'ok', service: 'Cuida+ API' }));
  app.get('/api/state', (_req, res) => res.json(store.state));

  app.put('/api/elder', async (req, res) => {
    const { name, birthDate, phone: contactPhone, address, conditions = '', notes = '' } = req.body;
    if (!text(name, 120) || !date(birthDate) || !phone(contactPhone) || !text(address, 250)) {
      return res.status(400).json({ error: 'Preencha nome, data de nascimento, telefone e morada com valores válidos.' });
    }
    if (new Date(birthDate) >= new Date()) return res.status(400).json({ error: 'A data de nascimento deve ser anterior à data atual.' });
    store.state.elder = { ...store.state.elder, name: name.trim(), birthDate, phone: contactPhone.trim(), address: address.trim(), conditions: conditions.trim(), notes: notes.trim() };
    await store.save();
    res.json(store.state.elder);
  });

  app.post('/api/contacts', async (req, res) => {
    const { name, relationship, phone: contactPhone, email = '', priority } = req.body;
    if (!text(name, 120) || !text(relationship, 80) || !phone(contactPhone) || ![1, 2, 3].includes(Number(priority))) {
      return res.status(400).json({ error: 'Indique nome, parentesco, telefone válido e prioridade entre 1 e 3.' });
    }
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return res.status(400).json({ error: 'O email não é válido.' });
    const contact = { id: randomUUID(), name: name.trim(), relationship: relationship.trim(), phone: contactPhone.trim(), email: email.trim(), priority: Number(priority) };
    store.state.contacts.push(contact);
    store.state.contacts.sort((a, b) => a.priority - b.priority);
    await store.save();
    res.status(201).json(contact);
  });

  app.delete('/api/contacts/:id', async (req, res) => {
    const index = store.state.contacts.findIndex((item) => item.id === req.params.id);
    if (index < 0) return res.status(404).json({ error: 'Contacto não encontrado.' });
    store.state.contacts.splice(index, 1);
    await store.save();
    res.status(204).end();
  });

  app.post('/api/readings', async (req, res) => {
    const systolic = Number(req.body.systolic);
    const diastolic = Number(req.body.diastolic);
    const pulse = Number(req.body.pulse);
    if (!Number.isInteger(systolic) || systolic < 50 || systolic > 260 || !Number.isInteger(diastolic) || diastolic < 30 || diastolic > 180 || !Number.isInteger(pulse) || pulse < 30 || pulse > 220) {
      return res.status(400).json({ error: 'Verifique os valores: sistólica 50–260, diastólica 30–180 e pulso 30–220.' });
    }
    const reading = { id: randomUUID(), systolic, diastolic, pulse, measuredAt: new Date().toISOString() };
    store.state.readings.unshift(reading);
    await store.save();
    res.status(201).json({ ...reading, classification: classifyBloodPressure(systolic, diastolic) });
  });

  app.post('/api/falls/simulate', async (req, res) => {
    const active = store.state.falls.find((fall) => fall.status === 'active');
    if (active) return res.status(409).json({ error: 'Já existe um alerta de queda ativo.', fall: active });
    const fall = {
      id: randomUUID(), detectedAt: new Date().toISOString(), status: 'active', source: 'Acelerómetro (simulação)',
      confidence: 0.96, location: 'Sala de estar',
      notifications: store.state.contacts.map((contact) => ({ contactId: contact.id, name: contact.name, channel: 'SMS simulado', status: 'sent' }))
    };
    store.state.falls.unshift(fall);
    await store.save();
    res.status(201).json(fall);
  });

  app.post('/api/falls/:id/resolve', async (req, res) => {
    const fall = store.state.falls.find((item) => item.id === req.params.id);
    if (!fall) return res.status(404).json({ error: 'Alerta não encontrado.' });
    if (fall.status !== 'active') return res.status(409).json({ error: 'Este alerta já foi encerrado.' });
    const outcome = req.body.outcome;
    if (!['confirmed', 'false_alarm'].includes(outcome)) return res.status(400).json({ error: 'Indique se foi queda confirmada ou falso alarme.' });
    fall.status = outcome;
    fall.resolvedAt = new Date().toISOString();
    await store.save();
    res.json(fall);
  });

  app.post('/api/reset', async (_req, res) => res.json(await store.reset()));
  app.use((error, _req, res, _next) => {
    console.error(error);
    res.status(500).json({ error: 'Ocorreu um erro interno. Tente novamente.' });
  });
  return app;
}

const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/').split('/').pop());
if (isMain) {
  const store = await new Store().init();
  const port = Number(process.env.API_PORT || 3001);
  createApp(store).listen(port, '127.0.0.1', () => console.log(`Cuida+ API: http://127.0.0.1:${port}`));
}
