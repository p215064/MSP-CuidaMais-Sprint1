import { useEffect, useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import {
  Activity, BellRing, Check, ChevronRight, HeartPulse, Home, Phone,
  Plus, ShieldCheck, Trash2, UserRound, UsersRound, Watch, X
} from 'lucide-react';

type Elder = { name: string; birthDate: string; phone: string; address: string; conditions: string; notes: string };
type Contact = { id: string; name: string; relationship: string; phone: string; email: string; priority: number };
type Reading = { id: string; systolic: number; diastolic: number; pulse: number; measuredAt: string };
type Fall = { id: string; detectedAt: string; status: 'active' | 'confirmed' | 'false_alarm'; source: string; confidence: number; location: string; notifications: { name: string; channel: string; status: string }[] };
type State = { elder: Elder; contacts: Contact[]; readings: Reading[]; falls: Fall[] };
type View = 'inicio' | 'perfil' | 'contactos' | 'tensao' | 'alertas';

const emptyElder: Elder = { name: '', birthDate: '', phone: '', address: '', conditions: '', notes: '' };
const nav = [
  { id: 'inicio' as View, label: 'Visão geral', icon: Home },
  { id: 'perfil' as View, label: 'Perfil do idoso', icon: UserRound },
  { id: 'contactos' as View, label: 'Contactos familiares', icon: UsersRound },
  { id: 'tensao' as View, label: 'Tensão arterial', icon: HeartPulse },
  { id: 'alertas' as View, label: 'Deteção de quedas', icon: BellRing },
];

async function request(url: string, options?: RequestInit) {
  const response = await fetch(url, { ...options, headers: { 'Content-Type': 'application/json', ...options?.headers } });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.error || 'Não foi possível concluir o pedido.');
  }
  return response.status === 204 ? null : response.json();
}

function classify(reading?: Reading) {
  if (!reading) return { label: 'Sem registos', tone: 'neutral' };
  if (reading.systolic >= 180 || reading.diastolic >= 120) return { label: 'Crise hipertensiva', tone: 'danger' };
  if (reading.systolic >= 140 || reading.diastolic >= 90) return { label: 'Tensão elevada', tone: 'warning' };
  if (reading.systolic < 90 || reading.diastolic < 60) return { label: 'Tensão baixa', tone: 'info' };
  return { label: 'Dentro dos valores de referência', tone: 'success' };
}

const formatDate = (value: string, withTime = false) => new Intl.DateTimeFormat('pt-PT', { day: '2-digit', month: 'short', year: 'numeric', ...(withTime ? { hour: '2-digit', minute: '2-digit' } : {}) }).format(new Date(value));

export default function App() {
  const [data, setData] = useState<State | null>(null);
  const [view, setView] = useState<View>('inicio');
  const [elderForm, setElderForm] = useState<Elder>(emptyElder);
  const [notice, setNotice] = useState<{ type: 'ok' | 'error'; text: string } | null>(null);
  const [busy, setBusy] = useState(false);

  const load = async () => {
    try {
      const state: State = await request('/api/state');
      setData(state);
      setElderForm(state.elder);
    } catch (error) {
      setNotice({ type: 'error', text: error instanceof Error ? error.message : 'Erro ao carregar.' });
    }
  };
  useEffect(() => { load(); }, []);

  const notify = (text: string, type: 'ok' | 'error' = 'ok') => {
    setNotice({ text, type });
    window.setTimeout(() => setNotice(null), 4500);
  };
  const run = async (action: () => Promise<unknown>, success: string) => {
    setBusy(true);
    try { await action(); await load(); notify(success); }
    catch (error) { notify(error instanceof Error ? error.message : 'Ocorreu um erro.', 'error'); }
    finally { setBusy(false); }
  };

  const activeFall = data?.falls.find((fall) => fall.status === 'active');
  const latest = data?.readings[0];
  const status = classify(latest);
  const average = useMemo(() => {
    if (!data?.readings.length) return { systolic: 0, diastolic: 0 };
    const recent = data.readings.slice(0, 7);
    return { systolic: Math.round(recent.reduce((sum, item) => sum + item.systolic, 0) / recent.length), diastolic: Math.round(recent.reduce((sum, item) => sum + item.diastolic, 0) / recent.length) };
  }, [data]);

  if (!data) return <main className="loading"><HeartPulse size={42} /><h1>Cuida+</h1><p>A ligar ao sistema de apoio…</p>{notice && <p className="error-text">{notice.text}</p>}</main>;

  const saveElder = (event: FormEvent) => {
    event.preventDefault();
    run(() => request('/api/elder', { method: 'PUT', body: JSON.stringify(elderForm) }), 'Perfil do idoso guardado com sucesso.');
  };
  const addContact = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const payload = Object.fromEntries(form.entries());
    run(() => request('/api/contacts', { method: 'POST', body: JSON.stringify({ ...payload, priority: Number(payload.priority) }) }), 'Contacto familiar adicionado.');
    event.currentTarget.reset();
  };
  const addReading = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    run(() => request('/api/readings', { method: 'POST', body: JSON.stringify(Object.fromEntries(form.entries())) }), 'Medição registada e classificada.');
    event.currentTarget.reset();
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button className="brand" onClick={() => setView('inicio')} aria-label="Cuida+ — início"><span className="brand-mark"><HeartPulse /></span><span>Cuida<span>+</span></span></button>
        <p className="nav-caption">ACOMPANHAMENTO</p>
        <nav aria-label="Navegação principal">
          {nav.map(({ id, label, icon: Icon }) => <button key={id} className={view === id ? 'nav-item active' : 'nav-item'} onClick={() => setView(id)}><Icon size={20} /><span>{label}</span>{id === 'alertas' && activeFall && <span className="nav-dot" />}</button>)}
        </nav>
        <div className="safety-note"><ShieldCheck size={23} /><div><strong>Ambiente seguro</strong><span>Dados guardados localmente</span></div></div>
        <div className="profile-mini"><span className="avatar">{data.elder.name.split(' ').map((part) => part[0]).slice(0, 2).join('')}</span><div><strong>{data.elder.name}</strong><span>Perfil acompanhado</span></div></div>
      </aside>

      <main className="main-content">
        <header className="topbar"><div><p className="eyebrow">DOMINGO, 25 DE OUTUBRO</p><h1>{nav.find((item) => item.id === view)?.label}</h1></div><button className="icon-button" aria-label="Notificações" onClick={() => setView('alertas')}><BellRing />{activeFall && <span />}</button></header>
        {notice && <div className={`toast ${notice.type}`} role="status">{notice.type === 'ok' ? <Check /> : <X />}<span>{notice.text}</span><button onClick={() => setNotice(null)} aria-label="Fechar"><X size={16} /></button></div>}

        {view === 'inicio' && <>
          {activeFall && <section className="emergency-banner"><span className="pulse-icon"><BellRing /></span><div><p>ALERTA ATIVO</p><h2>Possível queda detetada</h2><span>{activeFall.location} · {formatDate(activeFall.detectedAt, true)}</span></div><button onClick={() => setView('alertas')}>Responder agora <ChevronRight /></button></section>}
          <section className="welcome"><div><p className="eyebrow">RESUMO DIÁRIO</p><h2>Bom dia. Como está a {data.elder.name.split(' ')[0]}?</h2><p>Acompanhe os sinais importantes e mantenha a família por perto.</p></div><span className="welcome-art"><Activity /></span></section>
          <section className="metrics-grid">
            <button className="metric-card" onClick={() => setView('tensao')}><span className="metric-icon coral"><HeartPulse /></span><div className="metric-heading"><span>ÚLTIMA TENSÃO ARTERIAL</span><ChevronRight /></div><strong>{latest ? `${latest.systolic}/${latest.diastolic}` : '—'} <small>mmHg</small></strong><span className={`status-pill ${status.tone}`}>{status.label}</span></button>
            <button className="metric-card" onClick={() => setView('contactos')}><span className="metric-icon teal"><UsersRound /></span><div className="metric-heading"><span>REDE FAMILIAR</span><ChevronRight /></div><strong>{data.contacts.length} <small>contactos ativos</small></strong><span className="muted-line">{data.contacts[0] ? `${data.contacts[0].name} é o contacto prioritário` : 'Adicione o primeiro contacto'}</span></button>
            <button className="metric-card" onClick={() => setView('alertas')}><span className="metric-icon blue"><Watch /></span><div className="metric-heading"><span>SENSOR DE QUEDAS</span><ChevronRight /></div><strong>{activeFall ? 'Alerta' : 'Ativo'} <small>{activeFall ? 'por resolver' : 'e a monitorizar'}</small></strong><span className={`status-pill ${activeFall ? 'danger' : 'success'}`}>{activeFall ? 'Requer atenção' : 'Sem incidentes pendentes'}</span></button>
          </section>
          <section className="quick-section"><div className="section-heading"><div><p className="eyebrow">AÇÕES FREQUENTES</p><h2>O que precisa de fazer?</h2></div></div><div className="quick-grid"><button onClick={() => setView('tensao')}><Plus /><span><strong>Registar tensão</strong><small>Nova medição manual</small></span></button><button onClick={() => setView('contactos')}><Plus /><span><strong>Adicionar familiar</strong><small>Reforçar a rede de apoio</small></span></button><button onClick={() => setView('perfil')}><UserRound /><span><strong>Atualizar perfil</strong><small>Dados e notas de saúde</small></span></button></div></section>
          <p className="disclaimer">O Cuida+ apoia o acompanhamento, mas não substitui aconselhamento médico. Em emergência, ligue 112.</p>
        </>}

        {view === 'perfil' && <section className="panel"><div className="panel-title"><div><h2>Dados do idoso</h2><p>Informação essencial para um acompanhamento personalizado.</p></div><span className="large-icon"><UserRound /></span></div><form className="form-grid" onSubmit={saveElder}><label>Nome completo<input required value={elderForm.name} onChange={(e) => setElderForm({ ...elderForm, name: e.target.value })} /></label><label>Data de nascimento<input required type="date" value={elderForm.birthDate} onChange={(e) => setElderForm({ ...elderForm, birthDate: e.target.value })} /></label><label>Telefone<input required value={elderForm.phone} onChange={(e) => setElderForm({ ...elderForm, phone: e.target.value })} /></label><label>Morada<input required value={elderForm.address} onChange={(e) => setElderForm({ ...elderForm, address: e.target.value })} /></label><label className="full">Condições de saúde relevantes<input value={elderForm.conditions} onChange={(e) => setElderForm({ ...elderForm, conditions: e.target.value })} placeholder="Ex.: hipertensão, diabetes" /></label><label className="full">Notas de acompanhamento<textarea rows={4} value={elderForm.notes} onChange={(e) => setElderForm({ ...elderForm, notes: e.target.value })} /></label><div className="form-actions full"><button className="primary-button" disabled={busy} type="submit"><Check />Guardar perfil</button></div></form></section>}

        {view === 'contactos' && <div className="two-column"><section className="panel"><div className="panel-title"><div><h2>Rede de apoio</h2><p>Os contactos são notificados por ordem de prioridade.</p></div></div><div className="contact-list">{data.contacts.map((contact) => <article className="contact-row" key={contact.id}><span className="avatar soft">{contact.name.split(' ').map((part) => part[0]).slice(0, 2).join('')}</span><div><strong>{contact.name}</strong><span>{contact.relationship} · Prioridade {contact.priority}</span><small><Phone size={13} />{contact.phone}</small></div><button className="delete-button" aria-label={`Remover ${contact.name}`} onClick={() => run(() => request(`/api/contacts/${contact.id}`, { method: 'DELETE' }), 'Contacto removido.')}><Trash2 /></button></article>)}{!data.contacts.length && <p className="empty">Ainda não existem contactos familiares.</p>}</div></section><section className="panel"><div className="panel-title"><div><h2>Novo contacto</h2><p>Adicione uma pessoa de confiança.</p></div></div><form className="stack-form" onSubmit={addContact}><label>Nome completo<input name="name" required placeholder="Nome do familiar" /></label><label>Parentesco<input name="relationship" required placeholder="Ex.: filha, vizinho" /></label><label>Telefone<input name="phone" required placeholder="912 345 678" /></label><label>Email (opcional)<input name="email" type="email" placeholder="nome@email.pt" /></label><label>Prioridade<select name="priority" defaultValue="1"><option value="1">1 — Contactar primeiro</option><option value="2">2 — Contactar em segundo</option><option value="3">3 — Contactar em terceiro</option></select></label><button className="primary-button" disabled={busy}><Plus />Adicionar contacto</button></form></section></div>}

        {view === 'tensao' && <><section className="health-summary"><div><p className="eyebrow">MÉDIA DAS ÚLTIMAS MEDIÇÕES</p><strong>{average.systolic}<span>/</span>{average.diastolic}</strong><small>mmHg · sistólica / diastólica</small></div><div className={`health-status ${status.tone}`}><Activity /><span><small>ESTADO DA ÚLTIMA MEDIÇÃO</small><strong>{status.label}</strong></span></div></section><div className="two-column"><section className="panel"><div className="panel-title"><div><h2>Nova medição</h2><p>Registe os valores indicados pelo tensiómetro.</p></div></div><form className="stack-form" onSubmit={addReading}><div className="pressure-inputs"><label>Sistólica<input name="systolic" required type="number" min="50" max="260" placeholder="120" /><small>mmHg</small></label><label>Diastólica<input name="diastolic" required type="number" min="30" max="180" placeholder="80" /><small>mmHg</small></label></div><label>Pulso<input name="pulse" required type="number" min="30" max="220" placeholder="70" /><small>batimentos por minuto</small></label><button className="primary-button" disabled={busy}><Plus />Registar medição</button></form></section><section className="panel"><div className="panel-title"><div><h2>Histórico recente</h2><p>As classificações são apenas indicativas.</p></div></div><div className="reading-list">{data.readings.slice(0, 6).map((reading) => { const s = classify(reading); return <article key={reading.id}><span className={`reading-marker ${s.tone}`} /><div><strong>{reading.systolic}/{reading.diastolic} <small>mmHg</small></strong><span>{formatDate(reading.measuredAt, true)} · Pulso {reading.pulse} bpm</span></div><span className={`status-pill ${s.tone}`}>{s.label}</span></article>; })}</div></section></div></>}

        {view === 'alertas' && <><section className={activeFall ? 'fall-hero active' : 'fall-hero'}><span className="fall-symbol"><Watch /></span><div><p className="eyebrow">SENSOR WEARABLE</p><h2>{activeFall ? 'Possível queda detetada' : 'Monitorização ativa'}</h2><p>{activeFall ? `${activeFall.location} · confiança de ${Math.round(activeFall.confidence * 100)}% · ${formatDate(activeFall.detectedAt, true)}` : 'O acelerómetro está pronto para identificar movimentos súbitos e ausência de movimento.'}</p></div><span className={`status-pill ${activeFall ? 'danger' : 'success'}`}>{activeFall ? 'Ação necessária' : 'Proteção ativa'}</span></section>{activeFall ? <section className="panel alert-response"><h2>Está tudo bem?</h2><p>Foram enviadas notificações simuladas a {activeFall.notifications.length} contacto(s): {activeFall.notifications.map((item) => item.name).join(', ')}.</p><div className="response-buttons"><button className="secondary-button" disabled={busy} onClick={() => run(() => request(`/api/falls/${activeFall.id}/resolve`, { method: 'POST', body: JSON.stringify({ outcome: 'false_alarm' }) }), 'Alerta encerrado como falso alarme.')}><Check />Foi falso alarme</button><button className="danger-button" disabled={busy} onClick={() => run(() => request(`/api/falls/${activeFall.id}/resolve`, { method: 'POST', body: JSON.stringify({ outcome: 'confirmed' }) }), 'Queda confirmada. O incidente ficou registado.')}><BellRing />Confirmar queda</button></div></section> : <section className="panel simulation"><div><h2>Testar o fluxo de deteção</h2><p>A simulação cria um evento real no back-end e notifica os contactos por ordem de prioridade. Não são enviadas mensagens externas.</p></div><button className="danger-button" disabled={busy} onClick={() => run(() => request('/api/falls/simulate', { method: 'POST', body: '{}' }), 'Possível queda detetada. Contactos notificados (simulação).')}><Activity />Simular queda</button></section>}<section className="panel"><div className="panel-title"><div><h2>Histórico de incidentes</h2><p>Registos de eventos e respetiva resolução.</p></div></div>{data.falls.length ? <div className="incident-list">{data.falls.map((fall) => <article key={fall.id}><BellRing /><div><strong>{fall.status === 'active' ? 'Alerta ativo' : fall.status === 'confirmed' ? 'Queda confirmada' : 'Falso alarme'}</strong><span>{fall.location} · {formatDate(fall.detectedAt, true)}</span></div><span className={`status-pill ${fall.status === 'active' ? 'danger' : 'neutral'}`}>{fall.status === 'active' ? 'Pendente' : 'Resolvido'}</span></article>)}</div> : <p className="empty">Sem incidentes registados. O sistema encontra-se operacional.</p>}</section></>}
      </main>
    </div>
  );
}
