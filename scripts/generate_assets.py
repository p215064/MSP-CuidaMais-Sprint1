from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch, Rectangle
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / 'images'
BPMN = ROOT / 'models' / 'bpmn'
SYSML = ROOT / 'models' / 'sysml'
for folder in (IMG, BPMN, SYSML): folder.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titleweight':'bold'})
COLORS={'ink':'#193b3b','teal':'#147d72','light':'#e7f4f0','line':'#91aaa5','coral':'#b94e49','amber':'#c18a35','grey':'#f5f8f7'}
features=[
('F01','Registar conta do idoso','Validar dados','Guardar perfil','Confirmar registo'),
('F02','Adicionar contactos familiares','Validar contacto','Ordenar prioridade','Guardar contacto'),
('F03','Detetar queda','Ler acelerómetro','Queda provável?','Notificar contactos'),
('F04','Monitorizar tensão arterial','Receber medição','Classificar valores','Atualizar histórico'),
('F05','Gerir medicação','Verificar horário','Libertar dose','Alertar se omitida'),
('F06','Prevenir acidentes domésticos','Ler gás e fumo','Risco detetado?','Cortar energia e alertar'),
('F07','Controlar iluminação e temperatura','Ler presença e clima','Ajustar atuadores','Registar estado'),
('F08','Monitorizar sinais vitais','Recolher wearable','Detetar anomalia','Atualizar painel clínico'),
('F09','Prevenir úlceras de pressão','Ler pressão do colchão','Tempo excedido?','Acionar zonas do colchão'),
('F10','Vigiar deambulação','Localizar pulseira','Perímetro violado?','Bloquear porta e alertar'),
('F11','Integrar serviço de emergência','Confirmar emergência','Enviar contexto clínico','Receber referência externa'),
('F12','Integrar farmácia e dispensador','Consultar stock','Stock insuficiente?','Solicitar reposição à farmácia')]

def box(ax,x,y,w,h,text,fc='white',ec=None,rounded=True,fontsize=9,lw=1.3):
    patch=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012,rounding_size=0.025' if rounded else 'square,pad=0',facecolor=fc,edgecolor=ec or COLORS['ink'],linewidth=lw)
    ax.add_patch(patch); ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fontsize,color=COLORS['ink'],wrap=True)
    return patch

def arrow(ax,x1,y1,x2,y2,style='-|>',color=None,connectionstyle='arc3'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=13,linewidth=1.2,color=color or COLORS['ink'],connectionstyle=connectionstyle))

def setup(w=14,h=6):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off');return fig,ax

def save(fig,name):
    fig.savefig(IMG/name,dpi=180,bbox_inches='tight',facecolor='white');plt.close(fig)

# Gantt — 22 a 25 de outubro de 2026
tasks=[('T01','Definir papéis e âmbito',0,1),('T02','Identificar 12 funcionalidades',0,1),('T03','Modelar BPMN principal e subprocessos',1,2),('T04','Elicitar requisitos funcionais SysML',1,1),('T05','Analisar 4 RNFs e relações',2,1),('T06','Preparar planeamento e Gantt',0,1),('T07','Implementar back-end básico',1,2),('T08','Implementar front-end básico',2,1),('T09','Executar testes e capturas',3,1),('T10','Burndown, relatório e entrega',3,1)]
fig,ax=plt.subplots(figsize=(13,6.5));days=['22 out','23 out','24 out','25 out']
for i,(tid,name,start,dur) in enumerate(tasks):
    y=len(tasks)-1-i;ax.barh(y,dur,left=start,height=.58,color=COLORS['teal'] if tid not in ('T09','T10') else '#4d8d83');ax.text(start+.06,y,tid,va='center',ha='left',color='white',fontsize=8,fontweight='bold')
ax.set_yticks(range(len(tasks)),[x[1] for x in tasks][::-1]);ax.set_xticks(np.arange(4)+.5,days);ax.set_xlim(0,4);ax.set_xticks(np.arange(5),minor=True);ax.grid(which='minor',axis='x',color='#dce7e4');ax.set_axisbelow(True);ax.set_title('Sprint 1 — Diagrama de Gantt',loc='left',fontsize=16,pad=18,color=COLORS['ink']);ax.spines[:].set_visible(False);ax.tick_params(length=0,labelsize=9);fig.tight_layout();save(fig,'gantt-sprint-1.png')

# Burndown
fig,ax=plt.subplots(figsize=(10,5.4));x=np.arange(5);ideal=[80,60,40,20,0];actual=[80,64,42,18,0]
ax.plot(x,ideal,'--o',label='Ideal',color='#879b97');ax.plot(x,actual,'-o',label='Real',color=COLORS['teal'],linewidth=2.5);ax.fill_between(x,actual,alpha=.08,color=COLORS['teal']);ax.set_xticks(x,['Início','22 out','23 out','24 out','25 out']);ax.set_ylabel('Trabalho restante (horas)');ax.set_ylim(0,85);ax.grid(axis='y',alpha=.22);ax.spines[['top','right']].set_visible(False);ax.legend(frameon=False);ax.set_title('Sprint 1 — Burndown Chart',loc='left',fontsize=16,pad=16,color=COLORS['ink']);
for xi,yi in zip(x,actual):ax.annotate(f'{yi} h',(xi,yi),xytext=(0,9),textcoords='offset points',ha='center',fontsize=9)
fig.tight_layout();save(fig,'burndown-sprint-1.png')

# BPMN main process — barras de distribuição evitam cruzamentos entre ramos
fig,ax=setup(10,13);ax.text(.03,.975,'Processo principal BPMN — Operação do sistema Cuida+',fontsize=17,fontweight='bold',color=COLORS['ink']);ax.text(.03,.945,'Pool: Cuida+ | Lane: Plataforma cyber-física',fontsize=10,color='#637c78')
ax.add_patch(Rectangle((.025,.045),.95,.875,fill=False,edgecolor=COLORS['ink'],linewidth=1.4));ax.text(.03,.9,'Cuida+',fontsize=10,fontweight='bold')
start=Circle((.07,.5),.012,facecolor='white',edgecolor=COLORS['teal'],linewidth=2);ax.add_patch(start)
fork=Polygon([[.12,.5],[.145,.52],[.17,.5],[.145,.48]],closed=True,facecolor='white',edgecolor=COLORS['ink']);ax.add_patch(fork);ax.plot([.13,.16],[.5,.5],color=COLORS['ink']);ax.plot([.145,.145],[.485,.515],color=COLORS['ink']);arrow(ax,.082,.5,.12,.5)
positions=[]
for idx,(fid,name,*_) in enumerate(features):
    x=.31;y=.845-idx*.064;positions.append((x,y))
    box(ax,x,y,.38,.043,f'{fid}  {name}',fc=COLORS['light'],fontsize=8.2)
    ax.text(x+.012,y+.03,'+',fontsize=11,fontweight='bold',color=COLORS['teal'])
    arrow(ax,.23,y+.0215,x,y+.0215);arrow(ax,x+.38,y+.0215,.77,y+.0215)
ax.plot([.23,.23],[.15,.87],color=COLORS['ink'],linewidth=1.2);arrow(ax,.17,.5,.23,.5)
ax.plot([.77,.77],[.15,.87],color=COLORS['ink'],linewidth=1.2)
join=Polygon([[.83,.5],[.855,.52],[.88,.5],[.855,.48]],closed=True,facecolor='white',edgecolor=COLORS['ink']);ax.add_patch(join);ax.plot([.84,.87],[.5,.5],color=COLORS['ink']);ax.plot([.855,.855],[.485,.515],color=COLORS['ink']);arrow(ax,.77,.5,.83,.5)
ax.add_patch(Circle((.93,.5),.012,facecolor='white',edgecolor=COLORS['coral'],linewidth=3));arrow(ax,.88,.5,.918,.5)
ax.text(.04,.062,'Nota: ramos independentes ativados por eventos; cada subprocesso contém o seu próprio fluxo.',fontsize=8.5,color='#637c78')
save(fig,'bpmn-processo-principal.png')

# BPMN subprocess diagrams
for idx,(fid,name,t1,t2,t3) in enumerate(features):
    fig,ax=setup(13,3.6);ax.text(.025,.91,f'BPMN — Subprocesso {fid}: {name}',fontsize=15,fontweight='bold',color=COLORS['ink'])
    ax.add_patch(Rectangle((.025,.13),.95,.67,fill=False,edgecolor=COLORS['ink'],linewidth=1.2));ax.text(.03,.755,fid,fontsize=9,fontweight='bold')
    ax.add_patch(Circle((.075,.455),.021,facecolor='white',edgecolor=COLORS['teal'],linewidth=2));arrow(ax,.096,.455,.16,.455)
    box(ax,.16,.385,.18,.14,t1,fc='#f7faf9',fontsize=9);arrow(ax,.34,.455,.425,.455)
    if '?' in t2:
        diamond=Polygon([[.425,.455],[.49,.59],[.555,.455],[.49,.32]],closed=True,facecolor='#fff8e9',edgecolor=COLORS['ink']);ax.add_patch(diamond);ax.text(.49,.455,t2,ha='center',va='center',fontsize=8.5,wrap=True)
        arrow(ax,.555,.455,.64,.455);ax.text(.57,.48,'sim',fontsize=8)
        arrow(ax,.49,.32,.49,.21);arrow(ax,.49,.21,.84,.21);arrow(ax,.84,.21,.84,.385);ax.text(.505,.25,'não / monitorizar',fontsize=8)
    else:
        box(ax,.425,.385,.18,.14,t2,fc='#f7faf9',fontsize=9);arrow(ax,.605,.455,.64,.455)
    box(ax,.64,.385,.2,.14,t3,fc=COLORS['light'],fontsize=9);arrow(ax,.84,.455,.905,.455)
    ax.add_patch(Circle((.927,.455),.021,facecolor='white',edgecolor=COLORS['coral'],linewidth=3))
    save(fig,f'bpmn-{fid.lower()}.png')

# SysML requirement diagrams
reqs={
'F01':('RF01','O sistema deve permitir registar e atualizar a conta do idoso com dados pessoais e clínicos válidos.'),
'F02':('RF02','O sistema deve permitir adicionar contactos familiares e definir a prioridade de notificação.'),
'F03':('RF03','O sistema deve detetar uma queda provável, criar um alerta e notificar os contactos por prioridade.'),
'F04':('RF04','O sistema deve registar sistólica, diastólica e pulso, classificar e conservar o histórico.'),
'F05':('RF05','O sistema deve controlar horários, libertação e omissão de doses de medicação.'),
'F06':('RF06','O sistema deve detetar risco doméstico e comandar o corte seguro de gás ou energia.'),
'F07':('RF07','O sistema deve ajustar iluminação e temperatura segundo presença, horário e condições ambientais.'),
'F08':('RF08','O sistema deve receber sinais vitais do wearable, identificar anomalias e atualizar o painel clínico.'),
'F09':('RF09','O sistema deve analisar pressão e imobilidade e acionar a redistribuição de pressão do colchão.'),
'F10':('RF10','O sistema deve localizar a pulseira, detetar saída do perímetro e alertar a equipa.'),
'F11':('RF11','O sistema deve comunicar emergências e contexto clínico a um serviço externo e guardar a referência.'),
'F12':('RF12','O sistema deve consultar o stock do dispensador e solicitar reposição ao serviço da farmácia.')}
for group,ids in [('basicas',['F01','F02','F03','F04']),('existentes',['F05','F06','F07','F08','F09','F10']),('novas',['F11','F12'])]:
    fig,ax=setup(13,2.2*len(ids)+1.4);ax.text(.02,.97,f'SysML Requirements Diagram — Funcionalidades {group}',fontsize=16,fontweight='bold',va='top',color=COLORS['ink'])
    n=len(ids)
    for i,fid in enumerate(ids):
        y=.86-i*(.78/max(n,1));rid,text=reqs[fid]
        import textwrap
        feature_name=textwrap.fill(dict((f[0],f[1]) for f in features)[fid],22)
        requirement_text=textwrap.fill(text,82)
        box(ax,.04,y-.09,.16,.115,f'«feature»\n{fid}\n{feature_name}',fc='#edf5f2',fontsize=7.8,rounded=False)
        box(ax,.34,y-.12,.6,.16,f'«requirement» {rid}\n{requirement_text}',fc='white',fontsize=8.4,rounded=False)
        arrow(ax,.2,y-.03,.34,y-.03,style='-|>');ax.text(.235,y-.005,'«refine»',fontsize=8,color='#617a76')
    save(fig,f'sysml-requisitos-{group}.png')

# NFR diagram with contributions and conflicts
fig,ax=setup(13,8);ax.text(.03,.96,'SysML Requirements Diagram — Requisitos não funcionais e relações',fontsize=16,fontweight='bold',color=COLORS['ink'])
nfr=[('RNF01','Segurança e privacidade','Cifragem, controlo de acesso, consentimento e minimização de dados.'),('RNF04','Desempenho em tempo real','Alerta local em ≤ 2 s no percentil 95; registo de medições em ≤ 1 s.'),('RNF03','Usabilidade e acessibilidade','Interface responsiva, contraste, foco visível e controlos de grande dimensão.'),('RNF02','Disponibilidade e recuperação','Serviço local de alertas disponível 99,5% e recuperação automática.')]
pos=[(.07,.65),(.56,.65),(.07,.25),(.56,.25)]
for (rid,title,text),(x,y) in zip(nfr,pos):
    import textwrap
    box(ax,x,y,.37,.19,f'«requirement» {rid}\n{title}\n\n{textwrap.fill(text,48)}',fc='#f7faf9',fontsize=8.5,rounded=False)
arrow(ax,.255,.65,.255,.44,style='<->',color=COLORS['coral']);ax.text(.27,.535,'«conflict»\nprivacidade pode\nreduzir simplicidade',fontsize=8,color=COLORS['coral'])
arrow(ax,.44,.74,.56,.74,style='<->',color=COLORS['coral']);ax.text(.435,.79,'«conflict»\ncontrolos adicionam latência',fontsize=8,color=COLORS['coral'],ha='center')
arrow(ax,.745,.65,.745,.44,style='-|>',color=COLORS['teal']);ax.text(.757,.54,'«contribute»\nprocessamento eficiente\napoia disponibilidade',fontsize=8,color=COLORS['teal'])
arrow(ax,.56,.34,.44,.34,style='-|>',color=COLORS['teal']);ax.text(.5,.375,'«contribute»\nserviço disponível melhora a experiência',fontsize=8,color=COLORS['teal'],ha='center')
ax.text(.07,.12,'Decisão: autenticação e cifragem são obrigatórias; a otimização não pode remover controlos de segurança.\nOs conflitos serão validados por testes de desempenho e avaliação de acessibilidade.',fontsize=10,color=COLORS['ink'])
save(fig,'sysml-requisitos-nao-funcionais.png')

# BPMN 2.0 XML source, with one subprocess per feature
NS={'bpmn':'http://www.omg.org/spec/BPMN/20100524/MODEL','bpmndi':'http://www.omg.org/spec/BPMN/20100524/DI','dc':'http://www.omg.org/spec/DD/20100524/DC','di':'http://www.omg.org/spec/DD/20100524/DI'}
for prefix,uri in NS.items():ET.register_namespace(prefix,uri)
def q(p,tag):return f'{{{NS[p]}}}{tag}'
defs=ET.Element(q('bpmn','definitions'),{'id':'Definitions_CuidaMais','targetNamespace':'https://cuida-mais.example/bpmn','exporter':'Cuida+ Sprint 1','exporterVersion':'1.0'})
process=ET.SubElement(defs,q('bpmn','process'),{'id':'Process_CuidaMais','name':'Operação do sistema Cuida+','isExecutable':'false'})
ET.SubElement(process,q('bpmn','startEvent'),{'id':'Start_Main','name':'Evento do sistema'})
ET.SubElement(process,q('bpmn','parallelGateway'),{'id':'Gateway_Fork'})
for fid,name,*_ in features:
    sub=ET.SubElement(process,q('bpmn','subProcess'),{'id':f'SubProcess_{fid}','name':f'{fid} — {name}'})
    ET.SubElement(sub,q('bpmn','startEvent'),{'id':f'Start_{fid}'})
    ET.SubElement(sub,q('bpmn','task'),{'id':f'Task_{fid}_1','name':'Executar funcionalidade'})
    ET.SubElement(sub,q('bpmn','endEvent'),{'id':f'End_{fid}'})
    ET.SubElement(sub,q('bpmn','sequenceFlow'),{'id':f'Flow_{fid}_1','sourceRef':f'Start_{fid}','targetRef':f'Task_{fid}_1'})
    ET.SubElement(sub,q('bpmn','sequenceFlow'),{'id':f'Flow_{fid}_2','sourceRef':f'Task_{fid}_1','targetRef':f'End_{fid}'})
ET.SubElement(process,q('bpmn','parallelGateway'),{'id':'Gateway_Join'})
ET.SubElement(process,q('bpmn','endEvent'),{'id':'End_Main'})
ET.SubElement(process,q('bpmn','sequenceFlow'),{'id':'Flow_Start','sourceRef':'Start_Main','targetRef':'Gateway_Fork'})
for fid,*_ in features:
    ET.SubElement(process,q('bpmn','sequenceFlow'),{'id':f'Flow_Fork_{fid}','sourceRef':'Gateway_Fork','targetRef':f'SubProcess_{fid}'})
    ET.SubElement(process,q('bpmn','sequenceFlow'),{'id':f'Flow_Join_{fid}','sourceRef':f'SubProcess_{fid}','targetRef':'Gateway_Join'})
ET.SubElement(process,q('bpmn','sequenceFlow'),{'id':'Flow_End','sourceRef':'Gateway_Join','targetRef':'End_Main'})
xml=minidom.parseString(ET.tostring(defs,encoding='utf-8')).toprettyxml(indent='  ',encoding='utf-8')
(BPMN/'cuida-mais-sprint-1.bpmn').write_bytes(xml)

# SysML v2 textual source
lines=['package CuidaMais_Sprint1 {','  // Requisitos funcionais associados às 12 funcionalidades.']
for fid,_,*_ in features:
    rid,text=reqs[fid];lines += [f'  requirement {rid} {{',f'    doc /* {fid}: {text} */','  }']
for rid,title,text in nfr:
    lines += [f'  requirement {rid} {{',f'    doc /* {title}: {text} */','  }']
lines += ['  // Relações: RNF01 «conflict» RNF03 e RNF04; RNF04 «contribute» RNF02 e RNF03.','}']
(SYSML/'cuida-mais-requisitos.sysml').write_text('\n'.join(lines),encoding='utf-8')
print(f'Gerados {len(list(IMG.glob("*.png")))} diagramas e fontes BPMN/SysML em {ROOT}')
