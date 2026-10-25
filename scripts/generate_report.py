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
REPO=(ROOT/'repository.txt').read_text(encoding='utf-8').strip() if (ROOT/'repository.txt').exists() else 'A PREENCHER: publicar a pasta no GitHub e inserir aqui o URL'
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
    canvas.setFont('Helvetica',7.5);canvas.setFillColor(GREY);canvas.drawString(2.2*cm,h-1.2*cm,'Cuida+  |  MSP: Sprint 1')
    canvas.drawRightString(w-2.2*cm,1.15*cm,f'Página {doc.page}');canvas.restoreState()

def cover(canvas,doc):
    canvas.saveState();w,h=A4;canvas.setFillColor(NAVY);canvas.rect(0,h-1.2*cm,w,1.2*cm,fill=1,stroke=0);canvas.setFillColor(TEAL);canvas.rect(0,0,w,.5*cm,fill=1,stroke=0);canvas.restoreState()

# Cover
story.append(Spacer(1,3.2*cm));p('Cuida+','CoverTitle');p('Sistema ciber-físico de apoio a idosos','CoverSub');story.append(Spacer(1,1.1*cm));p('TRABALHO PRÁTICO: PRIMEIRO SPRINT','H2x');story[-1].alignment=TA_CENTER
p('Modelação BPMN, requisitos SysML, planeamento e protótipo web','CoverSub');story.append(Spacer(1,1.4*cm))
table(['Elemento','Informação'],[['Unidade curricular','MSP: Modelação e Simulação de Processos'],['Modalidade','Trabalho individual'],['Autor','Rodrigo Alexandre Vitória Mira: 79432'],['Período do Sprint 1','22 a 25 de outubro de 2026'],['Data de preparação','25 de outubro de 2026'],['Repositório GitHub',REPO]],[4.2*cm,11.8*cm])
p('<b>Nota de entrega:</b> submeter este relatório em PDF e o URL público do repositório GitHub. O código, os modelos, as imagens e este relatório encontram-se na estrutura de pastas entregue.','Callout')
page()

h1('1. Enquadramento e âmbito')
p('O Cuida+ junta sensores, atuadores e uma aplicação para ajudar pessoas idosas a viver com mais segurança, tanto em casa como numa instituição. Neste sprint defini as funcionalidades do sistema, os processos e os requisitos. Também implementei as quatro funcionalidades básicas pedidas no enunciado.')
p('Usei <b>BPMN 2.0</b> no processo principal e nos 12 subprocessos. Os requisitos foram representados com <b>SysML Requirements Diagrams</b>. Para o planeamento preparei um <b>diagrama de Gantt</b> e um <b>burndown chart</b>. O protótipo foi desenvolvido com <b>React, TypeScript e Express</b>. No repositório incluí as imagens e os ficheiros que permitem editar os modelos.')
h2('Decisões de âmbito')
for text in ['O protótipo implementa apenas F01–F04, como pedido no enunciado. As funcionalidades F05–F12 foram modeladas, mas ainda não foram implementadas.','A deteção de queda usa uma simulação do acelerómetro. Os SMS enviados à família também são simulados, não sendo enviadas mensagens reais.','F11 e F12 descrevem comunicação com sistemas externos. Nesta fase não foram usados serviços reais, pois seriam necessários acessos e autorizações.','A classificação da tensão arterial serve apenas de apoio ao protótipo e não é um diagnóstico. Em caso de emergência, a interface indica o contacto 112.']:
    p(text)
h2('Estrutura da entrega')
table(['Pasta / ficheiro','Conteúdo'],[['prototype/','Interface, servidor, dados de demonstração, testes e instruções.'],['models/bpmn/','Processo BPMN 2.0 com 12 subprocessos em XML.'],['models/sysml/','Fonte textual SysML v2 dos requisitos.'],['images/','Gantt, burndown, modelos e capturas do protótipo.'],['MSP_Sprint1_CuidaMais.pdf','Relatório com os modelos, comentários e decisões.']],[4.3*cm,11.7*cm])
page()

h1('2. Organização individual e qualidade')
p('O enunciado prevê grupos de quatro pessoas, mas fiz este trabalho <b>individualmente</b>. Assim, acumulei as funções de Scrum Master, Quality Controller e Team Member. Fiquei responsável pelo planeamento, modelos, desenvolvimento, testes e relatório.')
table(['Responsável','Papéis no Sprint 1','Responsabilidades'],[['Autor','Scrum Master','Planeamento, dependências, Gantt, burndown e gestão do âmbito.'],['Autor','Quality Controller','Revisão dos modelos, rastreabilidade e verificação da entrega.'],['Autor','Team Member','Servidor, interface, persistência, testes e capturas.']],[2.5*cm,4.1*cm,9.4*cm])
h2('Adaptação dos papéis ao trabalho individual')
p('Como trabalhei sozinho, não houve rotação do papel de Scrum Master. Na revisão do trabalho verifiquei os modelos, corri os testes e confirmei se as imagens e os comentários estavam de acordo com o protótipo.')
h2('Definição de pronto')
p('Considerei uma tarefa concluída depois de guardar o resultado no repositório e o rever. Quando aplicável, juntei também o modelo, o teste, a captura ou a parte do relatório correspondente.')
page()

h1('3. Planeamento do Sprint 1')
p('Planei 32 horas de <b>trabalho individual</b>. Na tabela indiquei as tarefas que tiveram de ficar prontas antes de começar cada atividade.')
tasks=[('T01','Definir papéis e âmbito','Nenhuma','Autor','2','Concluída'),('T02','Identificar 12 funcionalidades','T01','Autor','3','Concluída'),('T03','Modelar BPMN principal e 12 subprocessos','T02','Autor','5','Concluída'),('T04','Elicitar requisitos funcionais SysML','T02','Autor','4','Concluída'),('T05','Analisar 4 RNFs e relações','T04','Autor','2','Concluída'),('T06','Preparar planeamento e Gantt','T01','Autor','2','Concluída'),('T07','Implementar servidor básico','T02, T04','Autor','5','Concluída'),('T08','Implementar interface básica','T04, T07','Autor','5','Concluída'),('T09','Executar testes e capturas','T07, T08','Autor','2','Concluída'),('T10','Fechar burndown, relatório e entrega','T03, T05, T06, T09','Autor','2','Concluída')]
table(['ID','Tarefa','Dependências','Resp.','h','Estado'],tasks,[1*cm,6.1*cm,2.6*cm,1.8*cm,.7*cm,2.3*cm])
h2('Gantt e burndown')
image('gantt-sprint-1.png',width=16.7*cm,maxheight=10.2*cm,caption='Figura 1: Calendarização das tarefas do Sprint 1.')
page()
h1('3. Planeamento do Sprint 1: acompanhamento')
image('burndown-sprint-1.png',width=16.2*cm,maxheight=11.2*cm,caption='Figura 2: Comparação entre o burndown previsto e o registado.')
table(['Marco','Ideal restante','Real restante','Comentário'],[['Início','32 h','32 h','Âmbito e dependências definidos.'],['22 outubro','24 h','26 h','Início mais lento, sem mudanças ao âmbito.'],['23 outubro','16 h','17 h','Modelos e servidor permitiram recuperar o atraso.'],['24 outubro','8 h','7 h','Interface integrada e início dos testes.'],['25 outubro','0 h','0 h','Quatro funcionalidades verificadas e relatório terminado.']],[3*cm,2.6*cm,2.6*cm,7.8*cm])
p('O burndown mostra o trabalho que faltava em cada dia. Antes de fechar o sprint, verifiquei os testes da API, a compilação, a análise estática e os fluxos no navegador.','Callout')
page()

h1('4. Catálogo das 12 funcionalidades')
features=[('F01','Registar conta do idoso','Básica','Dados pessoais, contacto, morada e notas clínicas.'),('F02','Adicionar contactos familiares','Básica','Familiares e prioridade de notificação.'),('F03','Detetar queda','Básica','Evento de acelerómetro, alerta e resposta.'),('F04','Monitorizar tensão arterial','Básica','Medição, classificação indicativa e histórico.'),('F05','Gerir medicação','Sistema existente','Dispensador, horários, dose e omissão.'),('F06','Prevenir acidentes domésticos','Sistema existente','Gás/fumo e corte seguro de energia.'),('F07','Controlar iluminação e temperatura','Sistema existente','Presença, horário, iluminação e clima.'),('F08','Monitorizar sinais vitais','Sistema existente','Wearable, anomalias e painel clínico.'),('F09','Prevenir úlceras de pressão','Sistema existente','Colchão sensorizado e atuadores.'),('F10','Vigiar deambulação','Sistema existente','BLE/UWB, perímetro, porta e equipa.'),('F11','Integrar serviço de emergência','Nova: sistema externo','Envio de contexto e referência de atendimento.'),('F12','Integrar farmácia e dispensador','Nova: dispositivo + serviço','Stock local e reposição pela farmácia.')]
table(['ID','Funcionalidade','Origem','Decisão de conteúdo'],features,[1.1*cm,4.8*cm,3.3*cm,6.8*cm])
h2('Justificação das propostas novas')
p('<b>F11:</b> escolhi esta funcionalidade para que um alerta também possa ser enviado a um serviço de emergência. A resposta desse serviço fica associada ao incidente através de uma referência. Só devem ser partilhados os dados necessários e com consentimento.')
p('<b>F12:</b> liga o stock do dispensador à farmácia. Quando o stock é baixo, o sistema pode pedir reposição e acompanhar a resposta. Assim, a gestão da medicação não termina quando o dispensador fica vazio.')
p('Neste sprint só F01–F04 foram implementadas. As outras oito funcionalidades estão representadas nos processos e requisitos, mas ainda não fazem parte do protótipo.','Callout')
page()

h1('5. Modelação BPMN')
p('No processo principal coloquei as 12 funcionalidades em ramos independentes, porque cada uma pode ser iniciada por um evento diferente. O gateway paralelo serve para organizar esta vista e não significa que todas sejam executadas ao mesmo tempo. As atividades com o sinal “+” são subprocessos. Cada subprocesso tem início, tarefas, uma decisão quando necessário e fim.')
image('bpmn-processo-principal.png',width=15.8*cm,maxheight=21.8*cm,caption='Figura 3: Processo principal BPMN com os 12 subprocessos.')
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
    image(f'bpmn-{fid.lower()}.png',width=16.5*cm,maxheight=7.3*cm,caption=f'Figura {4+idx}: {fid}: {name}.')
    p(f'<b>Comentário:</b> {subprocess_comments[fid]}','Smallx')
    if idx%2==1 and idx<11:page()
page()

h1('6. Elicitação de requisitos')
p('Para levantar os requisitos, li os cenários do enunciado e pensei no que cada utilizador precisa de fazer e na resposta esperada do sistema. Considerei o idoso, a família, o cuidador, a equipa clínica, os serviços de emergência, a farmácia e o administrador.')
h2('Requisitos funcionais e critérios de aceitação')
reqs=[('RF01','Registar/atualizar a conta com dados válidos.','Guardar perfil completo; rejeitar nome vazio, telefone inválido ou data futura.'),('RF02','Adicionar familiares e prioridade de notificação.','Criar contacto válido; listar por prioridade; remover por identificador.'),('RF03','Detetar queda provável, alertar e notificar por prioridade.','Simulação cria um único alerta ativo; contactos registados; resolução obrigatória.'),('RF04','Registar tensão e pulso, classificar e conservar histórico.','Valores dentro dos limites; classificação coerente; leitura visível no histórico.'),('RF05','Controlar horários, doses e omissões.','No horário liberta dose configurada; ausência de recolha gera alerta.'),('RF06','Detetar risco e comandar corte seguro.','Evento de gás/fumo aciona atuador e notifica cuidador.'),('RF07','Ajustar luz e temperatura ao contexto.','Presença noturna ajusta iluminação; temperatura fora da faixa ajusta clima.'),('RF08','Receber sinais vitais e sinalizar anomalias.','Leitura wearable atualiza painel; anomalia gera evento clínico.'),('RF09','Analisar pressão e acionar redistribuição.','Imobilidade excessiva altera zonas de pressão e regista ação.'),('RF10','Detetar saída do perímetro e alertar equipa.','Localização fora da zona segura gera alerta e comando previsto.'),('RF11','Comunicar emergência e guardar referência externa.','Pedido autenticado contém contexto mínimo; resposta é reconciliada.'),('RF12','Consultar stock e solicitar reposição.','Stock abaixo do limiar gera pedido e acompanha estado da farmácia.')]
table(['ID','Requisito','Critério de aceitação / verificação'],reqs,[1.2*cm,6.4*cm,8.4*cm])
h2('Decisões de elicitação')
p('Não escolhi marcas nem fornecedores nos requisitos. Defini uma ordem para os contactos familiares, de modo a evitar enviar todos os alertas para toda a gente. Uma queda só fica resolvida depois de ser confirmada ou assinalada como falso alarme. Também incluí limites para impedir o registo de valores impossíveis.')
page()
h1('6.1 SysML: requisitos das funcionalidades básicas')
image('sysml-requisitos-basicas.png',width=16.2*cm,maxheight=21*cm,caption='Figura 16: Relações «refine» entre F01–F04 e RF01–RF04.')
page()
h1('6.2 SysML: requisitos das funcionalidades existentes')
image('sysml-requisitos-existentes.png',width=15.8*cm,maxheight=22*cm,caption='Figura 17: Relações «refine» entre F05–F10 e RF05–RF10.')
page()
h1('6.3 SysML: requisitos das funcionalidades novas')
image('sysml-requisitos-novas.png',width=16.2*cm,maxheight=15*cm,caption='Figura 18: Relações «refine» das duas integrações externas.')
h2('Rastreabilidade')
p('Cada funcionalidade tem um requisito com o mesmo número. Por exemplo, F01 corresponde a RF01 e F12 corresponde a RF12. Usei estes códigos nos modelos, no relatório e nos testes. No servidor, RF01–RF04 têm operações próprias.')
page()

h1('7. Requisitos não funcionais, contribuições e conflitos')
nfr=[('RNF01','Segurança e privacidade','Cifragem em trânsito e em repouso; autenticação; consentimento; minimização.','Revisão de segurança e testes de autorização.'),('RNF02','Disponibilidade e recuperação','Alertas locais com disponibilidade alvo de 99,5%; recuperação automática.','Ensaio de falha e indisponibilidade mensurada.'),('RNF03','Usabilidade e acessibilidade','Responsividade, contraste, foco visível, linguagem clara e controlos amplos.','Teste com utilizadores e auditoria de acessibilidade.'),('RNF04','Desempenho em tempo real','Alerta local ≤ 2 s no p95; registo de medição ≤ 1 s.','Teste de carga com latência por percentil.')]
table(['ID','Categoria','Meta / restrição','Verificação prevista'],nfr,[1.2*cm,3.4*cm,7.1*cm,4.3*cm])
image('sysml-requisitos-nao-funcionais.png',width=16.3*cm,maxheight=10.8*cm,caption='Figura 19: Relações «contribute» e «conflict» entre os quatro RNFs.')
p('<b>Conflitos:</b> a segurança pode aumentar o tempo de resposta e acrescentar passos à interface. Por isso, RNF01 pode dificultar RNF04 e RNF03. Não considerei retirar controlos de segurança para ganhar desempenho. A solução passa por melhorar o código e simplificar os fluxos de emergência.')
p('<b>Contribuições:</b> um sistema com boa resposta também fica mais disponível para quem o utiliza. Da mesma forma, um serviço disponível melhora a experiência de utilização. Os valores indicados são metas para o sistema. Não foram medidos nem certificados neste protótipo local.')
page()

h1('8. Protótipo: decisões técnicas')
table(['Aspeto','Decisão','Justificação'],[['Interface','React, TypeScript, Vite e CSS responsivo','Permite criar componentes interativos e adaptar a página ao telemóvel.'],['Servidor','Node.js e Express 5','Facilita a criação da API REST, a validação dos dados e os testes.'],['Persistência','Ficheiro JSON com escrita atómica','É suficiente para o protótipo e não precisa de uma base de dados externa.'],['Integração','Proxy Vite /api → 127.0.0.1:3001','Um só comando inicia a interface e o servidor.'],['Identidade','UUID para contactos, leituras e alertas','Permite identificar cada registo sem ambiguidades.'],['Acessibilidade','Labels, foco visível, contraste e layout móvel','Responde ao RNF03 e às necessidades dos utilizadores.'],['Limites','Wearable e notificações simulados','Permite testar os fluxos sem afirmar que existem dispositivos ligados.']],[3*cm,5.3*cm,7.7*cm])
h2('Endpoints do incremento básico')
table(['Funcionalidade','Operação'],[['RF01','PUT /api/elder'],['RF02','POST /api/contacts; DELETE /api/contacts/:id'],['RF03','POST /api/falls/simulate; POST /api/falls/:id/resolve'],['RF04','POST /api/readings; GET /api/state']],[4*cm,12*cm])
p('Usei dados fictícios nas demonstrações. O ficheiro server/data/db.json guarda o estado e permite repetir os testes manuais. O endpoint POST /api/reset repõe os dados iniciais do protótipo.')
page()

captures=[('01-visao-geral.png','8.1 Visão geral','Na página inicial juntei a última tensão registada, os contactos familiares, o sensor de quedas e as ações mais usadas.'),('02-perfil-idoso.png','8.2 Registo da conta do idoso','O formulário envia os dados para PUT /api/elder. O servidor valida a informação e guarda as alterações.'),('03-contactos-familiares.png','8.3 Contactos familiares','É possível adicionar, ordenar e remover contactos. Depois do teste ficaram três pessoas na rede familiar.'),('04-tensao-arterial.png','8.4 Monitorização da tensão arterial','A página permite registar sistólica, diastólica e pulso. Apresenta também a classificação indicativa, a média e o histórico.'),('05-deteccao-queda.png','8.5 Deteção de queda','A simulação criou um alerta e três notificações simuladas. O utilizador pode confirmar a queda ou assinalar falso alarme.'),('06-mobile.png','8.6 Versão móvel','No telemóvel, os cartões passam a ficar empilhados e continuam disponíveis as quatro funcionalidades.')]
for name,title,comment in captures:
    h1(title);p(comment);image('prototype/'+name,width=16.5*cm,maxheight=18.5*cm,caption=f'Captura: {title.split(" ",1)[1]}.')
    if name!='06-mobile.png':page()
page()

h1('9. Verificação e evidências')
table(['Verificação','Resultado','Evidência'],[['Testes automatizados da API','5/5 aprovados','Classificação; perfil; contactos; medições; queda e resolução.'],['Validações negativas','Aprovadas','Dados inválidos e valores fora dos limites devolvem HTTP 400.'],['Alerta duplicado','Bloqueado','Segunda simulação com alerta ativo devolve HTTP 409.'],['Análise estática ESLint','Sem erros','Código da aplicação verificado.'],['Compilação TypeScript/Vite','Concluída','Build de produção gerado sem erros.'],['Fluxos no navegador','4/4 concluídos','Perfil, contacto, medição, queda e resolução; sem erros de browser.'],['Responsividade','Verificada a 390 px','Captura móvel sem perda das ações principais.']],[4.5*cm,3.3*cm,8.2*cm])
h2('Limites da verificação')
p('Os testes servem para verificar o protótipo. Não provam que a deteção de quedas tem precisão clínica nem que o sistema pode ser usado como dispositivo médico. Ainda não testei carga, disponibilidade durante longos períodos, cifragem, autenticação ou ligação a serviços externos.')
h2('Reprodução')
p('Na pasta prototype, executar <b>npm install</b> e depois <b>npm run dev -- --host 0.0.0.0 --port 3000</b>. Os testes correm com <b>npm test</b>. Para verificar o código, usar <b>npm run lint</b> e <b>npm run build</b>. A aplicação abre em http://localhost:3000.')
page()

h1('10. Proposta para o Sprint 2')
p('Para o próximo sprint proponho manter as quatro funcionalidades básicas e acrescentar três das funcionalidades já existentes e uma nova. Ficam assim oito funcionalidades. A escolha final será discutida com o docente.')
table(['Elemento','Proposta','Justificação'],[['Existente 1','F05: Gerir medicação','Liga o horário, o dispensador e o alerta num mesmo processo.'],['Existente 2','F06: Prevenir acidentes domésticos','Usa sensores e atuadores com um benefício direto para a segurança.'],['Existente 3','F08: Monitorizar sinais vitais','Complementa F04 e acrescenta a ligação a um wearable.'],['Nova','F11: Integrar serviço de emergência','Permite testar a comunicação com um serviço externo.'],['RNF 1','RNF01: Segurança e privacidade','Necessário por causa dos dados pessoais e clínicos.'],['RNF 2','RNF02: Disponibilidade e recuperação','Os alertas devem continuar a funcionar quando ocorrem falhas.'],['RNF 3','RNF04: Desempenho em tempo real','Um alerta só é útil se chegar a tempo.']],[3*cm,5.4*cm,7.6*cm])
h2('Trabalho deixado para o Sprint 2')
p('Os diagramas BDD e IBD, os casos de uso, as sequências, o deployment, os padrões arquiteturais, o modelo de variabilidade e as configurações SPL ficam para o Sprint 2. Não os incluí como entregáveis deste sprint.')
h2('Checklist final do Sprint 1')
checklist=['Trabalho individual e papéis do autor definidos.','Tabela de dependências, Gantt e burndown incluídos.','12 funcionalidades identificadas na proporção 4 + 6 + 2.','Processo BPMN principal e 12 subprocessos incluídos.','Requisitos funcionais SysML e quatro RNFs com contribuições e conflitos.','Interface e servidor das quatro funcionalidades básicas verificados.','Capturas do protótipo incluídas.','Proposta do Sprint 2 pronta para discussão.']
for item in checklist:p(item)
p(f'<b>Repositório GitHub:</b> {REPO}','Callout')

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=2.2*cm,leftMargin=2.2*cm,topMargin=2*cm,bottomMargin=1.8*cm,title='Cuida+: Sprint 1',author='Rodrigo Alexandre Vitória Mira: 79432',subject='BPMN, SysML, planeamento e protótipo')
doc.build(story,onFirstPage=cover,onLaterPages=header_footer)
print(OUT)
