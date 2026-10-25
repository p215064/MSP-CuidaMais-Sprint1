# Entrega: Sprint 1 | Cuida+

## Conteúdo

- `MSP_Sprint1_CuidaMais.pdf`: relatório de 27 páginas com modelos, decisões, planeamento e capturas.
- `prototype/`: interface React/TypeScript e servidor Express, com dados fictícios e testes.
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

Abrir `http://localhost:3000`. A interface e a API são iniciadas pelo mesmo comando.

Validações já executadas com sucesso: 5 testes da API, ESLint, compilação TypeScript/Vite, quatro fluxos no navegador e captura móvel. As dependências de produção apresentam 0 vulnerabilidades conhecidas na auditoria npm final.

## Antes de submeter no Moodle

1. Identificação preenchida: Rodrigo Alexandre Vitória Mira, número 79432.
2. Repositório GitHub: https://github.com/p215064/MSP-CuidaMais-Sprint1
3. O URL está inserido na capa e na última página do PDF. Para regenerar depois de alterar `repository.txt`, executar `python scripts/generate_report.py` num ambiente Python com ReportLab e Pillow.
4. Confirmar que o repositório público contém as pastas `images`, `models` e `prototype`, e submeter o PDF juntamente com o URL no Moodle.

O trabalho está identificado como **individual**: o autor acumula os papéis de Scrum Master, Quality Controller e Team Member, sem membros fictícios nem rotação entre pessoas. A identificação e o URL do repositório estão preenchidos.
