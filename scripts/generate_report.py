from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from PIL import Image as PILImage

ROOT=Path(__file__).resolve().parents[1]
IMG=ROOT/'images'
OUT=ROOT/'MSP_Sprint1_CuidaMais.pdf'
REPO=(ROOT/'repository.txt').read_text(encoding='utf-8').strip() if (ROOT/'repository.txt').exists() else 'A PREENCHER — publicar a pasta no GitHub e inserir aqui o URL'
NAVY=HexColor('#193b3b');TEAL=HexColor('#147d72');GREY=HexColor('#657b78');LIGHT=HexColor('#edf5f2');RED=HexColor('#a94743')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle',fontName='Helvetica-Bold',fontSize=29,leading=35,textColor=NAVY,alignment=TA_CENTER,spaceAfter=16))
styles.add(ParagraphStyle(name='CoverSub',fontName='Helvetica',fontSize=13,leading=19,textColor=GREY,alignment=TA_CENTER))
styles.add(ParagraphStyle(name='H1x',fontName='Helvetica-Bold',fontSize=19,leading=24,textColor=NAVY,spaceBefore=4,spaceAfter=13,keepWithNext=True))
styles.add(ParagraphStyle(name='H2x',fontName='Helvetica-Bold',fontSize=13,leading=17,textColor=TEAL,spaceBefore=12,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='Bodyx',fontName='Helvetica',fontSize=9.5,leading=14.5,textColor=HexColor('#314947'),spaceAfter=8))
styles.add(ParagraphStyle(name='Smallx',fontName='Helvetica',fontSize=8,leading=11,textColor=GREY,spaceAfter=5))
styles.add(ParagraphStyle(name='Captionx',fontName='Helvetica-Oblique',fontSize=8,leading=11,textColor=GREY,alignment=TA_CENTER,spaceBefore=5,spaceAfter=9))
styles.add(ParagraphStyle(name='Cellx',fontName='Helvetica',fontSize=7.6,leading=10,textColor=HexColor('#314947')))
styles.add(ParagraphStyle(name='CellBold',fontName='Helvetica-Bold',fontSize=7.6,leading=10,textColor=NAVY))
styles.add(ParagraphStyle(name='Callout',fontName='Helvetica',fontSize=9,leading=14,textColor=NAVY,backColor=LIGHT,borderColor=HexColor('#c7dfd8'),borderWidth=.7,borderPadding=10,spaceBefore=7,spaceAfter=10))

story=[]
def p(text,style='Bodyx'):story.append(Paragraph(text,styles[style]))
def h1(text):story.append(Paragraph(text,styles['H1x']))
def h2(text):story.append(Paragraph(text,styles['H2x']))
def page():story.append(PageBreak())
def cell(value,bold=False):return Paragraph(str(value),styles['CellBold' if bold else 'Cellx'])
def table(headers,rows,widths,font=7.6):
    data=[[cell(x,True) for x in headers]]+[[cell(x) for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('LINEABOVE',(0,0),(-1,0),1.2,NAVY),('LINEBELOW',(0,0),(-1,0),.7,NAVY),('LINEBELOW',(0,-1),(-1,-1),1.1,NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,HexColor('#f7faf9')])]))
    story.append(t);story.append(Spacer(1,8))
def image(name,width=16.5*cm,maxheight=21*cm,caption=None):
    path=IMG/name
    with PILImage.open(path) as im:w,h=im.size
    height=width*h/w
    if height>maxheight:height=maxheight;width=height*w/h
    story.append(Image(str(path),width=width,height=height,hAlign='CENTER'))
    if caption:p(caption,'Captionx')

def header_footer(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(HexColor('#d8e4e0'));canvas.setLineWidth(.5);canvas.line(2.2*cm,h-1.45*cm,w-2.2*cm,h-1.45*cm)
    canvas.setFont('Helvetica',7.5);canvas.setFillColor(GREY);canvas.drawString(2.2*cm,h-1.2*cm,'Cuida+  |  MSP — Sprint 1')
    canvas.drawRightString(w-2.2*cm,1.15*cm,f'Página {doc.page}');canvas.restoreState()

def cover(canvas,doc):
    canvas.saveState();w,h=A4;canvas.setFillColor(NAVY);canvas.rect(0,h-1.2*cm,w,1.2*cm,fill=1,stroke=0);canvas.setFillColor(TEAL);canvas.rect(0,0,w,.5*cm,fill=1,stroke=0);canvas.restoreState()

# Cover
story.append(Spacer(1,3.2*cm));p('Cuida+','CoverTitle');p('Sistema ciber-físico de apoio a idosos','CoverSub');story.append(Spacer(1,1.1*cm));p('TRABALHO PRÁTICO — PRIMEIRO SPRINT','H2x');story[-1].alignment=TA_CENTER
p('Modelação BPMN, requisitos SysML, planeamento e protótipo full-stack','CoverSub');story.append(Spacer(1,1.4*cm))
table(['Elemento','Informação'],[['Unidade curricular','MSP — Modelação e Simulação de Processos'],['Modalidade','Trabalho individual'],['Autor','Rodrigo Alexandre Vitória Mira — 79432'],['Período do Sprint 1','22 a 25 de outubro de 2026'],['Data de preparação','25 de outubro de 2026'],['Repositório GitHub',REPO]],[4.2*cm,11.8*cm])
p('<b>Nota de entrega:</b> submeter este relatório em PDF e o URL público do repositório GitHub. O código, os modelos, as imagens e este relatório encontram-se na estrutura de pastas entregue.','Callout')
page()

h1('1. Enquadramento e âmbito')
p('O Cuida+ é concebido como um sistema ciber-físico que articula sensores, atuadores, serviços computacionais e pessoas para apoiar a autonomia e a segurança de idosos em casa e em instituições de cuidados. O Sprint 1 estabelece o catálogo de capacidades, os processos, os requisitos e uma prova de conceito das quatro funcionalidades básicas.')
p('Foram utilizados <b>BPMN 2.0</b> para o processo principal e os 12 subprocessos, <b>SysML Requirements Diagrams</b> para requisitos funcionais e não funcionais, <b>diagrama de Gantt</b> e <b>burndown chart</b> para o planeamento, e <b>React + TypeScript + Express</b> para o protótipo. Os ficheiros-fonte editáveis acompanham as imagens.')
h2('Decisões de âmbito')
for text in ['O protótipo implementa apenas F01–F04, conforme o enunciado; F05–F12 são modeladas, mas não implementadas neste sprint.','A deteção de queda é acionada por uma simulação de acelerómetro. As notificações familiares são registadas como SMS simulado; não são enviadas mensagens reais.','As integrações F11 e F12 são propostas de comunicação com sistemas externos. Não se invocam serviços reais sem credenciais, contratos de interface ou autorização.','A classificação da tensão arterial é indicativa e não constitui diagnóstico. A interface recomenda contactar o 112 em emergência.']:
    p('• '+text)
h2('Estrutura da entrega')
table(['Pasta / ficheiro','Conteúdo'],[['prototype/','Front-end, back-end, dados de demonstração, testes e instruções.'],['models/bpmn/','Processo BPMN 2.0 com 12 subprocessos em XML.'],['models/sysml/','Fonte textual SysML v2 dos requisitos.'],['images/','Gantt, burndown, modelos e capturas do protótipo.'],['MSP_Sprint1_CuidaMais.pdf','Relatório consolidado com modelos, comentários e decisões.']],[4.3*cm,11.7*cm])
page()

h1('2. Organização individual e qualidade')
p('Embora o enunciado preveja equipas de quatro elementos, este trabalho é realizado <b>individualmente</b>. O mesmo autor acumula os papéis de Scrum Master, Quality Controller e Team Member, cobrindo planeamento, modelação, desenvolvimento, testes e documentação. Não se criam membros fictícios nem uma rotação entre pessoas.')
table(['Responsável','Papéis no Sprint 1','Responsabilidades'],[['Autor','Scrum Master','Planeamento, dependências, Gantt, burndown e gestão do âmbito.'],['Autor','Quality Controller','Rastreabilidade, revisão BPMN/SysML, verificação e checklist de entrega.'],['Autor','Team Member','Back-end, front-end, persistência, testes e capturas.']],[2.5*cm,4.1*cm,9.4*cm])
h2('Adaptação dos papéis ao trabalho individual')
p('A rotação semanal do Scrum Master não é aplicável a uma equipa de uma pessoa: o autor mantém esse papel durante todo o trabalho. O princípio de qualidade “one for all, all for one” é operacionalizado através de autorrevisão estruturada, testes objetivos e inspeção visual dos modelos e do relatório.')
h2('Definição de pronto')
p('Uma tarefa só é considerada concluída quando o resultado está guardado no repositório, revisto pelo autor com base num checklist, sem erros conhecidos bloqueantes e acompanhado pela evidência aplicável: modelo exportado, teste automatizado, captura ou secção do relatório.')
page()

h1('3. Planeamento do Sprint 1')
p('A unidade de estimativa é a hora de <b>trabalho individual</b>. O sprint contém 32 horas planeadas. Todas as tarefas são atribuídas ao autor; as dependências indicam os artefactos necessários antes do início de cada tarefa.')
tasks=[('T01','Definir papéis e âmbito','—','Autor','2','Concluída'),('T02','Identificar 12 funcionalidades','T01','Autor','3','Concluída'),('T03','Modelar BPMN principal e 12 subprocessos','T02','Autor','5','Concluída'),('T04','Elicitar requisitos funcionais SysML','T02','Autor','4','Concluída'),('T05','Analisar 4 RNFs e relações','T04','Autor','2','Concluída'),('T06','Preparar planeamento e Gantt','T01','Autor','2','Concluída'),('T07','Implementar back-end básico','T02, T04','Autor','5','Concluída'),('T08','Implementar front-end básico','T04, T07','Autor','5','Concluída'),('T09','Executar testes e capturas','T07, T08','Autor','2','Concluída'),('T10','Fechar burndown, relatório e entrega','T03, T05, T06, T09','Autor','2','Concluída')]
table(['ID','Tarefa','Dependências','Resp.','h','Estado'],tasks,[1*cm,6.1*cm,2.6*cm,1.8*cm,.7*cm,2.3*cm])
h2('Gantt e burndown')
image('gantt-sprint-1.png',width=16.7*cm,maxheight=10.2*cm,caption='Figura 1 — Calendarização das tarefas individuais do Sprint 1.')
page()
h1('3. Planeamento do Sprint 1 — acompanhamento')
image('burndown-sprint-1.png',width=16.2*cm,maxheight=11.2*cm,caption='Figura 2 — Burndown individual ideal e registado no encerramento do sprint.')
table(['Marco','Ideal restante','Real restante','Comentário'],[['Início','32 h','32 h','Âmbito estimado e dependências identificadas.'],['22 outubro','24 h','26 h','Arranque mais lento; sem alteração de âmbito.'],['23 outubro','16 h','17 h','Modelação e back-end permitiram recuperar trabalho.'],['24 outubro','8 h','7 h','Front-end integrado; início dos testes.'],['25 outubro','0 h','0 h','Quatro funcionalidades básicas verificadas e relatório consolidado.']],[3*cm,2.6*cm,2.6*cm,7.8*cm])
p('O burndown mede trabalho individual restante, não qualidade. A conclusão só foi aceite depois dos testes da API, da compilação, da análise estática e da validação dos fluxos no navegador.','Callout')
page()

h1('4. Catálogo das 12 funcionalidades')
features=[('F01','Registar conta do idoso','Básica','Dados pessoais, contacto, morada e notas clínicas.'),('F02','Adicionar contactos familiares','Básica','Familiares e prioridade de notificação.'),('F03','Detetar queda','Básica','Evento de acelerómetro, alerta e resposta.'),('F04','Monitorizar tensão arterial','Básica','Medição, classificação indicativa e histórico.'),('F05','Gerir medicação','Sistema existente','Dispensador, horários, dose e omissão.'),('F06','Prevenir acidentes domésticos','Sistema existente','Gás/fumo e corte seguro de energia.'),('F07','Controlar iluminação e temperatura','Sistema existente','Presença, horário, iluminação e clima.'),('F08','Monitorizar sinais vitais','Sistema existente','Wearable, anomalias e painel clínico.'),('F09','Prevenir úlceras de pressão','Sistema existente','Colchão sensorizado e atuadores.'),('F10','Vigiar deambulação','Sistema existente','BLE/UWB, perímetro, porta e equipa.'),('F11','Integrar serviço de emergência','Nova — sistema externo','Envio de contexto e referência de atendimento.'),('F12','Integrar farmácia e dispensador','Nova — dispositivo + serviço','Stock local e reposição pela farmácia.')]
table(['ID','Funcionalidade','Origem','Decisão de conteúdo'],features,[1.1*cm,4.8*cm,3.3*cm,6.8*cm])
h2('Justificação das propostas novas')
p('<b>F11:</b> complementa os alertas familiares com comunicação a um serviço de emergência. A referência externa permite reconciliar o estado do incidente. O consentimento, a minimização dos dados e a operação em caso de indisponibilidade são requisitos derivados.')
p('<b>F12:</b> fecha o ciclo entre gestão de medicação, stock físico e reposição. O dispensador comunica o stock; a farmácia recebe um pedido, devolve o estado e evita que a automação termine na simples contagem de doses.')
p('As funcionalidades F01–F04 constituem o incremento executável deste sprint. As restantes oito são requisitos e processos candidatos, não funcionalidades já desenvolvidas.','Callout')
page()

h1('5. Modelação BPMN')
p('O processo principal representa as capacidades como ramos independentes desencadeados por eventos. O gateway paralelo é usado como vista de composição do catálogo, não como obrigação de executar todas as funcionalidades em simultâneo. Cada atividade com o marcador “+” é um subprocesso com início, tarefas, decisão quando aplicável e fim.')
image('bpmn-processo-principal.png',width=15.8*cm,maxheight=21.8*cm,caption='Figura 3 — Processo principal BPMN com os 12 subprocessos.')
page()
subprocess_comments={
'F01':'Validação antes da persistência; data de nascimento passada e campos obrigatórios.',
'F02':'Contacto validado e ordenação por prioridade; remoção disponível no protótipo.',
'F03':'Ramo negativo mantém monitorização; ramo positivo cria alerta e notificações simuladas.',
'F04':'Medição validada, classificada e adicionada ao histórico persistente.',
'F05':'A omissão desencadeia aviso local e remoto; fora do protótipo.',
'F06':'Sensores e atuadores formam o fecho ciber-físico de segurança.',
'F07':'Ajuste ambiental adaptativo sem intervenção manual do idoso.',
'F08':'Deteção de anomalia e atualização do painel para a equipa clínica.',
'F09':'A decisão usa pressão e duração da imobilidade antes de acionar o colchão.',
'F10':'A violação do perímetro origina alerta e comando físico da porta.',
'F11':'A resposta externa é correlacionada por uma referência de atendimento.',
'F12':'Stock insuficiente origina pedido à farmácia; a confirmação fecha o ciclo.'}
for idx,(fid,name,*_) in enumerate(features):
    if idx%2==0:
        h1(f'5.{idx+1}–5.{min(idx+2,12)} Subprocessos BPMN' if idx<11 else '5.12 Subprocesso BPMN')
    image(f'bpmn-{fid.lower()}.png',width=16.5*cm,maxheight=7.3*cm,caption=f'Figura {4+idx} — {fid}: {name}.')
    p(f'<b>Comentário:</b> {subprocess_comments[fid]}','Smallx')
    if idx%2==1 and idx<11:page()
page()

h1('6. Elicitação de requisitos')
p('A elicitação partiu dos cenários do enunciado e foi estruturada por stakeholder, evento, resposta observável e evidência de verificação. Os stakeholders considerados são o idoso, a família, o cuidador, a equipa clínica, os serviços de emergência, a farmácia e o administrador do sistema.')
h2('Requisitos funcionais e critérios de aceitação')
reqs=[('RF01','Registar/atualizar a conta com dados válidos.','Guardar perfil completo; rejeitar nome vazio, telefone inválido ou data futura.'),('RF02','Adicionar familiares e prioridade de notificação.','Criar contacto válido; listar por prioridade; remover por identificador.'),('RF03','Detetar queda provável, alertar e notificar por prioridade.','Simulação cria um único alerta ativo; contactos registados; resolução obrigatória.'),('RF04','Registar tensão e pulso, classificar e conservar histórico.','Valores dentro dos limites; classificação coerente; leitura visível no histórico.'),('RF05','Controlar horários, doses e omissões.','No horário liberta dose configurada; ausência de recolha gera alerta.'),('RF06','Detetar risco e comandar corte seguro.','Evento de gás/fumo aciona atuador e notifica cuidador.'),('RF07','Ajustar luz e temperatura ao contexto.','Presença noturna ajusta iluminação; temperatura fora da faixa ajusta clima.'),('RF08','Receber sinais vitais e sinalizar anomalias.','Leitura wearable atualiza painel; anomalia gera evento clínico.'),('RF09','Analisar pressão e acionar redistribuição.','Imobilidade excessiva altera zonas de pressão e regista ação.'),('RF10','Detetar saída do perímetro e alertar equipa.','Localização fora da zona segura gera alerta e comando previsto.'),('RF11','Comunicar emergência e guardar referência externa.','Pedido autenticado contém contexto mínimo; resposta é reconciliada.'),('RF12','Consultar stock e solicitar reposição.','Stock abaixo do limiar gera pedido e acompanha estado da farmácia.')]
table(['ID','Requisito','Critério de aceitação / verificação'],reqs,[1.2*cm,6.4*cm,8.4*cm])
h2('Decisões de elicitação')
p('Os requisitos são redigidos sem prescrever fornecedores. A prioridade de contactos evita alertas indiferenciados. A resolução de uma queda exige “queda confirmada” ou “falso alarme”, assegurando rastreabilidade. Limites explícitos de entrada impedem que valores impossíveis contaminem o histórico.')
page()
h1('6.1 SysML — requisitos das funcionalidades básicas')
image('sysml-requisitos-basicas.png',width=16.2*cm,maxheight=21*cm,caption='Figura 16 — Relações «refine» entre F01–F04 e RF01–RF04.')
page()
h1('6.2 SysML — requisitos das funcionalidades existentes')
image('sysml-requisitos-existentes.png',width=15.8*cm,maxheight=22*cm,caption='Figura 17 — Relações «refine» entre F05–F10 e RF05–RF10.')
page()
h1('6.3 SysML — requisitos das funcionalidades novas')
image('sysml-requisitos-novas.png',width=16.2*cm,maxheight=15*cm,caption='Figura 18 — Relações «refine» das duas integrações externas.')
h2('Rastreabilidade')
p('A correspondência é direta e verificável: F01↔RF01, …, F12↔RF12. Os identificadores permanecem estáveis nos modelos, no relatório e nos testes. O back-end expõe operações específicas para RF01–RF04, permitindo rastrear a implementação do incremento básico.')
page()

h1('7. Requisitos não funcionais, contribuições e conflitos')
nfr=[('RNF01','Segurança e privacidade','Cifragem em trânsito e em repouso; autenticação; consentimento; minimização.','Revisão de segurança e testes de autorização.'),('RNF02','Disponibilidade e recuperação','Alertas locais com disponibilidade alvo de 99,5%; recuperação automática.','Ensaio de falha e indisponibilidade mensurada.'),('RNF03','Usabilidade e acessibilidade','Responsividade, contraste, foco visível, linguagem clara e controlos amplos.','Teste com utilizadores e auditoria de acessibilidade.'),('RNF04','Desempenho em tempo real','Alerta local ≤ 2 s no p95; registo de medição ≤ 1 s.','Teste de carga com latência por percentil.')]
table(['ID','Categoria','Meta / restrição','Verificação prevista'],nfr,[1.2*cm,3.4*cm,7.1*cm,4.3*cm])
image('sysml-requisitos-nao-funcionais.png',width=16.3*cm,maxheight=10.8*cm,caption='Figura 19 — Relações «contribute» e «conflict» entre os quatro RNFs.')
p('<b>Conflitos:</b> RNF01 pode aumentar a latência exigida por RNF04 e introduzir passos que afetam RNF03. A decisão é não remover segurança para cumprir desempenho: devem otimizar-se implementação, cache segura e fluxos de emergência.')
p('<b>Contribuições:</b> RNF04 apoia RNF02 ao reduzir bloqueios e favorecer recuperação oportuna; RNF02 contribui para RNF03 porque um serviço disponível melhora a experiência. As metas de disponibilidade e desempenho são objetivos do sistema, não resultados certificados por este protótipo local.')
page()

h1('8. Protótipo — decisões técnicas')
table(['Aspeto','Decisão','Justificação'],[['Front-end','React, TypeScript, Vite e CSS responsivo','Componentes interativos, verificação de tipos e adaptação móvel.'],['Back-end','Node.js e Express 5','API REST explícita, validação no servidor e testes simples.'],['Persistência','Ficheiro JSON com escrita atómica','Suficiente para prova de conceito, sem dependência de base de dados externa.'],['Integração','Proxy Vite /api → 127.0.0.1:3001','Um comando inicia front-end e back-end; separação clara de responsabilidades.'],['Identidade','UUID para contactos, leituras e alertas','Evita colisões e permite resolver/remover registos sem ambiguidade.'],['Acessibilidade','Labels, foco visível, contraste e layout móvel','Coerente com RNF03 e necessidades dos utilizadores.'],['Limites deliberados','Wearable e notificações simulados','Permite validar o fluxo sem alegar integração física inexistente.']],[3*cm,5.3*cm,7.7*cm])
h2('Endpoints do incremento básico')
table(['Funcionalidade','Operação'],[['RF01','PUT /api/elder'],['RF02','POST /api/contacts; DELETE /api/contacts/:id'],['RF03','POST /api/falls/simulate; POST /api/falls/:id/resolve'],['RF04','POST /api/readings; GET /api/state']],[4*cm,12*cm])
p('Os dados de demonstração são fictícios. O ficheiro server/data/db.json permite repetir as capturas e os testes manuais. O endpoint POST /api/reset repõe o estado inicial apenas no ambiente de protótipo.')
page()

captures=[('01-visao-geral.png','8.1 Visão geral','A página inicial consolida última tensão, rede familiar, sensor de quedas e ações frequentes.'),('02-perfil-idoso.png','8.2 Registo da conta do idoso','Formulario ligado a PUT /api/elder, com dados persistentes e validação no back-end.'),('03-contactos-familiares.png','8.3 Contactos familiares','Criação, priorização e remoção de contactos; a rede passa a conter três pessoas após o teste.'),('04-tensao-arterial.png','8.4 Monitorização da tensão arterial','Registo de sistólica, diastólica e pulso, classificação indicativa, média e histórico.'),('05-deteccao-queda.png','8.5 Deteção de queda','Alerta ativo criado pela simulação; três notificações simuladas; opções de confirmação ou falso alarme.'),('06-mobile.png','8.6 Versão móvel','Navegação compacta e cartões empilhados, preservando o acesso às quatro funcionalidades.')]
for name,title,comment in captures:
    h1(title);p(comment);image('prototype/'+name,width=16.5*cm,maxheight=18.5*cm,caption=f'Captura — {title.split(" ",1)[1]}.')
    if name!='06-mobile.png':page()
page()

h1('9. Verificação e evidências')
table(['Verificação','Resultado','Evidência'],[['Testes automatizados da API','5/5 aprovados','Classificação; perfil; contactos; medições; queda e resolução.'],['Validações negativas','Aprovadas','Dados inválidos e valores fora dos limites devolvem HTTP 400.'],['Alerta duplicado','Bloqueado','Segunda simulação com alerta ativo devolve HTTP 409.'],['Análise estática ESLint','Sem erros','Código da aplicação verificado.'],['Compilação TypeScript/Vite','Concluída','Build de produção gerado sem erros.'],['Fluxos no navegador','4/4 concluídos','Perfil, contacto, medição, queda e resolução; sem erros de browser.'],['Responsividade','Verificada a 390 px','Captura móvel sem perda das ações principais.']],[4.5*cm,3.3*cm,8.2*cm])
h2('Limites da verificação')
p('Os testes demonstram o comportamento do protótipo, não a precisão clínica da deteção de quedas nem a conformidade com dispositivos médicos. Não foram executados testes de carga, disponibilidade prolongada, cifragem, autenticação ou interoperabilidade externa. Estes pontos permanecem abertos para os requisitos e sprints aplicáveis.')
h2('Reprodução')
p('Na pasta prototype: <b>npm install</b>, <b>npm run dev -- --host 0.0.0.0 --port 3000</b>. Testes: <b>npm test</b>. Verificação: <b>npm run lint</b> e <b>npm run build</b>. A aplicação fica disponível em http://localhost:3000.')
page()

h1('10. Proposta para o Sprint 2')
p('Mantendo as quatro funcionalidades básicas, propõe-se acrescentar três funcionalidades escolhidas dos sistemas existentes e uma nova, totalizando oito funcionalidades no próximo incremento. A seleção fica sujeita a negociação com o docente, tal como exigido.')
table(['Elemento','Proposta','Justificação'],[['Existente 1','F05 — Gerir medicação','Fecho ciber-físico claro entre horário, dispensador e alerta.'],['Existente 2','F06 — Prevenir acidentes domésticos','Sensores e atuadores com benefício direto de segurança.'],['Existente 3','F08 — Monitorizar sinais vitais','Complementa F04 e introduz integração com wearable.'],['Nova','F11 — Integrar serviço de emergência','Valida comunicação com serviço externo e reconciliação de incidentes.'],['RNF 1','RNF01 — Segurança e privacidade','Obrigatória para dados pessoais e clínicos.'],['RNF 2','RNF02 — Disponibilidade e recuperação','Alertas devem continuar operacionais perante falhas.'],['RNF 3','RNF04 — Desempenho em tempo real','A utilidade dos alertas depende de resposta atempada.']],[3*cm,5.4*cm,7.6*cm])
h2('Trabalho explicitamente adiado')
p('Os diagramas arquiteturais BDD/IBD, casos de uso, sequências, deployment, padrões arquiteturais, modelo de variabilidade e configurações SPL pertencem ao Sprint 2 e não são apresentados como entregáveis do Sprint 1.')
h2('Checklist final do Sprint 1')
checklist=['Modalidade individual e acumulação dos papéis pelo autor definidas.','Tabela de dependências, Gantt e burndown individual incluídos.','12 funcionalidades identificadas na proporção 4 + 6 + 2.','Processo BPMN principal e 12 subprocessos incluídos.','Requisitos funcionais SysML e quatro RNFs com contribuições/conflitos incluídos.','Protótipo front-end e back-end das quatro funcionalidades básicas verificado.','Capturas do protótipo incluídas.','Proposta do Sprint 2 pronta para negociação.']
for item in checklist:p('✓ '+item)
p(f'<b>Repositório GitHub:</b> {REPO}','Callout')

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=2.2*cm,leftMargin=2.2*cm,topMargin=2*cm,bottomMargin=1.8*cm,title='Cuida+ — Sprint 1',author='Rodrigo Alexandre Vitória Mira — 79432',subject='BPMN, SysML, planeamento e protótipo')
doc.build(story,onFirstPage=cover,onLaterPages=header_footer)
print(OUT)
