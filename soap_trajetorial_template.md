# SOAP Trajetorial - Template de Preenchimento

## INSTRUÇÕES PARA IA

**Objetivo**: Documentar consulta única com análise multidimensional da trajetória atual do paciente.

**Metodologia VOITHER**: 
- Capturar COMPLEXIDADE multidimensional
- Mapear TRAJETÓRIA temporal (passado→presente→futuro)
- Identificar RECURSOS e potencialidades
- Avaliar RISCOS e fatores protetivos
- Quantificar estado em 10 dimensões (escala 0-5)

**Foco**: Sessão atual como janela para compreender totalidade da experiência do paciente.

---

## CABEÇALHO

### Dados da Consulta
- **Nome**: `[EXTRAIR: Nome completo do paciente]`
- **Idade**: `[EXTRAIR: Idade mencionada ou calcular]`
- **Prontuário**: `[USAR: Número fornecido ou formato padrão]`
- **Data**: `[DATA: Da consulta]`
- **Tipo Sessão**: `[IDENTIFICAR: Primeira consulta, retorno, urgência, etc.]`
- **Profissional**: `[EXTRAIR: Nome do profissional responsável]`

---

## S - SUBJETIVO

### Narrativa do Paciente (Próprias Palavras)

**INSTRUÇÃO**: Capture a narrativa usando preferencialmente as PRÓPRIAS PALAVRAS do paciente.

**Técnica de extração**:
- Identifique sequências de fala direta do paciente
- Mantenha expressões idiomáticas e gírias
- Preserve estrutura sintática original quando possível
- Inclua hesitações significativas ("é... tipo assim...")

**Formato de preenchimento**:
```
"[TRANSCREVER: Sequências literais da fala do paciente que capture sua forma única de expressar a experiência atual]"

[NARRATIVE: Complementar com descrição em terceira pessoa conectando os elementos mencionados pelo paciente]
```

### Queixa Principal & Demanda Atual

**INSTRUÇÃO**: Distinguir entre queixa (sintoma) e demanda (o que realmente busca).

#### Queixa Principal
`[EXTRAIR: O que paciente identifica como problema principal]`

#### Demanda Atual  
`[INTERPRETAR: O que realmente busca - pode ser diferente da queixa explícita]`

#### Expectativas com o Tratamento
`[EXTRAIR: O que espera que aconteça, como imagina que pode ser ajudado]`

### Estado Emocional Relatado

**INSTRUÇÃO**: Marque baseado em evidências da transcrição.

**Estados identificados na transcrição**:
- ☐ Ansioso/Agitado `[EVIDÊNCIA: Citar trecho que indica]`
- ☐ Deprimido/Triste `[EVIDÊNCIA: Citar trecho que indica]`
- ☐ Eufórico/Irritado `[EVIDÊNCIA: Citar trecho que indica]`
- ☐ Confuso/Desorientado `[EVIDÊNCIA: Citar trecho que indica]`
- ☐ Calmo/Estável `[EVIDÊNCIA: Citar trecho que indica]`
- ☐ Outro: `[ESPECIFICAR estado único mencionado]`

---

## O - OBJETIVO

### Observações Comportamentais

**INSTRUÇÃO**: Capture observações objetivas mencionadas na transcrição ou inferíveis do padrão discursivo.

**Elementos a identificar**:
- Padrão de fala (velocidade, fluência, coerência)
- Organização do pensamento
- Capacidade de manter foco
- Modulação emocional durante a sessão
- Sinais de agitação ou inquietação

**Formato**:
```
Durante a consulta, [Nome] apresentou [descrever padrão observado]. Sua fala caracterizou-se por [velocidade/organização]. Demonstrou [capacidade de concentração]. [Outros aspectos comportamentais observáveis pela transcrição].
```

### Exame do Estado Mental

**INSTRUÇÃO**: Marque baseado em evidências da transcrição.

#### Aparência
- ☐ Adequada `[Se mencionado cuidado pessoal adequado]`
- ☐ Negligenciada `[Se mencionado descuido com aparência]`
- ☐ Bizarra `[Se mencionadas particularidades na apresentação]`

#### Comportamento
- ☐ Cooperativo `[Se demonstra colaboração na sessão]`
- ☐ Agitado `[Se revela inquietação, dificuldade de ficar parado]`
- ☐ Retraído `[Se mostra fechado, pouco responsivo]`

#### Discurso
- ☐ Normal `[Fluxo e velocidade adequados]`
- ☐ Acelerado `[Fala rápida, difícil de interromper]`
- ☐ Lentificado `[Fala lenta, pausas prolongadas]`

#### Afeto
- ☐ Eutímico `[Humor equilibrado]`
- ☐ Deprimido `[Tristeza, desânimo]`
- ☐ Ansioso `[Apreensão, nervosismo]`
- ☐ Irritável `[Facilmente irritado]`

#### Pensamento
- ☐ Organizado `[Sequência lógica, coerente]`
- ☐ Desorganizado `[Falta de sequência lógica]`
- ☐ Delirante `[Ideias bizarras, sem base na realidade]`

#### Cognição
- ☐ Preservada `[Memória, atenção, orientação adequadas]`
- ☐ Alterada `[Déficits cognitivos evidentes]`

---

## A - AVALIAÇÃO (Análise Multidimensional)

### Perfil Dimensional (Escala 0-5)

**INSTRUÇÃO**: Pontue cada dimensão baseado nas evidências da transcrição.

**Escala de Pontuação**:
- **0**: Gravemente comprometido (disfuncional)
- **1**: Severamente comprometido (funcionalidade muito limitada)
- **2**: Moderadamente comprometido (funcionalidade parcial)
- **3**: Levemente comprometido (funcionalidade com limitações)
- **4**: Funcional com limitações menores
- **5**: Plenamente funcional

#### Temporal (Relação com tempo)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Como paciente se relaciona com passado, presente, futuro]`

#### Relacional (Vínculos interpessoais)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Qualidade das relações mencionadas]`

#### Espacial (Relação com territórios)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Como se relaciona com casa, trabalho, espaços]`

#### Linguística (Organização discursiva)
**Pontuação**: `[0-5]`
**Evidências**: `[AVALIAR: Coerência, complexidade, expressividade da fala]`

#### Emocional (Regulação afetiva)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Capacidade de modular e expressar emoções]`

#### Cognitiva (Funcionamento mental)
**Pontuação**: `[0-5]`
**Evidências**: `[AVALIAR: Atenção, memória, capacidade executiva]`

#### Comportamental (Padrões de ação)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Capacidade de tomar decisões, agir efetivamente]`

#### Existencial (Sentido e propósito)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Expressões de significado, propósito, esperança]`

#### Somática (Manifestações corporais)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Sintomas físicos, energia, vitalidade]`

#### Transcendente (Capacidade de transcendência)
**Pontuação**: `[0-5]`
**Evidências**: `[EXTRAIR: Capacidade de ir além das limitações atuais]`

### Trajetória Evolutiva

**INSTRUÇÃO**: Mapear como o paciente situa sua experiência temporalmente.

#### PASSADO
`[EXTRAIR: Como paciente se refere a eventos formativos, traumas, conquistas do passado]`

#### PRESENTE  
`[EXTRAIR: Como descreve sua situação atual, desafios imediatos]`

#### FUTURO
`[EXTRAIR: Esperanças, medos, planos, perspectivas futuras]`

### Diagnóstico Principal & Comorbidades

**INSTRUÇÃO**: Formular hipóteses diagnósticas baseadas no material da sessão.

#### Diagnóstico Principal
`[FORMULAR: Hipótese diagnóstica principal baseada nos critérios apresentados]`

#### Comorbidades Identificadas
`[LISTAR: Outros transtornos ou condições evidenciadas]`

#### Diagnósticos Diferenciais
`[CONSIDERAR: Outras possibilidades diagnósticas a investigar]`

### Fatores de Risco & Proteção

#### RISCOS

**Risco Suicida**:
- ☐ Baixo `[Sem ideação]`
- ☐ Moderado `[Ideação sem plano]`
- ☐ Alto `[Ideação com plano]`
- ☐ Iminente `[Intenção imediata]`

**Outros Riscos**:
`[IDENTIFICAR: Uso de substâncias, violência, negligência, isolamento, etc.]`

#### PROTEÇÃO

**Fatores Protetivos Identificados**:
`[EXTRAIR: Suporte social, recursos pessoais, estratégias de enfrentamento, etc.]`

**Motivação para Tratamento**:
`[AVALIAR: Grau de engajamento e motivação para mudança]`

---

## P - PLANO (Intervenções Trajetoriais)

### Objetivos Terapêuticos

**INSTRUÇÃO**: Definir objetivos baseados na avaliação multidimensional.

#### Objetivos Imediatos (1-2 semanas)
`[DEFINIR: Metas de curto prazo baseadas nas necessidades urgentes]`

#### Objetivos de Médio Prazo (1-3 meses)
`[DEFINIR: Metas intermediárias para estabilização e desenvolvimento]`

#### Objetivos de Longo Prazo (3+ meses)
`[DEFINIR: Metas de transformação e crescimento]`

### Intervenções Específicas

**INSTRUÇÃO**: Marcar modalidades apropriadas baseadas na avaliação.

- ☐ Psicoterapia Individual `[JUSTIFICAR: Por que necessária]`
- ☐ Terapia Grupal `[JUSTIFICAR: Benefícios esperados]`
- ☐ Terapia Familiar `[JUSTIFICAR: Quando família é relevante]`
- ☐ Medicação `[ESPECIFICAR: Classe terapêutica indicada]`
- ☐ Oficinas Terapêuticas `[ESPECIFICAR: Tipo de atividade]`
- ☐ Acompanhamento Social `[JUSTIFICAR: Necessidades sociais]`
- ☐ Outro: `[ESPECIFICAR: Intervenção específica necessária]`

### Próximos Passos & Follow-up

#### Próxima Consulta
- **Data sugerida**: `[DEFINIR: Baseado na urgência do caso]`
- **Foco**: `[ESPECIFICAR: O que priorizar no próximo encontro]`

#### Tarefas Entre Sessões
`[PROPOR: Atividades, observações, mudanças a implementar]`

#### Critérios de Reavaliação
`[DEFINIR: Indicadores para ajustar plano terapêutico]`

### Urgências & Alertas

**INSTRUÇÃO**: Identificar situações que requerem atenção imediata.

#### Riscos Imediatos Identificados
- ☐ Risco suicida `[DETALHAR: Nível e plano de manejo]`
- ☐ Risco heteroagressivo `[AVALIAR: Potencial e alvos]`
- ☐ Descompensação psicótica `[EVIDÊNCIAS: Sinais de alerta]`
- ☐ Uso abusivo substâncias `[GRAVIDADE: Padrão atual]`
- ☐ Vulnerabilidade social `[ESPECIFICAR: Tipo de vulnerabilidade]`
- ☐ Abandono tratamento `[FATORES: Que podem levar ao abandono]`

#### Plano de Contingência
`[DEFINIR: O que fazer em caso de crise ou emergência]`

#### Rede de Apoio para Crises
`[IDENTIFICAR: Pessoas ou serviços a acionar em emergência]`

---

## SÍNTESE CLÍNICA

### Formulação do Caso

**INSTRUÇÃO**: Sintetizar compreensão do caso em 2-3 parágrafos.

```
[Nome] apresenta-se como [descrição da pessoa e apresentação]. Sua trajetória caracteriza-se por [elementos principais da história]. O quadro atual sugere [interpretação clínica baseada na avaliação multidimensional]. 

Os principais desafios identificados incluem [listar problemas prioritários], enquanto seus recursos incluem [listar forças e potencialidades]. A intervenção proposta visa [objetivos principais] através de [estratégias específicas].

O prognóstico é [favorável/reservado/desfavorável] considerando [fatores prognósticos]. Requer acompanhamento [frequência] com foco em [áreas prioritárias].
```

### Prognóstico

#### Fatores Favoráveis
`[LISTAR: Elementos que favorecem boa evolução]`

#### Fatores Desfavoráveis  
`[LISTAR: Elementos que podem comprometer evolução]`

#### Estimativa Temporal
`[ESTIMAR: Tempo esperado para melhora significativa]`

---

## METADADOS PARA PROCESSAMENTO

### Marcadores Linguísticos de Gravidade:
- **Alta**: Desorganização, neologismos, incoerência
- **Moderada**: Circunstancialidade, tangencialidade  
- **Baixa**: Discurso organizado com desvios menores

### Padrões de Risco a Identificar:
- **Ideação suicida**: "Não aguento mais", "queria dormir para sempre"
- **Desorganização**: Saltos temáticos, perda do fio condutor
- **Delírios**: Convicções bizarras, interpretações irreais
- **Mania**: Grandiosidade, aceleração, projetos irreais

### Recursos Terapêuticos a Valorizar:
- **Insight**: "Acho que isso não está certo"
- **Motivação**: "Quero mudar", "preciso de ajuda"
- **Suporte**: Menção a pessoas significativas
- **Enfrentamento**: Estratégias de resolução de problemas

### Dimensões Críticas para Monitoramento:
- **Temporal**: Orientação e perspectiva temporal
- **Relacional**: Qualidade dos vínculos
- **Emocional**: Regulação afetiva
- **Existencial**: Sentido de propósito
- **Comportamental**: Capacidade de ação efetiva

### Indicadores de Evolução Favorável:
- Maior organização discursiva
- Aumento de insight
- Fortalecimento de vínculos
- Perspectivas futuras mais realistas
- Estratégias de enfrentamento mais efetivas