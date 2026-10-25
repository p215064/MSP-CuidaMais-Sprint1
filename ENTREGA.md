# Entrega — Sprint 1 | Cuida+

## Conteúdo

- `MSP_Sprint1_CuidaMais.pdf`: relatório de 27 páginas com modelos, decisões, planeamento e capturas.
- `prototype/`: front-end React/TypeScript e back-end Express, com dados fictícios e testes.
- `models/bpmn/`: fonte BPMN 2.0 com processo principal e 12 subprocessos.
- `models/sysml/`: fonte SysML v2 com 12 requisitos funcionais e 4 não funcionais.
- `images/`: Gantt, burndown, diagramas e capturas.
- `scripts/`: geração reproduzível dos diagramas e do relatório.

## Executar o protótipo

Na pasta `prototype`, com Node.js 20 ou superior:

```bash
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

Abrir `http://localhost:3000`. O front-end e a API são iniciados pelo mesmo comando.

Validações já executadas com sucesso: 5 testes da API, ESLint, compilação TypeScript/Vite, quatro fluxos no navegador e captura móvel. As dependências de produção apresentam 0 vulnerabilidades conhecidas na auditoria npm final.

## Antes de submeter no Moodle

1. Substituir “Membro 1” a “Membro 4” pelos nomes e números dos elementos da equipa no relatório.
2. Publicar todo o conteúdo desta pasta num repositório GitHub e partilhar o acesso com o docente.
3. Inserir o URL do repositório no campo assinalado na capa e na última página do PDF. Para regenerar depois de alterar `repository.txt`, executar `python scripts/generate_report.py` num ambiente Python com ReportLab e Pillow.
4. Confirmar que o repositório contém as pastas `images`, `models` e `prototype`, e submeter o PDF juntamente com o URL.

Não foi possível publicar o repositório nem preencher a identificação da equipa automaticamente porque esses dados/acessos não foram fornecidos. Todo o restante conteúdo está pronto.
