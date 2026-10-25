# Cuida+ — Protótipo do Sprint 1

Protótipo full-stack das quatro funcionalidades básicas: registo/edição do perfil do idoso, gestão de contactos familiares, deteção simulada de quedas com notificação simulada e monitorização da tensão arterial.

## Executar

Requisitos: Node.js 20 ou superior.

```bash
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

Abrir `http://localhost:3000`. A API é iniciada simultaneamente em `http://127.0.0.1:3001`; o Vite encaminha `/api` para o back-end. Os dados ficam em `server/data/db.json`.

## Testar e compilar

```bash
npm test
npm run lint
npm run build
```

Os testes cobrem as quatro funcionalidades básicas, validações, classificação da tensão e resolução de alertas. Para repor os dados de demonstração, enviar `POST /api/reset`.

## API

- `GET /api/state` — estado completo do protótipo.
- `PUT /api/elder` — criar/atualizar o perfil do idoso.
- `POST /api/contacts` e `DELETE /api/contacts/:id` — gerir contactos.
- `POST /api/readings` — registar e classificar uma medição.
- `POST /api/falls/simulate` — simular a deteção de uma queda.
- `POST /api/falls/:id/resolve` — confirmar queda ou assinalar falso alarme.

## Decisões e limites

React, TypeScript e Vite no front-end; Express e persistência JSON atómica no back-end. A deteção de queda e as notificações são simulações deliberadas: não existe ligação a wearable, SMS ou email neste sprint. A classificação da tensão é indicativa e não constitui diagnóstico. Em emergência, contactar o 112.
